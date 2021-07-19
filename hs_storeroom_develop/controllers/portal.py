# -*- coding: utf-8 -*-
import json
import logging
from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.account.controllers.portal import PortalAccount
from werkzeug.exceptions import Forbidden, NotFound

_logger = logging.getLogger(__name__)


class PortalInherit(PortalAccount):

	def _invoice_get_page_view_values(self, invoice, access_token, **kwargs):
		values = super(PortalInherit, self)._invoice_get_page_view_values(invoice, access_token, **kwargs)
		logging.info("Metodo llamado _invoice_get_page_view_values")
		logging.info(values)
		if values['acquirers']:
			acquirers = values.get('acquirers')
			values['acquirers'] = acquirers.filtered(lambda acq: acq.payment_section == 'invoice')
			"""
			acquieres_array = []
			for acq in values['acquirers']:
				if acq.payment_section == 'invoice':
					acquieres_array.append(acq)
			render_values['acquirers'] = acquieres_array
			"""
		return values