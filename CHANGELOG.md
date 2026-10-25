# Changelog

## 1.1.5

- §23 now says to cut what the addressee already knows, not just move it below the request, and never to remind a reader of what they said themselves. The audit checks §23 again in memos and letters, and lists Russian calques among the tells that most often survive.
- The audit no longer lets two separate statements of the source be joined by a cause or purpose the source did not state.
- `barla.py` now catches the Russian calques `-yň çäklerinde`, `öz içine alýar`, `bolup durýar` and padding `amala aşyrylýar`; `Siziň bilşiňiz ýaly` and reminders of what the reader said (§23); the Turkish `-abilir/-ebilir` (`gowulaşabilir` → `gowulaşyp biler`); and an apostrophe before an ending (`YouTube'da`, `Aşgabat'da`).
- Added a sixth corpus case: a memo to a general director, with hidden characters and a Cyrillic letter inside a Latin word.

## 1.1.4

- `barla.py` now catches an ending that breaks harmony after the plural (`mekdeplerda` → `mekdeplerde`), knowledge-limit wording before a guess (`Elimdäki maglumatlara görä`, §21), and Markdown headings that capitalize every word. The emoji note no longer makes an exception for social posts.
- Added a test corpus in `tests/corpus/`: five machine-written Turkmen texts (news, posts, an article) with the facts that must survive, the tells and errors that must go, and an accepted result for each. `tests/grade.py` grades any result against a case; the corpus tests run on every push. The grader catches each mistake earlier versions made: the invented jury role, the softened sayings and unnamed experts, and `kompýuteri oturdyldy`.

## 1.1.3

- A person's title, role or relation to an event must come word for word from the source. A vague `bilen baglanyşykly` stays vague and the user is asked, instead of becoming a role such as `eminler toparyndan`. Added to the audit, to §14 with this example, and to the one-file prompt. Found in a test where the skill made a teacher a member of the jury.
- `barla.py` no longer flags AI phrases inside «...» quotations, since quoted words belong to someone else.

## 1.1.2

- `barla.py` no longer reads `bir` in `diňe bir`, `her bir`, `hiç bir`, `ýene bir` and `haýsy bir` as the number one, so `diňe bir meseleleri` is not reported as a plural after a number.

## 1.1.1

- The draft audit now says what counts as a fact: something a reader could check (a name, number, date, place, event, or a quote of a named person). Sayings, answers to an objection nobody raised and claims of unnamed experts are not facts; §3, §5 and §15 cut them instead of softening them, and every such cut is listed in the notes to the user. Found in a test where `Endik — saglygyň açary`, `... diýip pikir edýänler hem bar` and `Hünärmenleriň pikiriçe` survived in a softer form.
- The audit also checks that every sentence keeps a clear subject after the sentence before it is cut (`Ýodalaryň ugrunda`, not `Ugrunda`).
- `barla.py --fix` removes invisible characters (zero-width spaces, soft hyphens, direction marks, Unicode tag characters) and turns unusual spaces into normal ones; `-o` writes the cleaned text to a file. Detection now also covers tag characters, direction overrides and thin or wide spaces.

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
