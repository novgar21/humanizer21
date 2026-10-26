# Changelog

## 1.2.0

- New `barla.py --dict` mode lists words that a Turkmen word list does not know, as notes. The list is the Hunspell dictionary of nazartm/turkmen-spell-check-dictionary (about 62,000 stems, Apache 2.0), shipped compressed in `scripts/sozluk/`, plus our additions in `scripts/sozluk/gosmaca.txt`. `barla.py` reads it with its own code and stays standard-library only; on all 1,954 words of the test corpus it gives the same answers as a reference Hunspell implementation. Names, sentence starts, Roman numerals, endings after numbers and words split by hidden characters are skipped.
- It catches slips the other checks miss, such as `welaýatyda` for `welaýatynda`. Its first run on the corpus raised six doubtful words; a native speaker settled them, and the accepted results now get no notes at all. `gosmaca.txt` can also mark a wrong form the dictionary accepts (`!düwni`).
- From those answers: `düwün` keeps its vowel (`düwüni`); after a dropped `u` the next vowel is `u` (`howzunda`, `howzuny`, `oglunyň`, not `howzynda`); `fabrigini` and `münber` are right; and `basseýn` is not used: a pool and a river basin are both `howuz` (`Murgap derýasynyň howzunda`). This corrects the `basseýn` row added in 1.1.7 and two accepted corpus results. `barla.py` flags `howzynda`, `oglynyň` and `basseýn`.
- The skill treats a note from the word list as "check this word": it never changes a word only because the list does not know it.
- `-yp` + `-myş` (`tanalypmyş`, `gelipmiş`) is now described as Turkmen hearsay, kept as the source has it; only the bare Turkish `gelmiş` is an error. Confirmed by a native speaker.
- Added `dokamak` and `daňmak` to the table of words that look interchangeable: carpets and their knots are woven.

## 1.1.8

- The audit now catches contradictions in any source, not only in translations: two facts that cannot both be true (`5–9-njy maý` next to `Üç günüň dowamynda`) go under "to verify" instead of being passed on silently.
- The audit keeps rankings (`iň köp`, `birinji ýeri`), real lists as lists, and a source's statement that information is missing (`resmi maglumat ýok`). Words of a named person in an interview count as a quote.
- When a vowel drops, the person of the ending stays: `oglunyň` (his/her son's), not `ogluň` (your son's). A table of these forms is in `references/orthography.md`. Found in a test where `ogulynyň` became `ogluň`.
- New tells, folded into existing patterns: one exclaimed word as a sentence (§2), a pause staged for the reader (§4), arrows in place of a verb (§17). Pair words with a hyphen (`gije-gündiz`) are marked as normal Turkmen, and edits in files leave tables, numbers and links alone.
- `barla.py --compare SOURCE` lists numbers, quotes, names, table rows and list items that a result lost. The grader uses it to check that quotes and tables survive.
- `barla.py` now catches the wrong dropped-vowel forms (`ogulynyň`, `agyzy`), a missing consonant change (`agaçyň` → `agajyň`, `kitapy` → `kitaby`), month names and place words with a capital letter inside a sentence (`5-nji Maý`, `Aşgabat Şäheri`), a question suffix written apart (`gördüňiz mi`), the Turkish `-iyor`, and plurals after `2 müňden gowrak` and after compounds such as `2 täze haly fabrikleri`.
- Added a tenth corpus case: a long feature about Turkmen carpets with an interview.

## 1.1.7

- Quotes keep their own punctuation. Inside «...» only the quotation marks change, in any language, and the dash and connector rules do not apply there. In a translation the speaker's marks carry over one for one: a dash stays a dash. Found in two tests where a translation turned every dash inside a quote into a comma.
- Set formulas of the genre are not "corrected" by grammar: `berk jan saglyk` stays as it is in a list of wishes.
- Translations restore the Turkmen form of names and places spelled the Russian way (`Мурадов` → `Myradow`, `Эрк-Кала` → `Erkgala`, `Хаузханское водохранилище` → `Hanhowuz suw howdany`); a new table in `references/turkmen-tells.md` lists the common changes.
- When the source contradicts itself or names a well-known thing wrongly (`канал Мургаб` for the river Murgap), the skill writes the correct form and lists it under "to verify" with the source's wording.
- Added `basseýn` (a river basin) and `derýa`/`kanal` to the table of words that look interchangeable.
- A request with several parts is checked for every part before the answer goes out.
- `barla.py` now catches a plural after a number with several words in between (`9 sany uly baýramçylyk konsertleri`, `5 daşary ýurt media guramalary`), and stops at verbs, case forms, units and fixed compounds (`iki çagalar bagy`, `14 reportaž taýýarladylar`). It no longer counts dashes inside quotes, in ranges (`7:00–9:00`) or at the start of dialogue turns, no longer flags Roman numerals (`XIX`, `XX`) or brand names such as `YouTube`, and catches more forms of "I hope this helps" (`Umyt edýärin, bu ... size ýarar`).
- Added two corpus cases: a long Turkmen annual report and a long Russian article translated into Turkmen.

## 1.1.6

- Added a table of words that look interchangeable but are not, starting with `howuz` (a built basin: `ýüzüş howzy`) and `howdan` (a reservoir in the open), confirmed by a native speaker after a translation test produced `ýüzüş howdany` for a pool in a sports complex.
- When the skill translates or picks between two close words it is not sure about, it now lists the choice under "to verify" with the alternative.
- Added a seventh corpus case: a Russian press release translated into Turkmen.

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
