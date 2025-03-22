import string
import heapq
import random
import xml.etree.ElementTree as ET
from DisjointSet import DisjointSet


class Graph:
    def __init__(self, file_name=None):
        self.vertexes = {}

        if file_name:
            print("Loading Graph...", end="")
            self.load_vertexes(file_name)
            print("\rLoaded Words")
            print("Bridging Connections...", end="")
            self.make_connections()
            print("\rBridging Complete")
            print("Removing Loners...", end="")
            self.remove_edge_less_vertexes()
            print("\rRemoved Loners")
            print("Removing word islets...", end="")
            self.remove_islets()
            print("\rRemoved word islets")

            print("Graph Loaded")

    def __str__(self):
        result = ""
        for vertex in self.vertexes.values():
            result += str(vertex) + "\n"
        return result

    def export_graph(self, file_path):
        """
        Exports the graph as a GraphML file.
        :param file_path: The output file path where the GraphML will be written.
        """
        # Create the GraphML root and graph tags
        graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
        graph = ET.SubElement(graphml, "graph", id="G", edgedefault="undirected")

        # Add all vertices as nodes
        for vertex in self.vertexes.values():
            ET.SubElement(graph, "node", id=vertex.get_id())

        # Add unique edges, avoiding duplicates
        added_edges = set()  # Track unique edges (undirected edges are treated as sets)
        for vertex in self.vertexes.values():
            for neighbor in vertex.get_edges():
                # Create an edge as a frozenset of the nodes (undirected)
                edge = frozenset([vertex.get_id(), neighbor])
                if edge not in added_edges:
                    ET.SubElement(graph, "edge", source=vertex.get_id(), target=neighbor)
                    added_edges.add(edge)

        # Create the XML tree and write to the file path
        tree = ET.ElementTree(graphml)
        try:
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            print(f"Graph exported successfully to {file_path}")
        except IOError as e:
            print(f"An IOError occurred while writing the file: {e}")

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

    def get_vertexes(self):
        return self.vertexes

    # Connect Set Up Methods
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

    def remove_islets(self):
        # looks through the connected graph and finds islets of that are smaller
        # than minimum_island_size and removes them

        # create a disjoint set and then use the disjoint set to define groupings
        disjoint_set = DisjointSet(self.vertexes)

        for vertex in self.vertexes.keys():
            # loop through the edges and add them to the union
            for neighbor in self.vertexes[vertex].get_edges():
                if disjoint_set.find(vertex) != disjoint_set.find(neighbor):
                    disjoint_set.union(vertex, neighbor)

        # Now we're going to loop through the vertexes and then remove the small islets

        minimum_island_size = 5
        vertex_ids_to_remove = []

        for vertex in self.vertexes.keys():
            if disjoint_set.get_size(vertex) <= minimum_island_size:
                vertex_ids_to_remove.append(vertex)

        for vertex_id in vertex_ids_to_remove:
            del self.vertexes[vertex_id]

    # Paths/Grouping
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

    def generate_puzzle(self):
        # a simple function that keeps grabbing two random words, until it finds 2 that have a path to each other and
        # then outputs the shortest path between them

        puzzle_found = False

        while not puzzle_found:
            start_word = random.randint(0, len(self.vertexes) - 1)
            end_word = random.randint(0, len(self.vertexes) - 1)
            shortest_path = self.find_shortest_path(list(self.vertexes.keys())[start_word],
                                                    list(self.vertexes.keys())[end_word])
            if len(shortest_path) > 0:
                puzzle_found = True
                return shortest_path

    def bulk_generate_puzzles(self, puzzle_count):
        # generates a specified amount of puzzles
        generated_puzzles = []

        for i in range(puzzle_count):
            new_puzzle = self.generate_puzzle()
            generated_puzzles.append(new_puzzle)


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

    def has_neighbor(self, word):
        return word in self.edges

    def __str__(self):
        return self.vertex_id + " - " + str(self.edges)
