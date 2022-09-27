from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"


    categ_id = fields.Many2one(string="Service", related="product_id.categ_id", store=True)

    site_ids = fields.Many2many(string="Sites", comodel_name="res.partner", domain= lambda self:  [('type', '=', 'site')])
    all_site = fields.Boolean(string="All site", default=True)
    salesman_id = fields.Many2one(related='order_id.user_id', store=True, string='Energy manager', readonly=True)

    @api.onchange('site_ids')
    def _on_site_changed(self):
        for line in self:
            if not line.site_ids:
                line.all_site = True
            else:
                line.all_site = False

    @api.onchange('order_partner_id', 'product_id', 'name', 'product_uom_qty')
    def _on_partner_changed(self):
        _logger.info("on partner changed")
        for line in self:
            if line.order_id and line.order_id.partner_id:
                return {'domain': {'site_ids': [('type','=', 'site'),('id', 'in', line.order_id.partner_id.child_ids.ids)]}}

    def write(self, vals):
        old_categ = self.categ_id
        res = super(SaleOrderLine, self).write(vals)
        new_categ = self.categ_id
        if old_categ != new_categ:
            self.handle_unlink_rel(old_categ)
            self.handle_create_rel(new_categ)

        return res

    def handle_create_rel(self, categ):
        for line in self:
            if line.product_id and line.order_id.opportunity_id:
                rel = self.env["aya.service.rel"].search([("lead_id", "=", line.order_id.opportunity_id.id), ("service_id","=", categ.id)], limit=1)
                if not rel:
                    rel = self.env["aya.service.rel"].create({
                        "lead_id": line.order_id.opportunity_id.id,
                        "service_id": categ.id,
                    })            
        
    @api.model
    def create(self, vals):
        obj = super(SaleOrderLine, self).create(vals)
        obj.handle_create_rel(obj.categ_id)
        return obj

    def handle_unlink_rel(self, categ):
        for line in self:
            if line.order_id.opportunity_id and line.product_id:
                rel = self.env["aya.service.rel"].search([("lead_id", "=", line.order_id.opportunity_id.id), ("service_id","=", categ.id)], limit=1)
                if rel:
                    rel.unlink()            

    def unlink(self):
        for line in self:
            line.handle_unlink_rel(line.categ_id)
        return super(SaleOrderLine, self).unlink()