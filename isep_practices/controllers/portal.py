from datetime import date

from odoo import http, _, fields, api
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, Controller, content_disposition
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager, get_records_pager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PracticesController(Controller):

    @http.route(['/practices'], type='http', auth='public', website=True)
    def my_practices(self, **kw):

        return http.request.render('isep_practices.practice_submenu')

    @http.route(['/my/practices'], type='http', auth='public', website=True)
    def my_practices_form(self, **kw):

        user_id = [user for user in request.env['res.users'].search([('id', '=', http.request.env.context.get('uid'))])]
        partner_id = [partner for partner in request.env['res.partner'].search([('id', '=', user_id[0].partner_id.id)])]
        country_id = [partner for partner in request.env['res.country'].search([('code', '=', 'ES')])]
        res_better_zip = [code_zip for code_zip in request.env['res.better.zip'].search([('state_id', '=', partner_id[0].state_id.id),
                                                                                         ('country_id', '=', country_id[0].id)])]
        #center_id = [center_p for center_p in request.env['res.partner'].search([('center', '=', True)])]
        tutor_id = [tutor_p for tutor_p in request.env['res.partner'].search([('tutor', '=', True)])]
        student_unique = [students for students in request.env['op.student'].search([('partner_id', '=', partner_id[0].id)])]

        student = ''
        admissions = ''
        center_id = ''
        #schedules = ''
        admi_id = ''
        schedules = request.env['practice.schedule'].search([])
        if len(student_unique) > 0:
            student = student_unique
            admissions = [admission for admission in request.env['op.admission'].search([('student_id', '=', student[0].id)])]
        if kw:
            print(kw['res_better_zip'])
            filter_admission = [admo for admo in request.env['op.admission'].search([('student_id', '=', student[0].id),
                                                                                     ('id', '=', kw['op_admission_id'])])]
            filter_course = request.env['practice.center.course'].search(
                [('op_course_id', '=', filter_admission[0].course_id.id)])
            course_center = [courses.partner_id.id for courses in filter_course]

            admi_id = kw['op_admission_id']

            if kw['res_better_zip'] != '':
                center_id = [center_p for center_p in request.env['res.partner'].search(
                    [('center', '=', True), ('zip', '=', kw['res_better_zip']), ('id', 'in', course_center)])]
                #center_schedule = [center_s.practice_schedule_id.id for center_s in center_id]
                #schedules = request.env['practice.schedule'].search([('id', 'in', center_schedule)])


        print(schedules)
        #print(res_better_zip)
        value = {
                    'center': center_id,
                    'tutor': tutor_id,
                    'student': student,
                    'admissions': admissions,
                    'res_better_zip': res_better_zip,
                    'schedule': schedules,
                    'server_admission': admi_id
        }
        print(http.request.context)
        return http.request.render('isep_practices.my_practices_form', value)

    @http.route(['/my/practice/create'], type='http', auth='public', website=True)
    def my_practices_create(self, **kw):
        request.env["practice.practice"].sudo().create(kw)
        print(kw)
