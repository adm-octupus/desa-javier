# -*- coding: utf-8 -*-
from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    ott_default_create_invoice = fields.Boolean(string="Default create invoice", default=False)

    def get_limited_partners_loading(self):
        partner_ids = super().get_limited_partners_loading()
        Partner = self.env['res.partner']
        filtered_partner_ids = []
        
        # Filtrar solo los partners que tienen habilitado ott_pos_partner_enabled_in_pos
        for pid_tuple in partner_ids:
            partner = Partner.browse(pid_tuple[0])
            if partner.ott_pos_partner_enabled_in_pos:
                filtered_partner_ids.append(pid_tuple)
        
        # Aseguramos que el partner 'ec_final_consumer' se incluya si está habilitado
        ec_final_consumer = self.env.ref('l10n_ec.ec_final_consumer')
        if ec_final_consumer.ott_pos_partner_enabled_in_pos and (ec_final_consumer.id,) not in filtered_partner_ids:
            filtered_partner_ids.append((ec_final_consumer.id,))
        
        return filtered_partner_ids