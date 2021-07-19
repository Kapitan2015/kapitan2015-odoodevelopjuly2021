from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class InvoiceRefund(models.TransientModel):

	_inherit = "account.invoice.refund"
	
	@api.multi
	def invoice_refund(self):
		super(InvoiceRefund, self).invoice_refund()
		# refund = self.env.ref('account.action_invoice_tree1').read()[0]
		# refund['target'] = 'main'
		return {
			"type": "ir.actions.act_window",
			'view_type': 'form',
			'view_mode': 'tree,form',
			"res_model": "account.invoice",
        }
		
		# <field name="auto_refresh">10</field>
		# refund['tag'] ='reload'
		# refund['target'] = 'new'
		# view_ref = self.env.ref('account.invoice_form')
		# refund['views'] = 'action_invoice_tree1'
		
		# if self._context.get('active_model') == 'account.invoice.refund' and 'action_invoice_out_refund':
		# 	ctx = dict(self._context)
		# 	# _logger.info(self._context)
		# 	ctx['active_model'] = 'account.invoice'
		# 	ctx['active_id'] = self.id
		# 	ctx['type'] = 'out_invoice'
		# 	ctx['default_type'] = 'out_invoice'
		# 	ctx['active_ids'] = (self.ids)
		# 	# active_ids': [94], 'default_type': 'out_refund'
		# 	logging.info("Valor de CTX: " + str(ctx))
		# 	refund['context'] = self.with_context(ctx)
		# _logger.info(refund)
		# return refund

	""" def invoice_refund(self, mode='modify'):
		refund = super(InvoiceRefund, self).invoice_refund()
		if mode == 'modify':
			if type == 'out_invoice':
				if self._context.get('active_model') == 'account.invoice.refund':
					ctx = dict(self._context)
					_logger.info(self._context)
					ctx['active_model'] = 'account.invoice'
					ctx['active_id'] = self.id
					ctx['type'] = 'out_invoice'
					logging.info("Valor de CTX: " + str(ctx))
			# template.with_context(ctx)
				refund['target'] = 'main'
				refund['context'] = self.with_context(ctx)
		_logger.info(refund)
		return refund """

