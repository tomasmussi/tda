import numpy

class Greedy(object):

	def __init__(self, grid, lanzaderas, ships):
		# Estrategia Greedy no necesita conocer el mapa,
		# solo necesita conocer el paso i y en base a eso actuar
		self.transpose = zip(*grid)
		self.lanzaderas = lanzaderas
		self.ships = ships

	"""
	Blancos seleccionados por las lanzaderas, aca es donde se ve implementada la estrategia del
	algoritmo para seleccionar los barcos a los cuales hacer danio
	"""
	def targets(self, turn, ships):

		column = turn % len(self.transpose)
		grid_column = self.transpose[column]
		# La estrategia de Greedo es en cada iteracion maximizar el danio posible que
		# se le pueden hacer a los barcos. Es decir, mira la columna, y el que tenga el mayor
		# danio posible sera el blanco de las lanzaderas
		targets = []
		#print column
		#print grid_column
		#print ships
		# Busco de mayor a menor danio posible en la grilla, los barcos a los cuales tirarles
		indexes = numpy.argsort(-(numpy.array(grid_column)))
		#print indexes
		# Al principio danio hecho en el turno es 0
		damage = [ 0 for i in range(len(ships))]
		ship_it = 0
		target_ship = indexes[ship_it]

		# Moverse al primer barco no destruido
		while (ships[target_ship] < 0 and ship_it < len(ships)):
			# Si el barco esta destruido y no me fui de rango, buscar siguiente barco
			ship_it += 1
			if (ship_it < len(ships)):
				target_ship = indexes[ship_it]

		# Mientras tenga tiros para tirar Y barcos para hundir
		lanz_it = 0
		while (lanz_it < self.lanzaderas and ship_it < len(ships)):
			# Ver si el danio hecho en este turno ya hunde el barco
			if (damage[target_ship] < ships[target_ship]):
				# Hago danio, pasar a la siguiente lanzadera
				lanz_it += 1
				damage[target_ship] += grid_column[target_ship]
				targets.append(target_ship)
			else:
				# No hago danio, pasar al siguiente barco
				ship_it += 1
				if (ship_it < len(ships)):
					target_ship = indexes[ship_it]
		return targets



	def __str__(self):
		return "Greedo"
