# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class POSCustomNotes(models.Model):
	_name = 'pos.order.note'
	_rec_name = 'order_note'

	sequence = fields.Integer('Sequence' , readonly=True)
	order_note = fields.Char('Order Note')

	@api.model
	def create(self,vals):
		vals['sequence'] =self.env['ir.sequence'].get('pos.order.note')
		return super(POSCustomNotes, self).create(vals)

class PosOrderNote(models.Model):
	_inherit = 'pos.order.line'

	notes_line = fields.Char('Notes')	

class InheritPosOrder(models.Model):
	_inherit = 'pos.order'


	@api.model
	def create_from_ui(self, orders):
		order_ids = super(InheritPosOrder, self).create_from_ui(orders)
		for order_id in order_ids:
			try:
				pos_order_id = self.browse(order_id)
				if pos_order_id:
					ref_order = [o['data'] for o in orders if o['data'].get('name') == pos_order_id.pos_reference]
					for order in ref_order:
						note = order.get('get_to_stay')
						pos_order_id.write({'note':  note})

			except Exception as e:
				_logger.error('Error in point of sale validation: %s', tools.ustr(e))
		return order_ids

	

