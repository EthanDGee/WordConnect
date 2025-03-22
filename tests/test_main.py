import unittest

from src.main import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(word_list_path="../data/filtered_words.txt")

    def test_valid_jump_same_word(self):
        self.assertFalse(self.game.valid_jump("party", "party"))

    def test_valid_jump_add_one_letter(self):
        self.assertTrue(self.game.valid_jump("par", "part"))

    def test_valid_jump_drop_one_letter(self):
        self.assertTrue(self.game.valid_jump("party", "part"))

    def test_valid_jump_swap_one_letter(self):
        self.assertTrue(self.game.valid_jump("cat", "bat"))

    def test_invalid_jump_too_many_letters_added(self):
        self.assertFalse(self.game.valid_jump("par", "party"))

    def test_invalid_jump_too_many_letters_dropped(self):
        self.assertFalse(self.game.valid_jump("party", "par"))
        self.assertFalse(self.game.valid_jump("elephant", "ele"))
        self.assertFalse(self.game.valid_jump("butterfly", "butter"))
        self.assertFalse(self.game.valid_jump("running", "run"))
        self.assertFalse(self.game.valid_jump("dancing", "dang"))

    def test_invalid_jump_not_in_possible_words(self):
        self.assertFalse(self.game.valid_jump("par", "pak"))

    def test_invalid_jump_swap_more_than_one_letter(self):
        self.assertFalse(self.game.valid_jump("cat", "dog"))
        self.assertFalse(self.game.valid_jump("part", "pass"))

    def test_valid_jump_mixed_case_letters(self):
        self.assertTrue(self.game.valid_jump("Par", "Part"))
        self.assertFalse(self.game.valid_jump("Par", "pak"))

    def test_invalid_jump_empty_strings(self):
        self.assertFalse(self.game.valid_jump("", ""))

    def test_invalid_jump_one_empty_string(self):
        self.assertFalse(self.game.valid_jump("party", ""))
        self.assertFalse(self.game.valid_jump("", "party"))

    def test_valid_jump_replace_entire_word_one_letter_diff(self):
        self.assertTrue(self.game.valid_jump("talk", "tall"))
        self.assertTrue(self.game.valid_jump("park", "perk"))
        self.assertTrue(self.game.valid_jump("word", "ward"))
        self.assertTrue(self.game.valid_jump("play", "ploy"))
        self.assertTrue(self.game.valid_jump("lamp", "limp"))

    def test_invalid_jump_same_length_multiple_changes(self):
        self.assertFalse(self.game.valid_jump("talk", "tail"))
        self.assertFalse(self.game.valid_jump("park", "pill"))
        self.assertFalse(self.game.valid_jump("word", "warm"))
        self.assertFalse(self.game.valid_jump("play", "pale"))
        self.assertFalse(self.game.valid_jump("lamp", "limb"))

    def test_valid_jump_longer_words_add_one_letter(self):
        self.assertTrue(self.game.valid_jump("runner", "runners"))
        self.assertTrue(self.game.valid_jump("hose", "house"))
        self.assertTrue(self.game.valid_jump("sow", "show"))
        self.assertTrue(self.game.valid_jump("clam", "claim"))

    def test_valid_jump_longer_words_drop_one_letter(self):
        self.assertTrue(self.game.valid_jump("runners", "runner"))
        self.assertTrue(self.game.valid_jump("house", "hose"))
        self.assertTrue(self.game.valid_jump("show", "sow"))
        self.assertTrue(self.game.valid_jump("claim", "clam"))


    def test_invalid_jump_non_alphabetic_characters(self):
        self.assertFalse(self.game.valid_jump("party", "party1"))
        self.assertFalse(self.game.valid_jump("house", "h0use"))
        self.assertFalse(self.game.valid_jump("mice", "m1ce"))
        self.assertFalse(self.game.valid_jump("mitten", "5mitten"))
        self.assertFalse(self.game.valid_jump("doggy", "doggy!"))


if __name__ == "__main__":
    unittest.main()
