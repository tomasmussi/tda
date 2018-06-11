from itertools import combinations_with_replacement as combinations
import sys

class Dinamica(object):

	def __init__(self, grid, lanzaderas, ships):
		self.grid = grid
		self.lanzaderas = lanzaderas
		self.ships = ships

		print self.min_points(self.ships, 0, 0, float('inf'))
		sys.exit(0)



	def update_damage(self, ships, p, turn):
		updated_ships = list(ships)
		for ship_index in p:
			updated_ships[ship_index] -= self.grid[ship_index][turn % len(self.grid[0])]
		return updated_ships

	def min_points(self, ships, turn, points, total_min):
		print ships, turn, points
		if all(x <= 0 for x in ships):
			return points
		ships_alive_index = [i for i in range(len(ships)) if ships[i] > 0]
		for p in combinations(ships_alive_index, self.lanzaderas): #Lanzaderas deberian poder disparar al mismo barco
			updated_ships = self.update_damage(ships, p, turn)
			turn_points = sum(1 for s in updated_ships if s > 0)
			next_min = self.min_points(updated_ships, turn+1, points+turn_points, total_min)
			print turn, next_min, total_min
			total_min = min(total_min, next_min)
		return total_min

	"""
	Blancos seleccionados por las lanzaderas, aca es donde se ve implementada la estrategia del
	algoritmo para seleccionar los barcos a los cuales hacer danio
	"""
	def targets(self, iteration, ships):
		# La estrategia de Dinamico es
		targets = []


		return targets

	def __str__(self):
		return "Dinamico"
