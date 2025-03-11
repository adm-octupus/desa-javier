# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'posted', 'cancel'}
}

class OttCardBatchSettlement(models.Model):
    _name = 'ott.card.batch.settlement'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Card Batch Settlement'
    _order = 'create_date desc'

    card_batch_id = fields.Many2one('ott.card.batch', string='Related Card Btach', ondelete='cascade')
    company_id = fields.Many2one(related='card_batch_id.company_id', string='Company')
    currency_id = fields.Many2one(related='card_batch_id.currency_id', string='Currency')
    batch = fields.Char(related="card_batch_id.batch", string='Batch', store=True, readonly=True)
    card_red_id = fields.Many2one(related="card_batch_id.card_red_id", string='Red ID', store=True, readonly=True)
    card_red_name = fields.Char(related="card_batch_id.card_red_name", string='Red Code', store=True, readonly=True)
    card_red_code = fields.Char(related="card_batch_id.card_red_code", string='Red Name', store=True, readonly=True)
    invoice_ids = fields.One2many('account.move', 'card_batch_settlement_id', string='Related Invoices')
    invoice_count = fields.Integer(string='Number of Invoices', compute='_compute_invoice_count', store=True)

    card_batch_settlement_transaction_ids = fields.One2many('ott.card.batch.settlement.transaction', 'card_batch_settlement_id', string='Related Settlement Transaction')
    card_batch_settlement_withhol_ids = fields.One2many('ott.card.batch.settlement.withhol', 'card_batch_settlement_id', string='Related Settlement Withhol')
    
    issue_date = fields.Date(string='Issue date', states=READONLY_FIELD_STATES, tracking=1)
  
    name = fields.Char(string='Document', default='New', readonly=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Vendor", readonly=False, change_default=True, index=True,
        tracking=3,
        states=READONLY_FIELD_STATES,
        check_company=True,
        domain="[('type', '!=', 'private'), ('company_id', 'in', (False, company_id))]")

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('posted', "Posted"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    settlement_account_id = fields.Many2one(
        comodel_name='account.account',
        check_company=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]",
    )

    commission_account_id = fields.Many2one(
        comodel_name='account.account',
        check_company=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]",
    )

    total_deposit_amount = fields.Monetary(
        string="Total Deposit",
        currency_field="currency_id",
        compute='_compute_total_deposit_amount',
        store=True
    )

    total_commission_amount = fields.Monetary(
        string="Total Commission",
        currency_field="currency_id",
        compute='_compute_total_commission_amount',
        store=True
    )

    total_vat_amount = fields.Monetary(
        string="Total VAT",
        currency_field="currency_id",
        compute='_compute_total_vat_amount',
        store=True
    )

    total_withhol_amount = fields.Monetary(
        string="Total Withholding",
        currency_field="currency_id",
        compute='_compute_total_withhol_amount',
        store=True
    )

    total_to_be_paid_amount = fields.Monetary(
        string="To be paid",
        currency_field="currency_id",
        compute='_compute_total_to_be_paid_amount',
        store=True
    )
     
    withhol_document_number = fields.Char(string='Document Number')
    withhol_authorization_number = fields.Char(
        string="Authorization number",
        size=49,
        copy=False, index=True,
        tracking=True,
        help="EDI authorization number (same as access key), set upon posting",
    )

    def action_create_and_open_invoice(self):
        # Creando factura de proveedor (in_invoice)
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'card_batch_settlement_id': self.id,
            'partner_id': self.partner_id.id,
        })

        return {
            'name': 'Nueva Factura Proveedor',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'domain': [('move_type', '=', 'in_invoice')],
            'target': 'current',
        }

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for settlement in self:
            settlement.invoice_count = len(settlement.invoice_ids)

    def action_open_invoice(self):
        self.ensure_one()
        if not self.invoice_ids:
            return {'type': 'ir.actions.act_window_close'}

        if len(self.invoice_ids) == 1:
            return {
                'name': 'Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_ids.id,
                'target': 'current',
                'context': {'form_view_initial_mode': 'edit'},
            }
        else:
            return {
                'name': 'Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.invoice_ids.ids)],
                'target': 'current',
            }

    @api.depends('card_batch_settlement_transaction_ids.amount_deposit')
    def _compute_total_deposit_amount(self):
        for record in self:
            record.total_deposit_amount = sum(record.card_batch_settlement_transaction_ids.mapped('amount_deposit'))

    @api.depends('card_batch_settlement_transaction_ids.amount_commission')
    def _compute_total_commission_amount(self):
        for record in self:
            record.total_commission_amount = sum(record.card_batch_settlement_transaction_ids.mapped('amount_commission'))

    @api.depends('card_batch_settlement_transaction_ids.amount_vat')
    def _compute_total_vat_amount(self):
        for record in self:
            record.total_vat_amount = sum(record.card_batch_settlement_transaction_ids.mapped('amount_vat'))

    @api.depends('card_batch_settlement_withhol_ids.amount')
    def _compute_total_withhol_amount(self):
        for record in self:
            record.total_withhol_amount = sum(record.card_batch_settlement_withhol_ids.mapped('amount'))

    @api.depends('total_deposit_amount', 'total_commission_amount', 'total_vat_amount', 'total_withhol_amount')
    def _compute_total_to_be_paid_amount(self):
        for record in self:
            record.total_to_be_paid_amount = record.total_deposit_amount - record.total_commission_amount - record.total_vat_amount - record.total_withhol_amount
