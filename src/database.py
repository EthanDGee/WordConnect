import sqlite3
import json


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

    def add_puzzle(self, start: str, goal: str, score: int, solution: list):
        # adds a puzzle to the database
        self.connection.execute("INSERT INTO puzzle (start, goal, score, solution) VALUES (?, ?, ?, ?)",
                                (start, goal, score, json.dumps(solution)))
        self.connection.commit()

    def get_random_score_puzzle(self, score: int):
        self.connection.execute("SELECT * FROM puzzle WHERE score = ?", (score,))


if __name__ == "__main__":
    db = Database("game_test")

