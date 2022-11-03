# -*- coding: utf-8 -*-
# from odoo import http


# class SalesDualCurrency(http.Controller):
#     @http.route('/sales_dual_currency/sales_dual_currency', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_dual_currency/sales_dual_currency/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_dual_currency.listing', {
#             'root': '/sales_dual_currency/sales_dual_currency',
#             'objects': http.request.env['sales_dual_currency.sales_dual_currency'].search([]),
#         })

#     @http.route('/sales_dual_currency/sales_dual_currency/objects/<model("sales_dual_currency.sales_dual_currency"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_dual_currency.object', {
#             'object': obj
#         })
