# -*- coding: utf-8 -*-

from email.policy import default
from operator import length_hint
import string
from odoo import models, fields, api
import json

class purchase_dual_currencydos(models.Model):
    #_name = 'sales.dc'
    _inherit = "purchase.order"
   
    def usd_modify(self):
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        us = 1/daily_amount
        return us
    field_tax_base = fields.Float(string='Usd Tasa', default=usd_modify, required=True)#campo
    tax_totals_json2 = fields.Char(string='Tax Base', store=True)
    currency_purchase = fields.Char(string='Rate USD', store=True) 


    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    @api.onchange('field_tax_base')
    def  _compute_tax_totals_json(self):
        res = super(purchase_dual_currencydos, self)._compute_tax_totals_json()
        def compute_taxes(order_line):

            return order_line.taxes_id._origin.compute_all(**order_line._prepare_compute_all_values())
        
        account_move = self.env['account.move']
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        us = 1/daily_amount
        us2 = self.field_tax_base
        for order2 in self:
            usd_id =self.env['res.currency'].search([('name','=','USD')])
            tax_lines_data2 = account_move._prepare_tax_lines_data_for_totals_from_object(order2.order_line, compute_taxes)
            XZ = tax_lines_data2
            try:
                XZ = tax_lines_data2[0]
                XZ_VAL = XZ['tax_amount']
                XZ.update({'tax_amount': XZ_VAL / us2})
            except:
                print ('no hay impuestos agregados')
            tax_totals2 = account_move._get_tax_totals(order2.partner_id,   tax_lines_data2, order2.amount_total/us2, order2.amount_untaxed/us2, usd_id)
            order2.tax_totals_json2 = json.dumps(tax_totals2)
        return res
    