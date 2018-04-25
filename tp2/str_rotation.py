
from collections import deque

def main():

	st = "hola"
	d = deque(st)
	for i in xrange(len(st)):
		print d
		d.rotate(1)

if __name__ == '__main__':
	main()