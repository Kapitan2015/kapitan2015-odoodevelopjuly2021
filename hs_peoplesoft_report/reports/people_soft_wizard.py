# -*- coding: utf-8 -*-


from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class PeopleSoftWizard(models.TransientModel):
	_name = 'account.people.soft.wizard'
	_description = 'Final People Soft Wizzard'

	message = fields.Text(string="Advertencia", default="Esta apunto de "\
		"crear un reporte final de people soft. Una vez presione el boton "\
		"de aceptar, las facturas seleccionadas no estaran disponibles en "\
		"otros reportes finales de people soft.")


	def open_people_soft(self):
		doc_ids = self.env.context['active_ids']
		context = {
			'model':'account.peaplesoft.report',
			'docs': doc_ids
		}
		return {
			'type': 'ir.actions.client',
			'name': _('People Soft'),
			'tag': 'account_report',
			'options': {'partner_ids': [self.id]},
			'ignore_session': 'both',
			'context': str(context)
		}