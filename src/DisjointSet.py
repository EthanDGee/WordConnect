class DisjointSet:
	def __init__(self, elements):
		# Initialize each element as its own parent
		self.parent = {element: element for element in elements.keys()}
		# Initialize size of each element's subset as 1
		self.size = {element: 1 for element in elements.keys()}

	def find(self, x):
		# Find the root of x with path compression
		if self.parent[x] != x:
			self.parent[x] = self.find(self.parent[x])
		return self.parent[x]

	def union(self, x, y):
		# Merge the sets containing x and y (by size)
		root_x = self.find(x)
		root_y = self.find(y)

		if root_x != root_y:
			# Merge smaller tree into the larger tree
			if self.size[root_x] < self.size[root_y]:
				self.parent[root_x] = root_y
				self.size[root_y] += self.size[root_x]
			else:
				self.parent[root_y] = root_x
				self.size[root_x] += self.size[root_y]

	def get_size(self, x):
		# Get the size of the subset containing x
		root_x = self.find(x)
		return self.size[root_x]