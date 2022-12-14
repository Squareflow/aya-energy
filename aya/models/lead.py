from odoo import _, api, fields, models
import datetime
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
        obj.opportunity_count = counter.get_and_increment_count()

        return obj

    @api.depends("partner_id", "opportunity_count")
    def _compute_opportunity_code(self):
        for lead in self:
            if lead.partner_id:
                if not lead.create_date:
                    date = datetime.datetime.now()
                else:
                    date = lead.create_date
                year = str(date.year)[2:]
                if date.month < 10:
                    month = "0"+ str(date.month)
                else:
                    month = str(date.month)
                code = str(lead.partner_id.id).zfill(4) + year + month + str(lead.opportunity_count).zfill(4)
                lead.opportunity_code = code
            else:
                lead.opportunity_code = "/"