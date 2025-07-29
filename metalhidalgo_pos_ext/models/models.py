# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class metalhidalgo_pos_ext(models.Model):
#     _name = 'metalhidalgo_pos_ext.metalhidalgo_pos_ext'
#     _description = 'metalhidalgo_pos_ext.metalhidalgo_pos_ext'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
