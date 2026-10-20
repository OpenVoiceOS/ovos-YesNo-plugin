import os.path
import unittest
import json
from ovos_yes_no import HeuristicYesNoEngine


class TestYesNoGL(unittest.TestCase):
    """Unit tests for HeuristicYesNoEngine with Galician language."""

    def setUp(self):
        """Initialize the engine and load Galician test data."""
        self.engine = HeuristicYesNoEngine()
        # Load the test data from the JSON file
        with open(os.path.join(os.path.dirname(__file__), "test_sentences_gl.json"), "r") as f:
            self.test_data = json.load(f)

    def test_yes_responses_gl(self):
        """Test that Galician yes sentences are correctly identified."""
        for sentence in self.test_data["yes"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pregunta", sentence, "gl-es")
                self.assertTrue(res, f"Expected True for '{sentence}'")

    def test_no_responses_gl(self):
        """Test that Galician no sentences are correctly identified."""
        for sentence in self.test_data["no"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pregunta", sentence, "gl-es")
                self.assertFalse(res, f"Expected False for '{sentence}'")

    def test_null_responses_gl(self):
        """Test that neutral Galician sentences return None."""
        for sentence in self.test_data["null"]:
            with self.subTest(sentence=sentence):
                res = self.engine.yes_or_no("pregunta", sentence, "gl-es")
                self.assertIsNone(res, f"Expected None for '{sentence}'")
