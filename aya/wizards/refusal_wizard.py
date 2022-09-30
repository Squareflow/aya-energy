from odoo import _, api, fields, models

import logging
import datetime

_logger = logging.getLogger(__name__)

class RefusalWizard(models.TransientModel):
    _name = "aya.refusal.wizard"
    _description = "Aya Refusal Wizard"


    order_id = fields.Many2one(string="Offer", comodel_name="sale.order")
    refusal_comment = fields.Text(string="Refusal reason")

    def refuse(self):
        for wizard in self:
            wizard.order_id.state = "draft"
            if wizard.order_id.partner_id:
                if datetime.datetime.now().weekday() < 4:
                    next_date = datetime.datetime.now()+ datetime.timedelta(days=1)
                else:
                    next_date = datetime.datetime.now()+ datetime.timedelta(days=7 - datetime.datetime.now().weekday())
                wizard.order_id.activity_schedule("note.mail_activity_data_reminder", summary='Offer rejected', note= "The offer "+wizard.order_id.name+" for the client "+wizard.order_id.partner_id.name+" has been rejected please modify it.\n <br/> Refusal reason: "+wizard.refusal_comment, user_id= wizard.order_id.user_id.id, date_deadline= next_date)
            #wizard.order_id.message_post(body=wizard.refusal_comment)