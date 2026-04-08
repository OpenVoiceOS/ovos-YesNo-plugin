import os.path
import unittest
import json
from ovos_yes_no import HeuristicYesNoEngine


class TestYesNoPT(unittest.TestCase):
    """Unit tests for HeuristicYesNoEngine with Portuguese language."""

    def setUp(self):
        """Initialize the engine and load Portuguese test data."""
        self.engine = HeuristicYesNoEngine()
        # Load the test data from the JSON file
        with open(os.path.join(os.path.dirname(__file__), "test_sentences_pt.json"), "r") as f:
            self.test_data = json.load(f)

    def test_yes_responses_pt(self):
        """Test that Portuguese yes sentences are correctly identified."""
        for sentence in self.test_data["yes"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pergunta", sentence, "pt-pt")
                self.assertTrue(res, f"Expected True for '{sentence}'")

    def test_no_responses_pt(self):
        """Test that Portuguese no sentences are correctly identified."""
        for sentence in self.test_data["no"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pergunta", sentence, "pt-pt")
                self.assertFalse(res, f"Expected False for '{sentence}'")

    def test_null_responses_pt(self):
        """Test that neutral Portuguese sentences return None."""
        for sentence in self.test_data["null"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pergunta", sentence, "pt-pt")
                self.assertIsNone(res, f"Expected None for '{sentence}'")
