from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
         ("private", "Private Address"),
         ("site", "Site")
        ], string='Address Type',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")