# -*- coding: utf-8 -*-
# import urllib3.request, urllib3.parse, urllib3.error, json
import certifi
import urllib3, json
import base64
import socket
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MukiREST(models.Model):
	_name = "muki.rest"
	_description = "Visitor Search"

	user_id = fields.Many2one('res.users', string="Current User",
		default=lambda self: self.env.user)

	#CAMPOS WIZARD 
	hvisit = fields.Char("Visitor ID")
	whstatus = fields.Selection([
		('Check-OUT', 'Check-OUT'),
		('Cancelled', 'Cancelled'),
		('Declined', 'Declined'),
		('Draft', 'Draft'),
		('Revision', 'Revision'),
		('Check-IN', 'Check-IN'),
		('Approved', 'Approved'),
		('Submit', 'Submit')],string = 'Status')
	wnombre = fields.Char("Name")
	wfname = fields.Char("First Name")
	wlname = fields.Char("Last Name")
	wvisitor_email = fields.Char("Email")
	
	#CAMPOS VISTA
	hstatus = fields.Selection([
		('Check-OUT', 'Check-OUT'),
		('Cancelled', 'Cancelled'),
		('Declined', 'Declined'),
		('Draft', 'Draft'),
		('Revision', 'Revision'),
		('Check-IN', 'Check-IN'),
		('Approved', 'Approved'),
		('Submit', 'Submit')],string = 'Status')
	nombre = fields.Char("Name")
	fname = fields.Char("First Name")
	lname = fields.Char("Last Name")
	visitor_email = fields.Char("Email")
	hvisit2 = fields.Char("Visitor ID")
	hstreet = fields.Char("Street")
	hstreet2 = fields.Char("Street2")
	hcity = fields.Char("City")
	hzip = fields.Char("Zip")
	hcountry = fields.Char("Country")
	hcateg = fields.Char("Visitor Category")

	#FUNCION PARA HACER REPLACE DE VALORES NONE
	def replace(self,data, search, replacement, parent=None, index=None):
		if data == search:
			parent[index] = replacement
		elif isinstance(data, (list, dict)):
			for index, item in enumerate(data) if isinstance(data, list) else data.items():
				self.replace(item, search, replacement, parent=data, index=index)

	#FUNCION PARA HACER VALIDACION DE LOS KEYS DENTRO DE ADDRESS
	def verify_keys(self,address):
		if {'line1', 'line2','country', 'city', 'zip'} <= address.keys():
			return True
		else:
			return False
	
	#FUNCION PARA AGREGAR VALORES A LA VISTA DE RESULTADOS
	def add_visitor(self, datas):
		logging.info("Se esta llamando la funcion:")
		for value in datas.values():
			for data in value:
				self.hvisit2= data['user_id']
				self.nombre= data['visitor_name']
				self.fname= data['first_name']
				self.lname= data['last_name']
				self.visitor_email=data['email']
				self.hstatus=data['status']
				self.hcateg=data['visitor_category']
				self.address = data['funding']['address']
				# logging.info("ADDRESS: " + str(address))
				if self.address != '':
					if self.verify_keys(self.address):
						self.hstreet=self.address['line1']
						self.hstreet2=self.address['line2']
						self.hcity=self.address['city']
						self.hzip=self.address['zip']
						self.hcountry=self.address['country']
						# logging.info("DENTRO DEL IF: " + str(address))
				else:
					self.hstreet=""
					self.hstreet2=""
					self.hcity=""
					self.hzip=""
					self.hcountry=""
					# logging.info("DENTRO DEL ELSE: " + str(address))
		
		self.env['muki.rest'].create({
			'hvisit2': self.hvisit2,
			'nombre': self.nombre,
			'fname': self.fname,
			'lname': self.lname,
			'visitor_email': self.visitor_email,
			'hstatus': self.hstatus,
			'hcateg':self.hcateg,
			'hstreet':self.hstreet,
			'hstreet2':self.hstreet2,
			'hcity':self.hcity,
			'hzip':self.hzip,
			'hcountry':self.hcountry,
			})

	#FUNCION PARA HACER REQUEST Y OBTENER JSON CON LOS RESULTADOS DE LA BUSQUEDA
	def search_visitor(self):
		ip_address = '35.222.101.46'
		#CONVIRTIENDO A FORMATO ASCII EL IP
		ip_address_bytes = ip_address.encode('ascii')
		#CONVIRTIENDO A BASE64 EL IP
		ipBase = base64.b64encode(ip_address_bytes)
		http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
		url = 'https://visitors.stri.si.edu/services/getVisits'
		
		values = dict()
		filtros_dic = {
			"visitor_id":self.hvisit2,
			"status": self.whstatus,
			"visitor_name":self.wnombre,
			"name":self.wfname,
			"last_name":self.wlname,
			"email":self.wvisitor_email}

		for key, value in filtros_dic.items():
			if (value != False):
				values[key] = value
		logging.info("VALUES: " + str(values))
	
		headers={'Accept': 'application/json',
				'X-VSO-caller': ipBase}

		datas = http.request('POST', url, fields=values, headers=headers)
		#MOSTRAR EXCEPCION EN CASO DE NO OBTENER RESULTADO
		try:
			datas = json.loads(datas.data.decode('utf-8'))
			#REEMPLAZANDO VALORES VACIOS POR EL STRING ''
			self.replace(datas, None, '')
			self.replace(datas, [], '')
			logging.info("CONTENIDO: " + str(datas.values()))
			self.add_visitor(datas)
		except Exception:
			raise UserError(_('No se han encontrado resultados!'))
			# raise RedirectWarning("No se han encontrado resultados!", action.id, _('OK'))
		
		action = self.env.ref('template_module.muki_rest_action').read()[0]
		action['target'] = 'main'
		return action

		# print(datas)

