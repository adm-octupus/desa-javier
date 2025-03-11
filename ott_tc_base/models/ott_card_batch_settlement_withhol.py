# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class OttCardBatchSettlementWithhol(models.Model):
    _name = 'ott.card.batch.settlement.withhol'
    _description = 'Card Batch Settlement Withhol'
    _order = 'create_date desc'

    card_batch_settlement_id = fields.Many2one('ott.card.batch.settlement', string='Related Card Batch Settlement', ondelete='cascade')
    company_id = fields.Many2one(related='card_batch_settlement_id.company_id', string='Company')
    currency_id = fields.Many2one(related='card_batch_settlement_id.currency_id', string='Currency')

    tax_id = fields.Many2one(
        comodel_name='account.tax',
        string="Tax",
    )

    tax_account_id = fields.Many2one(
        comodel_name='account.account',
        check_company=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]",
    )

    base = fields.Monetary(
        string="Base", store=True, readonly=False,
    )
    amount = fields.Monetary(
        string="Amount",
        compute='_compute_amount', store=True, readonly=False,
    )

    @api.depends('tax_id', 'base')
    def _compute_amount(self):
        # Recomputes amount according to "base amount" and tax percentage
        for line in self:
            tax_amount = 0.0
            tax_account_id = False
            if line.tax_id:
                tax_amount, tax_account_id = self._tax_compute_all_helper(line.base, line.tax_id)
            line.amount = tax_amount
            line.tax_account_id = tax_account_id

    # === Helper methods ====
    @api.model
    def _tax_compute_all_helper(self, base, tax_id):
        # Computes the withholding tax amount provided a base and a tax
        # It is equivalent to: amount = self.base * self.tax_id.amount / 100
        taxes_res = tax_id.compute_all(
            base,
            currency=tax_id.company_id.currency_id,
            quantity=1.0,
            product=False,
            partner=False,
            is_refund=False,
        )
        tax_amount = taxes_res['taxes'][0]['amount']
        tax_amount = abs(tax_amount)  # For ignoring the sign of the percentage on tax configuration
        tax_account_id = taxes_res['taxes'][0]['account_id']
        return tax_amount, tax_account_id