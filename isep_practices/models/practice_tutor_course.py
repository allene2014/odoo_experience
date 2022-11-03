# -*- encoding: utf-8 -*-
from odoo import fields, models

class PracticeTutorCourse(models.Model):
    _name = 'practice.tutor.course'
    _description = "Association course with tutor"
    _rec_name = 'op_course_id'

    op_course_id = fields.Many2one('op.course', string="Course", required=True)
    tutor_id = fields.Char(related='partner_id.name')
    partner_id = fields.Many2one('res.partner')