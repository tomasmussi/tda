import heapq
import Queue

from heapq import *

class Grafo(object):

	def __init__(self):
		self.vertices = {}

	def agregarVertice(self, vertice):
		if vertice in self.vertices:
			return False
		self.vertices[vertice] = {}
		return True

	def borrarVertice(self, vertice):
		vertices = self.vertices
		if not vertice in vertices:
			return False
		vertices.pop(vertice)
		for otros in vertices.keys():
			if vertice in vertices[otros]:
				vertices[otros].pop(vertice)
		return True

	def agregarArista(self, v1, v2, peso = 1.0):
		vertices = self.vertices
		if v1 not in vertices or v2 not in vertices:
			return False
		vertices[v1][v2] = peso
		return True

	def borrarArista(self, v1, v2):
		vertices = self.vertices
		# Verifico que los vertices existan
		if v1 not in vertices or v2 not in vertices:
			return False
		# Verifico que la arista exista
		if v2 not in vertices[v1] or v1 not in vertices[v2]:
			return False
		# Borro
		vertices[v1].pop(v2)
		return True

	def obtenerPeso(self, v1, v2):
		vertices = self.vertices
		# Verifico que los vertices existan
		if v1 not in vertices or v2 not in vertices:
			return None
		# Verifico que la arista exista
		if (not self.hayArista(v1, v2)):
			return None
		return vertices[v1][v2]

	def obtenerAristas(self, v):
		if not v in self.vertices:
			return None
		return self.vertices[v].keys()

	def hayArista(self, v1, v2):
		if v1 not in self.vertices or v2 not in self.vertices:
			return False
		return v2 in self.vertices[v1]


	def bfs(self, v):
		visitados = {}
		distancias = {}
		prev = {}

		cola = Queue.Queue()
		distancias[v] = 0
		visitados[v] = True
		prev[v] = None
		if (v in self.vertices):
			cola.put(v)

		while (not cola.empty()):
			vertice = cola.get()
			vecinos = self.obtenerAristas(vertice)
			for vecino in vecinos:
				if vecino not in visitados and self.obtenerPeso(vertice, vecino) > 0:
					prev[vecino] = vertice
					distancias[vecino] = distancias[vertice] + 1
					visitados[vecino] = True
					cola.put(vecino)
		return prev, distancias

	def recorridoDijkstra(self, v):
		# LLamo vertices para no estar todo el tiempo con self
		vertices = self.vertices
		# Inicializo arreglos de distancia y anteriores
		distancia = dict()
		visitado = dict()
		anterior = dict()
		for x in vertices:
			distancia[x] = float('inf')
			visitado[x] = False
			anterior[x] = None
		heap = []
		distancia[v] = 0
		heappush(heap, {distancia[v]: v})
		while (len(heap) != 0):
			diccionario = heappop(heap)
			unVertice = diccionario.values()[0]
			visitado[unVertice] = True
			for vecino in vertices[unVertice].keys():
				dist = distancia[unVertice] + vertices[unVertice][vecino]
				if dist < distancia[vecino]:
					distancia[vecino] = dist
					anterior[vecino] = unVertice
					heappush(heap, {distancia[vecino]: vecino})


		return distancia, anterior

	def ford_fulkerson(self, fuente, sumidero):
		vertices = self.vertices

		flujo_maximo = 0

		path, distancias = self.bfs(fuente)
		while sumidero in distancias.keys() and distancias[sumidero] != float('inf'):

			# Busco la capacidad maxima
			flujo_parcial = float("Inf")
			s = sumidero
			while(s !=  fuente):
				flujo_parcial = min (flujo_parcial, self.obtenerPeso(path[s],s))
				s = path[s]

			flujo_maximo +=  flujo_parcial

			# Actualizo los flujos
			v = sumidero
			while(v !=  fuente):
				u = path[v]
				vertices[u][v] -= flujo_parcial
				
				if u not in vertices[v].keys():
					vertices[v][u] = flujo_parcial
				else:
					vertices[v][u] += flujo_parcial
				v = path[v]
		
			path, distancias = self.bfs(fuente)
		return flujo_maximo


	def recorridoMinimo(self, v1, v2):
		if v1 == v2:
			return [v1]
		dist, anteriores = self.recorridoDijkstra(v1)
		camino = []
		if dist[v2] == float('inf'):
			return camino
		camino.append(v2)
		vertice = anteriores[v2]
		while vertice != v1:
			camino.append(vertice)
			vertice = anteriores[vertice]
		camino.append(v1)
		camino.reverse()
		return camino


	def distanciaMinima(self, v1, v2):
		if v1 == v2:
			return 0.0
		distancia, anteriores = self.recorridoDijkstra(v1)
		return distancia[v2]

	def dfs(self, v1, v2):
		visited = {}
		for v in self.vertices:
			visited[v] = False

		previous = {}
		stack = [v1]
		finished = False

		while stack and not finished:
			w = stack.pop()
			visited[w] = True
			if (w == v2):
				break
			for neighbor in self.vertices[w]:
				if (not visited[neighbor]):
					previous[neighbor] = w
					stack.append(neighbor)
		path = []
		w = v2

		while w != v1:
			path.append(w)
			w = previous[w]
		path.append(v1)
		path.reverse()
		limit = float('inf')
		for i in range(len(path) - 1):
			u = path[i]
			w = path[i+1]
			if (self.obtenerPeso(u,w) < limit):
				limit = self.obtenerPeso(u,w)
		return path, limit


	def flujo_maximo(self, fuente, target):
		residual = Grafo()
		return residual


