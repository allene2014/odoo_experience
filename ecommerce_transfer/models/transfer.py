# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, SUPERUSER_ID, _

#from odoo.addons.website_sale.models.sale_order import SaleOrder


class SalesModification(models.Model):																																																								
	_inherit = 'sale.order'
	_description = 'funtion to write in the POS table the movement generate in ecommerce'

	sale_electronic = fields.Boolean(string='venta electronica', default=False, store=True)

	def _get_valid_session(self):
		PosSession = self.env['pos.session']
		#closed_session = PosSession.browse(self.env.ref('ecommerce_transfer.pos_ecommerce_main'))
		closed_session = self.env.ref('ecommerce_transfer.pos_ecommerce_main')
		print ('XXXXXXXECOMMERCE TRANFERXXXXXXXXXX')
		print ('XXXXXXXECOMMERCE TRANFERXXXXXXXXXX')
		print ('XXXXXXXECOMMERCE TRANFERXXXXXXXXXX')
		print(closed_session)
		print(closed_session.id)
		rescue_session = PosSession.search([
			('state', 'not in', ('closed', 'closing_control')),
			('rescue', '=', True),
			('config_id', '=', closed_session.id),
			], limit=1)
		if rescue_session:
			return rescue_session
		new_session = PosSession.create({
			'config_id': closed_session.id,
			'name': _('(RESCUE FOR %(session)s)') % {'session': closed_session.name},
			'rescue': True,
			})
		new_session.action_pos_session_open()
		return new_session

	def _Writing_Dictionay(self, data):
		pass

	
	def create(self, vals):
		res = super(SalesModification, self).create(vals)
		print('*************IMPRIMIO DESDE EL SOBRE ESCRITO*****************')
		print(vals)
		mydict={}
		numero_orden=vals.get('name')
		order = self.env['pos.order']
		session = self._get_valid_session()

		print(session.name, 'en el create')
		#vals['name']=session.name
		#vals['prueba']="valor de prueba"

		sale_web= self.env['sale.order'].search([('name','=',numero_orden)])
		print(vals,'**********VALS*****************')

		if sale_web.name == numero_orden:
			print(sale_web.amount_total,'************************')

			order.create({
				'name':sale_web.name,
				'date_order':sale_web.date_order,
				'user_id':'',
				'amount_tax':sale_web.amount_tax,
				'amount_total':sale_web.amount_total,
				'amount_paid':sale_web.amount_total,
				'amount_return':0,
				'company_id':vals.get('company_id'),
				'pricelist_id':vals.get('pricelist_id'),
				'partner_id': vals.get('partner_id'),
				'session_id':session.id,
				
				})
		return res 


	