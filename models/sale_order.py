# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime, timedelta
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_done = fields.Boolean(
        string='Picking done',
        compute='_compute_picking_done',
        search='_search_picking_done'
    )

    @api.multi
    def _compute_picking_done(self):
        for order in self:
            done = order.picking_ids.filtered(
                lambda x: x.state in ['done'])
            if len(done):
                order.picking_done = True
            else:
                order.picking_done = False

    @api.model
    def _search_picking_done(self, operator, operand):
        if operand == True:
            return [('picking_ids.state', '=', 'done')]
        else :
            return [('picking_ids.state', '!=', 'done')]

    @api.model
    def cancel_old_website_orders(self, hours_old=48):

        confirmation_date = datetime.now() - timedelta(hours=hours_old)
        order_ids = self.search([
            ('state', '=', 'sale'),
            ('picking_ids.state', 'not in', ['done', 'cancel']),
            ('confirmation_date', '<', fields.Datetime.to_string(confirmation_date)),
            ('team_id.team_type', '=',  'website')]).action_cancel()
