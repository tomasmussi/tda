
from heapq import *

"""
Clase Heap para implementar heapsort
"""
class Heap(object):

	def __init__(self, alist = []):
		self.l = alist or []

	def parent(self, index):
		return (index - 1) / 2

	#def upheap(self, index):

	#def downheap(self, index):


	#def heapify(self, )

	def heapsort(self):
		heap = []
		for x in xrange(len(self.l)):
			heappush(heap, self.l[x])
		return [heappop(heap) for i in range(len(heap))]
