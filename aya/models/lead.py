from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    service_ids = fields.One2many(string="Services", comodel_name="aya.service.rel", inverse_name="lead_id")
    user_id = fields.Many2one('res.users', string='Energy manager', index=True, tracking=True, default=lambda self: self.env.user)

    contract_id = fields.Many2one(string="Contract", comodel_name="aya.contract")

    opportunity_code = fields.Char(string="Opportunity code", compute="_compute_opportunity_code", store=True)

    opportunity_count = fields.Integer(string="Opportunity_count")

    @api.model
    def create(self, vals):
        obj = super(Lead, self).create(vals)
        counter = self.env["aya.opportunity.counter"].search([], limit=1)
        if not counter:
            counter = self.env["aya.opportunity.counter"].create({})
        obj.opportunity_count = counter.count
        counter.count += 1
        return obj

    @api.depends("partner_id", "partner_id.client_code", "opportunity_count")
    def _compute_opportunity_code(self):
        for lead in self:
            if lead.partner_id:
                year = str(lead.create_date.year)[2:]
                if lead.create_date.month < 10:
                    month = "0"+ str(lead.create_date.month)
                else:
                    month = str(lead.create_date.month)
                code = lead.partner_id.client_code + "/" + year+"/"+month+"/"+ str(lead.opportunity_count)
                lead.opportunity_code = code
            else:
                lead.opportunity_code = "/"