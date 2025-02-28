# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OttCardRed(models.Model):
    _name = 'ott.card.red'
    _description = 'Card Red'
    
    code = fields.Char(string='Code')
    name = fields.Char(string='Name')