# Turkmen-specific tells of machine text

What gives away machine-written Turkmen even after the generic AI habits are gone. Most of it comes from two sources: Turkish, which models know far better than Turkmen, and Russian or English sentences translated word by word.

Contents: 1 Turkish interference · 2 letter slips · 3 Russian and English calques · 4 word order · 5 grammar slips · 6 register mistakes · 7 machine Turkmen phrases

---

## 1. Turkish interference

A model that is unsure of a Turkmen word often reaches for the Turkish one. A Turkmen reader spots it at once.

**Letters.** `ı`, `ğ`, `İ`, `c`, `v` in a Turkmen word are always wrong (foreign names kept in original spelling aside): `kız → gyz`, `değil → däl`, `ve → we`, `cevap → jogap`.

**Words.** The most frequent ones:

| Turkish | Turkmen |
|---|---|
| ve, veya | we, ýa-da |
| ile, için, gibi | bilen, üçin, ýaly |
| ama, ancak, fakat | emma, ýöne |
| çok | köp; "very" = örän |
| daha | has, ýene |
| en (superlative) | iň |
| önemli, önem | möhüm, ähmiýet |
| şimdi | häzir |
| sadece | diňe |
| olarak | hökmünde, bolup |
| sonra, önce | soň, öň |
| şey | zat |
| durum | ýagdaý |
| sorun | mesele, kynçylyk |
| bilgi | maglumat |
| hizmet | hyzmat |
| ekonomi | ykdysadyýet |
| okul | mekdep |
| küçük, büyük | kiçi, uly |
| kullanmak, istemek, anlamak, konuşmak | ulanmak, islemek, düşünmek, gürleşmek |
| onun, benim, senin | onuň, meniň, seniň |

**Grammar.** Turkish forms that slip in:

- `-iyor` present: `geliyor → gelýär`
- `-mış` past: `gelmiş → gelipdir`
- `-ebilir`: `gelebilir → gelip biler`
- `-diğini`: `geldiğini → gelendigini`
- `mi` written separately: `geldi mi → geldimi`
- apostrophe before suffixes: `Aşgabat'ta → Aşgabatda`
- `-ta/-tan`, `-ti/-tı` after voiceless consonants: Turkmen always has `-da/-dan`, `-dy/-di`: `işte → işde`, `gitti → gitdi`
- `y` inserted before the dative: `obaya → oba`

The full table is in `morphology.md`, section 14.

## 2. Letter slips

- `y` for `ý`: `yurt, yaşamak, niyet, kompyuter, oktyabr` → `ýurt, ýaşamak, niýet, kompýuter, oktýabr`. A `y` directly before a vowel is almost always wrong.
- `e` for `ä` in front suffixes: `gelýer → gelýär`, `tizrek → tizräk`, `şäherdeki → şäherdäki`.
- `n` for `ň`: `Türkmenistanyn → Türkmenistanyň`, `menin → meniň`, `son → soň`.
- Wrong harmony in suffixes: `kompýuterlar → kompýuterler`, `kitaplerde → kitaplarda`.
- Missing consonant change: `kitapy → kitaby`, `agaçy → agajy`, `maksatyny → maksadyny`.
- Missing dropped vowel: `oguly → ogly`, `agyzy → agzy`.
- Cyrillic letters hidden inside Latin words (`а`, `е`, `о`, `р`, `с` look identical). `barla.py` finds them.

## 3. Russian and English calques

A sentence can be grammatical and still sound translated. These patterns are grammatical Turkmen on the surface but follow the Russian or English original:

| Calque | Origin | More natural |
|---|---|---|
| `möhüm rol oýnaýar` | играет важную роль / plays a key role | `uly orun eýeleýär`, `täsir edýär`, or say what it does |
| `-yň çäklerinde` | в рамках | `-yň esasynda`, `-a laýyklykda`, or a plain `-da` |
| `bolup durýar` in every sentence | является | `-dyr`, or no copula: `Aşgabat – paýtagt.` |
| `boýunça` for every "по" | по | a case ending, `barada`, `babatda`, `ugrunda` |
| `tarapyndan` passives everywhere | кем-то / by someone | active voice: `Ministrlik taslamany taýýarlady.` |
| `öz içine alýar` | включает в себя | `-dan ybarat`, `... bar`, `girýär` |
| `ýüzbe-ýüz bolmak` with abstract challenges in every paragraph | сталкиваться / to face | `kynçylyk döredi`, `... bilen işlemeli boldy` |
| `şuny bilmek möhümdir` | важно знать / it's important to know | state the fact |
| `Bu manyly` | it makes sense | `Bu düşnükli`, `Bu dogry` |
| `Ine näme üçin:` | вот почему: / here's why: | give the reason in the sentence |
| translated idioms (`buzy döwmek` for "break the ice") | English idioms | a Turkmen expression or plain words |

Chains of four or more genitives (`ýurdumyzyň ykdysadyýetiniň pudaklarynyň ösüşiniň ...`) also read as translated. Break them into two sentences or use a verb.

