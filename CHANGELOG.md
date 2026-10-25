# Changelog

## 1.1.0

- Reorganized the AI patterns into 23 numbered patterns in six sections, strongest first, with a *weak alone* rule for tells that prove nothing on their own. Added seven patterns with Turkmen examples: sayings that sound deep (§3), arguing with no one (§5), stacked qualifiers (§9), vague connection (§14), a heading repeated in the first sentence (§18), writing about the document (§22) and re-explaining what the reader knows (§23).
- Added a two-pass audit before the final text. Every sentence of the draft must trace back to a sentence of the source, so encouragement or calls to action the source never had (`Başlamak kyn däl.`) are deleted.
- Added voice matching: a sample of the user's own writing sets sentence length, word choice, formulas, dashes and emoji.
- Emoji are now removed by default in every genre, including social posts, unless the user asks for them or their sample uses them.
- Added a "show your work" output that returns the draft, the remaining tells and the final text.
- `barla.py` now catches `y` written for `ý` after a vowel (`peydaly`, `bay`), a plural after a number with adjectives in between (`6 täze mikrofonlar`), any `Geliň, ... -eliň` opener, and dashes in short texts.
- Added the rule that the subject of a passive verb keeps its base form (`12 kompýuter oturdyldy`, not `kompýuteri`), a slip found while testing this version.
- Added Claude Code and Cursor plugin manifests, an OpenAI agents file, contribution rules, issue templates and a package check that runs on every push.
- Credited Humanizer by Siqi Chen (MIT), on which the general AI patterns are based, in `THIRD_PARTY_NOTICES.md`.

## 1.0.0

- First release: Turkmen orthography, morphology, punctuation and lexicon references summarized from Ene dilim, Turkish and Russian interference list, AI writing patterns with Turkmen examples, genre rules for news, letters, documents and posts, the `barla.py` checker, a one-file prompt for other assistants, and an npx installer.
