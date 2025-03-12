# -*- coding: utf-8 -*-
# from odoo import http


# class OttPaqtanaIntegration(http.Controller):
#     @http.route('/ott_paqtana_integration/ott_paqtana_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ott_paqtana_integration/ott_paqtana_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ott_paqtana_integration.listing', {
#             'root': '/ott_paqtana_integration/ott_paqtana_integration',
#             'objects': http.request.env['ott_paqtana_integration.ott_paqtana_integration'].search([]),
#         })

#     @http.route('/ott_paqtana_integration/ott_paqtana_integration/objects/<model("ott_paqtana_integration.ott_paqtana_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ott_paqtana_integration.object', {
#             'object': obj
#         })
