from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class OpportunityCounter(models.Model):
    _name = "aya.opportunity.counter"
    _description = "Aya opportunity counter"

    count = fields.Integer(string="Counter", default=1)