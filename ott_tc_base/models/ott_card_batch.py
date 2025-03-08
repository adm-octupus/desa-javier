# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OttCardBatchSettlement(models.Model):
    _name = 'ott.card.batch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Card Batch'
    _order = 'create_date desc'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency')

    source_module = fields.Selection([], string='Source module')
    batch = fields.Char(string='Batch', required=True)
    card_red_id = fields.Many2one('ott.card.red', string='Card Red', required=True)
    card_red_name = fields.Char(related="card_red_id.name", string='Red Name', store=True, readonly=True)
    card_red_code = fields.Char(related="card_red_id.code", string='Red Code', store=True, readonly=True)
    number_vouchers = fields.Integer(string='Number vouchers', required=True)
    total_collected = fields.Monetary(string="Total Collected", currency_field="currency_id", required=True)
    total_settled = fields.Monetary(string="Total Settled", currency_field="currency_id")
    difference = fields.Monetary(string="Difference", currency_field="currency_id", compute="_compute_difference", store=True)
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('settled', 'Settled'),
    ], string='State', default='pending')


    @api.depends('total_collected', 'total_settled')
    def _compute_difference(self):
        for card_batch in self:
            card_batch.difference = card_batch.total_collected - card_batch.total_settled

    
    def button_create_batch_settlement(self):
        print('test')