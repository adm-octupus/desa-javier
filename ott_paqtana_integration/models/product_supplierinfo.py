# -*- coding: utf-8 -*-
from odoo import fields, models, _

class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    ott_max_qty = fields.Float('Max Quantity', default=0.0, required=True)
    ott_multiple_qty = fields.Float('Multiple Quantity', default=0.0, required=True)
