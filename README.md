# humanizer21

A Turkmen language humanizer for AI assistants.

Language models write Turkmen badly in two ways at once. They carry over the usual chatbot habits ("Elbetde!", "Şuny bellemek gerek", a summary paragraph nobody asked for), and they slip in Turkish words, Russian sentence patterns and spelling mistakes that any Turkmen reader spots in the first line. humanizer21 fixes both. It turns machine-sounding Turkmen into text a careful native editor would sign off on, and it can write or translate into Turkmen from scratch with the same rules.

Turkmen is the main language. The skill also removes AI patterns from Russian, English and Turkish text, and you can talk to it in any of those four languages.

## What it fixes

- Chatbot leftovers: greetings, praise of the question, "I hope this helps", offers of more help.
- Filler and staging: announcing a point instead of making it, empty "not only X but Y" contrasts, deep-sounding sayings, answers to objections nobody raised, inflated significance, summary paragraphs, connector chains. There are 23 numbered patterns in all, strongest first.
- Formatting by reflex: bold labels, emoji, decorative headings, dashes in every sentence.
- Turkish interference: `için`, `önemli`, `daha`, `ve`, the letters `ı`, `ğ`, `c`, `v`, Turkish verb forms like `geliyor` or `gelebilir`.
- Russian calques: `möhüm rol oýnaýar`, `-yň çäklerinde`, `bolup durýar` in every sentence.
- Spelling: `y` written for `ý`, missing `ä` and `ň`, vowel harmony in suffixes, consonant changes (`kitaby`, `agajy`), ordinals (`2026-njy`, `2025-nji`), a plural after a number.
- Punctuation: «» quotation marks, commas with `emma`, `ýöne`, `sebäbi`, the rules for direct speech and dialogue, dashes used everywhere.

Before it answers, it audits its own draft: every sentence must trace back to the source, and every fact of the source must still be there. A rewrite never gains a sentence of encouragement or a call to action that the original did not have.

It keeps what belongs to the genre. A Turkmen news item keeps its official titles and set formulas; a letter keeps `Hormatly ...` and `Hormat bilen`. Facts, names, numbers and dates are never changed, added or dropped.

## Example

Input, as a chatbot wrote it:

> Elbetde! Size bu barada habar ýazyp bereýin.
>
> Şuny bellemek gerek, Aşgabatda täze mekdep açyldy — bu diňe bir bina däl, eýsem geljege ýol açýan möhüm ädim. Mekdep 960 okuwçy için niyetlenen we ähli synp otaglary häzirki zaman kompýuterlar bilen enjamlaşdyrylan.

After humanizer21:

> Aşgabatda täze mekdep açyldy. Ol 960 okuwçy üçin niýetlenen. Synp otaglarynyň hemmesi häzirki zaman kompýuterleri bilen enjamlaşdyryldy.

What changed: the chatbot opening is gone, and so are "it should be noted" and the "not just a building but a step towards the future" line. `için` (Turkish) became `üçin`, `niyetlenen` became `niýetlenen`, and `kompýuterlar` became `kompýuterler` because the stem has a front vowel.

More worked examples, including a letter, a social post and a translation from Russian, are in [references/examples.md](references/examples.md).

## Install

### Claude Code

As a plugin (Claude Code 2.1.275 or later):

```
/plugin install humanizer21 --marketplace novgar21/humanizer21
```

On older versions, add the marketplace first:

```
/plugin marketplace add novgar21/humanizer21
/plugin install humanizer21@humanizer21
```

Or as a plain skill, without the plugin system:

```bash
npx github:novgar21/humanizer21
```

This copies the skill to `~/.claude/skills/humanizer21`, so it works in every project. Options:

```bash
npx github:novgar21/humanizer21 --project       # only this project: ./.claude/skills
npx github:novgar21/humanizer21 --dir <path>    # any other skills folder
npx github:novgar21/humanizer21 --uninstall     # remove it again
```

Once the package is published on npm, `npx humanizer21` works the same way.

### claude.ai

```bash
npx github:novgar21/humanizer21 --zip
```

