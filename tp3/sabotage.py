import os.path
import sys
import csv
import copy
from grafo import Grafo
import operator


def read_net(file_net):
	net = Grafo()
	vertices = {}
	edges = {}
	with open(file_net, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			v1 = int(row[0])
			v2 = int(row[1])
			weight = int(row[2])
			vertices[v1] = v1
			vertices[v2] = v2
			edges[(v1,v2)] = weight
	for k in vertices.keys():
		net.agregarVertice(k)
	for t in edges.keys():
		net.agregarArista(t[0], t[1], edges[t])
	return net

def protection_method_one(net):
	original_net = copy.deepcopy(net)
	# Calculo ford fulkerson
	print "Flujo maximo: " + str(net.ford_fulkerson(1,4))

	# Paso los grafos a una forma "plana", ej: grafo[1][2] = 3 <=> grafo[1,2] = 3

	# Agrega complejidad 2M = cantidad de aristas mas dos veces para analizar el grafo de forma mas "amigable"
	original_net_plain = original_net.convertir_plano()
	residual_net_plain = net.convertir_plano()

	# Calculo diferencia entre flujos
	delta_flux = { x: original_net_plain[x] - residual_net_plain[x] for x in original_net_plain if x in residual_net_plain }
	# Ordeno las diferencias
	delta_flux = sorted(delta_flux.items(), key=operator.itemgetter(1))

	print "Custodiar el: " + str(delta_flux[-1][0]) + ' que lleva un flujo de ' + str(delta_flux[-1][1]) + \
			' y el: ' + str(delta_flux[-2][0]) + ' que lleva un flujo de ' +  str(delta_flux[-2][1])

def main():
	if (len(sys.argv) == 1):
		if (not os.path.isfile('redsecreta.map')):
			print("Debe especificar archivo de red, o crear el archivo 'redsecreta.map'")
			exit(1)
		else:
			file_net = 'redsecreta.map'
	elif (len(sys.argv) == 2):
		if (not os.path.isfile(sys.argv[1])):
			print("No existe archivo " + str(sys.argv[1]))
			exit(1)
		else:
			file_net = sys.argv[1].strip()
	else:
		print("Demasiados argumentos")
		print("python sabotage.py")
		print("python sabotage.py mapa.map")
		exit(1)

	print("Usando archivo: " + file_net)

	net = read_net(file_net)
	# Hago una copia porque adentro la rompo toda
	protection_method_one(copy.deepcopy(net))




if __name__ == '__main__':
	main()