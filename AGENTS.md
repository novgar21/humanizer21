# Guide for contributors and agents

How to change humanizer21 without breaking the skill, its package or its Turkmen.

## What this repo contains

humanizer21 is an agent skill written in Markdown, with one Python checker and a Node installer. `SKILL.md` is the prompt agents read on every use; the files in `references/` are read only when a task needs them.

| File | Role |
|---|---|
| `SKILL.md` | Workflow, voice, output rules. Read on every use, so keep it short. |
| `references/ai-patterns.md` | The numbered AI patterns (§1 to §23), with Turkmen examples. |
| `references/turkmen-tells.md` | Turkish words, Russian calques, machine Turkmen phrases. |
| `references/orthography.md`, `morphology.md`, `punctuation-lexicon.md` | Turkmen rules summarized from Ene dilim. |
| `references/styles.md`, `examples.md` | Genre rules and before/after examples. |
| `scripts/barla.py` | The checker. Standard library only, Python 3.8+. |
| `prompts/system-prompt.md` | One-file version for assistants that do not load skills. Must stay under 8,000 characters. |
| `bin/install.js` | The npx installer. No dependencies. |
| `.claude-plugin/`, `.cursor-plugin/`, `agents/openai.yaml` | Plugin and agent manifests. |
| `scripts/validate-package.py` | Checks versions, manifests, pattern numbers and sizes. |

## Rules for changes

- **Turkmen first.** A change to a Turkmen rule needs a native speaker's review and, where possible, a reference to the Ene dilim page it comes from. Mark rules that come from press practice rather than Ene dilim with *(usage)*.
- **Never copy** text or dictionary data from Ene dilim. Summarize in your own words.
- **Patterns** are numbered from 1 without gaps, strongest first. Prefer folding a new tell into an existing pattern. If you renumber, update every `§` reference in `SKILL.md` and `references/`.
- **Version.** Keep one version in `SKILL.md` (`metadata.version`), the first `CHANGELOG.md` heading, `package.json` and both plugin manifests.
- **Description.** The plugin manifests use the first two sentences of the `SKILL.md` description.
- **Length.** `SKILL.md` stays under 2,500 words; detail goes into `references/`.
- **Facts.** Examples in the references must never add a fact in the "after" text that the "before" text lacks.
- **Checker.** Every new check in `barla.py` gets a test in `tests/test_barla.py`, including a test that correct text stays clean.
- **Corpus.** When a rewrite goes wrong in a way the rules should have prevented, add the text to `tests/corpus/` as a new case with `input.txt`, `expected.json` and a corrected `reference.txt`. Run `python3 tests/grade.py` on the skill's next answer before releasing a fix.
- **History.** Add a `CHANGELOG.md` note for any change in behavior.

## Checks before publishing

```bash
npm test
python3 scripts/validate-package.py
claude plugin validate .
```

## Writing style

Plain language in prompts, documentation and messages: the main point first, common words, active voice, short sentences, one term for one thing. Keep exact identifiers, commands, paths, Turkmen examples and watched phrases unchanged.
