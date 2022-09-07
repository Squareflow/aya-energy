from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Service(models.Model):
    _name = "aya.service"
    _description = "Aya Service"

    name = fields.Char(string="Name")