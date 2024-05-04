# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import http.client
import json

import logging
_logger = logging.getLogger(__name__)


class SystemLicense(models.Model):
    _description = "System License"
    _name = 'system.license'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _rec_name = 'user_id'


    user_id = fields.Many2one('res.users', string='User', required=True)
    last_update = fields.Datetime(string='Date Update')
    number_calls = fields.Integer(string='Number Calls')
    lines_ids = fields.One2many('system.license.line', 'system_license_id', string='Lines')


    def load_licence(self):
        _logger.info('== begin load_licence ==')

        # Hacemos Validaciones
        if not self.user_id:
            raise ValidationError(_('User is required'))

        if not self.user_id.client_id:
            raise ValidationError(_('Client ID is required'))


        self.last_update = fields.Datetime.now()
        self.number_calls = self.number_calls + 1

        conn = http.client.HTTPSConnection("exploreteia.com")

        # ir.config_parameter licence_password
        licence_password = self.env['ir.config_parameter'].sudo().get_param('licence_password')

        if not licence_password:
            raise ValidationError(_('Licence Password is required'))


        payload = json.dumps({
          "passwd": licence_password,
          "client": self.user_id.client_id
        })
        headers = {
          'Content-Type': 'application/json'
        }
        conn.request("POST", "/rest/ListCodes.php", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Necesito tenerlo en un json
        data = json.loads(data.decode("utf-8"))
        print(data)

        for obj in data:
            # Compruebo que el id no exista
            system_license_line_id = self.env['system.license.line'].search([
                        ('system_license_id', '=', self.id),
                        ('name', '=', obj["id"])
                    ], limit=1)

            # Si ya existe lo modifcamos
            if system_license_line_id:
                system_license_line_id.write({
                                'code': obj["code"],
                                'type': obj["type"],
                                'total_uses': obj["totalUses"],
                                'date': obj["date"],
                                'used': obj["used"],
                            })

                # actualizo el consumo
                license_consumption_id = self.env['license.consumption'].search([
                        ('user_id', '=', self.user_id.id),
                        ('name', '=', obj["id"])
                    ], limit=1)

            else:
                # Si no existe lo creamos
                license_consumption_id = self.env['license.consumption'].create({
                    'name': obj["id"],
                    'user_id': self.user_id.id,
                })


                val = {
                    'name': obj["id"],
                    'code': obj["code"],
                    'type': obj["type"],
                    'total_uses': obj["totalUses"],
                    'date': obj["date"],
                    'system_license_id': self.id,
                    'used': obj["used"],
                    'license_consumption_id': license_consumption_id.id
                }
                self.env['system.license.line'].create(val)


        # actualizo los consumo
        _logger.info("Actualizo los Consumo")
        for line in self.lines_ids:
            _logger.info(line.license_consumption_id)

            conn = http.client.HTTPSConnection("exploreteia.com")
            payload = json.dumps({
              "passwd": licence_password,
              "codeId": line.license_consumption_id.name
            })
            headers = {
              'Content-Type': 'application/json'
            }
            conn.request("POST", "/rest/GetCodeInfo.php", payload, headers)
            res = conn.getresponse()
            data = res.read()

            # Necesito tenerlo en un json
            data = json.loads(data.decode("utf-8"))

            print(data)

            """
            {'code': 'PRUEBA3453', 'type': '0', 'totalUses': 20, 'used': 10, 'date': '2024-12-07 12:12:12', 'consumptions': ['2024-01-07 10:30:33', '2024-01-08 17:45:21', '2024-01-17 14:27:40', '2024-01-19 06:58:03', '2024-01-22 19:33:12', '2024-01-25 11:20:07', '2024-01-29 08:04:56', '2024-02-01 20:52:39', '2024-02-03 12:17:28', '2024-02-08 03:59:45']}
            """

            # Recorro los consumptions
            for consumption in data["consumptions"]:
                # Compruebo que el id no exista
                license_consumption_line_id = self.env['license.consumption.line'].search([
                            ('license_consumption_id', '=', line.license_consumption_id.id),
                            ('name', '=', consumption)
                        ], limit=1)

                # Si no existe lo creamos
                if not license_consumption_line_id:
                    val = {
                        'name': consumption,
                        'license_consumption_id': line.license_consumption_id.id
                    }
                    self.env['license.consumption.line'].create(val)


class SystemLicenseLine(models.Model):
    _description = "System License Line"
    _name = 'system.license.line'


    name = fields.Char(string='id')
    license_consumption_id = fields.Many2one('license.consumption', string='id')
    code = fields.Char(string='Code')
    type = fields.Integer(string='Type')
    total_uses = fields.Integer(string='Total Uses')
    used = fields.Integer(string='Used')
    date = fields.Datetime(string='Date')
    system_license_id = fields.Many2one('system.license', string='System License', required=True)

