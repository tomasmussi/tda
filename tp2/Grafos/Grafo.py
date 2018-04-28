# -*- coding: utf-8 -*-
from Vertice import *
from heapq import *
import sys

def relajar_vertice(heap,vertice1,vertice2,peso_arista):
	"""Función auxiliar que dado dos vertices y un peso determina si el valor de la distancia
	 mínima entre ellos debe ser actualizado; y en caso afirmativo lo actualiza."""
	d = vertice1.dist + peso_arista
	if d < vertice2.dist:
		vertice2.dist = d
		vertice2.padre = vertice1

def actualizar_heap(heap,vertice):
		"""Función auxiliar que dado un vertice actualiza el valor de su par asociado en la lista"""
		for par in heap:
			if par[1]==vertice:
				par[0]=vertice.dist
		heapify(heap)

def agregar_padres(lista_recorrido,vertice):
	"""Función auxiliar que dado un vértice agrega su padre a la lista y luego se llama recursivamente.
	La condición de corte es cuando el vértice dado no tiene padre."""
	dad = vertice.padre
	if dad != None:
		lista_recorrido.insert(0,dad.dato)
		agregar_padres(lista_recorrido,dad)

class Grafo(object):
	"""Clase que representa un Grafo mediante un diccionario de adyacencias"""
	def __init__(self):
		"""Crea una instancia de la clase sin vértices ni aristas y con el vértice central indefinido.
		El vértice central es aquel desde el cual se calculan las distancia ménimas a todos los demás vértices
		cuando se llama a Dijkstra."""
		self.vertices = {}
		self.conversion = {}
		self.vertice_central = None

	def agregar_vertice(self, dato):
		"""Primitiva que agrega un vértice al grafo"""
		vertice = Vertice(dato)
		self.conversion[dato] = vertice
		self.vertices[vertice] = []

	def agregar_arista(self,peso,dato1,dato2):
		"""Primitiva que agrega una arista al grafo.
		Si alguno de los vértices a unir no existe levanta una excepcion"""
		try:
			vertice1 = self.conversion[dato1]
			vertice2 = self.conversion[dato2]
			self.vertices[vertice1].append((peso,vertice2))
			self.vertices[vertice2].append((peso,vertice1))
		except KeyError:
			raise Exception("Uno de los vértices no existe")

	def dijkstra(self,vertice_inicial):
		"""Implementación del algoritmo de Dijkstra utilizando una cola de prioridad:
		calcula la distancia mínima a cada nodo desde el vértice dado."""
		#Inicializacion:
		self.vertice_central = vertice_inicial
		lista_tratados = []
		heap = []
		for clave,valor in self.vertices.iteritems():
			if clave == vertice_inicial:
				vertice_inicial.dist=0
				vertice_inicial.padre=None
			else:
				clave.dist = float("inf") #Representa el infinito en python, todo otro numero sera menor
			heappush(heap,[clave.dist,clave]) #Se encola la distancia para que la cola pueda comparar los elementos

		#Comienza el algoritmo
		while heap:
			l = heappop(heap) #l es [vertice.dist,vertice]
			vertice = l[1]
			lista_tratados.append(vertice)
			for adyacente in self.vertices[vertice]: #adyacente es (peso,arista)
				relajar_vertice(heap,vertice,adyacente[1],adyacente[0])
				actualizar_heap(heap,adyacente[1])

	def camino_minimo(self,dato1,dato2):
		"""Primitiva que dados dos vértices"""
		try:
			vertice_inicial = self.conversion[dato1]
			vertice_final = self.conversion[dato2]
		except KeyError:
			raise Exception("Uno de los vértices no existe")

		if vertice_inicial != self.vertice_central: #Esto es si no se calculo Dijkstra desde el vertice pasado por parametro
			self.dijkstra(vertice_inicial)

		lista_recorrido = [] #Sera una lista de vertices en el orden del recorrido minimo
		distancia = int(vertice_final.dist)
		lista_recorrido.insert(0,vertice_final.dato)
		agregar_padres(lista_recorrido,vertice_final)
		return lista_recorrido , distancia 
