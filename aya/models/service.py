from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class Service(models.Model):
    _name = "product.category"
    _inherit = "product.category"
    _description = "Aya Service"
