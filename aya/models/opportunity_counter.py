from odoo import _, api, fields, models

import logging
import datetime


_logger = logging.getLogger(__name__)

class OpportunityCounter(models.Model):
    _name = "aya.opportunity.counter"
    _description = "Aya opportunity counter"

    count = fields.Integer(string="Counter", default=1)

    year = fields.Integer(string="Year")


    def get_and_increment_count(self):
        for counter in self:
            this_year = datetime.datetime.now().year
            if this_year != counter.year:
                counter.count = 1
            count = counter.count
            counter.count += 1 
            counter.year = this_year
            return count           