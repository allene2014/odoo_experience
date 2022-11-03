# -*- encoding: utf-8 -*-
from odoo import fields, models

class PracticeTemary(models.Model):
    _name = 'practice.temary'
    _description = "Temary"

    name = fields.Char(string='Name', size=200)
    content = fields.Text(string='Content')
    op_course_id = fields.Many2one('op.course', string="Course")
    active = fields.Boolean(default=True)
