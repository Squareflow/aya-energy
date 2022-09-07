from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class ServiceRelation(models.Model):
    _name = "aya.service.rel"
    _description = "Service Relation"

    name = fields.Char(string="Name")
    service_id = fields.Many2one(string="Service", comodel_name="aya.service")
    lead_id = fields.Many2one(string="Lead", comodel_name="crm.lead")