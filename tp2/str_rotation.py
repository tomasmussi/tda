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
Busca por fuerza bruta rotaciones de word sobre text_search.
Devuelve True si word es una rotacion de text_search
Devuelve False en caso contrario
"""
def brute_force(word, text_search):
	# Asegurar que estamos comparando strings de misma longitud
	assert(len(text_search) == len(word))
	if (DEBUG):
		print "Verificando que " +str(word) + " es una rotacion de " + str(text_search)
	if (text_search == word):
		# Son la misma palabra
		return True
	deq = deque(word)
	for i in xrange(len(text_search)):
		deq.rotate(1)
		if ("".join(deq) == text_search):
			if (DEBUG):
				print str(word) + " con rotacion " + "".join(deq) + " == " + str(text_search)
			return True
	return False

def solve_by_brute_force(cases):
	for key in cases.keys():
		assert(brute_force(cases[key], key))
		assert(not brute_force(NO_MATCH, key))




"""
 algorithm kmp_table:
    input:
        an array of characters, W (the word to be analyzed)
        an array of integers, T (the table to be filled)
    output:
        nothing (but during operation, it populates the table)

    define variables:
        an integer, pos <= 1 (the current position we are computing in T)
        an integer, cnd <= 0 (the zero-based index in W of the next character of the current candidate substring)

    let T[0] <= -1

    while pos < length(W) do
        if W[pos] = W[cnd] then
            let T[pos] <= T[cnd], pos <= pos + 1, cnd <= cnd + 1
        else
            let T[pos] <= cnd

            let cnd <= T[cnd] (to increase performance)

            while cnd >= 0 and W[pos] <> W[cnd] do
                let cnd <= T[cnd]

            let pos <= pos + 1, cnd <= cnd + 1

    let T[pos] <= cnd (only need when all word occurrences searched)
"""
def get_kmp_table_lookup(word):
	table = {}
	pos = 1
	cnd = 0
	table[0] = -1
	while (pos < len(word)):
		if (word[pos] == word[cnd]):
			table[pos] = table[cnd]
			pos += 1
			cnd += 1
		else:
			table[pos] = cnd
			cnd = table[cnd]
			while (cnd >= 0 and word[pos] != word[cnd]):
				cnd = table[cnd]
			pos += 1
			cnd += 1
	table[pos] = cnd
	return table





"""
Algoritmo de kmp, implementado a partir del pseudocodigo en wikipedia:
https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
algorithm kmp_search:
    input:
        an array of characters, S (the text to be searched)
        an array of characters, W (the word sought)
    output:
        an array of integers, P (positions in S at which W is found)
        an integer, nP (number of positions)

    define variables:
        an integer, j <= 0 (the position of the current character in S)
        an integer, k <= 0 (the position of the current character in W)
        an array of integers, T (the table, computed elsewhere)

    let nP <= 0

    while j < length(S) do
        if W[k] = S[j] then
            let j <= j + 1
            let k <= k + 1
            if k = length(W) then
                (occurrence found, if only first occurrence is needed, m may be returned here)
                let P[nP] <= j - k, nP <= nP + 1
                let k <= T[k] (T[length(W)] can't be -1)
        else
            let k <= T[k]
            if k < 0 then
                let j <= j + 1
                let k <= k + 1
"""
def kmp(word, text_search):
	assert(len(text_search) == len(word))
	if (DEBUG):
		print "KMP: verificando que " +str(word) + " es una rotacion de " + str(text_search)
	j = 0 # Index in text_search
	k = 0 # Index in word
	table_lookup = get_kmp_table_lookup(word)

	while (j < len(text_search)): # O(n) siendo n la longitud de la palabra
		if (word[k] == text_search[j]): # O(1)
			j += 1
			k += 1
			if (k == len(word) - 1):
				return True
				#k = table_lookup[k]
		else:
			k = table_lookup[k]
			if (k < 0):
				j += 1
				k += 1

	return False



def solve_by_kmp(cases):
	for key in cases.keys():
		assert(kmp(cases[key], key))
		assert(not kmp(NO_MATCH, key))

def main():
	cases = generate_cases()
	solve_by_brute_force(cases)
	solve_by_kmp(cases)


if __name__ == '__main__':
	main()