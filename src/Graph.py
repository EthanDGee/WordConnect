import string
import heapq
import random


class Graph:
	def __init__(self, file_name=None):
		self.vertexes = {}
		if file_name:
			print("Loading Graph...")
			self.load_vertexes(file_name)
			print("\rLoaded Words")
			print("Bridging Connections...")
			self.make_connections()
			print("\rBridging Complete")
			print("Removing Vertexes with 0 Edges...")
			self.remove_edge_less_vertexes()
			print("\rRemoved Vertexes with 0 Edges")
			print("Graph Loaded")

	# Vertex Methods
	def has_vertex(self, vertex_id):
		return vertex_id in self.vertexes

	def add_vertex(self, new_vertex):
		self.vertexes[new_vertex.vertex_id] = new_vertex

	def load_vertexes(self, file_name):
		# given an input file of words, create the vertexes.
		try:
			with open(file_name, "r") as reader:
				for line in reader:
					word = line.strip()  # Remove any surrounding whitespace or newline characters
					if not self.has_vertex(word):
						# Create and add new vertex
						new_vertex = Vertex(word)
						self.add_vertex(new_vertex)
		except IOError as e:
			print(f"An IOError occurred: {e}")

	# Bridging Connections
	def make_connections(self):
		# loops through all vertexes/words
		for word, vertex in self.vertexes.items():

			# loops through the letters and swaps them one at a time looking for valid words
			for letter_index in range(len(word)):
				# Loop through all lowercase letters (a-z)
				for potential_letter in string.ascii_lowercase:
					# print(f"{word} - {word[:letter_index] + potential_letter + word[letter_index + 1:]}")
					new_word = word[:letter_index] + potential_letter + word[letter_index + 1:]
					if new_word != word and self.has_vertex(new_word):
						self.vertexes[word].add_edge(new_word)

				# Attempt to remove a letter
				removed_word = word[:letter_index] + word[letter_index + 1:]
				if self.has_vertex(removed_word):
					self.vertexes[word].add_edge(removed_word)
					self.vertexes[removed_word].add_edge(word)

	def remove_edge_less_vertexes(self):
		# removes all vertexes from the graph that have a degree of 0

		vertex_ids_to_remove = []
		for vertex in self.vertexes.values():
			if vertex.get_degree() == 0:
				vertex_ids_to_remove.append(vertex.get_id())

		for vertex_id in vertex_ids_to_remove:
			del self.vertexes[vertex_id]

	def find_shortest_path(self, start_word, end_word):

		#  Uses Dijkstra's algorithm to find the shortest path between two words

		# returns A list of words representing the shortest path from `start_word` to `end_word`.
		# If no path exists, returns an empty list.

		# Priority queue for Dijkstra's algorithm (min-heap)
		priority_queue = []

		distances = {word: float('inf') for word in self.vertexes}
		distances[start_word] = 0

		# Keep track of predecessors to reconstruct the path
		predecessors = {word: None for word in self.vertexes}
		heapq.heappush(priority_queue, (0, start_word))

		while priority_queue:
			# Get the current node with the smallest distance from the queue
			current_distance, current_word = heapq.heappop(priority_queue)

			# If we reached the end word, reconstruct the path
			if current_word == end_word:
				word_path = []
				while current_word is not None:
					word_path.append(current_word)
					current_word = predecessors[current_word]
				return word_path[::-1]  # Reverse the path and return

			# Iterate over neighbors of the current word
			for neighbor in self.vertexes[current_word].edges:
				# Calculate the distance to the neighbor
				distance = current_distance + 1  # Assuming all edges have weight 1

				# If the calculated distance is shorter, update the distance and predecessor
				if distance < distances[neighbor]:
					distances[neighbor] = distance
					predecessors[neighbor] = current_word
					heapq.heappush(priority_queue, (distance, neighbor))

		# If no path is found, return an empty list
		return []

	def get_vertexes(self):
		return self.vertexes

	def __str__(self):
		result = ""
		for vertex in self.vertexes.values():
			result += str(vertex) + "\n"
		return result


class Vertex:
	def __init__(self, vertex_id):
		self.vertex_id = vertex_id
		self.edges = set()

	def add_edge(self, word):
		self.edges.add(word)

	def get_edges(self):
		return self.edges

	def get_id(self):
		return self.vertex_id

	def get_degree(self):
		return len(self.edges)

	def __str__(self):
		return self.vertex_id + " - " + str(self.edges)


if __name__ == "__main__":
	graph = Graph("../data/words_trimmed.txt")
	print(graph)
	possible_words = list(graph.vertexes.keys())

	for x in range(100):
		random_words = random.sample(possible_words, 2)
		print(f"{random_words[0]} -> {random_words[1]}")
		path = graph.find_shortest_path(random_words[0], random_words[1])
		if not path:
			print("No Path Found")
		else:
			print(path)
