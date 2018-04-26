import os.path
from random import randint
from collections import deque

DIR = "words"
DEBUG = True
# String that is not a rotation of any of the words
NO_MATCH = "NOTMATCHST"

TEST_LIST = ["OPENSESAME","ITALIANICE","ONEATATIME","EVENSTEVEN","ALOHASTATE","ANNABELLEE",
"OVALOFFICE","SOURGRAPES","ADAMSAPPLE","DONQUIXOTE","EASTORANGE","EASYSTREET","EISENHOWER",
"IVORYTOWER","OPERASERIA","PAGETURNER","PAPERTIGER","PIRATESHIP","RABBITEARS","SANTACLAUS",
"THENATURAL", "ABRACADABR"]

def pruebas():
	st = "hola"
	d = deque(st)
	for i in xrange(len(st)):
		print d
		d.rotate(1)
	print d
	print d == deque(st)
	d.rotate(1)
	print d == deque(st)

def generate_cases():
	if (not os.path.isdir(DIR)):
		os.makedirs(DIR)
	if (not os.path.isfile(DIR + "/words.txt")):
		with open(DIR + '/words.txt', 'w') as f:
			for i in xrange(len(TEST_LIST)):
				rotation = deque(TEST_LIST[i])
				number = randint(0, 10)
				rotation.rotate(number)
				f.write(TEST_LIST[i] + "," + "".join(rotation) + "\n")
	with open(DIR + '/words.txt', 'r') as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	cases = {}
	for line in content:
		spt = line.split(',')
		cases[spt[0]] = spt[1]
	return cases

"""
Busca por fuerza bruta rotaciones de una palabra sobre otra.
Devuelve True si s2 es una rotacion de s1
Devuelve False en caso contrario
"""
def brute_force(s1, s2):
	# Asegurar que estamos comparando strings de misma longitud
	assert(len(s1) == len(s2))
	if (DEBUG):
		print "Verificando que " +str(s2) + " es una rotacion de " + str(s1)
	if (s1 == s2):
		# Son la misma palabra
		return True
	deq = deque(s2)
	for i in xrange(len(s1)):
		deq.rotate(1)
		if ("".join(deq) == s1):
			if (DEBUG):
				print str(s2) + " con rotacion " + "".join(deq) + " == " + str(s1)
			return True
	return False

def solve_by_brute_force(cases):
	for key in cases.keys():
		assert(brute_force(key, cases[key]))
		assert(not brute_force(key, NO_MATCH))

def kmp(s1, s2):
	assert(len(s1) == len(s2))
	if (DEBUG):
		print "KMP: verificando que " +str(s2) + " es una rotacion de " + str(s1)
	return True


def solve_by_kmp(cases):
	for key in cases.keys():
		assert(kmp(key, cases[key]))
		assert(not kmp(key, NO_MATCH))

def main():
	cases = generate_cases()
	solve_by_brute_force(cases)
	solve_by_kmp(cases)


if __name__ == '__main__':
	main()