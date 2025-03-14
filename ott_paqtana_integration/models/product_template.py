# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ott_maximum_min_qty_supplier = fields.Float('Maximum quantity supplier', compute='_compute_ott_maximum_qty_supplier', store=True)
    ott_maximum_multiple_qty_supplier = fields.Float('Maximum quantity supplier', compute='_compute_ott_maximum_qty_supplier', store=True)
    ott_average_delay_qty_supplier = fields.Float('Average delay supplier', compute='_compute_ott_maximum_qty_supplier', store=True)
    ott_paqtana_workspace_id = fields.Many2one(
        comodel_name='ott.paqtana.workspace',
        string='Paqtana workspace code',
        check_company=True, domain="[('company_id', '=', company_id)]",
    )

    @api.depends('seller_ids')
    def _compute_ott_maximum_qty_supplier(self): 
        for product in self:
            # Obtener el proveedor con la mayor min_qty y asignar solo el número
            max_min_qty_supplier = max(product.seller_ids, key=lambda s: s.min_qty, default=False)
            product.ott_maximum_min_qty_supplier = max_min_qty_supplier.min_qty if max_min_qty_supplier else 0

            # Obtener el proveedor con la mayor ott_multiple_qty y asignar solo el número
            max_multiple_qty_supplier = max(product.seller_ids, key=lambda s: s.ott_multiple_qty, default=False)
            product.ott_maximum_multiple_qty_supplier = max_multiple_qty_supplier.ott_multiple_qty if max_multiple_qty_supplier else 0

            # Calcular el promedio de delay, evitando división por 0
            product.ott_average_delay_qty_supplier = (
                sum(product.seller_ids.mapped("delay")) / len(product.seller_ids) if product.seller_ids else 0
            )
    