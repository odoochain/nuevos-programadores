# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import http.client
import json

class UnitaryLicense(models.Model):
    _description = "Unitary License"
    _name = 'unitary.license'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char('Code', copy=False)
    _id = fields.Char('id', copy=False)
    type = fields.Char('type', copy=False)
    total_uses = fields.Integer('total_uses', copy=False)
    used = fields.Integer('used', copy=False)
    date = fields.Date('dateTime', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)