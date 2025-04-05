import unittest
from src.graph import Graph


class TestGraph(unittest.TestCase):

    def test_add_vertex(self):
        graph = Graph()
        graph.add_vertex(type("Vertex", (object,), {"vertex_id": "A"}))
        self.assertTrue(graph.has_vertex("A"))

    def test_has_vertex(self):
        graph = Graph()
        graph.add_vertex(type("Vertex", (object,), {"vertex_id": "A"}))
        self.assertTrue(graph.has_vertex("A"))
        self.assertFalse(graph.has_vertex("B"))

    def test_remove_islets(self):
        graph = Graph()
        v1 = type("Vertex", (object,), {"vertex_id": "A", "get_edges": lambda: []})
        v2 = type("Vertex", (object,), {"vertex_id": "B", "get_edges": lambda: []})
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.remove_islets()
        self.assertEqual(len(graph.get_vertexes()), 0)

    def test_find_shortest_path(self):
        graph = Graph()
        v1 = type("Vertex", (object,), {"vertex_id": "A", "edges": ["B"]})
        v2 = type("Vertex", (object,), {"vertex_id": "B", "edges": ["C"]})
        v3 = type("Vertex", (object,), {"vertex_id": "C", "edges": []})
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_vertex(v3)
        path = graph.find_shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

if __name__ == "__main__":
    unittest.main()
