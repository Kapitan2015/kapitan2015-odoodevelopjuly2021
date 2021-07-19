# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



import logging
_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
	_inherit = 'ir.attachment'

	@api.model_create_multi
	def create(self, vals_list):
		if self._context.get('active_model', '') == 'account.invoice.refund' or self._context.get('active_model', '') == 'res.partner':
			ctx = dict(self.env.context or {})
			ctx['default_type'] = 'binary'
			ctx.pop('active_model', None)
			logging.info("CONTEXTO: " + str(ctx))
			return super(IrAttachment, self).with_context(ctx).create(vals_list)
		else:
			return super(IrAttachment, self).create(vals_list)


class IrActionsReport(models.Model):
	_inherit = 'ir.actions.report'


	@api.multi
	def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
		return super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content=pdf_content, res_ids=res_ids)
