# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    """
    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            if not "wId" in rec.name:
                rec.vat = rec.id"""