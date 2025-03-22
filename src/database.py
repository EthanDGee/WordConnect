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

        def convert_cursor_to_puzzle(self, row: sqlite3.Row):
            start = row[1]
            goal = row[2]
            score = row[3]
            solution = row[4]

            return self.__init__(start, goal, score, solution)

    def add_puzzle(self, start: str, goal: str, score: int, solution: list):
        # adds a puzzle to the database
        self.connection.execute("INSERT INTO puzzle (start, goal, score, solution) VALUES (?, ?, ?, ?)",
                                (start, goal, score, json.dumps(solution)))
        self.connection.commit()

    def get_random_score_puzzle(self, score: int):
        # returns a random puzzle from database that matches the provided score.
        cursor = self.connection.execute("SELECT * FROM puzzle WHERE score = ? ORDER BY RANDOM() LIMIT 1", (score,))
        row = cursor.fetchone()
        return self.Puzzle.convert_cursor_to_puzzle(row) if row else None


if __name__ == "__main__":
    db = Database("game_test")
    db.add_puzzle("a", "b", 3, [])
    db.add_puzzle("c", "d", 3, [])
    db.add_puzzle("e", "f", 3, [])
    db.add_puzzle("g", "h", 2, [])
    db.add_puzzle("i", "j", 2, [])
    db.add_puzzle("k", "l", 2, [])
    db.add_puzzle("m", "n", 2, [])
    db.add_puzzle("o", "p", 1, [])
    db.add_puzzle("q", "r", 1, [])
    db.add_puzzle("s", "t", 5, [])

    print(db.get_random_score_puzzle(3)["start"])
