# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OttCardBrand(models.Model):
    _name = 'ott.card.brand'
    _description = 'Card brand'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')