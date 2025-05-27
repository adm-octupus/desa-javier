# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    garmin_internal_code = fields.Char('Internal Code', store=True)
