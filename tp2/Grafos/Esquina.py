# -*- coding: utf-8 -*-
class Esquina(object):
	"""Representa una esquina de Avellaneda/Polo Norte"""
	def __init__ (self,id_esquina,x,y,latitud,longitud):
		"""Crea una instancia de la clase a partir de una id, sus coordenadas
		x e y en metros y sus coordenadas de latitud y longitud"""
		self.id_esquina = id_esquina
		self.x = x
		self.y = y
		self.latitud = latitud
		self.longitud = longitud

	def __hash__(self):
		"""Define la funcion de hashing para la clase.
		Esto permite utilizar a las instancias como claves de un diccionario"""
		return id(self)
		
	def __cmp__(self,other):
		"""Define la funcion de comparacion para la clase.
		Esto permite utilizar a las instancias como claves de un diccionario"""
		return cmp(id(self),id(other))

	def __str__(self):
		return str(self.id_esquina)

	def agregar_fabrica(self,fabrica):
		"""Agregar la información de que hay una fábrica en la esquina."""
		self.fabrica = fabrica

	def obtener_id(self):
		return self.id_esquina

	def obtener_esquina(self):
		return self.x,self.y

	def obtener_ubicacion_mapa(self):
		return self.latitud,self.longitud
