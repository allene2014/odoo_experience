# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, SUPERUSER_ID, _

#from odoo.addons.website_sale.models.sale_order import SaleOrder


class SalesModification(models.Model):																																																								
	_inherit = 'website'
	_description = 'funtion to write in the POS table the movement generate in ecommerce'

	#sale_electronic = fields.Boolean(string='venta electronica', default=False, store=True)

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

	
	def sale_get_order(self):
		res = super(SalesModification, self).sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False)
		print('*************IMPRIMIO DESDE EL SOBRE ESCRITO*****************')
		#order = self.env['pos.order']
		#print('SOBRESCRIBIENDO EL MODELO CREATE')
		#session = self._get_valid_session()
		return res



	#	print(vals, 'estos son los valores rescatados')
		#pass
	    #vals['name'] = self._get_batch_name(vals.get('batch_type'), vals.get('date', fields.Date.context_today(self)), vals)
	    #print ("****************DESDE EL MODELO ECOMMERCE TRANFER***************************")
	    #print ("****************DESDE EL MODELO ECOMMERCE TRANFER***************************")
	    #print (vals)
	    #vals['prueba']='nuevo valor'
	    #print('NEX_VALS')
	    #print(vals)
	    #print('NEX_VALS')
	    #vals={
	    #'name':'',
	    #'date_order':'',
	    #'user_id':'',
	    #'amount_tax':'',
	    #'amount_total':'',
	    #'amount_paid':'',
	    #'amount_return':'',
	    #'company_id':'',
	    #'pricelist_id':'',
	    #'partner_id':'null',
	    #'sequence_number':'',
	    #'session_id':'',
	    #'currency_rate':'',
	    #'state':'',
	    #'account_move':'null',
	    #'note':'null',
	    #'nb_print':'',
	    #'pos_reference':'',
	    #'sale_journal':'',
	    #'fiscal_position_id':'',
	    #'to_invoice':'',
	    #'is_tipped':'',
	    #'tip_amount':'',
	    #'create_uid':'',
	    #'create_date':'',
	    #'write_uid':'',
	    #'write_date':'',
	    #'loyalty_points':'',
	    #'crm_team_id':''
	    #}
	    #rec = super(SalesModification, self).create(vals)
	    #order = self.env['pos.order']
	    #session = self._get_valid_session()
	    

	    #order.create(vals)
	    #crear el diccionario
	    #incluir el pos_id en el diccionario
	    #*#return rec

	#def _get_pos_order(self, order):
	#	PosSession = self.env['pos.session']
	#	closed_session = PosSession.browse(order['pos_session_id'])