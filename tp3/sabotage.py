import os.path
import sys
from grafo import Grafo


def read_net(file_net):
	net = Grafo()
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


if __name__ == '__main__':
	main()