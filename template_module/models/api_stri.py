import urllib.request, urllib.parse, urllib.error, json
import base64
import socket
import logging
_logger = logging.getLogger(__name__)

# con esto conseguiremos la IP del host que este ejecutando la peticion
# hostname = socket.gethostname()
# ip_address = socket.gethostbyname(hostname)
ip_address = '190.140.165.45'
# transformamos la ip a ascii para que la pueda leer el modulo base64
ip_address_bytes = ip_address.encode('ascii')
# se transforma en base 64
ipBase = base64.b64encode(ip_address_bytes)
# print(ipBase)
# url del web service
url = 'https://visitors.stri.si.edu/services/getVisits'
# aqui se armaria el diccionario con los valores necesarios para los filtros
values = {"status": "Check-OUT", "name": "Paula"}
# values = {"visitor_id": "visitor","status": "hstatus" }

# a continuacion, se utiliza urllib.parse.urlencode para transformar los valores a un formato valido del request
data = urllib.parse.urlencode(values).encode('utf-8')
# declaramos los headers necesarios
headers={'Accept': 'application/json',
	'X-VSO-caller': ipBase}

# aramamos el request tipo post de la libreria
req = urllib.request.Request(url, data=data, headers=headers)
# print(req)

# esta funcion deberia abrir la respuesta enviada en el request
rsp = urllib.request.urlopen(req)
logging.info("CONTIENE:" + str(rsp))
# print(rsp.read)
# con esta linea leemos los datos de la respuesta
content = rsp.read()
			
# imprimimos la respuesta, este content es el que se utilizaria para enviar la data a la vista segun se requiera
print(content)