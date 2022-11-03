# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaceDualCurrency(http.Controller):
#     @http.route('/purchace_dual_currency/purchace_dual_currency', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchace_dual_currency/purchace_dual_currency/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchace_dual_currency.listing', {
#             'root': '/purchace_dual_currency/purchace_dual_currency',
#             'objects': http.request.env['purchace_dual_currency.purchace_dual_currency'].search([]),
#         })

#     @http.route('/purchace_dual_currency/purchace_dual_currency/objects/<model("purchace_dual_currency.purchace_dual_currency"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchace_dual_currency.object', {
#             'object': obj
#         })
