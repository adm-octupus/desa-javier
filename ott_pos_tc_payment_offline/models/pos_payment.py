# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.ott_tc_base.util.common import OTT_CARD_TYPE, OTT_CARD_PAYMENT_TERMS

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    ott_card_red_id = fields.Many2one('ott.card.red', string='Card Red')
    ott_card_brand_id = fields.Many2one('ott.card.brand', string='Card Brand')
    ott_card_type = fields.Selection(selection=OTT_CARD_TYPE, string="Card type")
    ott_card_payment_terms = fields.Selection(selection=OTT_CARD_PAYMENT_TERMS, string="Payment terms")
    ott_card_period_id = fields.Many2one('ott.card.period', string='Card Period')

    def _export_for_ui(self, payment):
        result = super()._export_for_ui(payment)
        result.update({
            'ott_card_red_id': payment.ott_card_red_id,
            'ott_card_brand_id': payment.ott_card_brand_id,
            'ott_card_type': payment.ott_card_type,
            'ott_card_payment_terms': payment.ott_card_payment_terms,
            'ott_card_period_id': payment.ott_card_period_id,
        })
        return result