
"""
Clase Heap para implementar heapsort
"""
class Heap(object):

	def __init__(self, alist = []):
		self.heap = alist or []
		self.heapify()
		self.len = len(self.heap)

	def swap(self, i, j):
		aux = self.heap[i]
		self.heap[i] = self.heap[j]
		self.heap[j] = aux

	def parent(self, index):
		return (index - 1) / 2


	def empty(self):
		return self.len == 0

	def upheap(self, index):
		if (index > 0):
			i_parent = self.parent(index)
			if (self.heap[index] < self.heap[i_parent]):
				self.swap(index, i_parent)
				self.upheap(i_parent)

	def downheap(self, index):
		if (index < self.len):
			i_left = 2 * index + 1
			i_right = 2 * index + 2
			min_index = -1
			if (i_right < self.len):
				# Hay dos hijos
				if (self.heap[i_left] < self.heap[i_right]):
					min_index = i_left
				else:
					min_index = i_right
			elif (i_left < self.len):
				# Hay un hijo
				min_index = i_left
			if (min_index != -1 and self.heap[min_index] < self.heap[index]):
				self.swap(min_index, index)
				self.downheap(min_index)

	def push(self, element):
		self.heap.append(element)
		self.len += 1
		self.upheap(self.len - 1)

	def pop(self):
		if (self.empty()):
			return None
		self.swap(0, self.len - 1)
		element = self.heap[self.len - 1]
		self.len -= 1
		self.downheap(0)
		return element

	def heapify(self):
		index = (len(self.heap) - 2) / 2
		while (index >= 0):
			self.downheap(index)
			index -= 1

