# -*- coding: utf-8 -*-

import string
from odoo import models, fields, api
import json

class sales_dual_currencydos(models.Model):
    #_name = 'sales.dc'
    _inherit = "sale.order"

    
    #amount_dualc = fields.Monetary(string='Subtotal $', store=True)
    #price_dualc = fields.Monetary(string='Unit Price $', store=True)
    dual_invoice = fields.Boolean(string="invoice dual", default=False)
    tax_totals_dollar = fields.Char(compute='_compute_tax_totals_json')
    field_tax_base = fields.Char(string='Tax Base')


    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')

    def _compute_tax_totals_json(self):
        us=0
        res = super(sales_dual_currencydos, self)._compute_tax_totals_json()

        def compute_taxes(order_line):
            price2 = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
            order2 = order_line.order_id
            return order_line.tax_id._origin.compute_all(price2, order2.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order2.partner_shipping_id)
        account_move = self.env['account.move']
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        us = 1/daily_amount
       
        print (us, 'USD BCV')
        
        for order2 in self:
            usd_id =self.env['res.currency'].search([('name','=','USD')])
            tax_lines_data2 = account_move._prepare_tax_lines_data_for_totals_from_object(order2.order_line, compute_taxes)
            XZ = tax_lines_data2
            try:
                XZ = tax_lines_data2[0]
                XZ_VAL = XZ['tax_amount']
                XZ.update({'tax_amount': XZ_VAL / us})
            except:
                print ('no hay impuestos agregados')            
            tax_totals2 = account_move._get_tax_totals(order2.partner_id, tax_lines_data2, order2.amount_total/us, order2.amount_untaxed/us, usd_id)
            order2.tax_totals_dollar = json.dumps(tax_totals2)
            self.field_tax_base = order2.amount_total/us
        return res

