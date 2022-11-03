# -*- encoding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import base64
import logging

logger = logging.getLogger(__name__)

class PracticePractice(models.Model):
    _name = 'practice.practice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Practice"
    _rec_name = 'op_admission_id'

    weekly_hours = fields.Float(string='Weekly Hours', compute="_compute_weekly_hours")
    total_hours = fields.Float(string='Total Hours', compute="_compute_total_hours")
    start_date = fields.Date(string='Start Date')
    final_date = fields.Date(string='Final Date')
    practice_temary_id = fields.Many2one('practice.temary', string='Temary')
    tutor_id = fields.Many2one('res.partner', string='Tutor')
    op_student_id = fields.Many2one('op.student', string='Student')
    op_admission_id = fields.Many2one("op.admission", 'Admission')
    status_phase = fields.Selection([
        ('in progress', 'En Espera'),
        ('started', 'Iniciada'),
        ('pending by rating', 'Pendiente por Nota'),
        ('finished', 'Finalizada'), ], 'Phase', track_visibility='onchange', default='in progress')
    email_send = fields.Selection([
        ('framework_specific', 'Convenio Marco y Convenio Especifico enviados por correo'),
        ('not_send', 'Convenios no enviados'), ], 'Status Agreement', track_visibility='onchange')
    status_sign_specific = fields.Selection([
        ('Signatures Pending', 'Firma en Trámite'),
        ('Fully Signed', 'Totalmente Firmado'),
        ('cancelled', 'Cancelado'), ], 'Status Sign Specific Agreement', track_visibility='onchange', compute="_status_sign")
    status_sign_framework = fields.Selection([
        ('Signatures Pending', 'Firma en Trámite'),
        ('Fully Signed', 'Totalmente Firmado'),
        ('cancelled', 'Cancelado'), ], 'Status Sign Framework Agreement', track_visibility='onchange', compute="_status_sign")
    op_course_id = fields.Many2one('op.course', string='Course', related='op_admission_id.course_id', store=True)
    remuneration_center = fields.Float(string='Remuneration Center')
    center_id = fields.Many2one('res.partner', string='Center', domain="[('center', '=', True)]")
    payment_center = fields.Boolean(string='Payment to the Center', default=False)
    morning = fields.Boolean(string='Morning', default=False)
    afternoon = fields.Boolean(string='Afternoon', default=False)
    sign_request_specific_agrement_id = fields.Integer()
    sign_request_framework_agrement_id = fields.Integer()
    active = fields.Boolean(default=True)


    '''
    def _check_dates(self, cr, uid, ids, context=None):
        print('Paso')
        for rec in self.browse(cr, uid, ids):
            start_date = rec.start_date
            final_date = rec.final_date
            if start_date < final_date:
                return True
        return False
    '''
    _sql_constraints = [
        ('check_dates',
         'CHECK (start_date <= final_date)',
         'Fecha de inicio no debe ser menor a fecha final.'),
    ]
    id_sign_request_framework = 0
    id_sign_request_specific = 0

    @api.one
    @api.depends('sign_request_specific_agrement_id', 'sign_request_framework_agrement_id')
    def _status_sign(self):
        sign_framework = self.env['sign.request'].search([('id', '=', self.sign_request_framework_agrement_id)])
        sign_specific = self.env['sign.request'].search([('id', '=', self.sign_request_specific_agrement_id)])
        if len(sign_specific) and len(sign_framework):
            if sign_specific.state == "sent":
                self.status_sign_specific = 'Signatures Pending'
            if sign_framework.state == "sent":
                self.status_sign_framework = 'Signatures Pending'
            if sign_specific.state == "signed":
                self.status_sign_specific = 'Fully Signed'
            if sign_framework.state == "signed":
                self.status_sign_framework = 'Fully Signed'
            if sign_specific.state == "cancelled":
                self.status_sign_specific = 'cancelled'
            if sign_framework.state == "cancelled":
                self.status_sign_framework = 'cancelled'

    @api.onchange('center_id', 'op_admission_id')
    def filterContactByCenter(self):
        course = self.env['practice.center.course'].search([('op_course_id', '=', self.op_admission_id.course_id.id)])
        course_center = [courses.partner_id.id for courses in course]
        return {'domain': {'center_id': [('center', '=', True), ('id', 'in', course_center)]}}

    @api.onchange('center_id', 'op_admission_id', 'morning', 'afternoon')
    def filterCenterByTurn(self):
        turn_morning = self.env['practice.schedule'].search([('turn', '=', 'morning')])
        turn_schedule_morning = [turns.id for turns in turn_morning]
        turn_afternoon = self.env['practice.schedule'].search([('turn', '=', 'afternoon')])
        turn_schedule_afternoon = [turns.id for turns in turn_afternoon]
        turn_both = self.env['practice.schedule'].search([('turn', '=', 'both')])
        turn_schedule_both = [turns.id for turns in turn_both]

        if self.morning and self.afternoon:
            return {'domain': {'center_id': [('practice_schedule_id', 'in', turn_schedule_both)]}}
        if self.morning:
            return {'domain': {'center_id': [('practice_schedule_id', 'in', turn_schedule_morning)]}}
        if self.afternoon:
            return {'domain': {'center_id': [('practice_schedule_id', 'in', turn_schedule_afternoon)]}}
        else:
            course = self.env['practice.center.course'].search(
                [('op_course_id', '=', self.op_admission_id.course_id.id)])
            course_center = [courses.partner_id.id for courses in course]
            return {'domain': {'center_id': [('center', '=', True), ('id', 'in', course_center)]}}

    @api.onchange('tutor_id', 'center_id', 'op_admission_id')
    def filterContactByTutor(self):
        center = self.env['practice.center.tutor'].search([('partner_id', '=', self.center_id.id)])
        center_tutor = [centers.tutor_id.id for centers in center]
        course = self.env['practice.tutor.course'].search([('op_course_id', '=', self.op_admission_id.course_id.id)])
        tutor_course = [courses.partner_id.id for courses in course]
        return {'domain': {'tutor_id': [('tutor', '=', True), ('id', 'in', center_tutor), ('id', 'in', tutor_course)]}}

    @api.onchange('op_admission_id', 'op_student_id')
    def filterAdmisionByStudent(self):
        return {'domain': {'op_admission_id': [('student_id', '=', self.op_student_id.id)]}}

    def getDay(self):
        if self.start_date and self.final_date:
            my_time = datetime.min.time()
            start_date_datetime = datetime.combine(self.start_date, my_time)
            final_date_datetime = datetime.combine(self.final_date, my_time)
            start_date_new = datetime.strptime(str(start_date_datetime), "%Y-%m-%d %H:%M:%S").date()
            final_date_new = datetime.strptime(str(final_date_datetime), "%Y-%m-%d %H:%M:%S").date()
            result_date = final_date_new - start_date_new
            days = str(result_date).replace(' days, 0:00:00', '')
            weeks = int(days) // 7
            return weeks

    @api.one
    @api.depends('start_date', 'final_date', 'total_hours')
    def _compute_weekly_hours(self):
        if self.total_hours > 0 and self.start_date and self.final_date:
            print(self.getDay())
            for practice in self:
                practice.weekly_hours = practice.total_hours // practice.getDay()

    @api.one
    @api.depends('op_admission_id.batch_id.code')
    def _compute_total_hours(self):
        op_batch = self.env['op.batch'].search([('code', '=', self.op_admission_id.batch_id.code)])
        op_batch_subject_rel = op_batch.op_batch_subject_rel_ids
        for op_batch_subject in op_batch_subject_rel:
            if 'práctica' in str(op_batch_subject.subject_id.name).lower():
                self.total_hours = op_batch_subject.hours
                break

    #send to sign center

    def email_framework_agreement(self):
        id = self.id
        # generate pdf from report, use report's id as reference
        REPORT_ID = 'isep_practices.report_framework_agreement_template'
        report = self.env['ir.actions.report'].search([('report_name', '=', REPORT_ID)], limit=1)
        pdf = report and report.render_qweb_pdf(id)
        pdfbytes = str(pdf[0]).encode()
        ATTACHMENT_NAME = "convenio_marco_practicas_isep_y_" + self.center_id.name + ".pdf"
        # pdf result is a list
        b64_pdf = base64.b64encode(pdf[0])
        pdfstring = "data:application/pdf;base64," + str(b64_pdf, 'utf-8')

        upl_tpl = self.env['sign.template'].upload_template(ATTACHMENT_NAME, pdfstring, True)
        template_id = upl_tpl['template'] or False
        attachment_id = upl_tpl['attachment'] or False
        items = dict()
        #posy4 = 0.521
        items.update({'1': {'required': True, 'responsible_id': 1, 'page': 2, 'type_id': 1, 'posX': 0.596,
                            'posY': 0.537, 'width': 0.200, 'height': 0.050}})
        template_id = self.env['sign.template'].update_from_pdfviewer(template_id, False, items)
        template = self.env['sign.template'].browse(template_id)

        sign_send_request = self.env['sign.send.request'].with_context(active_id=template_id)
        ssrdict = sign_send_request.default_get(
            ['signer_ids', 'signer_id', 'signers_count', 'is_user_signer', 'template_id', 'follower_ids', 'subject',
             'message', 'filename', 'extension'])
        print('center', self.center_id.id)

        signer_ids = [(0, 0, {'role': 1, 'partner_id': self.center_id.id})]
        ssrdict['signer_ids'] = signer_ids
        template_email = self.env.ref(
            'isep_practices.specific_framework_agreement_mail'
        )
        ssrdict['message'] = template_email.body_html
        ssrcreate = sign_send_request.create(ssrdict)

        signers = [{'partner_id': signer.partner_id.id, 'role': 1} for signer in ssrcreate.signer_ids]
        sigrdict = self.env['sign.request'].initialize_new(template_id, signers, ssrcreate.follower_ids.ids,
                                                           ATTACHMENT_NAME, ssrcreate.subject, ssrcreate.message,
                                                           send=True)
        sign_request = sigrdict['id'] or False
        token = sigrdict['token'] or False
        sign_token = sigrdict['sign_token'] or False

        if sign_request and token:
            sign_request_o = self.env['sign.request'].browse(sign_request)
            sign_request_o.write({'state': 'sent'})
            self.sign_request_framework_agrement_id = sign_request_o.id
            sign_request_items = sign_request_o and sign_request_o.request_item_ids
            if sign_request_items:
                sign_request_items.write({'state': 'sent'})
                self.sign_request_id = sign_request_items[0].id
            return True
        else:
            return False

    #send sign center and student

    def email_specific_agreement(self):
        id = self.id
        # generate pdf from report, use report's id as reference
        REPORT_ID = 'isep_practices.report_specific_agreement_template'
        report = self.env['ir.actions.report'].search([('report_name', '=', REPORT_ID)], limit=1)
        pdf = report and report.render_qweb_pdf(id)
        pdfbytes = str(pdf[0]).encode()
        ATTACHMENT_NAME = "convenio_especifico_" + self.op_student_id.name + ".pdf"
        # pdf result is a list
        b64_pdf = base64.b64encode(pdf[0])
        pdfstring = "data:application/pdf;base64," + str(b64_pdf, 'utf-8')

        upl_tpl = self.env['sign.template'].upload_template(ATTACHMENT_NAME, pdfstring, True)
        template_id = upl_tpl['template'] or False
        attachment_id = upl_tpl['attachment'] or False
        items = dict()
        #posy4 = 0.521
        items.update({'0': {'required': False, 'responsible_id': 1, 'page': 2, 'type_id': 1, 'posX': 0.634,
                            'posY': 0.460, 'width': 0.200, 'height': 0.050}})
        items.update({'1': {'required': False, 'responsible_id': 1, 'page': 2, 'type_id': 1, 'posX': 0.165,
                            'posY': 0.461, 'width': 0.200, 'height': 0.050}})
        template_id = self.env['sign.template'].update_from_pdfviewer(template_id, False, items)
        template = self.env['sign.template'].browse(template_id)

        sign_send_request = self.env['sign.send.request'].with_context(active_id=template_id)
        ssrdict = sign_send_request.default_get(
            ['signer_ids', 'signer_id', 'signers_count', 'is_user_signer', 'template_id', 'follower_ids', 'subject',
             'message', 'filename', 'extension'])
        print('center', self.center_id.id)

        signer_ids = [(0, 0, {'role': 1, 'partner_id': self.op_student_id.partner_id.id}), (0, 0, {'role': 1, 'partner_id': self.tutor_id.id})]
        ssrdict['signer_ids'] = signer_ids
        template_email = self.env.ref(
            'isep_practices.specific_framework_agreement_mail'
        )
        ssrdict['message'] = template_email.body_html

        ssrcreate = sign_send_request.create(ssrdict)

        signers = [{'partner_id': signer.partner_id.id, 'role': 1} for signer in ssrcreate.signer_ids]

        sigrdict = self.env['sign.request'].initialize_new(template_id, signers, ssrcreate.follower_ids.ids,
                                                           ATTACHMENT_NAME, ssrcreate.subject, ssrcreate.message,
                                                           send=True)
        sign_request = sigrdict['id'] or False
        token = sigrdict['token'] or False
        sign_token = sigrdict['sign_token'] or False

        if sign_request and token:
            sign_request_o = self.env['sign.request'].browse(sign_request)
            print(sign_request_o.id)
            self.sign_request_specific_agrement_id = sign_request_o.id
            sign_request_o.write({'state': 'sent'})
            sign_request_items = sign_request_o and sign_request_o.request_item_ids
            if sign_request_items:
                sign_request_items.write({'state': 'sent'})
                self.sign_request_id = sign_request_items[0].id
            return True
        else:
            return False

    def action_create_signature_request(self):
        practice = self.search([('id', '=', self.id)])
        if not self.sign_request_specific_agrement_id and not self.sign_request_framework_agrement_id:
            if self.email_framework_agreement() and self.email_specific_agreement():
                value = {
                    'email_send': 'framework_specific',
                }
                practice.write(value)
            else:
                practice.write({'email_send': 'not_send'})
                raise UserError(_(
                    "Ha ocurrido un error al momento de generar la petición de firma, contacte con el administrador del sistema."))
        else:
            raise UserError(_(
                "No se puede enviar el convenio a firmar más de una vez"))

    @api.model
    def start_practice(self):
        practices = self.search([('start_date', '=', date.today())])
        if len(practices):
            for practice in practices:
                value = {'status_phase': 'started'}
                practice.write(value)
                logger.info('****************************************')
                logger.info('* UPDATE PHASE OF PRACTICE TO STARTED  *')
                logger.info('****************************************')

    @api.model
    def finish_practice(self):
        practices = self.search([('final_date', '<=', date.today())])
        if len(practices):
            print(practices)
            for practice in practices:
                if practice.status_phase != 'finished':
                    op_exam_attendees = self.env['op.exam.attendees'].search(
                        [('student_id', '=', practice.op_student_id.id),
                         ('course_id', '=', practice.op_admission_id.course_id.id),
                         ('batch_id', '=', practice.op_admission_id.batch_id.id)])
                    if len(op_exam_attendees):
                        for op_exam_attendee in op_exam_attendees:
                            print(op_exam_attendee)
                            op_exam = self.env['op.exam'].search(
                                [('id', '=', op_exam_attendee.exam_id.id)])
                            if len(op_exam):
                                print(op_exam)
                                if 'práctica' in str(op_exam.subject_id.name).lower() or 'practica' in str(
                                        op_exam.subject_id.name).lower():
                                    if op_exam_attendee.marks > 0:

                                        value = {'status_phase': 'finished'}
                                        practice.write(value)
                                        logger.info('****************************************')
                                        logger.info('* UPDATE PHASE OF PRACTICE TO FINISHED *')
                                        logger.info('****************************************')
                                    else:
                                        if practice.status_phase != 'pending by rating':
                                            value = {'status_phase': 'pending by rating'}
                                            practice.write(value)
                                            logger.info('*************************************************')
                                            logger.info('* UPDATE PHASE OF PRACTICE TO PENDING BY RATING *')
                                            logger.info('*************************************************')
