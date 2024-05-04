# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import http.client
import json

import logging
_logger = logging.getLogger(__name__)


class LicenseConsumption(models.Model):
    _description = "License Consumption"
    _name = 'license.consumption'

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='User', required=True)
    lines_ids = fields.One2many('license.consumption.line', 'license_consumption_id', string='Lines')


class LicenseConsumptionLine(models.Model):
    _description = "License Consumption Line"
    _name = 'license.consumption.line'

    name = fields.Datetime(string='Date Update')
    license_consumption_id = fields.Many2one('license.consumption', string='License Consumption')
