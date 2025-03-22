from better_profanity import profanity


def is_valid_word(word):
    # Checks whether a word is valid or not, A 'valid word' has all its characters between 'a' and 'z'.
    if len(word) == 0:
        return False

    for char in word:
        if ord(char) < 97 or ord(char) > 122:  # ASCII range for 'a' to 'z'
            return False

    return True


def trim_words(initial_data_file_name, destination_file_name):
    profanity.load_censor_words()

    # parses through a given file and only returns the valid words.
    try:
        with open(initial_data_file_name, "r") as reader, open(destination_file_name, "w") as writer:
            for line in reader:
                word = line.strip()  # Remove any surrounding whitespace or newline characters
                if not is_valid_word(word) or profanity.contains_profanity(word):
                    print(f"Failed Word - {word}")
                else:
                    writer.write(word + '\n')
    except IOError as e:
        print(f"An IOError occurred: {e}")


if __name__ == "__main__":
    src_file_name = "../data/words.txt"
    dest_file_name = "../data/words_trimmed.txt"
    trim_words(src_file_name, dest_file_name)
