from odoo import _, api, fields, models

import logging


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


    def mark_as_waiting(self):
        for order in self:
            order.state = "waiting"
    

    def mark_as_approved(self):
        for order in self:
            order.state = "approved"
            if order.partner_id:
                order.message_post(partner_ids=[order.user_id.partner_id], body="The offer "+order.name+" for the client "+order.partner_id+" has been approved. You can now send it.")

    def reject_order(self):
        for order in self:
            order.state = "draft"
            if order.partner_id:
                order.message_post(partner_ids=[order.user_id.partner_id], body="The offer "+order.name+" for the client "+order.partner_id+" has been rejected please modify it.")