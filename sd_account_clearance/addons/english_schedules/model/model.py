# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo.addons.mail.models import mail_template


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    schedule_a_eng = fields.Text('Schedule A')
    schedule_b_eng = fields.Text('Schedule B')
    schedule_c_eng = fields.Text('Schedule C')
    schedule_d_eng = fields.Text('Schedule D')
    schedule_e_eng = fields.Text('Schedule E')
    schedule_f_eng = fields.Text('Schedule F')
    schedule_g_eng = fields.Text('Schedule G')
    schedule_h_eng = fields.Text('Schedule H')
    schedule_i_eng = fields.Text('Schedule I')

    @api.onchange('booking_id')
    def onchange_asset_project_id(self):
        self.schedule_a = self.booking_id.asset_project_id.schedule_a
        self.schedule_b = self.booking_id.asset_project_id.schedule_b
        self.schedule_c = self.booking_id.asset_project_id.schedule_c
        self.schedule_d = self.booking_id.asset_project_id.schedule_d
        self.schedule_e = self.booking_id.asset_project_id.schedule_e
        self.schedule_f = self.booking_id.asset_project_id.schedule_f
        self.schedule_g = self.booking_id.asset_project_id.schedule_g
        self.schedule_h = self.booking_id.asset_project_id.schedule_h
        self.schedule_i = self.booking_id.asset_project_id.schedule_i
        self.schedule_a_eng = self.booking_id.asset_project_id.schedule_a_eng
        self.schedule_b_eng = self.booking_id.asset_project_id.schedule_b_eng
        self.schedule_c_eng = self.booking_id.asset_project_id.schedule_c_eng
        self.schedule_d_eng = self.booking_id.asset_project_id.schedule_d_eng
        self.schedule_e_eng = self.booking_id.asset_project_id.schedule_e_eng
        self.schedule_f_eng = self.booking_id.asset_project_id.schedule_f_eng
        self.schedule_g_eng = self.booking_id.asset_project_id.schedule_g_eng
        self.schedule_h_eng = self.booking_id.asset_project_id.schedule_h_eng
        self.schedule_i_eng = self.booking_id.asset_project_id.schedule_i_eng
        sales_terms_ids = self.env['sale.payment.term'].search(
            [('asset_project_id', '=', self.booking_id.asset_project_id.id)])
        self.sale_term_id = self.asset_project_id.sale_term_id.id
        return {'domain': {'sale_term_id': [('id', 'in', sales_terms_ids.ids)]}}

    @api.model
    def get_eng_schedules_from_project(self):
        sos = self.env['sale.order'].search([])
        for rec in sos:
            proj = self.env['account.asset.asset'].search([('id', '=', rec.booking_id.asset_project_id.id)])
            if proj:
                rec.schedule_a_eng = proj.schedule_a_eng
                rec.schedule_b_eng = proj.schedule_b_eng
                rec.schedule_c_eng = proj.schedule_c_eng
                rec.schedule_d_eng = proj.schedule_d_eng
                rec.schedule_e_eng = proj.schedule_e_eng
                rec.schedule_f_eng = proj.schedule_f_eng
                rec.schedule_g_eng = proj.schedule_g_eng
                rec.schedule_h_eng = proj.schedule_h_eng
                rec.schedule_i_eng = proj.schedule_i_eng

    @api.model
    def unset_spa_terms(self):
        sos = self.env['sale.order'].search([])
        for rec in sos:
            if not rec.spa_terms_copy:
                rec.spa_terms_copy = rec.sale_term_id.text


class AccountAssetAsset(models.Model):
    _inherit = "account.asset.asset"


    schedule_a_eng = fields.Text('Schedule A')
    schedule_b_eng = fields.Text('Schedule B')
    schedule_c_eng = fields.Text('Schedule C')
    schedule_d_eng = fields.Text('Schedule D')
    schedule_e_eng = fields.Text('Schedule E')
    schedule_f_eng = fields.Text('Schedule F')
    schedule_g_eng = fields.Text('Schedule G')
    schedule_h_eng = fields.Text('Schedule H')
    schedule_i_eng = fields.Text('Schedule I')