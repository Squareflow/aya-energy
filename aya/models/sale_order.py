from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging
import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting', "Waiting for approval"),
        ('approved', "Approved"),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    is_a_contract_agreement = fields.Boolean(string="Is a framework agreement")
    contract_id = fields.Many2one(string="Framework agreement", comodel_name="aya.contract")


    def handle_assign_contract(self):
        for order in self:
            contracts = self.env["sale.order"].search([("contract_id","=", order.contract_id.id)])
            if len(contracts) > 1:
                raise UserError("The framework agreement is already linked to another Sale order")
            order.contract_id.order_id = order.id

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if "contract_id" in vals and self.contract_id:
            self.handle_assign_contract()
        return res

    @api.model
    def create(self, vals):
        obj = super(SaleOrder, self).create(vals)
        if obj.contract_id:
            obj.handle_assign_contract()
        return obj

    def mark_as_waiting(self):
        for order in self:
            order.state = "waiting"
    

    def mark_as_approved(self):
        for order in self:
            order.state = "approved"
            if order.partner_id:
                if datetime.datetime.now().weekday() < 4:
                    next_date = datetime.datetime.now()+ datetime.timedelta(days=1)
                else:
                    next_date = datetime.datetime.now()+ datetime.timedelta(days=7 - datetime.datetime.now().weekday())
                order.activity_schedule("note.mail_activity_data_reminder", summary='Offer approved', note= "The offer "+order.name+" for the client "+order.partner_id.name+" has been approved. You can now send it.", user_id= order.user_id.id, date_deadline= next_date)
                
                #order.message_post(partner_ids=[order.user_id.partner_id.id], body="The offer "+order.name+" for the client "+order.partner_id.name+" has been approved. You can now send it.")

    def reject_order(self):
        for order in self:
            view = self.env.ref('aya.aya_refusal_form')
            return {
            'name': 'Refusal reason ',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'aya.refusal.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                "default_order_id": order.id,
                },
            }