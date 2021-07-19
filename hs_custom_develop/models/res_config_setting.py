# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	journal_strifund = fields.Many2one('account.journal', 
		config_parameter='hs_custom_develop.default_journal_strifund')