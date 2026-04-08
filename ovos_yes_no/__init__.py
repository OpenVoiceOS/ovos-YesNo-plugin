import json
import os.path
import re
from typing import Optional

from langcodes import tag_distance
from ovos_plugin_manager.templates.agents import YesNoEngine
from ovos_utils.lang import standardize_lang_tag
from quebra_frases import word_tokenize


class HeuristicYesNoEngine(YesNoEngine):
    """
    Engine for evaluating answers to yes/no questions.

    Determines if a user input means "yes", "no" or undefined
    """
    def __init__(self, config=None):
        super().__init__(config)
        locale = f"{os.path.dirname(__file__)}/locale"
        self.resources = {}
        for lang in os.listdir(locale):
            fname = f"{locale}/{lang}/yesno.json"
            if os.path.isfile(fname):
                with open(fname) as f:
                    lang = standardize_lang_tag(lang)
                    self.resources[lang] = json.load(f)

    @staticmethod
    def normalize(text: str, lang: str):
        # Remove single characters surrounded by spaces
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        # Convert to lowercase
        text = text.lower()

        # Handle language-specific normalization
        if lang.startswith("en"):
            text = text.replace("don't", "do not")

        stopwords = ["the"]
        if lang.startswith("pt"):
            stopwords = ["esta", "está", "estás", "é", "de", "com", "são"]
        words = [w for w in word_tokenize(text) if w not in stopwords]
        return " ".join(words)

    def _match_lang(self, lang: str) -> str:
        lang = standardize_lang_tag(lang)
        if lang not in self.resources:
            best_lang = None
            best_dist = 10000000
            for candidate in self.resources.keys():
                dist = tag_distance(lang, candidate)
                if dist < best_dist:
                    best_lang = candidate
                    best_dist = dist
            if best_dist > 10:
                raise ValueError(f"Unsupported language: {lang}")
            lang = best_lang
        return lang

    def yes_or_no(self, question: str, response: str, lang: Optional[str] = None) -> Optional[bool]:
        """
        True: user answered yes
        False: user answered no
        None: invalid/neutral answer
        """
        lang = lang or "en-us"
        lang = self._match_lang(lang)
        text = self.normalize(response, lang)

        # if user says yes but later says no, he changed his mind mid-sentence
        # the highest index is the last yesno word
        res = None
        best = -1

        # Compile regex patterns
        yes_pattern = re.compile(r'\b(?:' + '|'.join(self.resources[lang]["yes"]) + r')\b')
        no_pattern = re.compile(r'\b(?:' + '|'.join(self.resources[lang]["no"]) + r')\b')
        neutral_yes_pattern = re.compile(r'\b(?:' + '|'.join(self.resources[lang].get("neutral_yes", [])) + r')\b')
        neutral_no_pattern = re.compile(r'\b(?:' + '|'.join(self.resources[lang].get("neutral_no", [])) + r')\b')

        # Match yes words
        for match in yes_pattern.finditer(text):
            idx = match.start()
            if idx >= best:
                best = idx
                res = True

        # Match no words
        for match in no_pattern.finditer(text):
            idx = match.start()
            if idx >= best:
                best = idx

                # Handle double negatives (e.g., "not a lie")
                double_negatives = [
                    f"{match.group()} {neutral}"
                    for neutral in self.resources[lang].get("neutral_no", [])
                ]
                for pattern in double_negatives:
                    if re.search(re.escape(pattern), text):
                        res = True
                        break
                else:
                    res = False

        # Match neutral no (if no "yes" detected before)
        if res is None:
            for match in neutral_no_pattern.finditer(text):
                idx = match.start()
                if idx >= best:
                    best = idx
                    res = False

        # Match neutral yes (if no "no" detected before)
        if res is None:
            for match in neutral_yes_pattern.finditer(text):
                idx = match.start()
                if idx >= best:
                    best = idx
                    res = True

        # None - neutral
        # True - yes
        # False - no
        return res


if __name__ == "__main__":
    cfg = {}
    bot = HeuristicYesNoEngine(config=cfg)
    print(bot.yes_or_no("The sun is blue", "disagree", lang="en-AU"))
