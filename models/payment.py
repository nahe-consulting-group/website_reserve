# -*- coding: utf-8 -*-

from odoo import models, fields,api
import logging
from odoo.tools import float_compare
from odoo.exceptions import UserError
from  datetime import datetime , timedelta 
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    def _confirm_so(self):
        """ Check tx state, confirm the potential SO """
        self.ensure_one()
        if self.sale_order_id.state not in ['draft', 'sent', 'sale']:
            _logger.warning('<%s> transaction STATE INCORRECT for order %s (ID %s, state %s)', self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id, self.sale_order_id.state)
            return 'pay_sale_invalid_doc_state'
        if not float_compare(self.amount, self.sale_order_id.amount_total, 2) == 0:
            _logger.warning(
                '<%s> transaction AMOUNT MISMATCH for order %s (ID %s): expected %r, got %r',
                self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id,
                self.sale_order_id.amount_total, self.amount,
            )
            self.sale_order_id.message_post(
                subject=_("Amount Mismatch (%s)") % self.acquirer_id.provider,
                body=_("The sale order was not confirmed despite response from the acquirer (%s): SO amount is %r but acquirer replied with %r.") % (
                    self.acquirer_id.provider,
                    self.sale_order_id.amount_total,
                    self.amount,
                )
            )
            return 'pay_sale_tx_amount'

        if self.state == 'authorized' and self.acquirer_id.capture_manually:
            _logger.info('<%s> transaction authorized, auto-confirming order %s (ID %s)', self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id)
            if self.sale_order_id.state in ('draft', 'sent'):
                self.sale_order_id.with_context(send_email=True).action_confirm()
        elif self.state == 'done':
            _logger.info('<%s> transaction completed, auto-confirming order %s (ID %s)', self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id)
            if self.sale_order_id.state in ('draft', 'sent'):
                self.sale_order_id.with_context(send_email=True).action_confirm()
        elif self.state not in ['cancel', 'error'] and self.sale_order_id.state == 'draft':
            _logger.info('<%s> transaction pending/to confirm manually, sending quote email for order %s (ID %s)', self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id)
            self.sale_order_id.force_quotation_send()
        else:
            _logger.warning('<%s> transaction MISMATCH for order %s (ID %s)', self.acquirer_id.provider, self.sale_order_id.name, self.sale_order_id.id)
            return 'pay_sale_tx_state'
        return True