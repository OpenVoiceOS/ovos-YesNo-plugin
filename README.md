# ovos-yes-no-plugin

A heuristic yes/no answer parser for [OpenVoiceOS](https://openvoiceos.org).
Classifies a spoken or typed response as **yes** (`True`), **no** (`False`), or **neutral/unclear** (`None`).

## Install

```bash
pip install ovos-yes-no-plugin
```

## Quick Start

```python
from ovos_yes_no import HeuristicYesNoEngine

engine = HeuristicYesNoEngine()

engine.yes_or_no("Do you want to continue?", "yes", "en-us")        # True
engine.yes_or_no("Do you want to continue?", "no way", "en-us")     # False
engine.yes_or_no("Do you want to continue?", "beans", "en-us")      # None
engine.yes_or_no("Do you want to continue?", "it's not a lie", "en-us")  # True (double negative)
engine.yes_or_no("Do you want to continue?", "yes, but actually, no", "en-us")  # False (last word wins)
```

## OVOS Integration

The plugin registers under the `opm.agents.yesno` entry-point group with the key
`ovos-yes-no-plugin`. OVOS and `ovos-plugin-manager` will load it automatically when
a `YesNoEngine` is requested.

```python
from ovos_plugin_manager.agents import get_yesno_plugin

engine = get_yesno_plugin("ovos-yes-no-plugin")
result = engine.yes_or_no("Shall I set a reminder?", "please do", "en-us")  # True
```

## Configuration

No mandatory configuration. An optional `config` dict is accepted by the constructor
and passed through to the base class — the only supported key is `lang` (the default
language to use when `yes_or_no` is called without an explicit `lang` argument).

```python
engine = HeuristicYesNoEngine(config={"lang": "de-de"})
```

## Algorithm

`HeuristicYesNoEngine.yes_or_no` — `ovos_yes_no/__init__.py:71`

The engine scans the normalised response for words listed in a per-language
`locale/<lang>/yesno.json` resource file. The file defines four word lists:

| Key | Role |
|---|---|
| `yes` | Unambiguous affirmatives: `yes`, `yeah`, `affirmative`, … |
| `no` | Unambiguous negatives: `no`, `nah`, `disagree`, … |
| `neutral_yes` | Soft affirmatives counted only when no `no` word is present: `sure`, `please`, … |
| `neutral_no` | Soft negatives counted only when no `yes` word is present: `wrong`, `mistake`, `lie`, … |

Decision rules (in order):

1. **Last word wins.** When both a `yes` word and a `no` word appear, the one at the
   higher character index is taken as the user's final intent.
2. **Double negatives.** A `no`-category word immediately followed by a `neutral_no`
   word (e.g., `not` + `lie` → `"not a lie"`) is interpreted as affirmative.
3. **Neutral words.** If neither a `yes` nor a `no` word was found, `neutral_yes` and
   `neutral_no` words are considered as weak signals.
4. **Default.** No recognised word → return `None`.

Language matching uses `langcodes.tag_distance` to find the closest available locale,
so `en-AU` silently falls back to `en-US`.

## Supported Languages

The bundled `locale/` directory contains resource files for:

`an`, `az`, `ca-ES`, `cs-CZ`, `da-DK`, `de-DE`, `en-US`, `es-ES`, `eu-ES`,
`fa-IR`, `fr-FR`, `hu-HU`, `it-IT`, `nl-NL`, `pl-PL`, `pt-BR`, `ru-RU`,
`sv-SE`, `tr-TR`, `uk-UA`

## Adding a New Language

Create `ovos_yes_no/locale/<lang-TAG>/yesno.json` with the four word lists described
above. Phrase selection tips:

- `neutral_yes`: mild agreement words that are positive but not direct synonyms of
  "yes" (e.g., French `"bien sur"`, Portuguese `"claro"`).
- `neutral_no`: words that imply disapproval indirectly (e.g., French `"mensonge"`,
  Portuguese `"errado"`).
- Double-negative structures vary widely between languages — test them explicitly.

## Limitations

- No sarcasm or idiom detection.
- Vocabulary is limited to the words in the resource files; slang not listed will be
  ignored.
- Complex nested negations beyond one level may yield incorrect results.
- Missing or incomplete resource files cause the engine to return `None` for that
  language rather than raising an error.

## License

Apache 2.0
