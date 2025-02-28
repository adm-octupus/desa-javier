# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OttCardPeriod(models.Model):
    _name = 'ott.card.period'
    _description = 'Card Period'
    
    code = fields.Char(string='Code')
    name = fields.Char(string='Name')