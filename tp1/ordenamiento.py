import time
from random import shuffle
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
}


def evaluate_method(method, n = 10):
	l,x = list_test(n)
	start = time.time()
	methods[method](x)
	end = time.time()
	assert(compare(l,x))
	elapsed = end - start
	print str(elapsed) + " segundos"

def main():
	#evaluate_method("seleccion", 10000)
	#evaluate_method("insercion", 10000)
	evaluate_method("quicksort", 1000000)

if __name__ == '__main__':
	main()
