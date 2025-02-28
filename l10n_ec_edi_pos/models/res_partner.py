# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    ott_pos_partner_enabled_in_pos = fields.Boolean('Partner enabled for use in POS', defualt=False, help='Only partners who have this option checked will appear in the POS')

    @api.model
    def create_from_ui(self, partner):
        partner['ott_pos_partner_enabled_in_pos'] = True
        return super(ResPartner, self).create_from_ui(partner)