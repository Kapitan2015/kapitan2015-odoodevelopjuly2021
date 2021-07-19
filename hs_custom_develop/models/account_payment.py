# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo import exceptions


import logging
_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
	_inherit = 'account.payment'


	@api.multi
	def cancel(self):
		"""Sobreescribimos el metodo cancel para evitar que se pueda cancelar
		un pago si el mismo tiene asignado uno o varias facturas.
		"""
		for payment in self:
			if payment.reconciled_invoice_ids:
				raise exceptions.UserError(_('No puede cancelar pagos que esten asignados a una factura.'
				'Rompa la relación con la factura y cancele el pago.'))

		return super(AccountPayment, self).cancel()