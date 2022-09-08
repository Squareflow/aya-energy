from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    service_ids = fields.One2many(string="Services", comodel_name="aya.service.rel", inverse_name="lead_id")
    


    @api.onchange('service_ids')
    def _on_mission_changed(self):
        for lead in self:
            ids = self.env["aya.service"].search([], limit=2)
            _logger.info("YO")
            _logger.info(ids)
            return {'domain': {'service_ids': [('service_id', 'in', ids.ids)]}}