from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Contract(models.Model):
    _name = "aya.contract"
    _description = "Framework agreement"

    name = fields.Char(string="Nom")
    contact_id = fields.Many2one(string="Client", comodel_name="res.partner")
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")

    order_id = fields.Many2one(string="Sale order", comodel_name="sale.order")

    lead_ids = fields.One2many(string="Leads", comodel_name="crm.lead", inverse_name="contract_id")


    def action_get_order(self):
        for contract in self:
            return {
                    'name': 'Framework agreeme,t',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'target': "self",
                    'res_id': self.order_id.id,
                }