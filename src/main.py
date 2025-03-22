from database import Database


def display_word_sequence(word_path):
    for word in word_path:
        print(word, end=" -> ")
    print()


class Game:
    def __init__(self, word_list_path):
        self.possible_words = self.load_words(word_list_path)

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

    def valid_jump(self, start: str, next: str):
        # a function that determines if a users word is a valid jump from the current word
        # if the word jump is valid return True
        # else return false, and print error

        start = start.lower()
        next = next.lower()

        if start == next:
            print("Invalid Jump: You can't jump to the same word.")
            return False

        # check for too many or too little letters
        if len(start) - len(next) >= 2:
            print("Invalid Jump: You can only add one letter at a time.")
            return False
        elif len(start) - len(next) <= -2:
            print("Invalid Jump: You can only drop one letter at a time.")
            return False

        # check if it's in the much larger user list
        if next not in self.possible_words:
            return False

        # if they're the same size check for only one swapped letter
        if len(start) == len(next):
            swapped_letters = 0
            for i in range(len(start)):
                if start[i] != next[i]:
                    swapped_letters += 1
            if swapped_letters != 1:
                print("Invalid Jump: You can only swap one letter at a time.")

        # if a letter was dropped
        if len(start) > len(next):
            for i in range(len(next)):
                if start[i] != next[i]:
                    print("Invalid Jump: You can only swap one letter at a time.")
                    return False

                print("Invalid Jump: You can only drop one letter at a time.")



        # if a letter was added
        if len(start) < len(next):
            changed_letters = 0
            start_index = 0
            next_index = 0
            while start_index < len(start) and next_index < len(next):
                if start[start_index] != next[next_index]:
                    next_index += 1
                    changed_letters += 1
                else:
                    start_index += 1
                    next_index += 1

            if changed_letters != 1:
                print("Invalid Jump: You can only drop one letter at a time.")

        # if all tests have been passed
        return True



if __name__ == "__main__":

    game = Game("../data/filtered_words.txt")
    game.tutorial()
    db = Database("game_data.db")

    while True:
        puzzle = db.get_random_score_puzzle(3)

    possible_words = list(graph.vertexes.keys())

    # Initiate Game Loop
    while True:
        print("finding pair...", end='\r')

        random_words = random.sample(possible_words, 2)
        path = graph.find_shortest_path(random_words[0], random_words[1])
        guess_count = 0
        current_word = ""
        if path:
            print(f"Pair Found! - {random_words[0]} -> {random_words[1]} in {len(path) - 1}\n{random_words[0]}")

            last_word = random_words[0]
            current_word = ""

            # until we reach the goal
            while last_word != random_words[1]:

                # prompt the user for a wordPAW
                while not graph.vertexes.get(last_word).has_neighbor(current_word):
                    current_word = input().lower().strip()
                    if current_word == "q":
                        break
                    if current_word not in graph.vertexes:
                        print(f"Invalid word - current word {last_word}")
                        current_word = ""
                    else:
                        guess_count += 1
                        print(f"Valid Word - {guess_count}")
                if current_word == "q":
                    break
                last_word = current_word

        if current_word != "q":
            print(f"You got the word in {guess_count} guesses!")
        # an extra 1 is removed from user due to loop issues (there's no do-while loops in python)
        print(f"The Computer got there in {len(path)} guesses.")
        display_word_sequence(path)
        print("\n\n")
