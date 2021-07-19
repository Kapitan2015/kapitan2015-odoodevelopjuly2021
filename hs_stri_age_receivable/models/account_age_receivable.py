# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, exceptions, _

from odoo.tools import float_is_zero
from odoo.tools.misc import format_date
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class AgeReceivableInherit(models.AbstractModel):
	_inherit = "account.aged.receivable"


	def _get_columns_name(self, options):
		columns = super(AgeReceivableInherit, self)._get_columns_name(options)

		# Actualizamos el valor de la JRNL por No. Documento 
		columns[3] = {'name': _('Document')}

		# Eliminamos la columna JRNL, Pos: 1
		columns.pop(1)

		# Eliminamos la columna account, Pos 2 -> 1
		columns.pop(1)

		# Nada a pasado
		return columns


	def _get_document_name(self, item):
		uid = item.get('id')
		doc_type = item.get('caret_options')
		entry = self.env['account.move.line'].browse(uid)
		if entry.invoice_id:
			document = entry.invoice_id.number
		elif entry.statement_id:
			document = entry.statement_id.name
		else:
			document = entry.payment_id.name
		return document


	@api.model
	def _get_lines(self, options, line_id=None):
		lines = super(AgeReceivableInherit, self)._get_lines(options, line_id=line_id)
		for item in lines:
			if item.get('level') == 2:
				# removemos la columna JRNL y la columna account
				columns = item.get('columns')
				columns.pop(0)
				columns.pop(0)
				item['columns'] = columns

			elif item.get('level') == 4:
				# removemos la columna JRNL y la columna account
				columns = item.get('columns')
				columns.pop(0)
				columns.pop(0)


				# Obtenemos el ID y asi obtener la info a mostrar en
				# la columna Document
				columns[0] = {'name': self._get_document_name(item) }

				# Actualizamos la columna de referencia
				item['columns'] = columns
		return lines
