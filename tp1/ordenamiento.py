import time
from random import shuffle

DEBUG = False

def swap(lista, i, j):
	aux = lista[i]
	lista[i] = lista[j]
	lista[j] = aux

def selection_sort(lista):
	length = len(lista)
	for i in xrange(0, length - 1):
		min_index = i
		for j in xrange(i + 1, length):
			if (lista[j] < lista[min_index]):
				min_index = j
		swap(lista, i, min_index)

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

def print_test(sorted, test):
	equals = compare(sorted, test)
	if (equals):
		print "Las listas son iguales"
	else:
		print "NO FUNCIONO!"


def evaluate_method(method):
	l,x = list_test(10000)
	start = time.time()
	method(x)
	end = time.time()
	assert(compare(l,x))
	elapsed = end - start
	print str(elapsed) + " segundos"

def main():
	evaluate_method(selection_sort)

if __name__ == '__main__':
	main()
