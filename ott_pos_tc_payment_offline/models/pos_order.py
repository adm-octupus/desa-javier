# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        result = super()._payment_fields(order, ui_paymentline)
        result.update({
            'ott_card_red_id': ui_paymentline.get('ott_card_red_id'),
            'ott_card_brand_id': ui_paymentline.get('ott_card_brand_id'),
            'ott_card_type': ui_paymentline.get('ott_card_type'),
            'ott_card_payment_terms': ui_paymentline.get('ott_card_payment_terms'),
            'ott_card_period_id': ui_paymentline.get('ott_card_period_id'),
        })
        return result
