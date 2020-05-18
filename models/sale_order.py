# -*- coding: utf-8 -*-

from odoo import models, fields,api
import logging
from odoo.tools import float_compare
from odoo.exceptions import UserError
from  datetime import datetime , timedelta 
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def cancel_old_website_orders(self,hours_old = 48):

        confirmation_date = datetime.now() - timedelta(hours = hours_old)
        order_ids = self.search([
            ('state','=','sale'),
            ('picking_ids.state','not in',['done','cancel']), 
            ('confirmation_date','<', fields.Datetime.to_string(confirmation_date)),
            ('team_id.team_type','=',  'website')]).action_cancel()
