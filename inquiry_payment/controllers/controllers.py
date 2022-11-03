# -*- coding: utf-8 -*-
# from odoo import http


# class InquiryPayment(http.Controller):
#     @http.route('/inquiry_payment/inquiry_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inquiry_payment/inquiry_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inquiry_payment.listing', {
#             'root': '/inquiry_payment/inquiry_payment',
#             'objects': http.request.env['inquiry_payment.inquiry_payment'].search([]),
#         })

#     @http.route('/inquiry_payment/inquiry_payment/objects/<model("inquiry_payment.inquiry_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inquiry_payment.object', {
#             'object': obj
#         })
