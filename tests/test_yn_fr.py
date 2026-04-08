import json
import os.path
import unittest

from ovos_yes_no import HeuristicYesNoEngine


class TestYesNoFrench(unittest.TestCase):
    """Unit tests for HeuristicYesNoEngine with French language."""

    def setUp(self):
        """Initialize the engine and load French test data."""
        self.engine = HeuristicYesNoEngine()
        with open(os.path.join(os.path.dirname(__file__), "test_sentences_fr.json"), "r") as f:
            self.test_data = json.load(f)

    def test_yes_responses_fr(self):
        """Test that French yes sentences are correctly identified."""
        for sentence in self.test_data["yes"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "fr-fr")
                self.assertTrue(res, f"Expected True for '{sentence}'")

    def test_no_responses_fr(self):
        """Test that French no sentences are correctly identified."""
        for sentence in self.test_data["no"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "fr-fr")
                self.assertFalse(res, f"Expected False for '{sentence}'")

    def test_null_responses_fr(self):
        """Test that neutral French sentences return None."""
        for sentence in self.test_data["null"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "fr-fr")
                self.assertIsNone(res, f"Expected None for '{sentence}'")
