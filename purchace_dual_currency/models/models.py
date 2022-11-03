# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class purchace_dual_currency(models.Model):
#     _name = 'purchace_dual_currency.purchace_dual_currency'
#     _description = 'purchace_dual_currency.purchace_dual_currency'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
