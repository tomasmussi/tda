import os.path
from random import randint
from collections import deque

DIR = "words"
DEBUG = False
# String that is not a rotation of any of the words
NO_MATCH = "NOTMATCHST"

TEST_LIST = ["OPENSESAME","ITALIANICE","ONEATATIME","EVENSTEVEN","ALOHASTATE","ANNABELLEE",
"OVALOFFICE","SOURGRAPES","ADAMSAPPLE","DONQUIXOTE","EASTORANGE","EASYSTREET","EISENHOWER",
"IVORYTOWER","OPERASERIA","PAGETURNER","PAPERTIGER","PIRATESHIP","RABBITEARS","SANTACLAUS",
"THENATURAL", "ABRACADABR", "BANANANANA"]

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
Busca por fuerza bruta rotaciones de word sobre text_search.
Devuelve True si word es una rotacion de text_search
Devuelve False en caso contrario
"""
def brute_force_rotation(string1, string2):
	# Asegurar que estamos comparando strings de misma longitud
	assert(len(string1) == len(string2))
	if (DEBUG):
		print "Verificando que " +str(string2) + " es una rotacion de " + str(string1)
	deq = deque(string2)
	for i in xrange(len(string2)):
		deq.rotate(1)
		if ("".join(deq) == string1):
			if (DEBUG):
				print str(string2) + " con rotacion " + "".join(deq) + " == " + str(string1)
			return True
	return False

def solve_by_brute_force(cases):
	for key in cases.keys():
		assert(brute_force_rotation(cases[key], key))
		assert(not brute_force_rotation(NO_MATCH, key))

def compute_failure(word):
	# By convention, fail[0] = -1, meaning that if the first pattern/word character doesn't match,
	# kmp should just give up and try next text character
    fail = [None] * len(word) #Initialize List/Array
    j = -1
    for i in range(len(word)):
        if ((j > -1) and (word[i] == word[j])):
            fail[i] = fail[j]
        else:
            fail[i] = j
        while ((j > -1) and (word[i] != word[j])):
            j = fail[j]
        j += 1
    return fail

def kmp(word, text_search, fail=None):
	# returns the index in text_search of the first appearance of word or -1 if it's not found
	# j -> Index in Word/Pattern
	# i -> Index in Text
	assert(not len(word) > len(text_search))
	j = 0
	m = len(word) - 1
	if (not fail):
		fail = compute_failure(word)

	for i in range(len(text_search)):
		while ((j > -1) and (text_search[i] != word[j])):
			j = fail[j]
		if (j == m):
			return i - m # Va el 1?
		j += 1
	return -1

def brute_force_kmp_rotation(string1, string2):
	# Asegurar que estamos comparando strings de misma longitud
	assert(len(string1) == len(string2))
	if (DEBUG):
		print "Verificando que " +str(string2) + " es una rotacion de " + str(string1)
	deq = deque(string2)
	fail = compute_failure(string1)
	for i in xrange(len(string2)):
		deq.rotate(1)
		if (kmp(string1, "".join(deq), fail) != -1):
			if (DEBUG):
				print str(string2) + " con rotacion " + "".join(deq) + " == " + str(string1)
			return True
	return False

def solve_by_brute_force_kmp(cases):
	for key in cases.keys():
		assert(brute_force_kmp_rotation(cases[key], key))
		assert(not brute_force_kmp_rotation(NO_MATCH, key))

def kmp_rotation(string1, string2):
	assert(len(string1) == len(string2))
	if (DEBUG):
		print "Verificando que " +str(word) + " es una rotacion de " + str(text_search)
	text = string2 * 2 #Sobra el ultimo caracter
	if kmp(string1, text) != -1:
		return True
	return False


def solve_by_kmp(cases):
	for key in cases.keys():
		assert(kmp_rotation(cases[key], key))
		assert(not kmp_rotation(NO_MATCH, key))

def main():
	cases = generate_cases()
	solve_by_brute_force(cases)
	solve_by_brute_force_kmp(cases)
	solve_by_kmp(cases)


if __name__ == '__main__':
	main()
