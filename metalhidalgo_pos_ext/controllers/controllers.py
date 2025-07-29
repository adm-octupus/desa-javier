# -*- coding: utf-8 -*-
# from odoo import http


# class MetalhidalgoPosExt(http.Controller):
#     @http.route('/metalhidalgo_pos_ext/metalhidalgo_pos_ext', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/metalhidalgo_pos_ext/metalhidalgo_pos_ext/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('metalhidalgo_pos_ext.listing', {
#             'root': '/metalhidalgo_pos_ext/metalhidalgo_pos_ext',
#             'objects': http.request.env['metalhidalgo_pos_ext.metalhidalgo_pos_ext'].search([]),
#         })

#     @http.route('/metalhidalgo_pos_ext/metalhidalgo_pos_ext/objects/<model("metalhidalgo_pos_ext.metalhidalgo_pos_ext"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('metalhidalgo_pos_ext.object', {
#             'object': obj
#         })
