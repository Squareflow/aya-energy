from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class EAN(models.Model):
    _name = "aya.ean"
    _description = "Aya EAN"

    contact_id = fields.Many2one(string="Customer")
    name = fields.Char(string="EAN code", required=True)
    type = fields.Selection(string="Type", selection=[("gas", "Gas"), ("elec", "Electricity")], required=True)
    consumption = fields.Float(string="(in MWH) Consumption")
    network = fields.Selection(string="Network", selection=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    capacity = fields.Float(string="(in KVA) Capacity ")
    supplier = fields.Many2one(string="Supplier", comodel_name="res.partner")

