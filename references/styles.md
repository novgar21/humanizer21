# Registers: what "human" means in each kind of Turkmen text

A human-sounding news item and a human-sounding chat message have almost nothing in common. Decide the register first, then decide what counts as a tell.

Contents: 1 news · 2 official and business letters · 3 documents (orders, reports, regulations) · 4 social posts · 5 messages and chat · 6 essays, blogs, literary text · 7 Russian and English text

---

## 1. News (state and public media)

Turkmen news follows a fixed genre. A Turkmen reader expects its formulas; removing them makes the text look foreign, not human.

**Keep:**

- full official titles at first mention, exactly as the source gives them (`Türkmenistanyň Prezidenti Serdar Berdimuhamedow`), and the shorter accepted forms afterwards (`Döwlet Baştutanymyz`, `Prezident`)
- set formulas the source uses (`Hormatly Prezidentimiziň başlangyjy bilen`, `Garaşsyzlygymyzyň ... ýyllygy mynasybetli`), long enumerations of real participants, ministries and regions
- indirect speech with `-dygyny belledi`, `-dygyny nygtady`, `-jakdygyny habar berdi`
- the definite past `-dy/-di` as the base tense
- `diňe bir ... däl, eýsem ...` when the source uses it

**Remove or fix:**

- generic inflation the model added on its own that is not in the source (`täze sahypa açýar`, `ajaýyp mümkinçilik`, `geljegi nurly`)
- `Şuny bellemek gerek`, `Ýokarda agzalanlardan görnüşi ýaly`, summary paragraphs that repeat the lead
- the same verb of saying in every sentence: rotate `aýtdy`, `belledi`, `nygtady`, `habar berdi`, `beýan etdi`
- Turkish and Russian interference, as everywhere

**Structure:**

1. Lead: who, what, where, when, in one or two sentences.
2. Details: figures, places, participants.
3. Statements in indirect speech, or a short direct quote in «».
4. Background, if any.

**Headline:** short, no full stop, either a noun phrase (`Aşgabatda täze mekdep`) or a sentence ending in the verb (`Aşgabatda täze mekdep açyldy`).

**Never change** names, titles, figures, dates, the names of laws and programmes, or the order of officials. If the source has an error in one of these, point it out instead of fixing it silently.

## 2. Official and business letters

**Shape:**

```
Hormatly [name or position],

[Reason in one sentence.] [Request or information.] [Deadline, attachment or next step.]

Hormat bilen,
[Name]
[Position]
```

- `Siz` (capitalized in letters as a courtesy) throughout; never switch to `sen`.
- One request per paragraph. A letter of three short paragraphs is normal.
- The salutation and closing are not chatbot residue. Delete only additions such as `Umyt edýärin, siz meniň haýyşymy kanagatlandyrarsyňyz!` followed by `Başga soraglaryňyz bar bolsa...`.
- Formal verbs are fine (`haýyş edýärin`, `habar berýärin`, `iberýärin`), but not stacked: `haýyşymyň kanagatlandyrylmagyny haýyş edýärin` is padding.

## 3. Documents: orders, reports, regulations

- The genre wants passive and verbal nouns (`tassyklansyn`, `ýerine ýetirilmegine gözegçilik etmek`). Keep the genre forms.
- Remove what no document contains: rhetorical questions, `Geliň, ...`, emotional adjectives, a closing paragraph addressed to the reader.
- Numbering, dates (`2026-njy ýylyň 25-nji oktýabryndaky`), and the names of bodies must follow the orthography rules exactly.

## 4. Social posts

- Short sentences, concrete detail, one idea per post.
- A direct address to readers is natural (`Siz näme pikir edýärsiňiz?`) once, at the end.
- Emoji: zero to two, only if the account uses them. Never one per line.
- No headings, no bold labels with colons, no list of "tips" when two sentences would do.
- Choose `sen` or `siz` by the audience and keep it.
- Do not strip a post to a dry list of facts. Speaking to the reader is part of the genre: `Filmleri «Watan» kinoteatrynda görüp bilersiňiz` is a natural way to give the same fact. What you must not do is add claims or calls the source does not have (`gelmegi unutmaň!`, "the best festival of the year"). If a call to action would help, suggest it in your note instead of writing it into the post.
- Avoid the same noun in two neighbouring sentences; Turkmen links sentences with `ol`, `onda`, `oňa` or a synonym.

## 5. Messages and chat

- Colloquial forms are allowed and make the text sound real: `menem`, `senem`, `alamok`, `bilemok`, `gelýäs`.
- Very short is fine. No greeting paragraph, no summary, no offer of further help.
- Keep the user's own slang and spelling habits if they gave a sample, but fix outright errors only when asked.

## 6. Essays, blogs, literary text

- Keep the author's opinions, doubts, jokes and asides. Removing tells is half the work; the text still needs a person behind it.
- Vary sentence length on purpose.
- Dialogue follows the dash rules in `punctuation-lexicon.md`.
- In fiction, invented details are the point; do not "correct" them.

## 7. Russian, English and Turkish text

The structural patterns in `ai-patterns.md` apply in every language. For Russian, the typical chatbot markers are `Важно отметить`, `Давайте разберёмся`, `не просто ..., а ...`, `играет ключевую роль`, `в современном мире`, `Таким образом`, a long dash in every sentence, and `Надеюсь, это поможет`. Apply the same process; skip the Turkmen-specific checks.

For Turkish, typical chatbot markers are `Şunu belirtmek gerekir ki`, `Önemle vurgulamak gerekir`, `Günümüzde`, `Sonuç olarak`, `Özetle`, `sadece ... değil, aynı zamanda ...`, `önemli bir rol oynamaktadır`, `kritik öneme sahiptir`, long chains of `-mektedir/-maktadır` where a plain `-iyor` or past tense would do, `Harika bir soru!`, and `Umarım bu yardımcı olur`. Edit Turkish as Turkish: Turkish spelling and grammar are correct in a Turkish text.

For English, the full pattern list in `ai-patterns.md` applies as written (not just X but Y, delve, crucial, pivotal, tapestry, "I hope this helps").