## 4. Word order

- The verb belongs at the end. `Ol geldi düýn.` → `Ol düýn geldi.`
- Long relative clauses in Russian or English word order (`adam, kim geldi, ...`) do not exist in Turkmen. Use a participle: `gelen adam`.
- `we ... we ... we` between verbs: use converbs: `Ol gelip oturdy-da, gürrüň berdi.`
- A heavy subject followed by a short predicate is fine in Turkmen; do not split it into English-style fragments.

## 5. Grammar slips

- Plural after a number: `üç kitaplar → üç kitap`, `10 müň adamlar → 10 müň adam`.
- Accusative on the subject of a passive verb: `12 sany kompýuteri oturdyldy → 12 sany kompýuter oturdyldy`, `karary kabul edildi → karar kabul edildi`. With a passive verb the thing acted on is the subject and stays in the base form; `-y/-i` there reads as "his/its computer" or as an object with no verb to take it. Check this whenever you turn a plural into a singular after a number.
- Missing `n` after the 3rd person possessive: `welaýatyda → welaýatynda`, `kararyy → kararyny`.
- Ordinals without the right suffix: `9-nji → 9-njy`, `6-nci → 6-njy`, `2025-njy → 2025-nji`.
- Question particle written apart: `bilýärsiň mi → bilýärsiňmi`.
- `sen` and `siz` mixed in one text. Pick one form of address and keep it.
- Mixed tenses in a news item: the default is the definite past `-dy/-di`; reported facts may use `-ypdyr`.

## 5a. Names and places translated from Russian

Russian spells Turkmen names by its own rules. In a translation, give them back their Turkmen form; do not transliterate letter by letter.

| Russian | Turkmen | What changes |
|---|---|---|
| `Мурадов`, `Чарыева`, `Ходжаев`, `Атаева` | `Myradow`, `Çaryýewa`, `Hojaýew`, `Ataýewa` | `у` after a back vowel is often `y`; `-ев` after a vowel is `-ýew`; `дж` is `j`; `в` is `w` |
| `Аннагельдыев`, `Гельдиев`, `Овезова` | `Annageldiýew`, `Geldiýew`, `Öwezowa` | Russian drops `ä`, `ö`, `ü`; restore them from the Turkmen name |
| `Эрк-Кала`, `Гонур-депе` | `Erkgala`, `Goňurdepe` | `кала` is `gala`; compound place names are one word |
| `Хаузханское водохранилище` | `Hanhowuz suw howdany` | the proper name keeps `howuz`; the reservoir itself is `suw howdany` |
| `Векильбазарский этрап`, `Байрамали` | `Wekilbazar etraby`, `Baýramaly` | drop the Russian adjective ending |
| `гурёш`, `хяким`, `дайханское объединение` | `göreş`, `häkim`, `daýhan birleşigi` | Turkmen words in Russian spelling |

If you are not sure of the Turkmen form of a name, keep your best form and list it under "to verify".

**Errors in the source.** A translation that repeats a factual slip of the source spreads it. If the source contradicts itself or names a well-known thing wrongly (`вдоль канала Мургаб` in a text that elsewhere calls the Murgap a river), write the correct form (`Murgap derýasynyň ugrunda`) and list it under "to verify" with the source's wording. If you cannot tell which version is right, keep the source's and list it.

## 6. Register mistakes

- Official verbs where nothing official happens: `amala aşyrdym` for "I did", `durmuşa geçirdik` for "we made". Use `etdim`, `etdik`.
- Ceremonial adjectives (`deňsiz-taýsyz`, `beýik`, `şanly`) added by the model to a neutral text that did not have them. Remove them. In a news item that already uses them as fixed formulas, keep the source's formulas and do not add new ones.
- Colloquial forms (`menem`, `alamok`, `gelýäs`) in an official document, or bookish chains in a friendly message.
- Poetic words (`mekan`, `gurt`, `görmegeý`) in neutral prose.

## 7. Machine Turkmen phrases

Phrases that chatbots produce in Turkmen far more often than people do. One is not proof; three in a paragraph are.

- openers: `Elbetde!`, `Gowy sorag!`, `Ine, siziň üçin ...`, `Geliň, ... seredeliň`, `Bu gün biz ... barada gürleşeris`
- signposts: `Şuny bellemek gerek`, `Aýratyn bellemeli zat`, `Ýokarda agzalanlardan görnüşi ýaly`, `Netijede`, `Jemläp aýtsak`, `Umuman aýdanyňda`
- inflation: `täze sahypa açýar`, `möhüm ädim`, `ýol açýar`, `ajaýyp mümkinçilik`, `aýratyn ähmiýete eýe`, `geljegi nurly`
- closers: `Umyt edýärin, bu size kömek eder`, `Başga soragyňyz bar bolsa, ýazyň`, `Size üstünlik arzuw edýärin!` (at the end of a non-letter)
- connectors at the start of almost every sentence: `Şeýle hem`, `Mundan başga`, `Bu bolsa`, `Şonuň üçin`, `Hususan-da`
