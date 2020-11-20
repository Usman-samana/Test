from odoo import models, fields, api


class AccountClearance(models.Model):
    _name = 'account.clearance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Account Clearance'

    subject = fields.Char('Subject')
    sequence = fields.Char('Sequence', readonly=True)
    clearance_type = fields.Many2one('clearance.type', 'Clearance Type')
    booking_id = fields.Many2one('crm.booking', 'Booking', related='spa.booking_id')
    spa = fields.Many2one('sale.order', 'Related SPA')
    project = fields.Many2one('account.asset.asset', 'Project', related='spa.booking_id.asset_project_id')
    property = fields.Many2one('account.asset.asset', 'Property', related='spa.booking_id.property_id')

    spa_status = fields.Selection([
        ('draft', 'Draft'),
        ('under_legal_review_print', 'Under legal Review for Print'),
        ('under_acc_verification_print', 'Under Account Verification for Print'),
        ('under_confirmation_print', 'Under Confirmation for Print'),
        ('unconfirmed_print', 'Unconfirmed SPA OK for Print'),
        ('under_legal_review', 'Under Legal Review'),
        ('under_acc_verification', 'Under Accounts Verify'),
        ('under_approval', 'Under Approval'),
        ('sale', 'Approved SPA'),
        ('refund_cancellation', 'Refund Cancellation'),
        ('reject', 'Rejected'),
        ('paid', 'Approved SPA-Paid'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='SPA Status', related='spa.state', readonly=True)

    booking_status = fields.Selection([
        ('draft', 'Draft'),
        ('under_discount_approval', 'Under Discount Approval'),
        ('tentative_booking', 'Tentative Booking'),
        ('review', 'Under Review'),
        ('confirm_spa', 'Confirmed for SPA'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancel')
    ], string='Booking Status', related='booking_id.is_buy_state', readonly=True)
    total_spa = fields.Float('Total SPA Value', compute='_spavalue')
    total_collection = fields.Float('Total Collection', compute='totalcoll')
    pending_collections = fields.Float('Pending Collections', compute='pending')
    total_due_amount = fields.Float('Total Due Amount', compute='installment')
    due_balance_collections = fields.Float('Balance Due Collection', compute='dueamount')

    @api.depends('spa','spa.total_spa_value')
    def _spavalue(self):
        for rec in self:
            rec.total_spa = rec.spa.total_spa_value

    @api.depends('spa','spa.total_receipts')
    def totalcoll(self):
        for rec in self:
            rec.total_collection = rec.spa.total_receipts

    @api.depends('spa','spa.pending_balance')
    def pending(self):
        for rec in self:
            rec.pending_collections = rec.spa.pending_balance

    @api.depends('spa','spa.instalmnt_bls_pend_plus_admin_oqood')
    def installment(self):
        for rec in self:
            rec.total_due_amount = rec.spa.instalmnt_bls_pend_plus_admin_oqood

    @api.depends('spa','spa.balance_due_collection')
    def dueamount(self):
        for rec in self:
            rec.due_balance_collections = rec.spa.balance_due_collection

    name = fields.Char('Name', related='booking_id.partner_id.name')
    partner_id = fields.Many2one('res.partner', string='Name', related='booking_id.partner_id')
    mobile = fields.Char('Mobile', related='booking_id.partner_id.mobile')
    email = fields.Char("Email", related='booking_id.partner_id.email')
    nationality = fields.Char("Nationality", related='booking_id.partner_id.nationality')
    address = fields.Char("Address", related='booking_id.partner_id.street')
    total_spa_customer = fields.Integer('Total SPA', readonly= True)
    total_bookings = fields.Integer("Total Bookings",readonly= True)

    due_amount_to_clear = fields.Char("Due Amount to Clear")
    account_remarks = fields.Text("Accounts Remarks")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_accounts_verification', 'Under Accounts Verification'),
        ('under_review', 'Under Review'),
        ('under_approval', 'Under Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancel', 'Canceled')
    ], string='Status', readonly=True, default='draft')

    def submit(self):
        for rec in self:
            rec.state = 'under_accounts_verification'

    def verify(self):
        for rec in self:
            rec.state = 'under_review'

    def review(self):
        for rec in self:
            rec.state = "under_approval"

    def approve(self):
        for rec in self:
            rec.state = "approved"

    def action_reject(self):
        for rec in self:
            rec.state = "rejected"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    @api.model
    def create(self, vals):
        if not vals.get('sequence', ''):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'account.clearance')
        result = super(AccountClearance, self).create(vals)
        return result

    @api.onchange('partner_id')
    def get_totals(self):
        spa_ids = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id), ('state', '!=', 'cancel')])
        cb_ids = self.env['crm.booking'].search([('partner_id', '=', self.partner_id.id), ('is_buy_state', '!=', 'cancel')])
        if spa_ids and self.partner_id:
            self.total_spa_customer = len(spa_ids.ids)
        else:
            self.total_spa_customer = False
        if cb_ids and self.partner_id:
            self.total_bookings = len(cb_ids.ids)
        else:
            self.total_bookings = False


class ClearanceType(models.Model):
    _name = 'clearance.type'
    _description = 'Clearance Type Form'

    name = fields.Char('Name')
    active = fields.Boolean(string='Active', default=True)
