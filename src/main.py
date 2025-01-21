from Graph import Graph
import random

if __name__ == "__main__":
	graph = Graph("../data/words_trimmed.txt")
	# print(graph)
	print(len(graph.vertexes))
	# graph.export_graph("../data/graph.graphml")

	possible_words = list(graph.vertexes.keys())

	for x in range(10):
		random_words = random.sample(possible_words, 2)
		print(f"{random_words[0]} -> {random_words[1]}", end="")
		path = graph.find_shortest_path(random_words[0], random_words[1])
		if not path:
			print("\nNo Path Found")
		else:
			print(f" in {len(path)-2}\n{path}")
