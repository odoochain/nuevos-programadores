from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    client_id = fields.Integer(string='Client ID')
