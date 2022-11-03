# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api


class sales_dual_currency(models.Model):
    _inherit = ["purchase.order.line"]

    def usd_modify(self):
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        us = 1/daily_amount
        return us
    field_tax_base = fields.Float(string='Usd Tasa', related='order_id.field_tax_base', default=usd_modify, required=True)

    
    price_dual = fields.Float(string='$ Price unit', compute='_compute_amount', readonly=False, store=True)
    subtotal_dual = fields.Float(string='$ Subtotal', compute='_compute_amount', store=True)
    field_test = fields.Float(string='Usd Tasa')
    

    @api.onchange('price_unit')
    def _compute_amount(self):
        tasa = 0
        res = super(sales_dual_currency, self)._compute_amount()
        daily_amount = self.env['res.currency'].search([('name','=','USD')], limit=1).rate
        tasa = 1/daily_amount
        print (tasa, 'USD BCV')


        for rec in self:
            try:
                rec.price_dual = rec.price_unit / self.field_tax_base
                rec.subtotal_dual = rec.price_total / self.field_tax_base
            except:
                "valores"
        

        return res




