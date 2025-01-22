from graph import Graph
import random


def display_word_sequence(word_path):
	for word in word_path:
		print(word, end=" -> ")
	print()




if __name__ == "__main__":
	graph = Graph("../data/words_trimmed.txt")

	graph.export_graph("../data/graph.graphml")

	possible_words = list(graph.vertexes.keys())

	# Initiate Game Loop
	while True:
		print("finding pair...", end='\r')
		random_words = random.sample(possible_words, 2)
		path = graph.find_shortest_path(random_words[0], random_words[1])
		guess_count = 0
		if path:
			print(f"Pair Found! - {random_words[0]} -> {random_words[1]} in {len(path) - 2}\n{random_words[0]}")

			last_word = random_words[0]
			current_word = ""

			# until we reach the goal
			while last_word != random_words[1]:

				# prompt the user for a word
				while not graph.vertexes.get(last_word).has_neighbor(current_word):
					current_word = input().lower().strip()
					if current_word == "q":
						break
					if current_word not in graph.vertexes:
						print("Invalid word")
						current_word = ""
					else:
						guess_count += 1
						print(f"Valid Word - {guess_count}")
				if current_word == "q":
					break
				last_word = current_word

		print(f"You got the word in {guess_count} guesses!")
		# an extra 1 is removed from user due to loop issues (there's no do-while loops in python)
		print(f"The Computer was about to get there in {len(path) - 3} guesses.")
		display_word_sequence(path)
qqq