Then upload `humanizer21.zip` in **Settings > Capabilities > Skills > Upload skill**. Skills need a Pro, Max, Team or Enterprise plan with code execution turned on. You can also download `humanizer21.zip` from the [latest release](https://github.com/novgar21/humanizer21/releases/latest) instead of running npx. Use that file rather than GitHub's "Download ZIP" button: claude.ai needs the folder inside the zip to be named `humanizer21`.

On a Mac, Safari unpacks downloaded zips by default. If you end up with a `humanizer21` folder, right-click it and choose **Compress**, or download with another browser.

### ChatGPT, Grok, Gemini, DeepSeek and others

These assistants do not load skill folders, so humanizer21 ships a single prompt file that holds the core rules:

```bash
npx github:novgar21/humanizer21 --prompt
```

This saves `humanizer21-prompt.md` (about 7,000 characters, within ChatGPT's 8,000-character limit for instructions). Then:

- **ChatGPT:** create a custom GPT or a project, paste the file into its instructions, and upload the files from `references/` as knowledge.
- **Grok:** paste it into custom instructions or a project's instructions, and attach the `references/` files to the project.
- **Gemini:** create a Gem, paste the prompt as its instructions, and add the `references/` files.
- **Anything else:** paste the prompt at the start of the chat.

The prompt alone covers the most common problems. The reference files make a noticeable difference for grammar, so attach them where the assistant allows it.

### Manual install

Copy `SKILL.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `references/` and `scripts/` into a folder named `humanizer21` inside your agent's skills directory. This works for any agent that reads `SKILL.md` files, such as Codex or Cursor; the repository also carries their manifests (`agents/openai.yaml`, `.cursor-plugin/plugin.json`).

## Usage

Just ask in your own language. The skill answers in the language you write in and keeps the edited text in its own language.

Turkmen:

```
Şu habary adam eli bilen ýazylan ýaly et, emeli aň yzlaryny aýyr: ...
Teksti barla, diňe ýalňyşlary görkez, täzeden gaýtalap ýazma: ...
Müdirden rugsat almak üçin hat ýaz, 3-nji noýabrdan 7-nji noýabra çenli.
```

Russian:

```
Сделай этот туркменский текст человечным и грамотным: ...
Переведи на туркменский для поста в Instagram: ...
```

English:

```
Proofread this Turkmen press release and remove anything that sounds AI-written: ...
Write a short Turkmen announcement about the library's new opening hours.
```

Turkish:

```
Bu Türkmence metni düzelt ve yapay zekâ izlerini temizle: ...
Bu Türkçe metni daha doğal hale getir: ...
```

Modes:

- **Edit or write** (default): you get the final text and a short list of the main changes.
- **Check only**: ask it not to rewrite, and you get a list of problems with their location and a fix for each.
- **Show your work**: ask how it got there, and you get the draft, the tells that survived it, and the final text.
- **Inside another task**: when the assistant is already writing a post or a document for you in Turkmen, the skill runs quietly and you only see the result.

### Write in your own voice

Paste two or three paragraphs you wrote yourself, or a few earlier articles from your outlet, together with the text to edit:

```
Meniň ýazgymyň nusgasy: [2-3 abzas]

Şu teksti meniň stilimde ýaz: [tekst]
```

humanizer21 matches the sample's sentence length, word choice, set formulas and punctuation. If your sample uses emoji or dashes, it keeps them at the same rate; otherwise it removes emoji in every genre, social posts included.

## The checker

`scripts/barla.py` is a small command-line checker for Turkmen text. It needs Python 3.8 or newer and nothing else.

```bash
python3 scripts/barla.py text.txt
python3 scripts/barla.py text.txt --json
python3 scripts/barla.py text.txt --allow "Coca-Cola,Microsoft"
cat text.txt | python3 scripts/barla.py -
python3 scripts/barla.py text.txt --fix -o clean.txt
python3 scripts/barla.py result.txt --compare source.txt
python3 scripts/barla.py text.txt --dict
```

`--fix` removes characters a reader cannot see: zero-width spaces, soft hyphens, direction marks and Unicode tag characters, and turns non-breaking, thin and wide spaces into normal ones. Text pasted from chat windows, PDFs and web pages often carries them, and they break site search, line breaks and character counts. Letters, punctuation and line breaks stay as they are.

`--compare` checks a result against its source and lists what may have been lost: numbers, quotes that changed, names, table rows and list items. It works for translations too, where it compares numbers, the count of quotes, table rows and list items.

`--dict` also lists words that a Turkmen word list does not know, as notes. The list is the Hunspell dictionary of [turkmen-spell-check-dictionary](https://github.com/nazartm/turkmen-spell-check-dictionary) (Apache 2.0) plus our own additions in `scripts/sozluk/gosmaca.txt`. It catches slips such as `welaýatyda`, `agaçyň` or `kompýuterlar`, but it does not know every correct word: new terms, names and forms with several endings show up too. Treat a note as "check this word", not as an error. On the ten accepted results of the test corpus it leaves no notes.

Sample output:

```
words: 40 | errors: 1 | warnings: 3 | notes: 0
ERROR 1:5     [ordinal] «2025-njy» → 2025-nji  Ordinal suffix follows the spoken last word (bäş): write 2025-nji.
WARN  1:114   [plural-after-number] «talyplar»  A noun after a number stays singular (üç kitap, 40 talyp).
WARN  1:241   [turkish-word] «ve» → we  Looks like a Turkish word, not Turkmen.
```

It flags letters outside the Turkmen alphabet, Cyrillic letters hidden in Latin words, `y` written next to another vowel (`niyet`, `peydaly`), Turkish words, plural harmony, ordinals, a plural after a number, the `n`/`ň` genitive slip, stock AI phrases, overused connectors, quotation marks, dashes, spacing and invisible Unicode characters. It points at problems; deciding what to change is still the editor's job, because a foreign brand may keep its `c` and an official formula may keep its contrast.

## What is inside

```
SKILL.md                         workflow the assistant follows
references/ai-patterns.md        23 AI writing patterns, with Turkmen examples
references/turkmen-tells.md      Turkish and Russian interference, machine phrases
references/orthography.md        alphabet, ý/y, vowel harmony, consonant changes, capitals
references/morphology.md         suffixes, cases, verb forms, numbers, postpositions
references/punctuation-lexicon.md  punctuation, quotes, dialogue, loanwords, register
references/styles.md             news, letters, documents, social posts, chat
references/examples.md           before and after
scripts/barla.py                 the checker
scripts/sozluk/                  Turkmen word list for barla.py --dict (Apache 2.0) and our additions
prompts/system-prompt.md         one-file version for other assistants
bin/install.js                   the npx installer
scripts/validate-package.py      package check: versions, manifests, pattern numbers, sizes
tests/                           tests for the checker, the installer and the corpus
tests/corpus/                    ten test texts with expected results
tests/grade.py                   grades a result against a corpus case
.claude-plugin/                  Claude Code plugin and marketplace manifests
CHANGELOG.md                     what changed in each version
AGENTS.md                        rules for contributors and coding agents
THIRD_PARTY_NOTICES.md           credits and licenses of the work this builds on
```

Run `npm test` and `python3 scripts/validate-package.py` before a pull request. GitHub runs both on every push.

### Test corpus

`tests/corpus/` holds ten machine-written texts: Turkmen news items, social posts, a website article, a memo, a long annual report and a long feature with an interview, and two Russian articles to translate into Turkmen. Each case has the input, the request, a list of facts that must survive and of tells and errors that must disappear, and an accepted result. To check how the skill did on a case, save its answer to a file and run:

```bash
python3 tests/grade.py tests/corpus/olimpiada-habary answer.txt
```

Every line of the output is a check; the last line is the score. A new tell or a new mistake belongs in the corpus as a new case.

## Sources

The grammar rules are summarized in our own words from [Ene dilim](https://enedilim.com/), the reference site for Turkmen spelling and grammar, and are used with the permission of the Ene dilim project. Many thanks to its authors. For a disputed spelling, the Ene dilim orthographic dictionary is the authority, and the skill checks words there when the assistant can browse.

The general AI writing patterns, the draft-audit-final workflow and voice matching are adapted from [Humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT), which in turn builds on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). humanizer21 rewrites them for Turkmen and adds the Turkmen rules. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Limitations

- It makes text read better to a Turkmen reader. It does not promise to pass "AI detectors", which are unreliable for Turkmen anyway.
- The assistant behind it still knows less Turkmen than Turkish or Russian. Important texts deserve a read by a native editor.
- Some rules come from standard press usage rather than from Ene dilim; the reference files mark them.

## Contributing

Corrections from native speakers are the most valuable contribution: a wrong rule, a missing Turkish false friend, a phrase that machines overuse. Open an [issue](https://github.com/novgar21/humanizer21/issues/new/choose); there are forms for a bad rewrite, a new tell and a wrong Turkmen rule. For a pull request, read [AGENTS.md](AGENTS.md) first.

## License

MIT © 2026 Novruz Garryyev
