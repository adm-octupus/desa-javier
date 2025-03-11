# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OttCardBatch(models.Model):
    _name = 'ott.card.batch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Card Batch'
    _order = 'create_date desc'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, string='Company')
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency')
    card_batch_settlement_ids = fields.One2many('ott.card.batch.settlement', 'card_batch_id', string='Related Settlements')
    card_batch_settlement_count = fields.Integer(string='Number of settlements', compute='_compute_card_batch_settlement_count', store=True)
    
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
        self.ensure_one()
        card_batch_settlement = self.env['ott.card.batch.settlement'].create({
            'card_batch_id': self.id,
            # 'origin': self.name,
            # agrega aquí otros campos necesarios
        })

        return {
            'name': 'New Settlement',
            'type': 'ir.actions.act_window',
            'res_model': 'ott.card.batch.settlement',
            'view_mode': 'form',
            'res_id': card_batch_settlement.id,
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'},
        }

    @api.depends('card_batch_settlement_ids')
    def _compute_card_batch_settlement_count(self):
        for settlement in self:
            settlement.card_batch_settlement_count = len(settlement.card_batch_settlement_ids)

    def action_open_card_batch_settlement(self):
        self.ensure_one()
        if not self.card_batch_settlement_ids:
            return {'type': 'ir.actions.act_window_close'}

        if len(self.card_batch_settlement_ids) == 1:
            return {
                'name': 'Settlement',
                'type': 'ir.actions.act_window',
                'res_model': 'ott.card.batch.settlement',
                'view_mode': 'form',
                'res_id': self.card_batch_settlement_ids.id,
                'target': 'current',
                'context': {'form_view_initial_mode': 'edit'},
            }
        else:
            return {
                'name': 'Settlements',
                'type': 'ir.actions.act_window',
                'res_model': 'ott.card.batch.settlement',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.card_batch_settlement_ids.ids)],
                'target': 'current',
            }

