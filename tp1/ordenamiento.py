import time
from random import shuffle
from random import randint
import heapq as hp
import os.path

# Hecho para ejecutar el peor caso de quicksort con diez mil elementos
import sys
sys.setrecursionlimit(10000)

DEBUG = False

N_FILES = 10
NUMBERS_PER_FILE = 10000
MILLON = 1000000

number_ranges = [50, 100, 500, 1000, 2000, 3000, 4000, 5000, 7500, 10000]

def swap(lista, i, j):
	aux = lista[i]
	lista[i] = lista[j]
	lista[j] = aux

"""
Algoritmo de seleccion:
Input:  lista de enteros
Output: Devuelve la lista ordenada
"""
def selection_sort(lista):
	length = len(lista)
	for i in xrange(0, length - 1):
		min_index = i
		for j in xrange(i + 1, length):
			if (lista[j] < lista[min_index]):
				min_index = j
		swap(lista, i, min_index)
	return lista

"""
Algoritmo de insercion
"""
def insertion_sort(lista):
	i = 0
	while (i < len(lista)):
		j = i
		while (j > 0 and lista[j-1] > lista[j]):
			swap(lista, j, j-1)
			j -=1
		i += 1
	return lista

"""
Metodo de quicksort para particionar la lista y dejar:
A la izquierda del pivot, los menores
A la derecha del pivot los mayores
Hay muchas formas de elegir el pivot, por ahora se opta por usar como pivot el ultimo elemento del rango
"""
def partition(lista, i_from, i_to):
	i_pivot = i_to
	pivot = lista[i_pivot]
	i = i_from - 1
	for j in xrange(i_from, i_to):
		if (lista[j] < pivot):
			i += 1
			swap(lista, i, j)
	swap(lista, i + 1, i_pivot)
	return i + 1

def quicksort_recursive(lista, i_from, i_to):
	if (i_from < i_to):
		# Elegir pivot y partir el array
		index_pivot = partition(lista, i_from, i_to)
		quicksort_recursive(lista, i_from, index_pivot - 1)
		quicksort_recursive(lista, index_pivot + 1, i_to)


def quicksort(lista):
	quicksort_recursive(lista, 0, len(lista) -1)
	return lista

def mergelists(left, right):
	l = []
	i_left = 0
	i_right = 0
	while (i_left < len(left) and i_right < len(right)):
		if (left[i_left] < right[i_right]):
			l.append(left[i_left])
			i_left += 1
		else:
			l.append(right[i_right])
			i_right += 1
	while (i_left < len(left)):
		l.append(left[i_left])
		i_left += 1
	while (i_right < len(right)):
		l.append(right[i_right])
		i_right += 1
	return l

def mergesort_recursive(lista):
	if (len(lista) <= 1):
		return lista
	middle = len(lista) / 2
	left = mergesort_recursive(lista[ : middle ])
	right = mergesort_recursive(lista[middle : ])
	return mergelists(left, right)

def mergesort(lista):
	return mergesort_recursive(lista)


def heapsort(iterable):
	h = []
	for value in iterable:
		hp.heappush(h, value)
	return [hp.heappop(h) for i in xrange(len(h))]

methods = {
	"seleccion" : selection_sort,
	"insercion" : insertion_sort,
	"quicksort" : quicksort,
	"mergesort" : mergesort,
	"heapsort" : heapsort
}


def compare(sorted_list, test):
	if (len(sorted_list) != len(test)):
		if (DEBUG):
			print "COMPARANDO LISTAS DE DISTINTO TAMANIO"
		return False
	for i in xrange(len(sorted_list)):
		if (sorted_list[i] != test[i]):
			return False
	return True



"""
Evalua el metodo de ordenamiento elegido. Method: metodo de ordenamiento, l lista de elementos ordenados
x lista de elementos desordenados
"""
def evaluate_method(method, l, x):
	start = time.time()
	x = methods[method](x)
	end = time.time()
	assert(compare(l,x))
	elapsed = end - start
	return elapsed

"""Construir 10 sets de numeros aleatorios con 10.000 numeros positivos
"""
def generate_numbers():
	if (not os.path.isdir("numeros")):
		os.makedirs("numeros")
		for i in xrange(N_FILES):
			with open('numeros/numeros_' + str(i) + '.txt', 'w') as f:
				for j in xrange(NUMBERS_PER_FILE):
					number = randint(0, MILLON)
					f.write(str(number) + '\n')
	else:
		print "No genero numeros"

def get_numbers_from_file(i):
	with open('numeros/numeros_' + str(i) + '.txt', 'r') as f:
		content = f.readlines()
	return [int(x) for x in content]

"""
Calcular los tiempos de ejecucion de cada algoritmo utilizando los primeros: 50, 100, 500, 1000, 2000, 3000, 4000, 5000,
7500, 10000 numeros de cada set
"""
def execute_sorts():
	output = []
	for i in xrange(N_FILES):
		numbers = get_numbers_from_file(i)
		for rango in number_ranges:
			for method in methods.keys():
				l = numbers[:rango]
				l.sort()
				x = numbers[:rango]
				time_taken = evaluate_method(method, l, x)
				output.append(str(i) + "," + method + "," + str(rango) + "," + str(time_taken))

	with open("numeros/ejecucion.csv", "wb") as f:
		f.write("iteracion,metodo,rango,tiempo\n")
		for i in output:
			f.write(i + '\n')

def write_list_to_file(filename, l):
	with open(filename, 'w') as f:
		for number in l:
			f.write(str(number) + '\n')

"""
Para cada algoritmo genera los peores casos de cada uno de los algoritmos de ordenamiento
"""
def generate_worst_cases():
	if (not os.path.isdir("worst-cases")):
		os.makedirs("worst-cases")
		for k in methods.keys():
			os.makedirs("worst-cases/"+k)
		for i in xrange(N_FILES):
			l = get_numbers_from_file(i)
			r = list(l)
			r.sort(reverse=True)
			write_list_to_file("worst-cases/seleccion/numeros_" + str(i) + ".txt", l) # No depende de datos
			write_list_to_file("worst-cases/insercion/numeros_" + str(i) + ".txt", r) # Mayor a menor
			write_list_to_file("worst-cases/quicksort/numeros_" + str(i) + ".txt", r) # Mayor a menor
			write_list_to_file("worst-cases/mergesort/numeros_" + str(i) + ".txt", r) # Caso especial
			write_list_to_file("worst-cases/heapsort/numeros_" + str(i) + ".txt", r) # Mayor a menor

def get_worst_from_file(i, method):
	with open('worst-cases/' + method + '/numeros_' + str(i) + '.txt', 'r') as f:
		content = f.readlines()
	return [int(x) for x in content]

"""
Calcular los tiempos de ejecucion de cada algoritmo utilizando los primeros: 50, 100, 500, 1000, 2000, 3000, 4000, 5000,
7500, 10000 numeros de cada set
"""
def execute_worst_cases():
	output = []
	for i in xrange(N_FILES):
		for method in methods.keys():
			numbers = get_worst_from_file(i, method)
			for rango in number_ranges:
				l = numbers[:rango]
				l.sort()
				x = numbers[:rango]
				time_taken = evaluate_method(method, l, x)
				output.append(str(i) + "," + method + "," + str(rango) + "," + str(time_taken))

	with open("numeros/peores.csv", "wb") as f:
		f.write("iteracion,metodo,rango,tiempo\n")
		for i in output:
			f.write(i + '\n')


def main():
	generate_numbers()
	execute_sorts()
	generate_worst_cases()
	execute_worst_cases()

if __name__ == '__main__':
	main()
