import sqlite3
import json
from os import supports_bytes_environ


class Database:
    def __init__(self, name: str):
        # Creates/connects to database and checks for validity

        self.connection = sqlite3.connect(f"{name}.db")
        self.connection.execute("CREATE TABLE IF NOT EXISTS puzzle "
                                "(id INTEGER PRIMARY KEY, "
                                "start TEXT,"
                                "goal TEXT,"
                                "score INTEGER,"
                                "solution BLOB)")

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
            solution = row[4]

            return cls(start, goal, score, solution)

    def add_puzzle(self, start: str, goal: str, score: int, solution: list):
        # adds a puzzle to the database
        row = self.connection.execute(
            "SELECT * FROM puzzle WHERE start = ? AND goal = ? AND score = ? AND solution = ?",
            (start, goal, score, json.dumps(solution))).fetchone()
        if not row:
            self.connection.execute("INSERT INTO puzzle (start, goal, score, solution) VALUES (?, ?, ?, ?)",
                                    (start, goal, score, json.dumps(solution)))
            self.connection.commit()

    def get_random_score_puzzle(self, score: int):
        # returns a random puzzle from database that matches the provided score.
        cursor = self.connection.execute("SELECT * FROM puzzle WHERE score = ? ORDER BY RANDOM() LIMIT 1", (score,))
        row = cursor.fetchone()
        return self.Puzzle.convert_row_to_puzzle(row) if row else None


if __name__ == "__main__":
    db = Database("game_test")
