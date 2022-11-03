# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

#from odoo.addons.website_sale.controllers.main import WebsiteSale

class RegisterPayment(http.Controller):
	@http.route('/register/pagomovil', type='http', auth="public", website=True)
	def call_webform(self, **kw):
		print("desde el nuevo controlador para cargar registro")
		return http.request.render("register_pay_ecommerce.payment_form_register",{})

	@http.route('/complete/register', type='http', auth="public", website=True)
	def register_payment(self, **kw):
		request.env['register.pagomovil'].sudo().create(kw)
		return http.request.render("register_pay_ecommerce.payment_register_done_template",{})

		#request.env[]





		
