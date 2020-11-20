# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class Schedule(http.Controller):

    @http.route('/schedule/<int:id>/',type='http', auth='public', website=True)
    def teacher(self, id, **kw):
        schedules = request.env['sale.rent.schedule'].search([('id','=',id)])
        if schedules:
            status = ''
            if schedules.installment_status:
                if schedules.installment_status == 'paid':
                    status = 'Paid'
                if schedules.installment_status == 'partially_paid':
                    status = 'Partially Paid'
                if schedules.installment_status == 'cancel':
                    status = 'Cancel'
                if schedules.installment_status == 'default':
                    status = 'Default'

            return http.request.render('sale_rent_schedule_custom.installment_template1', {
                'customer': schedules.partner_id.name,
                'sale': schedules.sale_id.name,
                'booking': str(schedules.booking_id.booking_number),
                'amount': schedules.amount,
                'receipt_total': schedules.receipt_total,
                'property': str(schedules.property_id.name) +' ('+ str(schedules.asset_property_id.name) +')',
                'project': str(schedules.asset_property_id.name),
                'surcharge': schedules.surcharge,
                'cheque': schedules.cheque_detail,
                'overdue': schedules.pen_amt,
                'due_date': schedules.start_date,
                'delay_days': schedules.delay_days,
                'installment_status': status,
                'receipt_date': schedules.receipt_date,
            })

    def selected_schedule_function(self, selected_id):
        schedules = request.env['sale.rent.schedule'].search([('id','=',selected_id)])
        if schedules:
            status = ''
            if schedules.installment_status:
                if schedules.installment_status == 'paid':
                    status = 'Paid'
                if schedules.installment_status == 'partially_paid':
                    status = 'Partially Paid'
                if schedules.installment_status == 'cancel':
                    status = 'Cancel'
                if schedules.installment_status == 'default':
                    status = 'Default'
            return {
                'customer': schedules.partner_id.name,
                'sale': schedules.sale_id.name,
                'booking': str(schedules.booking_id.booking_number),
                'amount': schedules.amount,
                'receipt_total': schedules.receipt_total,
                'property': str(schedules.property_id.name) +' ('+ str(schedules.asset_property_id.name) +')',
                'project': str(schedules.asset_property_id.name),
                'surcharge': schedules.surcharge,
                'cheque': schedules.cheque_detail,
                'overdue': schedules.pen_amt,
                'due_date': schedules.start_date,
                'delay_days': schedules.delay_days,
                'installment_status': status,
                'receipt_date': schedules.receipt_date,
            }

    @http.route(['/schedule/'], type='http', auth="public", website=True)
    def schedule(self, **kwargs):
        selected_schedule_id = int(kwargs.get('id'))
        return request.env['ir.ui.view'].render_template("sale_rent_schedule_custom.installment_template",
                              self.selected_schedule_function(selected_schedule_id))