# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class OttCardBatchSettlementTransaction(models.Model):
    _name = 'ott.card.batch.settlement.transaction'
    _description = 'Card Batch Settlement Transaction'
    _order = 'create_date desc'

    card_batch_settlement_id = fields.Many2one('ott.card.batch.settlement', string='Related Card Batch Settlement', ondelete='cascade')
    company_id = fields.Many2one(related='card_batch_settlement_id.company_id', string='Company')
    currency_id = fields.Many2one(related='card_batch_settlement_id.currency_id', string='Currency')

    amount_deposit = fields.Monetary(string="Deposit", currency_field="currency_id", required=True)
    amount_commission = fields.Monetary(string="Commission", currency_field="currency_id", required=True)
    amount_vat = fields.Monetary(string="VAT", currency_field="currency_id", required=True)
