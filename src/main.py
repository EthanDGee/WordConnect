from database import Database


def display_word_sequence(word_path):
    for word in word_path:
        print(word, end=" -> ")
    print()


class Game:
    def __init__(self, word_list_path):
        self.possible_words = self.load_words(word_list_path)
        self.db = Database("game_data.db")
        self.start_word = "filler-start-word"
        self.current_word = "filler-start-word"
        self.goal_word = "filler-goal-word"

    @staticmethod
    def load_words(word_list_path):
        loaded_words = []
        try:
            with open(word_list_path, "r") as reader:
                for line in reader:
                    word = line.strip()
                    loaded_words.append(word)

            return loaded_words
        except IOError as e:
            print(f"An IOError occurred: {e}")

    @staticmethod
    def tutorial():
        print("Welcome to Word Connect!")
        print(
            "You will be presented with a pair of words, and you will need to get between them in as few moves as possible.")
        print("You can only change one letter at a time. You can swap a letter, add a letter, or remove a letter.")
        print(" If you want to quit, type 'q'. Try your best to tie the computer (you will not beat it)")

    @staticmethod
    def format_user_guesses(guesses):
        return " -> ".join(guesses)

    def valid_jump(self, start: str, next_word: str):
        # a function that determines if a users word is a valid jump from the current word
        # if the word jump is valid return True
        # else return false, and print error

        start = start.lower()
        next_word = next_word.lower()

        # same word case
        if start == next_word:
            print("Invalid Jump: You can't jump to the same word.")
            return False

        # check for too many or too little letters
        if len(start) - len(next_word) >= 2:
            print("Invalid Jump: You can only add one letter at a time.")
            return False
        elif len(start) - len(next_word) <= -2:
            print("Invalid Jump: You can only drop one letter at a time.")
            return False

        # check if it's in the much larger user list
        if next_word not in self.possible_words:
            print("Invalid Jump: that word is not in the valid word list.")
            return False

        # if they're the same size check for only one swapped letter
        if len(start) == len(next_word):
            swapped_letters = 0
            for i in range(len(start)):
                if start[i] != next_word[i]:
                    swapped_letters += 1
            if swapped_letters != 1:
                print("Invalid Jump: You can only swap one letter at a time.")
                return False

        # if a letter was dropped
        elif len(start) > len(next_word):
            dropped_letters = 0
            start_index = 0
            next_index = 0

            while start_index < len(start) and next_index < len(next_word):
                if start[start_index] != next_word[next_index]:
                    start_index += 1
                    dropped_letters += 1
                else:
                    start_index += 1
                    next_index += 1

            if dropped_letters == 0 and start_index == len(start) - 1:
                # Letter is dropped at the very end (valid scenario)
                dropped_letters += 1

            elif dropped_letters != 1:
                print("Invalid Jump: You can only drop one letter at a time.")
                return False


        # if a letter was added
        elif len(start) < len(next_word):
            changed_letters = 0
            start_index = 0
            next_index = 0
            while start_index < len(start) and next_index < len(next_word):
                if start[start_index] != next_word[next_index]:
                    next_index += 1
                    changed_letters += 1
                else:
                    start_index += 1
                    next_index += 1

            if changed_letters == 0 and next_index == len(next_word) - 1:
                changed_letters += 1

            if changed_letters != 1:
                print("Invalid Jump: You can only add one letter at a time.")
                return False

        # if all tests have been passed
        return True

    def new_puzzle(self):
        puzzle = self.db.get_random_score_puzzle(5)
        not_solved = True
        print(f"New Puzzle - {puzzle.start} -> {puzzle.goal}")
        print(f"Score: {puzzle.score}")
        self.start_word = puzzle.start
        self.current_word = puzzle.start
        self.goal_word = puzzle.goal
        user_guesses = []
        while not_solved:
            print("Enter your next guess: ", end="")
            guess = input().lower()
            if guess.lower() == "b":
                self.back_track()

            if self.valid_jump(self.current_word, guess):
                print("Valid Jump")
                self.current_word = guess
                user_guesses.append(guess)
                # check for win
                if self.current_word == self.goal_word:
                    # insert start word at guess head
                    user_guesses.insert(0, puzzle.start)
                    not_solved = False
            elif guess == "q":
                print("Goodbye!")
                break
            else:
                print("Invalid Jump")

        print("You won!")
        print(f"You guessed the word in {len(user_guesses)} guesses.")
        print(self.format_user_guesses(user_guesses))
        print(f"The Computer guessed the word in {puzzle.score} guesses.")
        print(puzzle.format_solution())

    def back_track(self):
        if self.current_word == self.start_word:
            print("You can't go back any further.")
        else:
            self.current_word = self.start_word
            print(f"Backtracked to {self.start_word}")

if __name__ == "__main__":

    game = Game("../data/filtered_words.txt")
    game.tutorial()

    # Initiate Game Loop
    while True:
        game.new_puzzle()
