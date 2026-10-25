# Before and after

Worked examples. Each shows the input, what was wrong, and the result. The facts in "after" are only the facts in "before"; nothing is added.

---

## 1. News item written by a chatbot

**Before**

> Elbetde! Size bu barada habar ýazyp bereýin.
>
> Şuny bellemek gerek, Aşgabatda täze mekdep açyldy — bu diňe bir bina däl, eýsem geljege ýol açýan möhüm ädim. Mekdep 960 okuwçy için niyetlenen we ähli synp otaglary häzirki zaman kompýuterlar bilen enjamlaşdyrylan.
>
> Şeýle hem, mekdepde sport zaly — ýüzüş howzy — we kitaphana bar. Mundan başga, okuwçylar "sanly bilim" ulgamyndan peýdalanyp bilerler. Netijede, bu mekdep ýurdumyzyň bilim ulgamynda täze sahypa açýar we möhüm rol oýnar.
>
> Başga soragyňyz bar bolsa, ýazyň!

**What was wrong**

- chatbot opening and closing
- `Şuny bellemek gerek`, empty contrast, inflation (`ýol açýan möhüm ädim`, `täze sahypa açýar`), Russian calque `möhüm rol oýnar`
- Turkish `için`, `y` instead of `ý` in `niyetlenen`, harmony error `kompýuterlar`
- dashes used as commas, straight quotes, connector at the start of almost every sentence, a summary sentence that adds nothing

**After**

> Aşgabatda täze mekdep açyldy. Ol 960 okuwçy üçin niýetlenen. Synp otaglarynyň hemmesi häzirki zaman kompýuterleri bilen enjamlaşdyryldy.
>
> Mekdepde sport zaly, ýüzüş howzy we kitaphana bar. Okuwçylar «Sanly bilim» ulgamyndan peýdalanyp bilerler.

## 2. Request letter

**Before**

> Hormatly müdir! Size bu haty ýazmagymyň sebäbi şundan ybarat: men 3-nji noýabrdan 7-nji noýabra çenli bäş günlük dynç alyş üçin rugsat soramak isleýärin. Bu meniň üçin örän möhüm, sebäbi maşgala ýagdaýy sebäpli Mary şäherine gitmeli bolýaryn. Şeýle hem, meniň işlerimi bu aralykda Jeren Ataýewa ýerine ýetirer. Size öňünden çuňňur minnetdarlygymy bildirýärin we umyt edýärin, siz meniň haýyşymy kanagatlandyrarsyňyz! Başga soraglaryňyz bar bolsa, men elmydama taýýar.

**What was wrong**

- announced the reason for writing instead of giving it
- `Bu meniň üçin örän möhüm` adds pressure, not information
- `Şeýle hem` joins two unrelated facts
- chatbot closing (`Başga soraglaryňyz bar bolsa...`) inside a letter
- no letter closing

**After**

> Hormatly müdir,
>
> Maşgala ýagdaýy sebäpli Mary şäherine gitmeli bolýaryn. Şonuň üçin 3-nji noýabrdan 7-nji noýabra çenli bäş gün dynç almaga rugsat bermegiňizi haýyş edýärin. Bu günlerde meniň işlerimi Jeren Ataýewa ýerine ýetirer.
>
> Hormat bilen,
> [Ady, wezipesi]

## 3. Social post

**Before**

> Gowy sorag! Geliň, bu meselä seredeliň.
>
> **Esasy pikir:** Kitap okamak çok önemli, sebäbi ol pikirlenmegi ösdürýär. Hakykatdan hem, kitap okaýan adamlar daha köp bilýärler.
>
> **Netije:** Her gün azyndan 20 minut okaň. Bu siziň durumyňyzy gowulaşdyrar ✨
>
> Umyt edýärin, bu size kömek eder!

**What was wrong**

- chatbot wrapper at both ends, staged opener
- bold labels on a five-line post
- Turkish `çok önemli`, `daha`, `durum`
- `Hakykatdan hem,` as filler

**After**

> Kitap okamak pikirlenmegi ösdürýär, köp okaýan adam köp zady bilýär. Her gün azyndan 20 minut okap görüň.

## 4. Translation from Russian

**Source**

> В рамках реализации программы цифровизации в Ашхабаде был открыт новый центр обслуживания граждан, который играет важную роль в повышении качества государственных услуг.

**Word-for-word machine version**

> Sanlylaşdyryş maksatnamasyny durmuşa geçirmegiň çäklerinde Aşgabatda raýatlara hyzmat edýän täze merkez açyldy, ol döwlet hyzmatlarynyň hilini ýokarlandyrmakda möhüm rol oýnaýar.

**What was wrong**

- `durmuşa geçirmegiň çäklerinde` copies "в рамках реализации"
- `möhüm rol oýnaýar` copies "играет важную роль"
- the Russian relative clause (`..., ol ...`) kept as one long sentence

**After**

> Sanlylaşdyrmak maksatnamasy esasynda Aşgabatda raýatlara hyzmat edýän täze merkez açyldy. Onuň maksady döwlet hyzmatlarynyň hilini ýokarlandyrmak.

## 5. Only check, do not rewrite

When the user asks only for a check, return the problems, not a new text:

> 1:8 `için` → `üçin` (Turkish word)
> 1:15 `niyetlenen` → `niýetlenen` (ý before a vowel)
> 1:52 `kompýuterlar` → `kompýuterler` (front vowel e, so -ler)
> 2:3 `"sanly bilim"` → `«Sanly bilim»` (Turkmen quotation marks)
> 2:40 `möhüm rol oýnar` → Russian calque; for example `uly orun eýelär`
