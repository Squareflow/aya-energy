from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"


    categ_id = fields.Many2one(string="Service", related="product_id.categ_id", store=True)

    site_ids = fields.Many2many(string="Sites", comodel_name="res.partner", domain= lambda self:  [('type', '=', 'site')])
    salesman_id = fields.Many2one(related='order_id.user_id', store=True, string='Energy manager', readonly=True)


    @api.onchange('order_partner_id', 'product_id', 'name', 'product_uom_qty')
    def _on_partner_changed(self):
        _logger.info("on partner changed")
        for line in self:
            if line.order_id and line.order_id.partner_id:
                return {'domain': {'site_ids': [('type','=', 'site'),('id', 'in', line.order_id.partner_id.child_ids.ids)]}}