# -*- coding: utf-8 -*-
class Vertice(object):
	"""Clase que representa a un vértice a la clase Grafo."""
	def __init__(self, dato):
		"""Crea una instancia de la clase a partir del dato pasado por parámetro.
		Los atributos dist y padre son necesarios para calcular los caminos mínimos entre vértices."""
		self.dato = dato
		self.dist = 0
		self.padre = None
		
	def __hash__(self):
		"""Define la funcion de hashing para la clase.
		Esto permite utilizar a las instancias como claves de un diccionario"""
		return id(self)
		
	def __cmp__(self,other):
		"""Define la funcion de comparacion para la clase.
		Esto permite utilizar a las instancias como claves de un diccionario"""
		return cmp(id(self),id(other))

	def __str__(self):
		return str(self.dato)
