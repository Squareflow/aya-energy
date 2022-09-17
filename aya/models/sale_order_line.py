from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"


    categ_id = fields.Many2one(string="Service", related="product_id.categ_id", store=True)

    site_ids = fields.Many2many(string="Sites", comodel_name="res.partner", domain= lambda self:  [('type', '=', 'site')])
