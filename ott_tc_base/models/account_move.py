# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    card_batch_settlement_id = fields.Many2one('ott.card.batch.settlement', string='Related Card batch settlement', ondelete='cascade')