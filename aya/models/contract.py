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


    lead_ids = fields.One2many(string="Leads", comodel_name="crm.lead", inverse_name="contract_id")