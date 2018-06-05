import os.path
import sys
import csv
from grafo import Grafo


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
	path, bottleneck = net.dfs(0,1)
	print(path)
	print(bottleneck)



if __name__ == '__main__':
	main()