import unittest
from src.FileParser import is_valid_word



class TestFileParser(unittest.TestCase):

	def test_is_valid_word_all_lowercase(self):
		self.assertTrue(is_valid_word("valid"))

	def test_is_valid_word_empty_string(self):
		self.assertFalse(is_valid_word(""))

	def test_is_valid_word_with_uppercase(self):
		self.assertFalse(is_valid_word("InValid"))

	def test_is_valid_word_with_numbers(self):
		self.assertFalse(is_valid_word("word123"))

	def test_is_valid_word_with_special_characters(self):
		self.assertFalse(is_valid_word("word!@#"))

	def test_is_valid_word_with_mixed_characters(self):
		self.assertFalse(is_valid_word("word123!@#Valid"))

	def test_is_valid_word_with_only_special_characters(self):
		self.assertFalse(is_valid_word("!@#"))

	def test_is_valid_word_with_whitespace(self):
		self.assertFalse(is_valid_word("word with spaces"))


if __name__ == "__main__":
	unittest.main()
