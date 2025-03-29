from better_profanity import profanity
from wordfreq import zipf_frequency


class WordFilter:
    def __init__(self, initial_data_file_name, destination_file_name):
        self.initial_data_file_name = initial_data_file_name
        self.destination_file_name = destination_file_name
        self.frequency_threshold = 3.8

    @staticmethod
    def is_valid_word(word):
        # Checks whether a word is valid or not, A 'valid word' has all its characters between 'a' and 'z'.
        if len(word) == 0:
            return False

        for char in word:
            if ord(char) < 97 or ord(char) > 122:  # ASCII range for 'a' to 'z'
                return False

        return True

    def is_common_word(self, word):
        # returns whether a given word is a common word using it's word frequency
        return zipf_frequency(word, 'en') > self.frequency_threshold

    def trim_words(self):
        profanity.load_censor_words()
        filter_counts = {"invalid": 0, "profanity": 0, "uncommon": 0, "valid": 0}

        # parses through a given file and only returns the valid words.
        try:
            with open(self.initial_data_file_name, "r") as reader, open(self.destination_file_name, "w") as writer:
                for line in reader:
                    word = line.strip()  # Remove any surrounding whitespace or newline characters
                    if not self.is_valid_word(word):
                        print(f"Invalid Word- {word}")
                        filter_counts["invalid"] += 1
                    elif profanity.contains_profanity(word):
                        # prints only the first letter with the rest of the word represented by '*'s
                        print(f"Profanity Word - {word[0]}{'*' * (len(word) - 1)}")
                        filter_counts["profanity"] += 1
                    elif not self.is_common_word(word):
                        print(f"Uncommon Word - {word}")
                        filter_counts["uncommon"] += 1
                    elif len(word) == 1:
                        # due to the way word freq measurers word frequency all letters get improperly flagged as common.
                        print(f"Single Character Word - {word}")
                    else:
                        print(f"Valid Word - {word}")
                        filter_counts["valid"] += 1
                        writer.write(word + '\n')
            # add in i and a
            writer.write("i\na")
        except IOError as e:
            print(f"An IOError occurred: {e}")

        for filter_type in filter_counts.keys():
            print(f"{filter_type}: {filter_counts[filter_type]}")


if __name__ == "__main__":
    src_file_name = "../data/words.txt"
    dest_file_name = "../data/words_trimmed.txt"
    word_parser = WordFilter(src_file_name, dest_file_name)
    word_parser.trim_words()
