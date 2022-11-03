# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RegisterPagomovil(models.Model):
	_name = 'register.pagomovil'
	_description = 'registro de pagos desde el ecommerce'
	
	cedula = fields.Char(string="Cedula de Identidad", store=True)
	num_tlf = fields.Char(string="Numero Teléfonico", store=True)
	code_bank = fields.Char(string="Referencia Bancaria", store=True)