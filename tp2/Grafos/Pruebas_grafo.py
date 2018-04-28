from Grafo import Grafo
from Esquina import Esquina
from math import pow

def calcular_norma(coords1,coords2):
	x1,y1 = coords1
	x2,y2 = coords2
	return pow(pow(x1-x2,2) + pow(y1-y2,2) , 0.5)

def calcular_peso(esquina1,esquina2):
	t1 = (esquina1.x,esquina1.y)
	t2 = (esquina2.x,esquina2.y)
	peso = calcular_norma(t1,t2)
	return peso

def prueba1():
	grafo=Grafo()
	dicc_esquinas = {}
	esquina1=Esquina(1,0,0,111,111)
	esquina2=Esquina(2,3,3,222,222)
	esquina3=Esquina(3,5,5,333,333)
	esquina4=Esquina(4,7,7,444,444)
	esquina5=Esquina(5,12,12,555,555)
	grafo.agregar_vertice(esquina1)
	grafo.agregar_vertice(esquina2)
	grafo.agregar_vertice(esquina3)
	grafo.agregar_vertice(esquina4)
	grafo.agregar_vertice(esquina5)

	grafo.agregar_arista(calcular_peso(esquina1,esquina2),esquina1,esquina2)
	grafo.agregar_arista(calcular_peso(esquina1,esquina2),esquina1,esquina3)
	grafo.agregar_arista(calcular_peso(esquina1,esquina2),esquina1,esquina4)

	grafo.agregar_arista(calcular_peso(esquina2,esquina3),esquina2,esquina3)
	grafo.agregar_arista(calcular_peso(esquina3,esquina4),esquina3,esquina4)
	grafo.agregar_arista(calcular_peso(esquina4,esquina5),esquina4,esquina5)

	vert1 = grafo.conversion[esquina1]
	lista = grafo.vertices[vert1]
	for v in lista:
		print v[1]


def prueba2():
	grafo=Grafo()
	esquinaA=Esquina("a",0,0,111,111)
	esquinaB=Esquina("b",3,3,222,222)
	esquinaC=Esquina("c",1,10,333,333)
	esquinaD=Esquina("d",7,1,444,444)
	esquinaE=Esquina("e",9,3,555,555)
	esquinaF=Esquina("f",10,10,666,666)
	esquinaG=Esquina("g",5,7,777,777)
	esquinaH=Esquina("h",6,2,888,888)
	esquinaI=Esquina("i",8,8,999,999)
	grafo.agregar_vertice(esquinaA)
	grafo.agregar_vertice(esquinaB)
	grafo.agregar_vertice(esquinaC)
	grafo.agregar_vertice(esquinaD)
	grafo.agregar_vertice(esquinaE)
	grafo.agregar_vertice(esquinaF)
	grafo.agregar_vertice(esquinaG)
	grafo.agregar_vertice(esquinaH)
	grafo.agregar_vertice(esquinaI)

	grafo.agregar_arista(calcular_peso(esquinaA,esquinaB),esquinaA,esquinaB)
	#grafo.agregar_arista(calcular_peso(esquinaB,esquinaH),esquinaB,esquinaH)
	grafo.agregar_arista(calcular_peso(esquinaH,esquinaG),esquinaH,esquinaG)
	grafo.agregar_arista(calcular_peso(esquinaG,esquinaD),esquinaG,esquinaD)
	grafo.agregar_arista(calcular_peso(esquinaB,esquinaD),esquinaB,esquinaD)
	grafo.agregar_arista(calcular_peso(esquinaH,esquinaC),esquinaH,esquinaC)
	grafo.agregar_arista(calcular_peso(esquinaG,esquinaC),esquinaG,esquinaC)
	grafo.agregar_arista(calcular_peso(esquinaG,esquinaE),esquinaG,esquinaE)
	grafo.agregar_arista(calcular_peso(esquinaD,esquinaE),esquinaD,esquinaE)
	grafo.agregar_arista(calcular_peso(esquinaG,esquinaI),esquinaG,esquinaI)
	grafo.agregar_arista(calcular_peso(esquinaE,esquinaI),esquinaE,esquinaI)

	l,d = grafo.camino_minimo(esquinaA,esquinaI)
	for x in l:
		print x
	print d

#prueba1()
prueba2()