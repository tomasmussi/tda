from itertools import combinations_with_replacement, permutations
import numpy as np
import sys

M = {}

class Dinamica(object):

	def __init__(self, grid, lanzaderas, ships):
		self.grid = grid
		self.columns = len(grid[0])
		self.lanzaderas = lanzaderas
		self.ships = ships


		matrix = self.compute_turns_to_kill_matrix()
		solution = self.min_total_turns(matrix)

		self.targets_order = solution[0][0]
		print self.targets_order
		self.target_index = 0



	def min_total_turns(self, matrix):
		ships_index = [i for i in range(len(self.ships))]
		memory = {}
		for i in range(len(self.grid)):
			for j in range(self.columns):
				memory[((i,),j)] = matrix[i][j]
		for number_of_ships in range(2,len(self.ships)+1): #cantidad de barcos
			for p in permutations(ships_index, number_of_ships):
				for c in range(self.columns):
					turns_first = memory[((p[0],),c)]
					memory[(p,c)] = turns_first + memory[(p[1:],turns_first % self.columns)]
					if (number_of_ships == len(self.ships)): #Para el caso donde estan todos los barcos, solo me interesa la primera columna
						break
		possible_solutions = [(k,v) for k,v in memory.iteritems() if len(k[0]) == len(ships_index)]
		best_solution = reduce(lambda x,y: x if x[1] < y[1] else y, possible_solutions)
		return best_solution
		#for elem in sorted(memory.iteritems()):
			#print elem



	def compute_turns_to_kill_matrix(self):
		matrix = np.empty([len(self.grid), self.columns], dtype=int)
		for i in range(len(self.grid)): #ships
			suma_fila = sum(self.grid[i][j] for j in range(self.columns))
			factor = 0
			if self.ships[i] > self.lanzaderas * suma_fila:
				factor = self.ships[i] / (self.lanzaderas * suma_fila)
			for j in range(self.columns):
				ship = self.ships[i]
				turns = 0
				if factor > 0:
					turns += factor * self.columns
					ship -= factor * (self.lanzaderas * suma_fila)
				k = j
				while ship > 0:
					k = (j + turns) % self.columns
					ship -= self.lanzaderas * self.grid[i][k]
					turns += 1
				matrix[i][j] = turns
		return matrix


	def update_damage(self, ships, p, turn):
		updated_ships = list(ships)
		for ship_index in p:
			updated_ships[ship_index] -= self.grid[ship_index][turn % self.columns]
		return updated_ships

	def min_points_recurrent(self, ships, turn, points, total_min):
		if all(x <= 0 for x in ships):
			return points
		ships_alive_index = [i for i in range(len(ships)) if ships[i] > 0]
		for p in combinations_with_replacement(ships_alive_index, self.lanzaderas): #Lanzaderas deberian poder disparar al mismo barco
			updated_ships = self.update_damage(ships, p, turn)
			turn_points = sum(1 for s in updated_ships if s > 0)
			next_min = self.min_points_recurrent(updated_ships, turn+1, points+turn_points, total_min)
			total_min = min(total_min, next_min)
		return total_min

	def min_points_dp(self, ships, turn, points):
		ships = tuple(ships)
		if all(x <= 0 for x in ships):
			return points
		if (ships,points) not in M:
			local_min = float('inf')
			ships_alive_index = [i for i in range(len(ships)) if ships[i] > 0]
			for p in combinations_with_replacement(ships_alive_index, self.lanzaderas): #Lanzaderas deberian poder disparar al mismo barco
				updated_ships = self.update_damage(ships, p, turn)
				turn_points = sum(1 for s in updated_ships if s > 0)
				next_min = self.min_points_dp(updated_ships, turn+1, points+turn_points)
				local_min = min(local_min, next_min)
			M[(ships,points)] = local_min
		return M[(ships,points)]


	"""
	Blancos seleccionados por las lanzaderas, aca es donde se ve implementada la estrategia del
	algoritmo para seleccionar los barcos a los cuales hacer danio
	"""
	def targets(self, turn, ships):
		targets = []
		ship_index = self.targets_order[self.target_index]
		target_ship = ships[ship_index]
		while len(targets) < self.lanzaderas:
			targets.append(ship_index)
			target_ship -= self.grid[ship_index][turn % self.columns]
			if target_ship <= 0 and self.target_index < (len(self.targets_order) - 1):
				self.target_index += 1
				ship_index = self.targets_order[self.target_index]
				target_ship = ships[ship_index]
		return targets

	def __str__(self):
		return "Dinamico"
