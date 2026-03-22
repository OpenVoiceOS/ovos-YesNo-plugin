import json
import os.path
import unittest

from ovos_yes_no_solver import YesNoSolver


class TestYesNoFrench(unittest.TestCase):
    def setUp(self):
        self.solver = YesNoSolver()
        with open(os.path.join(os.path.dirname(__file__), "test_sentences_fr.json"), "r") as f:
            self.test_data = json.load(f)

    def test_yesno_fr(self):
        def test_utt(text, expected):
            res = self.solver.match_yes_or_no(text, "fr-fr")
            print(text, expected, res)
            self.assertEqual(res, expected)

        for sentence in self.test_data["yes"]:
            test_utt(sentence, True)

        for sentence in self.test_data["no"]:
            test_utt(sentence, False)

        for sentence in self.test_data["null"]:
            test_utt(sentence, None)
