# -*- coding: utf-8 -*-
# from odoo import http


# class ModulosPruebas(http.Controller):
#     @http.route('/modulos_pruebas/modulos_pruebas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulos_pruebas/modulos_pruebas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulos_pruebas.listing', {
#             'root': '/modulos_pruebas/modulos_pruebas',
#             'objects': http.request.env['modulos_pruebas.modulos_pruebas'].search([]),
#         })

#     @http.route('/modulos_pruebas/modulos_pruebas/objects/<model("modulos_pruebas.modulos_pruebas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulos_pruebas.object', {
#             'object': obj
#         })
