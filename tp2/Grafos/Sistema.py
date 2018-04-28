# -*- coding: utf-8 -*-
from Grafo import *
from Esquina import *
from Juguete import *
from Fabrica import *
from heapq import *
from math import pow
import sys

def calcular_norma(coords1,coords2):
	"""Función que dadas dos coordenadas de un plano calcula la norma entre ellas."""
	x1,y1 = coords1
	x2,y2 = coords2
	return pow(pow(x1-x2,2) + pow(y1-y2,2) , 0.5)

def calcular_peso(esquina1,esquina2):
	"""Función que dadas dos esquinas calcula el peso, es decir, la distancia entre ellas."""
	t1 = (esquina1.x,esquina1.y)
	t2 = (esquina2.x,esquina2.y)
	peso = calcular_norma(t1,t2)
	return peso

def problema_mochila(nro_de_elementos,capacidad,lista_pesos,lista_valores,lista_idrs):
	"""Función que dado una cantidad de elementos con sus pesos, valores e identificadores y una capacidad
	de mochila maxima, calcula la solucion optima que llena la mochila con el mayor valor total. Además devuelve
	una lista con todos las ids de los elementos que componen la solucián."""
	# Inicializo una matriz de "capacidad" filas y "nro_de_elementos" columnas con una lista
	# que contiene un cero y una lista vacia cada posicion de la matriz.
	matriz = [[ [0,[]] for x in xrange(nro_de_elementos+1)] for x in xrange(capacidad+1)]
	for j in xrange(1,capacidad+1): # Cada ciclo aumenta la capacidad de la mochila
		for i in xrange(1,nro_de_elementos+1): # Cada ciclo aumenta la cantidad de elementos considerados
			peso = lista_pesos[i-1]
			valor = lista_valores[i-1]
			idr = lista_idrs[i-1]
			if peso > j:
				matriz[j][i][0] = matriz[j][i-1][0]
				matriz[j][i][1] = matriz[j][i-1][1]
			if peso <= j:
				if matriz[j][i-1][0] >= (matriz[j-peso][i-1][0] + valor):
					matriz[j][i][0] = matriz[j][i-1][0]
					matriz[j][i][1] = matriz[j][i-1][1]
				else:
					matriz[j][i][0] = (matriz[j-peso][i-1][0] + valor)
					matriz[j][i][1] = list(matriz[j-peso][i-1][1]) # Esto crea una nueva lista igual a la anterior
					matriz[j][i][1].append(idr) # Agrego el idr del elemento que ahora es parte de la mejor solucion parcial
	return matriz[capacidad][nro_de_elementos][0],matriz[capacidad][nro_de_elementos][1]

def problema_charlas(diccionario_elementos):
	lista_charlas = []
	heap = []
	for x in diccionario_elementos:
		heappush(heap,[(diccionario_elementos[x].obtener_clausura(), diccionario_elementos[x].obtener_apertura(),\
						diccionario_elementos[x].obtener_identificador()), diccionario_elementos[x]])
	while heap:
			l = heappop(heap) #l es [vertice.dist,vertice]
			fabrica = l[1]
			if (len(lista_charlas) == 0) or (fabrica.obtener_apertura() >= lista_charlas[len(lista_charlas)-1].obtener_clausura()):
				lista_charlas.append(fabrica)
	return lista_charlas
			
class Sistema(object):
	"""Representa al sistema que se ocupa de resolver los problemas de Navidad."""
	def __init__(self,capacidad,id_esquina_polo_norte):
		"""Crea una instancia de la clase."""
		self.grafo = Grafo()
		self.dicc_fabricas = {}
		self.dicc_esquinas = {}
		self.capacidad = int(capacidad)
		self.polo_norte = int(id_esquina_polo_norte)

	def agregar_esquina(self,id_esquina,x,y,latitud,longitud):
		"""Funcion que se encarga de agregar una esquina al mapa."""
		nueva_esquina = Esquina(id_esquina, x, y, latitud, longitud)
		self.dicc_esquinas[id_esquina] = nueva_esquina
		self.grafo.agregar_vertice(nueva_esquina)

	def agregar_arista(self,id_esquina_inicial, id_esquina_final):
		esquina_inicial = self.dicc_esquinas[id_esquina_inicial]
		esquina_final = self.dicc_esquinas[id_esquina_final]
		peso = calcular_peso(esquina_inicial,esquina_final)
		self.grafo.agregar_arista(peso,esquina_inicial,esquina_final)

	def agregar_fabrica(self,id_fabrica,id_esquina,horario_entrada,horario_salida):
		nueva_fabrica = Fabrica(id_fabrica, id_esquina,horario_entrada, horario_salida)
		self.dicc_fabricas[id_fabrica] = nueva_fabrica

	def agregar_juguete(self,id_fabrica,id_juguete,valor,peso):
		try:
			nuevo_juguete = Juguete(id_fabrica,id_juguete,valor,peso)
			fabrica = self.dicc_fabricas[id_fabrica]
			fabrica.agregar_juguete(nuevo_juguete)
		except KeyError:
			print "Error: la fabrica con id %s no existe" % (id_fabrica)

	def valuar_juguetes(self,id_fabrica):
		fabrica = self.dicc_fabricas[id_fabrica]
		lista_ju = fabrica.listar_juguetes()
		#Armo las lista que seran los parametros del problema de la mochila.
		lista_pesos = []
		lista_valores = []
		lista_ids = []
		for jug in lista_ju:
			lista_pesos.append(jug.obtener_peso())
			lista_valores.append(jug.obtener_valor())
			lista_ids.append(jug.obtener_id())
		return problema_mochila(len(lista_ju),self.capacidad,lista_pesos,lista_valores, lista_ids)

	def listar_fabricas(self):
		lista = problema_charlas(self.dicc_fabricas)
		return str("Cantidad: "+str(len(lista)) + '\n' + '\n'.join(['%s' % str(v) for v in lista])) , lista

	def listar_camino_minimo(self, id_fabrica):
		fabrica = self.dicc_fabricas[id_fabrica]
		esquina_final = self.dicc_esquinas[fabrica.obtener_esquina()]
		esquina_inicial = self.dicc_esquinas[self.polo_norte]
		return self.grafo.camino_minimo(esquina_inicial,esquina_final)
