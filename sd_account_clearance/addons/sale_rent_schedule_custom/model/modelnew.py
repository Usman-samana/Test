# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.tools.translate import _
import time
from odoo.exceptions import UserError,Warning, ValidationError
from odoo import http


class SaleRentSchedule(models.Model):
    _inherit= "sale.rent.schedule"

    @api.model
    def send_installment_email(self):

        srs = self.env['sale.rent.schedule'].search([('state', '=', 'confirm')])
        for rec in srs:
            if rec.start_date:
                current_date = datetime.now().date()
                st_date = rec.start_date
                dates_diff = rec.start_date - current_date
                days = dates_diff.days
                # mr = self.env['mail.recipients'].search([('name','=','Courier Recipients')])
                # for rec in mr:
                #     if rec.user_ids:
                if days in [7,15]:
                    email_template = rec.env.ref('sale_rent_schedule_custom.email_next_installment')
                    outgoing_server = rec.env['ir.mail_server'].search([('smtp_user','=','noreply@samanadevelopers.com1')])
                    email_template.mail_server_id = outgoing_server.id
                    email_template.send_mail(rec.id, force_send=True)
                    # rec.env.cr.commit()

    @api.multi
    def open_pay_form(self):
        return {
            'name'     : 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type'     : 'ir.actions.act_url',
            'target'   : 'self',
            'url'      : 'http://samanadevelopers.com/pay/'
               }

    @api.multi
    def get_url(self,record):
        # action_id = record.env.ref('sale_rent_schedule_custom.action_sale_rent_mail')
        base_url = record.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/schedule/?id=' + str(
            record.id)
        # base_url = http.request.env['ir.config_parameter'].get_param('web.base.url') + '/web?id=' + str(
        #     record.id) + '&action=' + str(action_id.id) + '&' + 'model=' + record._name + '&' + 'view_type=form'
        return base_url


    @api.multi
    def create_invoice_auto(self):
        """
        Create invoice for Rent Schedule.
        @param self: The object pointer
        """

        inv_obj = self.env['account.invoice']
        sale_rent = self.env['sale.rent.schedule'].search([('start_date','<=',datetime.now().date()),('inv','!=',True)])
       
        for rec in sale_rent:
            if rec.sale_id and rec.booking_id:
                inv_line_values = rec.get_invloice_lines()
                inv_values = {
                    'sale_rent_sched_id':rec.id,
                    'partner_id': rec.sale_id.booking_id.partner_id.id or False,
                    'type': 'out_invoice',
                    'date_due': rec.start_date,
                    'property_id': rec.sale_id.booking_id.property_id.id or False,
                    'asset_project_id': rec.asset_property_id.id if rec.asset_property_id else rec.sale_id.booking_id.asset_project_id.id or False,
                    'date_invoice': datetime.now().strftime(
                        DEFAULT_SERVER_DATE_FORMAT) or False,
                    'invoice_line_ids': inv_line_values,
                }
                invoice_id = inv_obj.create(inv_values)
                invoice_id.action_invoice_open()
                rec.write({'invc_id': invoice_id.id, 'inv': True})
                payment = rec.env['account.payment'].search([('state','=','posted'),('spa_id','=', rec.sale_id.id)])
                unreconciled_payments = []
                for p in payment:
                    if p.journal_entry_id.line_ids.filtered(
                            lambda b: b.account_id.internal_type == 'receivable' and not b.reconciled).id in p.journal_entry_id.line_ids.ids:
                        unreconciled_payments.append(p.id)
                if unreconciled_payments:

                    for pay in rec.env['account.payment'].search([('id','in',unreconciled_payments)],order="payment_date ASC"):
                        if invoice_id.residual > 0:
                            payment_line = pay.journal_entry_id.line_ids.filtered(lambda a: a.account_id.internal_type == 'receivable')
                            if payment_line:
                                invoice_id.register_payment(payment_line)
                                # payment_line.reconciled = True
                        else:
                             break
                # inv_form_id = self.env.ref('account.invoice_form').id

    @api.multi
    def create_invoice(self):
        """
        Create invoice for Rent Schedule.
        @param self: The object pointer
        """

        for rec in self:
            inv_obj = rec.env['account.invoice']
            inv_line_values = rec.get_invloice_lines()
            inv_values = {
                'sale_rent_sched_id':rec.id,
                'partner_id': rec.sale_id.booking_id.partner_id.id or False,
                'type': 'out_invoice',
                'date_due': rec.start_date,
                'property_id': rec.property_id.id if rec.property_id else rec.sale_id.booking_id.property_id.id or False,
                'asset_project_id': rec.asset_property_id.id if rec.asset_property_id else rec.sale_id.booking_id.asset_project_id.id or False,
                'date_invoice': datetime.now().strftime(
                    DEFAULT_SERVER_DATE_FORMAT) or False,
                'invoice_line_ids': inv_line_values,
            }
            invoice_id = inv_obj.create(inv_values)
            invoice_id.action_invoice_open()
            rec.write({'invc_id': invoice_id.id, 'inv': True})
            rec.update({'invoice_ids': [(6, 0, invoice_id.ids)]})
            payment = rec.env['account.payment'].search([('state','=','posted'),('spa_id','=', rec.sale_id.id)])
            unreconciled_payments = []
            for p in payment:
                if p.journal_entry_id.line_ids.filtered(
                        lambda b: b.account_id.internal_type == 'receivable' and not b.reconciled).id in p.journal_entry_id.line_ids.ids:
                    unreconciled_payments.append(p.id)
            if unreconciled_payments:

                for pay in rec.env['account.payment'].search([('id','in',unreconciled_payments)],order="payment_date ASC"):
                    if invoice_id.residual > 0:
                        payment_line = pay.journal_entry_id.line_ids.filtered(lambda a: a.account_id.internal_type == 'receivable')
                        if payment_line:
                            invoice_id.register_payment(payment_line)
                            # payment_line.reconciled = True
                    else:
                         break
            inv_form_id = rec.env.ref('account.invoice_form').id

            return {
                'view_type': 'form',
                'view_id': inv_form_id,
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'res_id': rec.invc_id.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        if self.payment_type == 'inbound':
            self.check_reconcile()
        return res
