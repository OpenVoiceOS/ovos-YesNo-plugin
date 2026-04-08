# ✅ YesNo Parser

A simple tool to indicate whether a user answered "yes" or "no" to a yes/no prompt.

> 🧩 Suited to **parse** user responses
  
## 📥 Install

```bash
pip install ovos-yes-no-plugin
```

## Usage

Standalone usage examples from unittests

```python
from ovos_yes_no_solver import HeuristicYesNoEngine

engine = HeuristicYesNoEngine()

def test_utt(text, expected):
    res = engine.yes_or_no("question", text, "en-us")
    return res == expected

test_utt("yes", True)
test_utt("no", False)
test_utt("no way", False)
test_utt("don't think so", False)
test_utt("i think not", False)
test_utt("that's affirmative", True)
test_utt("beans", None)
test_utt("no, but actually, yes", True)
test_utt("yes, but actually, no", False)
test_utt("yes, yes, yes, but actually, no", False)
test_utt("please", True)
test_utt("please don't", False)
test_utt("I agree", True)
test_utt("agreed", True)
test_utt("I disagree", False)
test_utt("disagreed", False)

# test "neutral_yes" -> only count as yes word if there isn't a "no" in sentence
test_utt("no! please! I beg you", False)
test_utt("yes, i don't want it for sure", False)
test_utt("please! I beg you", True)
test_utt("i want it for sure", True)
test_utt("obviously", True)
test_utt("indeed", True)
test_utt("no, I obviously hate it", False)

# test "neutral_no" -> only count as no word if there isn't a "yes" in sentence
test_utt("do I hate it when companies sell my data? yes, that's certainly undesirable", True)
test_utt("that's certainly undesirable", False)
test_utt("yes, it's a lie", True)
test_utt("no, it's a lie", False)
test_utt("he is lying", False)
test_utt("correct, he is lying", True)
test_utt("it's a lie", False)
test_utt("you are mistaken", False)
test_utt("that's a mistake", False)
test_utt("wrong answer", False)

# test double negation
test_utt("it's not a lie", True)
test_utt("he is not lying", True)
test_utt("you are not mistaken", True)
test_utt("tou are not wrong", True)
```

## 🧠 Algorithm

The plugin's decision logic focuses on interpreting the user’s response as:
- **Affirmative** (✅ yes)
- **Negative** (❌ no)
- **Neutral** (🤷 none)

It achieves this by analyzing specific words and their positions in the input text.

> It is only meant to be slightly better than simply checking for "yes" and "no" in strings

### Key Steps:
1. **🛑 Last Word Priority**: The final relevant word is treated as the user's decision.
2. **📜 Yes and No Categories**: Predefined lists of affirmative (`["yes", "yeah"]`) and negative (`["no", "nah"]`) words determine intent.
3. **⚡ Neutral Words**: Subtle context-dependent terms like `["please", "indeed"]` act as hints.
4. **🔄 Double Negatives**: Phrases like `"not a lie"` are interpreted as affirmative.
5. **🤷 Default to Neutral**: Ambiguous responses return `None`.


The plugin decision logic focuses on interpreting the user’s response as affirmative (yes), negative (no), or neutral. It does this by examining the order and presence of specific words in the user’s input. 

<details>
  <summary>Click for more details</summary>


1. **Last Word Priority**:
   - The algorithm assumes that the user’s final words reflect their decision. It processes words in order and gives priority to the last relevant “yes” or “no” word, considering it as the final decision.

2. **Yes and No Categories**:
   - The language resource files include lists for "yes" and "no" words, which signify clear affirmative or negative intent. For example:
     - "yes": `["yes", "yeah", "yep", "affirmative"]`
     - "no": `["no", "nah", "negative", "disagree"]`

   - When a "yes" word appears later than a "no" word in the sentence (or vice versa), the later word is taken as the user’s final decision. For instance, if the input contains “yes, but no,” the decision would be "no."

3. **Neutral Categories**:
   - **"neutral_yes"** and **"neutral_no"** are softer, context-dependent affirmations or negations. These words may signal agreement or disagreement but lack the direct clarity of “yes” or “no.” Examples include:
     - "neutral_yes": `["sure", "please", "indeed"]`
     - "neutral_no": `["mistake", "inappropriate", "lie"]`
     
   - These words typically act as hints rather than clear indicators. The solver only relies on them if neither a direct "yes" nor "no" word is present. For example, if the input is “sure, please,” it would be interpreted as affirmative because of "neutral_yes."

4. **Double Negatives and Mixed Signals**:
   - The solver also considers the context around negative words to detect double negatives or mitigating expressions. For instance, if a “no” word appears alongside a “neutral_no” word (e.g., “not a lie”), the solver interprets this as an affirmative answer, assuming the negation cancels out the negative meaning.

