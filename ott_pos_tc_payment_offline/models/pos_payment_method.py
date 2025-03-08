# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_credit_card = fields.Boolean('Is Credit Card?', default=False)
    ott_card_brands_ids = fields.Many2many(string="Card brands", comodel_name='ott.card.brand')