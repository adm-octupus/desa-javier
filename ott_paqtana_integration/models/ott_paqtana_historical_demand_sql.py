# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from odoo import models, fields, tools, api

class OttPaqtanaHistoricalDemandSQL(models.Model):
    _name = "ott.paqtana.historical.demand.sql"
    _description = "Historical Demand SQL"
    _auto = False  # Indica que este modelo no tiene tabla propia (usa una vista SQL)

    id = fields.Char(string="Unique ID", readonly=True)
    product_id = fields.Many2one('product.template', string="Product")
    warehouse_id = fields.Many2one('stock.warehouse', string="Stock Warehouse Location")
    company_id = fields.Many2one('res.company', string="Company")
    sale_date = fields.Date(string="Sale date")
    quantity = fields.Float(string="Quantity")

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
                sw.id AS warehouse_id, -- Código de la bodega
                pt.id AS product_id,  -- Código del producto
                pt.company_id AS company_id,
                so.date_order::DATE AS sale_date,  -- Fecha de la venta (solo día)
                SUM(sol.product_uom_qty) AS quantity  -- Cantidad total vendida ese día
            FROM sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
            JOIN stock_warehouse sw ON so.warehouse_id = sw.id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            WHERE so.state IN ('sale', 'done')  -- Solo ventas confirmadas o completadas
            GROUP BY sw.id, pt.id, pt.company_id, so.date_order::DATE
            ORDER BY so.date_order::DATE DESC, sw.code;
        """
    @api.model
    def get_paqtana_historical_demand_json(self, company):
        """Consulta los datos de la vista SQL y los convierte en JSON con formato personalizado."""
        company_id = company.id
        default_workspace_code = company.ott_paqtana_default_workspace_id.code

        domain = ['|', ('company_id', '=', company_id), ('company_id', '=', False)]
        historical_demand_records = self.env["ott.paqtana.historical.demand.sql"].search(domain)

        # Estructura agrupada por producto y bodega
        grouped_data = defaultdict(lambda: {"dates": [], "quantities": []})

        for record in historical_demand_records:

            product_code = record.product_id.default_code if record.product_id.default_code else record.product_id.name
            workspace_code = record.product_id.ott_paqtana_workspace_id.code if record.product_id.ott_paqtana_workspace_id else default_workspace_code
                
            key = record.id # Combinación de producto y bodega
            grouped_data[key]["location"] = record.warehouse_id.code
            grouped_data[key]["code"] = product_code
            grouped_data[key]["workspaceCode"] = (workspace_code)
            grouped_data[key]["dates"].append(record.sale_date.strftime("%Y-%m-%d"))
            grouped_data[key]["quantities"].append(record.quantity)

        data = list(grouped_data.values())

        # Convertir a JSON string
        json_data = json.dumps({"data": data}, separators=(',', ':'), ensure_ascii=False)
        json_data = json.loads(json_data)
        
        return json_data
