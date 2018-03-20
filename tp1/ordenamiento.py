import time
from random import shuffle

from heap import Heap
#from random import randint

DEBUG = False



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


def heapsort(lista):
	heap = Heap(lista)
	new_list = []
	while (not heap.empty()):
		element = heap.pop()
		new_list.append(element)
	return new_list

def compare(sorted_list, test):
	if (len(sorted_list) != len(test)):
		if (DEBUG):
			print "COMPARANDO LISTAS DE DISTINTO TAMANIO"
		return False
	for i in xrange(len(sorted_list)):
		if (sorted_list[i] != test[i]):
			return False
	return True

def list_test(n = 10):
	sorted_list = [ x for x in xrange(n) ]
	shuffled = list(sorted_list)
	shuffle(shuffled)
	return sorted_list, shuffled

methods = {
	"seleccion" : selection_sort,
	"insercion" : insertion_sort,
	"quicksort" : quicksort,
	"mergesort" : mergesort,
	"heapsort" : heapsort
}


def evaluate_method(method, n = 10):
	l,x = list_test(n)
	start = time.time()
	x = methods[method](x)
	end = time.time()
	assert(compare(l,x))
	elapsed = end - start
	print method + " tardo en ordenar " + str(n) + " elementos " + str(elapsed) + " segundos"

def main():
	evaluate_method("seleccion", 1000)
	evaluate_method("insercion", 1000)
	evaluate_method("quicksort", 100000)
	evaluate_method("mergesort", 100000)
	evaluate_method("heapsort", 100000)

if __name__ == '__main__':
	main()
