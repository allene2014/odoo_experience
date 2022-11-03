# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sales_dual_currency(models.Model):
    _inherit = "sale.order.line"


    
    amount_dualc = fields.Float(string='Subtotal $', compute='_compute_amount', store=True, tracking=4)
    price_dualc = fields.Float(string='Unit Price $', compute='_compute_amount', store=True)


    #@api.depends('order_line.price_total')

    @api.onchange('price_total')
    def _compute_amount(self):
        tasa = 0
        res = super(sales_dual_currency, self)._compute_amount()
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        print (daily_amount, 'last')
        tasa = 1/daily_amount
        print (tasa, 'USD BCV') 
        for rec in self:
            rec.amount_dualc = rec.price_total / tasa
            rec.price_dualc = rec.price_unit / tasa
        return res




    

