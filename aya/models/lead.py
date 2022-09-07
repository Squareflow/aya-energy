from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    service_ids = fields.Many2many(string="Services", comodel_name="aya.service", relation="aya.service.relation", column1="lead_id", column2="service_id")
    