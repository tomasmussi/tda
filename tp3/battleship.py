import sys
import numpy as np
from greedy import Greedy
from dinamica import Dinamica
from time import sleep
from collections import deque

DEBUG = False
USE_SLEEP = True
DELAY = 0.5 # Medio segundo

"""
Lee la grilla del juego de batalla naval
El formato de cada fila es:
Vida 1 2 3 4 5
Vida es la vida del barco, y 1 2 3 4 5 es el danio que se produce en las columnas 1 2 3 4 5
"""
def read_grid(file):
	ships = []
	grid = []
	row_len = -1
	with open(file, 'rb') as reader:
		for line in reader:
			row = line.split(' ')
			if (row_len == -1):
				row_len = len(row)
			else:
				# Asegurar que el archivo esta bien formateado
				assert(len(row) == row_len)
			ships.append(int(row[0]))
			del row[0]
			ints = [ int(x) for x in row]
			grid.append(ints)
	return grid, ships


def print_turn(grid, ships, iteration, cols, score, targets = []):
	print("Turno: " + str(iteration))
	print("Barcos: " + str(ships_alive(ships)))
	for i in range(len(ships)):
		print("Barco[" + str(i) + "] vida: " + str(ships[i]) + ", potencial danio: " + str(grid[i][iteration % cols]))
	for i in range(len(targets)):
		print("Lanzadera[" + str(i) + "] blanco: " + str(targets[i]))
	print("Puntos acumulados: " + str(score))
	print("\n")


def print_grid(grid, ships, targets, column):
	# Punto opcional para imprimir turno a turno el avance del juego
	line_separator = "------"
	for i in range(len(grid[0])):
		line_separator += "------"
	correr = "          "
	for i in range(column):
		correr += "      "
	print correr + "|"
	print correr + "|"
	print correr + "|"
	for i in range(len(ships)):
		marks = ""
		for k in range(targets.count(i)):
			marks += " X "
		print line_separator
		line = ""
		for j in range(len(grid[i])):
			line += "| " + '{:3}'.format(grid[i][j])
			if j != len(grid[i])-1:
				line += " "
			else:
				line += "|"
		print '{:3}'.format(ships[i]) + " : " + line  + marks
	print line_separator
	print correr + "|"
	print correr + "|"
	print correr + "|"

def ships_alive(ships):
	return reduce(lambda count, i: count + (i > 0), ships, 0)

def game_finished(ships):
	for i in ships:
		if (i > 0):
			return False
	return True

def game(grid, ships, strategy):
	iteration = 0
	finished = False
	score = 0
	cols = len(grid[0])
	rows = len(ships)
	while (not finished):
		# Busco targets
		targets = strategy.targets(iteration, ships)
		print_grid(grid, ships, targets, iteration % cols)
		# Muestro el estado actual
		print_turn(grid, ships, iteration, cols, score, targets)

		# Updates
		# Do damage
		for row in targets:
			# Target[i] tiene el blanco del ship
			if (DEBUG):
				print (str(iteration) + " % " + str(cols) + " = " + str(iteration % cols))
				print ("Grid[" + str(row) + "][" + str(iteration % cols) + "] = " + str(grid[row][iteration % cols]))
				print ("Ship[" + str(row) + "] = " + str(ships[row]))
			ships[row] -= grid[row][iteration % cols]
			if (DEBUG):
				print ("Ship[" + str(row) + "] = " + str(ships[row]))

		# Increment score
		score += ships_alive(ships)

		iteration += 1
		finished = game_finished(ships)
		if (USE_SLEEP):
			sleep(DELAY)
	print("Finished!")
	print_turn(grid, ships, iteration, cols, score, targets)

def print_board(grid, ships):
	for i in range(len(ships)):
		print str(ships[i]) + " : " + str(grid[i])
	print("\n\n")


def realocate_ships(grid):
	new_grid = []
	indexes = []
	for i in range(len(grid)):
		# Para cada barco, busco el minimo
		min_index = np.argmin(grid[i])
		# Estructura auxiliar para rotar el array
		queue = deque(grid[i])
		queue.rotate(-min_index)
		new_grid.append(list(queue))

	return new_grid

"""
Main de la battala naval
Recibe: nombre de archivo de grilla, estrategia, lanzaderas
"""
def main():
	if (len(sys.argv) != 4):
		print("Parametros incorrectos, debe especificar grilla, estrategia y lanzaderas")
		print("Estrategias reconocidas: 'g' Greedy,\t 'd' Dinamica")
		print("Greedy: python battleship.py grid.txt g 2")
		print("Dinamica: python battleship.py grid.txt d 2")
		exit(1)

	grid, ships = read_grid(sys.argv[1]) # Archivo
	lanzaderas = int(sys.argv[3])
	new_grid = realocate_ships(grid)
	if (sys.argv[2] == 'g'):
		strategy = Greedy(grid, lanzaderas, ships)
		new_strategy = Greedy(new_grid, lanzaderas, ships)
	elif (sys.argv[2] == 'd'):
		strategy = Dinamica(grid, lanzaderas, ships)
		new_strategy = Dinamica(new_grid, lanzaderas, ships)
	else:
		print("Estrategia no reconocida, utilice 'g' para Greedy y 'd' para Dinamica")
		exit(2)

	print("Configuracion de juego:")
	print("Estrategia " + str(strategy) + " con " + str(strategy.lanzaderas) + " lanzaderas ")
	print_board(grid, ships)

	game(grid, list(ships), strategy)

	print("Utilizando estrategia para reubicar barcos para que duren mas\n\n")

	print("Antes")
	print_board(grid, ships)
	print("Reubicados")
	print_board(new_grid, ships)
	sleep(3)
	game(new_grid, list(ships), new_strategy)


if __name__ == '__main__':
	main()
