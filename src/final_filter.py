import pygame
# import nltk
from nltk.corpus import stopwords, wordnet


# nltk.download('stopwords') # uncomment these if you need to download the data
# nltk.download('wordnet')

# A SIMPLE TOOL THAT FILTERS THE REMAINING WORDS LEFT OVER FROM ALL THE OTHER STAGES, AND GRABS THE UNCOMMON ONES,
# AND LETS THE USER 'SWIPE' THROUGH THEM TO DECIDE IF THEY REMAIN IN THE POOL.

# Function to classify words into common and uncommon using nltk
def classify_words(word_list):
	# Get the set of commonly used English stopwords
	common_words = set(stopwords.words('english'))

	# Lists to store common and uncommon words
	uncommon_words = []

	for current_word in word_list:
		# Check if word exists in WordNet and is NOT a stopword
		if current_word not in common_words and not wordnet.synsets(current_word.lower()):
			uncommon_words.append(current_word)

	# remove them from the word
	for word in uncommon_words:
		word_list.remove(word)

	return word_list, uncommon_words


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Word Selector")

# Define fonts and colors
font = pygame.font.Font(None, 74)
neutral_grey = (30, 30, 30)
green = (0, 255, 0)
white = (255, 255, 255)


# Function to read words from a file
def load_words(file_path):
	with open(file_path, "r") as file:
		words = file.readlines()
	return [word.strip() for word in words]


# Function to save selected words to a file
def save_word(file_path, word):
	with open(file_path, "a") as file:
		file.write(word + "\n")


def save_words(file_path, words):
	with open(file_path, "a") as file:
		file.writelines(words)


# Load the words
words = load_words("../data/possible_words.txt")
output_file = "../data/filtered_words.txt"
current_word_idx = 0

# Filter the words

words, uncommon_words = classify_words(words)

# saving the good ones now
save_words(output_file, common_words)

print(f"Saved {len(words)} words to {output_file}")
print(f"Total words remaining to be sorted: {len(uncommon_words)}")

# Game loop
running = True
while running:
	screen.fill(neutral_grey)

	# Display the current word
	if current_word_idx < len(uncommon_words):
		word = uncommon_words[current_word_idx]
		text = font.render(word, True, white)
		screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
	else:
		# End message when all words are processed
		text = font.render("Done!", True, green)
		screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))

	pygame.display.flip()

	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and current_word_idx < len(uncommon_words):
			if event.key == pygame.K_RIGHT:  # Right arrow - save word
				save_word(output_file, words[current_word_idx])
				current_word_idx += 1
			elif event.key == pygame.K_LEFT:  # Left arrow - skip word
				current_word_idx += 1

# Quit Pygame
pygame.quit()
