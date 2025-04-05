from .database import Database


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
        self.word_sequence = []

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
            "You will be presented with a pair of words, and you will need to try and get between them in as few moves"
            " as possible.\nYou can only change one letter at a time. You can swap a letter, add a letter, or remove "
            "a letter.\nMade a mistake and want to go back a step? Type 'b' to go back to your previous word at no "
            "penalty to your score If you want to quit the current puzzle, type 'q'.\n Try your best to tie the "
            "computer, or if you're really skilled, and a little lucky, you can even try to beat it")

    def format_word_sequence(self):
        return self.start_word + " -> ".join(self.word_sequence)

    def valid_jump(self, current: str, next_word: str):
        """
        Determines if a given transition/jump between words is valid.

        Parameters:
        current: str
            The starting word for the validation process.
        next_word: str
            The word to which the transition is being checked for validity.

        Returns:
            success: bool
            error: str
        """
        # a function that determines if a users word is a valid jump from the current word
        # if the word jump is valid return True, and ""
        # else return false, and return error

        current = current.lower()
        next_word = next_word.lower()

        # same word case
        if current == next_word:
            return False, "Invalid Jump: You can't jump to the same word."

        # check for too many or too little letters
        if len(current) - len(next_word) >= 2:
            return False, "Invalid Jump: You can only add one letter at a time."
        elif len(current) - len(next_word) <= -2:
            return False, "Invalid Jump: You can only drop one letter at a time."

        # check if it's in the much larger user list
        if next_word not in self.possible_words:
            return False, f"Invalid Jump: {next_word} is not in the valid word list."

        # if they're the same size check for only one swapped letter
        if len(current) == len(next_word):
            swapped_letters = 0
            for i in range(len(current)):
                if current[i] != next_word[i]:
                    swapped_letters += 1
            if swapped_letters != 1:
                return False, "Invalid Jump: You can only swap one letter at a time."

        # if a letter was dropped
        elif len(current) > len(next_word):
            dropped_letters = 0
            start_index = 0
            next_index = 0

            while start_index < len(current) and next_index < len(next_word):
                if current[start_index] != next_word[next_index]:
                    start_index += 1
                    dropped_letters += 1
                else:
                    start_index += 1
                    next_index += 1

            if dropped_letters == 0 and start_index == len(current) - 1:
                # Letter is dropped at the very end (valid scenario)
                dropped_letters += 1

            elif dropped_letters != 1:

                return False, "Invalid Jump: You can only drop one letter at a time."


        # if a letter was added
        elif len(current) < len(next_word):
            changed_letters = 0
            start_index = 0
            next_index = 0
            while start_index < len(current) and next_index < len(next_word):
                if current[start_index] != next_word[next_index]:
                    next_index += 1
                    changed_letters += 1
                else:
                    start_index += 1
                    next_index += 1

            if changed_letters == 0 and next_index == len(next_word) - 1:
                changed_letters += 1

            if changed_letters != 1:
                return False, "Invalid Jump: You can only add one letter at a time."

        # if all tests have been passed
        return True, ""

    def new_puzzle(self):
        puzzle = self.db.get_random_score_puzzle(5)
        not_solved = True
        print(f"New Puzzle - {puzzle.start} -> {puzzle.goal}")
        print(f"Score: {puzzle.score}")
        self.start_word = puzzle.start
        self.current_word = puzzle.start
        self.goal_word = puzzle.goal
        self.word_sequence = []
        while not_solved:
            print("Enter your next guess: ", end="")
            guess = input().lower()
            if guess.lower() == "b":
                self.back_track()

            if self.valid_jump(self.current_word, guess):
                print("Valid Jump")
                self.current_word = guess
                self.word_sequence.append(guess)
                # check for win
                if self.current_word == self.goal_word:
                    not_solved = False
            elif guess == "q":
                break
            else:
                print("Invalid Jump")

        print("\n")

        if not_solved:
            print("You lost!")
            print(f"The Computer guessed the word in {puzzle.score} guesses.")
            print(puzzle.format_solution())
        else:
            print("You won!")
            print(f"You guessed the word in {len(self.word_sequence)} guesses.")
            print(self.format_word_sequence())
            print(f"The Computer guessed the word in {puzzle.score} guesses.")
            print(puzzle.format_solution())

        # add some white space for a clear gap between puzzles
        print("\n")

    def back_track(self):
        if len(self.word_sequence) == 0:
            print("You can't go back any further.")
            return False
        elif len(self.word_sequence) == 1:
            # the starting word is not a part of the word sequence and as result we cant get its word from the sequence
            self.word_sequence.pop()
            self.current_word = self.start_word
            print(f"Backtracked to {self.current_word}")
            return True
        else:
            # remove last word
            self.word_sequence.pop()
            # set current word to last of word sequence
            self.current_word = self.word_sequence[-1]
            print(f"Backtracked to {self.current_word}")
            return True


if __name__ == "__main__":

    game = Game("../data/filtered_words.txt")
    game.tutorial()

    # Initiate Game Loop
    while True:
        game.new_puzzle()
