import sqlite3
import json
from .graph import Graph


class Database:
    def __init__(self, name: str):
        # Creates/connects to database and checks for validity

        self.connection = sqlite3.connect(name)
        self.connection.execute("CREATE TABLE IF NOT EXISTS puzzle "
                                "(id INTEGER PRIMARY KEY, "
                                "start TEXT,"
                                "goal TEXT,"
                                "score INTEGER,"
                                "solution BLOB)")
        self.connection.commit()

    class Puzzle:
        def __init__(self, start: str, goal: str, score: int, solution: list):
            self.start = start
            self.goal = goal
            self.score = score
            self.solution = solution

        def __str__(self):
            return f"Puzzle(start={self.start}, goal={self.goal}, score={self.score}, solution={self.solution})"

        @classmethod
        def convert_row_to_puzzle(cls, row: sqlite3.Row):
            start = row[1]
            goal = row[2]
            score = row[3]
            solution = json.loads(row[4])

            return cls(start, goal, score, solution)

        @classmethod
        def convert_solution_to_puzzle(cls, solution: list):
            start = solution[0]
            end = solution[-1]
            score = len(solution)
            solution = solution
            return cls(start, end, score, solution)

        def format_solution(self):
            return " -> ".join(self.solution)

    def add_puzzle(self, puzzle):
        # adds a puzzle to the database
        row = self.connection.execute(
            "SELECT * FROM puzzle WHERE start = ? AND goal = ?",
            (puzzle.start, puzzle.goal)).fetchone()
        # since the game is identical forwards and back in order to avoid duplicates there has to be an additional
        # check if the reverse of the puzzle has already been added.

        reverse_row = self.connection.execute(
            "SELECT * FROM puzzle WHERE start = ? AND goal = ?",
            (puzzle.goal, puzzle.start)).fetchone()

        if row is None and reverse_row is None:
            self.connection.execute("INSERT INTO puzzle (start, goal, score, solution) VALUES (?, ?, ?, ?)",
                                    (puzzle.start, puzzle.goal, puzzle.score, json.dumps(puzzle.solution)))
            self.connection.commit()
            return True
        else:
            return False

    def get_random_score_puzzle(self, score: int):
        # returns a random puzzle from database that matches the provided score.
        cursor = self.connection.execute("SELECT * FROM puzzle WHERE score = ? ORDER BY RANDOM() LIMIT 1", (score,))
        row = cursor.fetchone()
        return self.Puzzle.convert_row_to_puzzle(row) if row else None

    def create_new_puzzles(self, amount):
        # adds an 'amount' of new puzzles to the database

        graph = Graph("../data/words_trimmed.txt")

        total_puzzles_added = 0
        while total_puzzles_added < amount:
            new_puzzle = graph.generate_puzzle()
            if self.add_puzzle(self.Puzzle.convert_solution_to_puzzle(new_puzzle)):
                total_puzzles_added += 1


if __name__ == "__main__":
    db = Database("../data/game_data.db")
    db.create_new_puzzles(10000)
    db.connection.close()
