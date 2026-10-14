import unittest

from ovos_yes_no import HeuristicYesNoEngine


class TestCapitalizedWordLists(unittest.TestCase):
    """Responses are lowercased before matching, so capitalized locale entries (it-IT) must still match."""

    def setUp(self):
        self.engine = HeuristicYesNoEngine()

    def test_italian_yes(self):
        for sentence in ("sì", "Sì", "certo", "confermo", "sono d'accordo"):
            with self.subTest(sentence=sentence):
                self.assertTrue(self.engine.yes_or_no("domanda", sentence, "it-it"))

    def test_italian_no(self):
        for sentence in ("no", "non sono d'accordo"):
            with self.subTest(sentence=sentence):
                self.assertFalse(self.engine.yes_or_no("domanda", sentence, "it-it"))

    def test_german_mixed_case_entry(self):
        self.assertTrue(self.engine.yes_or_no("frage", "in ordnung", "de-de"))

    def test_word_lists_are_lowercase(self):
        for lang, resources in self.engine.resources.items():
            for key, words in resources.items():
                with self.subTest(lang=lang, key=key):
                    self.assertEqual(words, [w.lower() for w in words])
