# -*- coding: utf-8 -*-
import json
from odoo import models, fields, tools, api

class OttPaqtanaMasterInventorySQL(models.Model):
    _name = "ott.paqtana.master.inventory.sql"
    _description = "Master inventory SQL"
    _auto = False  # Indica que este modelo no tiene tabla propia (usa una vista SQL)

    id = fields.Char(string="Unique ID", readonly=True)
    product_id = fields.Many2one('product.template', string="Product")
    stock_warehouse_id = fields.Many2one('stock.location', string="Stock Location")
    company_id = fields.Many2one('res.company', string="Company")
    location = fields.Char(string="Warehouse Code")
    on_hand_stock = fields.Float(string="On Hand Stock")
    transit_stock = fields.Float(string="Stock in Transit")
    open_demand_orders = fields.Integer(string="Open Demand Orders")

    def init(self):
        """Crea la vista SQL al instalar el módulo"""
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f"""
            CREATE VIEW {self._table} AS
            {self._get_sql_query()}
        """)

    @staticmethod
    def _get_sql_query():
        """Devuelve la consulta SQL optimizada"""
        return """
            SELECT 
                CONCAT(pt.id, '-', sw.id) AS id,
                pt.id AS product_id,
                sw.id AS stock_warehouse_id,
                pt.company_id AS company_id,
                sw.code AS location,  -- Código de la bodega
                SUM(sq.quantity) AS on_hand_stock,  -- Stock a la mano
                COALESCE(SUM(sm_in_transit.product_qty), 0) AS transit_stock,  -- Stock en tránsito
                COUNT(DISTINCT so.id) AS open_demand_orders  -- Pedidos abiertos pendientes
            FROM stock_quant sq
            JOIN stock_location sl ON sq.location_id = sl.id
            JOIN product_product pp ON sq.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            LEFT JOIN stock_warehouse sw ON sl.id = sw.view_location_id OR sl.location_id = sw.view_location_id

            -- Obtener stock en tránsito
            LEFT JOIN LATERAL (
                SELECT SUM(sm.product_qty) AS product_qty
                FROM stock_move sm
                WHERE sm.product_id = pp.id
                AND sm.location_dest_id = sl.id
                AND sm.state IN ('confirmed', 'waiting', 'assigned')
            ) sm_in_transit ON true

            -- Obtener la cantidad de pedidos abiertos sin despachar
            LEFT JOIN sale_order_line sol ON sol.product_id = pp.id
            LEFT JOIN sale_order so ON so.id = sol.order_id AND so.state = 'sale'
            LEFT JOIN stock_move sm_sale ON sm_sale.sale_line_id = sol.id AND sm_sale.state IN ('confirmed', 'waiting', 'assigned')

            WHERE sl.usage = 'internal'
            GROUP BY pt.id, sw.id, sl.id, sw.code, pt.company_id
            ORDER BY pt.id, sw.code;
        """

    @api.model
    def get_paqtana_master_inventory_json(self, company,):
        """Consulta los datos de la vista SQL y los convierte en JSON con formato personalizado.
        """
        company_id = company.id
        currency = company.currency_id.name
        default_workspace_code = company.ott_paqtana_default_workspace_id.code

        domain = ['|', ('company_id', '=', company_id), ('company_id', '=', False)]
        master_inventory_records = self.env["ott.paqtana.master.inventory.sql"].search(domain)

        data = []
        for record in master_inventory_records:
            product_code = record.product_id.default_code if record.product_id.default_code else record.product_id.name
            workspace_code = record.product_id.ott_paqtana_workspace_id.code if record.product_id.ott_paqtana_workspace_id else default_workspace_code
            
            item = {
                "location": record.location,
                "code": product_code,
                "description": record.product_id.name,
                "materialType": record.product_id.detailed_type,
                "multipleOrderQuantity": record.product_id.ott_maximum_multiple_qty_supplier,
                "currency": currency,
                "unitCost": record.product_id.standard_price,
                "minimumOrderQuantity": record.product_id.ott_maximum_min_qty_supplier,
                "unitOfMeasure": record.product_id.uom_id.name,
                "supplyLeadTime": record.product_id.ott_average_delay_qty_supplier,
                "onHandStock": record.on_hand_stock,
                "transitStock": record.transit_stock,
                "openDemandOrders": record.open_demand_orders,
                "additionalColumns": [],
                "workspaceCode": workspace_code
            }
            data.append(item)

        json_data = json.dumps({"data": data}, separators=(',', ':'), ensure_ascii=False)
        json_data = json.loads(json_data) 

        return json_data
