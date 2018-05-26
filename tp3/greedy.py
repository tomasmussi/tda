

class Greedy(object):

	def __init__(self, grid, lanzaderas):
		# Estrategia Greedy no necesita conocer el mapa,
		# solo necesita conocer el paso i y en base a eso actuar
		self.lanzaderas = lanzaderas

	"""
	Blancos seleccionados por las lanzaderas, aca es donde se ve implementada la estrategia del
	algoritmo para seleccionar los barcos a los cuales hacer danio
	"""
	def targets(self, grid_column, ships):
		# Logica dummy para ver la simulacion funcionando
		# Matar siempre el primer barco
		targets = []
		for l in range(self.lanzaderas):
			for i in range(len(ships)):
				if (ships[i] > 0):
					targets.append(i)
					break
		return targets


	def __str__(self):
		return "Greedo"


	def prueba(self):
		return self.lanzaderas