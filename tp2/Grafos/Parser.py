import sys
import csv
import os
from Sistema import *

READ = "r"
WRITE = "w"
MAPA = "mapa.csv"
JUGUETES = "juguetes.csv"
FABRICA = "fabricas.csv"

def parsear_esquina(linea, sistema):
	"""Parseo una esquina, devuelvo el id"""
	id = int(linea[0])
	x = float(linea[1])
	y = float(linea[2])
	latitud = float(linea[3])
	longitud = float(linea[4])
	sistema.agregar_esquina(id,x,y,latitud,longitud)
	return id

def parsear_calle(linea, sistema):
	"""Parseo una calle, devuelvo el id"""
	id = int(linea[0])
	esquina_inicial = int(linea[1])
	esquina_final = int(linea[2])
	sistema.agregar_arista(esquina_inicial,esquina_final)
	return id

def parsear_fabrica(linea, sistema):
	"""Parseo una fabrica, devuelvo el id"""
	id = int(linea[0])
	id_esquina = int(linea[1])
	hora_inicial = int(linea[2])
	hora_final = int(linea[3])
	sistema.agregar_fabrica(id,id_esquina,hora_inicial,hora_final)
	return id

def parsear_juguete(linea, sistema):
	"""Parseo un juguete, devuelvo el id"""
	id = int(linea[1])
	id_fabrica = int(linea[0])
	valor = int(linea[2])
	peso = int(linea[3])
	sistema.agregar_juguete(id_fabrica,id,valor,peso)
	return id

def leer_datos(datos):
	"""leer_datos se encarga de leer una linea de un archivo csv, mientras lea devuelve el proximo, 
	una vez que alcanza la ultima linea, devuelve None"""
	try:
		return datos.next()
	except StopIteration:
		return None

def abrir_archivo(nombre,modo=READ):
	"""Funcion que abre un archivo y valida especificamente los errores de que no exista o no tenga permiso"""
	try:
		return open(nombre,modo)
	except IOError, e:
		if  e.errno == ERROR_ARCH_NO_EXISTE:
			print "El archivo no existe"
		elif e.errno == ERROR_ARCH_NO_TIENE_PERMISO:
			print "Usted no tiene permisos para abrir el archivo"
		else:
			print "Error al abrir el archivo"
		return None

def abrir_csv(archivo):
	"""Funcion que devuelve un reader de csv, que en caso de que devuleva error lo muestra y devuelve None"""
	try:
		return csv.reader(archivo)
	except csv.Error:
		print "El archivo no tiene el formato indicado"
		return None

class Parser(object):
	"""El Parser es un objeto que en cada instancia va a parsear
	un archivo distinto, sabe el tipo en funcion de los argumentos del constructor"""
	def __init__(self, archivo):
		self.arch = archivo
	
	def _parse_mapa(self,sistema, archivo_csv):
		linea = leer_datos(archivo_csv)
		cantidad = int(linea[0])
		for x in xrange(cantidad):
			linea = leer_datos(archivo_csv)
			parsear_esquina(linea, sistema)
		linea = leer_datos(archivo_csv)
		cantidad = int(linea[0])
		for x in xrange(cantidad):
			linea = leer_datos(archivo_csv)
			parsear_calle(linea, sistema)

	def _parse_juguetes(self,sistema, archivo_csv):
		linea = leer_datos(archivo_csv)
		while linea:
			parsear_juguete(linea, sistema)
			linea = leer_datos(archivo_csv)

	def _parse_fabricas(self,sistema, archivo_csv):
		linea = leer_datos(archivo_csv)
		while linea:
			parsear_fabrica(linea, sistema)
			linea = leer_datos(archivo_csv)

	def parsear(self, sistema):
		archivoAbierto = abrir_archivo(self.arch, 'rU')
		archivo_csv = abrir_csv(archivoAbierto)
		if MAPA in self.arch:
			self._parse_mapa(sistema, archivo_csv)
		elif FABRICA in self.arch:
			self._parse_fabricas(sistema, archivo_csv)
		elif JUGUETES in self.arch:
			self._parse_juguetes(sistema, archivo_csv)
		archivoAbierto.close()
