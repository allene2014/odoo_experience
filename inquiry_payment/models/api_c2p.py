# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import requests
import json
import urllib3
import logging




_logger = logging.getLogger(__name__)

class ConsultaMercantil(models.Model):
	_name = 'payment.inquiry'
	_description = 'consulta las transaciones de mercantil c2p'
	

	integratorId = fields.Integer('Codigo de integrador')
	merchantId = fields.Integer('Codigo de comercio')
	movil_origen =fields.Char('Movil Origen')
	movil_destino =fields.Char('Movil Destino')
	numero_identificacion =fields.Char('Numero C.I')
	clave_compra =fields.Char('Clave de Compra')
	numero_factura =fields.Char('Numero de Factura')
	monto=fields.Float('Monto', store=True)
	#tipo=fields.Char('Tipo transacion', store=True)
	tipo=fields.Selection(selection=[('compra','Compra'),('vuelto','Vuelto'),], string='Tipo transacion', default="compra")

	payment_reference=fields.Char('Referencia de pago')
	resultado=fields.Boolean('resultado', default= False)
	warning =fields.Boolean(default= False)

	@api.constrains('monto')
	def value_resultado(self):
		for rec in self:
			if rec.monto == 0:
				rec.warning = True
	
	def flag_transaction(self):
		self.write({'resultado':True})



	def encrypt(self, param):
		param = param
		url = "http://127.0.0.1/crypt/encrypt.php"
		#url = "http://10.50.40.10/crypt/encrypt.php"

		payload = json.dumps({
		  "cvv": param,
		  "keybank": "A11103402525120190822HB01"
		})
		headers = {
		  'Content-Type': 'application/json'
		}
		try:
			requests.get(url,timeout=2)
			response = requests.request("POST", url, headers=headers, data=payload)

			print(response.text)
			ver = response.json()
			res_encryp=(ver.get('CVVEncriptado'))
			#seg = (aper['CVVEncriptado'])
			return res_encryp
		except:
			print("no se pudo conectar API encrypt")

	



	

	def ProcessC2p(self):
		
		movil_origen = self.encrypt(self.movil_origen)#*******CYPHER*********
		movil_destino = self.encrypt(self.movil_destino)#*******CYPHER*********
		cedula_identidad = self.encrypt(self.numero_identificacion)#*******CYPHER*********
		#clave_compra = self.encrypt(self.clave_compra)
		clave_compra =""
		numero_factura = self.numero_factura
		payment_reference=self.payment_reference
		monto = self.monto
		tipo = self.tipo
		method = ""
		if self.tipo == "vuelto":
			method = "p2p"
			clave_compra = ""
			payment_reference = ""
		else:
			method = "c2p"
			clave_compra = self.encrypt(self.clave_compra)




		
		print ('*******C 2 P ***********')
		print(movil_origen)
		print(movil_destino)
		print(cedula_identidad)
		print(clave_compra)
		print(numero_factura)
		print(payment_reference)
		print(monto)
		print(tipo)
		print(method)

		print ('*******C 2 P ***********')

		url = "https://apimbu.mercantilbanco.com/mercantil-banco/sandbox/v1/payment/c2p"

		payload = json.dumps({
		  "merchant_identify": {
		    "integratorId": 31,
		    "merchantId": 200284,
		    "terminalId": "abcde"
		  },
		  "client_identify": {
		    "ipaddress": "127.0.0.1",
		    "browser_agent": "Chrome 18.1.3",
		    "mobile": {
		      "manufacturer": "samsung",
		      "model": "s9",
		      "os_version": "oreo 9.1",
		      "location": {
		        "lat": 0,
		        "lng": 0
		      }
		    }
		  },
		  "transaction_c2p": {
		    "amount": monto,#2525.33, #monto
		    "currency": "VES",
		    "destination_bank_id": 105,
		    "destination_id": cedula_identidad, #"KNtWibVyfrZY8+XOKgDPRw==",#cedula identidad
		    "destination_mobile_number": movil_destino,#"fLIajK1Slvz878y13gQOoA==", #numero destino
		    "payment_reference": payment_reference,#"0057718281656", #referencia de pago
		    "origin_mobile_number": movil_origen,#"0PbWVea/C/hyO37XjEoFaA==", # numero de origen del pago
		    "trx_type": self.tipo,#"compra",
		    "payment_method": method, #"c2p",
		    "invoice_number": numero_factura,#"123456",
		    "twofactor_auth": clave_compra#"m250sf3wDkkTSvuyJ/z/Xg==" #
		  }
		})
		headers = {
		  'X-IBM-Client-Id': '81188330-c768-46fe-a378-ff3ac9e88824',
		  'Content-Type': 'application/json'
		}
		
		response = requests.request("POST", url, headers=headers, data=payload)
		code_return =response.status_code
		print("*****RESULTADO*********")
		print(response.text)
		print("*****RESULTADO*********")
		print(response)
		find = response.json()
		respuesta=(find.get('error_list'))
		
		print("*****FINAL*******")
		print(respuesta)
		print("*****FINAL*******")
		print (code_return)
	
		msg_banco = " "
		for rec in respuesta:
			msg_banco =rec
			print(msg_banco['error_code'])
			print(msg_banco['description'])

		if code_return == 200:
			self.resultado = True
			print(self.resultado)
			#self.warning=True
			raise Warning("Proceso Exitoso")
		elif code_return == 400:
			self.flag_transaction()
			raise Warning('Error! %s,' %msg_banco['description'])
		elif code_return == 401:
			self.flag_transaction()
			raise Warning('Error! %s' %msg_banco['description'])
		else:
			raise Warning("Error Problema en API")
			print(self.resultado)
		