5. **Default to Neutral**:
   - If no "yes" or "no" (including neutral forms) is found in the text, the solver defaults to `None`, indicating neutrality or ambiguity in the response.


</details>

## ⚠️ Limitations

This parser is effective for simple responses but has limitations due to the inherent complexity of natural language and cultural nuances. 

1. **❌ Context Sensitivity**: Cannot detect sarcasm or idioms.  
2. **🌍 Language Nuances**: May misinterpret cultural expressions or colloquialisms.  
3. **🔄 Double Negatives**: Complex layering of negations might yield errors.  
4. **📖 Vocabulary**: Limited to predefined words, missing rare or slang terms.  
5. **🤷 Ambiguity**: Defaults to `None` for unclear responses.  
6. **📂 Language Files**: Requires well-maintained language resources.  

<details>
  <summary>Click for more details</summary>


1. **Context Sensitivity**: 
   - This algorithm primarily focuses on individual keywords and their positions within the sentence, but it does not deeply understand context or nuanced expressions. Phrases with complex sentiment (e.g., sarcasm, idioms) may yield incorrect results because the algorithm cannot detect these subtleties.

2. **Language-Specific Ambiguities**:
   - The parser relies on lists of words stored in resource files, and these lists may not fully capture language-specific expressions or colloquialisms. For example, in English, “for sure” can mean agreement but might mean something different in other contexts or languages.
   - Translating “neutral” words like "please" or "mistake" for different languages can be challenging, as some expressions do not have direct equivalents and may require interpretation based on cultural context.

3. **Double Negatives and Mixed Intentions**:
   - While the algorithm can handle some double negatives (e.g., “not a lie” as an affirmative), it may fail in cases with complex layering of negations or ambiguous expressions. For instance, “I don’t disagree” may be interpreted as negative, but it often implies agreement in English.

4. **Limited Vocabulary**:
   - Since the algorithm only looks for predefined “yes” and “no” keywords, new or uncommon terms outside these lists are missed. This can be a problem for less frequently used affirmations or negations that aren’t included in the resource files. Keeping these files updated with all possible variations across languages is challenging and requires regular maintenance.

5. **Ambiguity and Neutral Responses**:
   - If the input contains neither clear “yes” nor “no” words, the solver defaults to `None`. However, this is a simplistic approach and may not capture the user’s intended response in cases where indirect language is used to express consent or disagreement.

6. **Dependency on Language Files**:
   - The algorithm depends heavily on the presence of language-specific resources (`yesno.json` files). If resources for a particular language are missing or incomplete, the algorithm raises an error. This restricts usage to supported languages and requires careful management of the resource files for each supported language.

7. **Unclear Scope for Edge Cases**:
   - Ambiguous cases, like where a “neutral_yes” word appears alongside a “neutral_no” word, may confuse the parser, which could lead to inconsistent interpretations. Currently, the algorithm lacks nuanced handling for cases that combine ambiguous terms with yes/no phrases.

</details>

## 🌐 Translating to Other Languages

When translating for other languages:
- Focus on **subtle affirmations** (e.g., "bien sûr" for French).
- Identify **indirect negatives** (e.g., "mensonge" for French).
- Account for **double negatives** to ensure accuracy.

When creating `neutral_yes` and `neutral_no` lists in other languages, keep these tips in mind:

1. **Subtle Affirmations**:
   - "neutral_yes" words should indicate mild agreement without being outright affirmatives. Common examples in English include "sure" or "indeed." Choose words that generally indicate positivity or agreement but aren't direct synonyms of "yes."

2. **Subtle Negations**:
   - For "neutral_no," look for words that imply disagreement or negativity indirectly, like "lie" or "mistake." These words should subtly indicate disapproval or dissent without being equivalent to “no.”

3. **Context-Dependent Meaning**:
   - Words in these categories may change meaning depending on context. Select words that are usually positive or negative but might also appear in complex statements. For example, in Portuguese, "claro" (meaning "clear" or "of course") can be a soft affirmation, while "errado" (meaning "wrong") implies mild disagreement.

4. **Handling Double Negatives**:
   - Be mindful of phrases where negating a neutral word implies affirmation (e.g., “not wrong” meaning "correct"). Include these subtleties in translations to avoid incorrect interpretations, especially in languages with common double-negative structures.

### Example for Translating

Suppose you're translating for French:
- **"neutral_yes"** might include words like "bien sûr" (of course) or "évidemment" (obviously), which imply agreement without a direct "yes."
- **"neutral_no"** might include words like "mensonge" (lie) or "erreur" (mistake), indicating a negative stance without a direct “no.”

Carefully selecting and testing these words for their indirect connotations can improve the solver's effectiveness across languages.

## 🧩 Contribute

Contributions to expand vocabulary, improve translations, or handle edge cases are welcome! 🎉  
