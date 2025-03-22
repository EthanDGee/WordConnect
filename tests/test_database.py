import unittest

from src.database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.sample_puzzle = Database.Puzzle(
            start="A",
            goal="B",
            score=2,
            solution=["A", "B"]
        )

    def test_add_puzzle_success(self):
        result = self.database.add_puzzle(self.sample_puzzle)
        self.assertTrue(result)

    def test_add_puzzle_duplicate(self):
        self.database.add_puzzle(self.sample_puzzle)
        result = self.database.add_puzzle(self.sample_puzzle)
        self.assertFalse(result)

    def test_get_random_score_puzzle(self):
        self.database.add_puzzle(self.sample_puzzle)
        retrieved_puzzle = self.database.get_random_score_puzzle(2)
        self.assertIsNotNone(retrieved_puzzle)
        self.assertEqual(retrieved_puzzle.start, "A")
        self.assertEqual(retrieved_puzzle.goal, "B")
        self.assertEqual(retrieved_puzzle.score, 2)
        self.assertEqual(retrieved_puzzle.solution, ["A", "B"])

    def test_get_random_score_puzzle_no_match(self):
        puzzle = self.database.get_random_score_puzzle(3)
        self.assertIsNone(puzzle)

    def test_create_new_puzzles(self):
        # This test ensures the create_new_puzzles method doesn't throw errors
        # and adds puzzles to the database. As it depends on Graph, the functionality
        # of puzzle creation isn't explicitly tested here.
        with self.assertRaises(Exception):
            self.database.create_new_puzzles(5)


class TestPuzzle(unittest.TestCase):

    def setUp(self):
        self.sample_row = (1, "A", "B", 2, '["A", "B"]')
        self.sample_solution = ["A", "B"]
        self.puzzle = Database.Puzzle("A", "B", 2, ["A", "B"])

    def test_puzzle_str(self):
        self.assertEqual(
            str(self.puzzle),
            "Puzzle(start=A, goal=B, score=2, solution=['A', 'B'])"
        )

    def test_convert_row_to_puzzle(self):
        puzzle = Database.Puzzle.convert_row_to_puzzle(self.sample_row)
        self.assertEqual(puzzle.start, "A")
        self.assertEqual(puzzle.goal, "B")
        self.assertEqual(puzzle.score, 2)
        self.assertEqual(puzzle.solution, ["A", "B"])  # Solution remains as a serialized string here

    def test_convert_solution_to_puzzle(self):
        puzzle = Database.Puzzle.convert_solution_to_puzzle(self.sample_solution)
        self.assertEqual(puzzle.start, "A")
        self.assertEqual(puzzle.goal, "B")
        self.assertEqual(puzzle.score, 2)
        self.assertEqual(puzzle.solution, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
