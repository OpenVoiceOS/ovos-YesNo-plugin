import os.path
import unittest
import json
from ovos_yes_no import HeuristicYesNoEngine


class TestYesNo(unittest.TestCase):
    """Unit tests for HeuristicYesNoEngine."""

    def setUp(self):
        """Initialize the engine and load test data."""
        self.engine = HeuristicYesNoEngine()
        # Load the test data from the JSON file
        with open(os.path.join(os.path.dirname(__file__), "test_sentences_en.json"), "r") as f:
            self.test_data = json.load(f)

    def test_yes_responses(self):
        """Test that yes sentences are correctly identified."""
        for sentence in self.test_data["yes"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "en-us")
                self.assertTrue(res, f"Expected True for '{sentence}'")

    def test_no_responses(self):
        """Test that no sentences are correctly identified."""
        for sentence in self.test_data["no"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "en-us")
                self.assertFalse(res, f"Expected False for '{sentence}'")

    def test_null_responses(self):
        """Test that neutral sentences return None."""
        for sentence in self.test_data["null"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("question", sentence, "en-us")
                self.assertIsNone(res, f"Expected None for '{sentence}'")

    def test_language_fallback(self):
        """Test that unsupported language variants fall back to closest match."""
        # en-AU should fall back to en-us
        res_au = self.engine.yes_or_no("question", "yes", "en-AU")
        res_us = self.engine.yes_or_no("question", "yes", "en-us")
        self.assertEqual(res_au, res_us, "en-AU should fall back to en-us")

    def test_unsupported_language(self):
        """Test that truly unsupported languages return None."""
        # Use a completely made-up language code that has no close match
        res = self.engine.yes_or_no("question", "yes", "zz-ZZ")
        self.assertIsNone(res, "Unsupported language should return None")
