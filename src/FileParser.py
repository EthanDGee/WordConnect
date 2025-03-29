from better_profanity import profanity
from nltk.corpus import stopwords
import nltk


class WordParser:
    def __init__(self, initial_data_file_name, destination_file_name):
        self.initial_data_file_name = initial_data_file_name
        self.destination_file_name = destination_file_name
        # load common words from the natural language toolkit library
        self.common_words = set(stopwords.words('english'))

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
        # returns whether a given word is a common word using the nltk library
        return word in self.common_words

    def trim_words(self):
        profanity.load_censor_words()

        # parses through a given file and only returns the valid words.
        try:
            with open(self.initial_data_file_name, "r") as reader, open(self.destination_file_name, "w") as writer:
                for line in reader:
                    word = line.strip()  # Remove any surrounding whitespace or newline characters
                    if not self.is_valid_word(word) or profanity.contains_profanity(word) or not self.is_common_word(word):
                        print(f"Failed Word - {word}")
                    else:
                        writer.write(word + '\n')
        except IOError as e:
            print(f"An IOError occurred: {e}")


if __name__ == "__main__":
    nltk.download('stopwords') # uncomment these if you need to download the common words

    src_file_name = "../data/words.txt"
    dest_file_name = "../data/words_trimmed.txt"
    word_parser = WordParser(src_file_name, dest_file_name)
    word_parser.trim_words()
