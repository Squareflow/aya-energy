from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class ServiceRelation(models.Model):
    _name = "aya.service.rel"
    _description = "Service Relation"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    service_id = fields.Many2one(string="Service", comodel_name="aya.service", required=True)
    lead_id = fields.Many2one(string="Lead", comodel_name="crm.lead")
    partner_id = fields.Many2one(string="Client", related="lead_id.partner_id", store=True)
    user_id = fields.Many2one(string="Energy partner", related="lead_id.user_id", store=True)
    stage_id = fields.Many2one(string="Stage", related="lead_id.stage_id", store=True)


    @api.depends('service_id', 'partner_id')
    def _compute_name(self):
        for rel in self:
            if rel.service_id and rel.partner_id:
                rel.name = rel.service_id.name + " " + rel.partner_id.name
            else:
                rel.name = "/"
