# -*- coding: utf-8 -*-
from odoo import models, fields, api
from num2words import num2words
from collections import defaultdict

class AccountMove(models.Model):
    _inherit = 'account.move'

    def amount_to_words(self):
        """Converts the total amount to words in Ecuadorian format"""
        self.ensure_one()
        integer_part = int(self.amount_total)
        decimal_part = int(round((self.amount_total - integer_part) * 100))
        amount_in_words = num2words(integer_part, lang='es').capitalize()
        return f"{amount_in_words} con {str(decimal_part).zfill(2)}/100 DÓLARES AMERICANOS"

    def get_formatted_invoice_lines(self):
        """Devuelve las líneas de factura formateadas para el reporte separando producto y seriales"""
        self.ensure_one()
        formatted_lines = []
        
        # Obtener todos los lotes de la factura usando la función nativa de Odoo
        lots_data = self._get_invoiced_lot_values()
        
        # Agrupar lotes por producto
        product_lots = defaultdict(list)
        for lot_data in lots_data:
            product_name = lot_data.get('product_name', '')
            lot_name = lot_data.get('lot_name', '')
            if lot_name:
                product_lots[product_name].append(lot_name)
        
        # Crear las líneas formateadas
        for line in self.invoice_line_ids:
            product_name = line.product_id.name
            serial_numbers = product_lots.get(line.product_id.display_name, [])
            
            formatted_serials = []
            current_row = []
            
            for i, serial in enumerate(serial_numbers):
                current_row.append(serial)
                if (i + 1) % 4 == 0:
                    formatted_serials.append(' | '.join(current_row))
                    current_row = []
            
            if current_row:
                formatted_serials.append(' | '.join(current_row))
            
            formatted_lines.append({
                'quantity': int(line.quantity) if line.quantity == int(line.quantity) else line.quantity,
                'product_name': product_name,
                'formatted_serials': formatted_serials,
                'price_unit': line.price_unit, 
                'price_subtotal': line.price_subtotal, 
            })

        return formatted_lines