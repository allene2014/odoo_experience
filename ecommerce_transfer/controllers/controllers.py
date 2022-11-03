# -*- coding: utf-8 -*-
# from odoo import http


# class EcommerceTransfer(http.Controller):
#     @http.route('/ecommerce_transfer/ecommerce_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecommerce_transfer/ecommerce_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecommerce_transfer.listing', {
#             'root': '/ecommerce_transfer/ecommerce_transfer',
#             'objects': http.request.env['ecommerce_transfer.ecommerce_transfer'].search([]),
#         })

#     @http.route('/ecommerce_transfer/ecommerce_transfer/objects/<model("ecommerce_transfer.ecommerce_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecommerce_transfer.object', {
#             'object': obj
#         })
