# AI writing patterns, with Turkmen examples

Adapted from [Humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT), rewritten for Turkmen. See `THIRD_PARTY_NOTICES.md`.

Every pattern here is the "safe default" a language model picks because it fits the widest range of readers. A person writes for one reader and one subject, so their choices are uneven and specific. That unevenness is what you are restoring.

Rules that run through the whole file:

- Every sentence you keep must give the reader something new, counting what came earlier in the text and in the conversation.
- Patterns are numbered strongest first. §1 to §5 and the leftovers in section E justify an edit on one sighting. A pattern marked *weak alone* needs other tells in the same passage before you act on it.
- Never add a fact, name, number, date, quote or claim that is not in the source. Removing a tell is never a reason to write a new sentence.

Contents: A staging (§1–§5) · B rhythm (§6–§10) · C inflation (§11–§16) · D formatting (§17–§19) · E leftovers (§20–§22) · F wrong reader (§23) · when not to act

---

## A. Staging instead of stating

The strongest and most frequent tells. The sentence signals importance instead of adding a fact.

### 1. Not X but Y

**Watch for:** `diňe bir X däl, eýsem Y`; `X däl-de, Y`; `bu jedel däl, bu hakykat`; the split form `Bu ... diýmek däl. Bu ... diýmek.`; a clipped negative tail (`..., hiç hili kynçylyksyz`).
**Problem:** the first half names something nobody claimed, so the second half sounds bigger without adding a claim. State the point. Keep the contrast when both halves carry information or the first half corrects a belief the reader really holds.
**Register:** in Turkmen official and news prose `diňe bir ... däl, eýsem ...` is a normal construction. Keep it in news unless it appears in nearly every paragraph; rewrite it elsewhere.

> Before: Bu programma diňe bir tekst ýazmak üçin däl, eýsem tablisa düzmek üçin hem ulanylýar.
>
> After: Bu programmada tekst hem ýazyp bolýar, tablisa hem düzüp bolýar.

### 2. One-line closers and summary paragraphs

**Watch for:** a final paragraph starting `Netijede`, `Jemläp aýtsak`, `Gysgaça aýtsak` that adds nothing; a one-line paragraph repeating the one before; a sentence after an example that names what it showed (`Bu bolsa ... aýdyň subutnamasydyr`, `Munuň özi uly mümkinçilik`); the same closer after several sections; one exclaimed word or fragment as a sentence (`Hakykatdanam!`, `Ajaýyp!`, `Ine, netije!`).
**Problem:** the line asks the reader to pause on a claim instead of adding to it. In a short text, end on the last concrete fact. Keep a closer only when it adds a fact or consequence.

> Before: Kitaphana sişenbe günleri hem işleýär. Bu bolsa okyjylar üçin uly mümkinçilik.
>
> After: Kitaphana sişenbe günleri hem işleýär.

### 3. Sayings that sound deep

**Watch for:** `Esasy mesele şunda`, `Hakykatda iň möhüm zat`, `Meseläniň düýbi`, `X — Y-iň açary`, `X — Y-iň dili`, `X tora öwrülýär`, aphorisms with a dash in the middle.
**Problem:** an ordinary point is dressed as a hidden truth. Replace the saying with the specific claim, or cut it if there is no claim under it. Rewording the saying (`endik bolsa saglygyň açary`) keeps the tell. A saying is not a fact, so cutting it does not break the rule against losing facts; mention the cut in your notes.

> Before: Esasy mesele tehnikada däl. Hakykatda, iň möhüm zat — adamlaryň oňa ynanmagy. Ynam — üstünligiň açary.
>
> After: Täze ulgamyň işlemegi üçin adamlaryň oňa ynanmagy gerek.

### 4. Staged run-up before the point

**Watch for:** `Şuny bellemek gerek`, `Aýratyn bellemeli zat`, `Geliň, ... seredeliň` (or `gürleşeliň`, `öwreneliň`, `düşüneliň`), `Ine, bilmeli zatlaryňyz`, `Indi ... geçeliň`, `Size bu haty ýazmagymyň sebäbi şundan ybarat`, a standalone `Açygyny aýtsam?`; a pause staged for the reader (`Bir pursat durup oýlanalyň`, `Indi bolsa iň gyzykly ýerine geçeliň`).
**Problem:** the writer announces the point instead of making it. Remove the run-up, not just its tone.

> Before: Şuny bellemek gerek, täze ýol 2027-nji ýylda ulanylmaga beriler.
>
> After: Täze ýol 2027-nji ýylda ulanylmaga beriler.

### 5. Arguing with no one

**Watch for:** `Bu ýerde gürrüň ... barada däl`, `Ýalňyş düşünilmesin`, `Käbirleri ... diýip pikir edip biler, ýöne ...`, `Ilkinji pikir ... bolup biler, emma ...`, `Elbetde, ... diýip bolmaz`.
**Problem:** the text answers an objection nobody raised, often a leftover from an earlier draft. Remove the defense; if it holds a real claim, state the claim. Softening it (`... diýip pikir edýänler hem bar. Emma ...`) keeps the tell.

> Before: Bu ýerde gürrüň diňe bahalar barada däl. Käbirleri täze tarifler gymmat diýip pikir edip biler, ýöne mesele başgada. Täze tarifler 1-nji ýanwardan güýje girýär.
>
> After: Täze tarifler 1-nji ýanwardan güýje girýär.

## B. Rhythm by rule

Shapes applied everywhere, whether or not the meaning asks for them.

### 6. Forced threes

**Problem:** ideas come in threes because three sounds complete: `ösüşi, abadançylygy we rowaçlygy`, `medeniýetiň, bilimiň we ruhy baýlygyň merkezi`. Check that each item adds a distinct idea. Keep three when the facts are three.
**Register:** official prose lists real participants, ministries and regions at length; keep those. Cut abstract triads in any register.

> Before: Festiwal medeniýeti, dostlugy we hyzmatdaşlygy berkitmäge gönükdirilendir.
>
> After: Festiwalyň maksady ýurtlaryň arasynda medeni gatnaşyklary ösdürmek.

### 7. Connector chains and repeated openings

**Problem:** almost every sentence starts with `Şeýle hem`, `Mundan başga`, `Bulardan başga`, `Bu bolsa`, `Şonuň üçin`, `Hususan-da`, or several sentences in a row start with the same subject. Keep a connector where it shows a real relation (cause, contrast, sequence); merge or reorder the rest.

> Before: Mekdepde sport zaly bar. Şeýle hem, ýüzüş howzy bar. Mundan başga, kitaphana hem bar.
>
> After: Mekdepde sport zaly, ýüzüş howzy we kitaphana bar.

### 8. Dashes as the universal connector

**Rule:** in the final text, use the long dash only for its Turkmen jobs: a noun predicate without `-dyr` (`Aşgabat – paýtagt`), dialogue, a dash before a generalizing word after a list, an omitted word, ranges, headlines. Replace every other dash with a comma, colon or full stop. If the user's voice sample uses dashes freely, keep its rate. *Weak alone:* one dash proves nothing; many do.

> Before: Işe pyýada gidiň — liftiň deregine basgançakdan peýdalanyň — agşamlar gezelenç ediň.
>
> After: Işe pyýada gidiň, liftiň deregine basgançakdan peýdalanyň, agşamlar gezelenç ediň.

### 9. Stacked qualifiers

**Watch for:** `belki`, `ähtimal`, `mümkin`, `käbir ýagdaýlarda`, `bolup biler`, `belli bir derejede` piled onto one claim.
**Problem:** repeated hedging makes every claim sound uncertain. Keep one qualifier when the source supports doubt; keep legal and safety notices. *Weak alone.*

> Before: Bu karar, belki, käbir ýagdaýlarda netijelere belli bir derejede täsir edip biler bolmagy mümkin.
>
> After: Bu karar netijelere täsir edip biler.

### 10. Uniform rhythm

**Problem:** every sentence of similar length, every paragraph three sentences. Merge two short sentences, split a long one, let a paragraph be one sentence. Do not overcorrect into telegram style either. *Weak alone.*

## C. Inflation and borrowed authority

The fact underneath is usually sound. Keep it and remove the dressing.

### 11. Overused words

**Watch for, in neutral text:** `möhüm` in every paragraph, `aýratyn`, `ajaýyp`, `täsin`, `ägirt uly`, `giň gerimli`, `nurly`, `gaýtalanmajak`, `deňsiz-taýsyz`, `misli görülmedik`, `ýokary derejeli`.
**Problem:** models use these far more than people do. In ceremonial news the source may use some as fixed formulas; keep the source's formulas and never add new ones.

### 12. Inflated significance

**Watch for:** `täze sahypa açýar`, `möhüm ädim`, `ýol açýar`, `aýratyn ähmiýete eýe`, `uly orun eýeleýär` (with nothing saying why), `geljegi nurly`, `täze belentliklere`, a final paragraph about the bright future.
**Problem:** an ordinary fact is said to mark a turning point. Keep the fact. If the source says what changed, say that instead.

> Before: Täze köpri şäheriň taryhynda täze sahypa açýan möhüm ädimdir.
>
> After: Şäherde täze köpri guruldy.

### 13. Sales language

**Watch for:** `ajaýyp mümkinçilik`, `iň gowy saýlaw`, `hökman görmeli`, `gözel tebigatyň gujagynda`, `baý medeni mirasy bilen tanalýan`.
**Problem:** the text reads like an advertisement. State what the thing is.

### 14. Vague connection

**Watch for:** `bilen bagly`, `bilen baglanyşykly`, `bilen gatnaşykly` where the source gives the actual relation.
**Problem:** the reader cannot tell whether the person founded, leads or merely attended. Name the relation the source gives. If the source does not say, keep the vague wording and ask the user in your notes what the relation is. Turning `bilen baglanyşykly` into a role (`eminler toparyndan`, `ýolbaşçysy`, `guramaçysy`) is inventing a fact, and in news it is the most dangerous kind: a wrong title next to a real name.

> Before (source says he leads it): Ol bu taslama bilen baglanyşykly.
>
> After: Ol bu taslamanyň ýolbaşçysy.

> Before (source gives no role): Mugallym Aýgül Orazowa olimpiadanyň eminler topary bilen baglanyşykly.
>
> Wrong: Eminler toparyndan mugallym Aýgül Orazowa ...
>
> Right: Olimpiada bilen baglanyşykly mugallym Aýgül Orazowa ... (note to the user: "the source does not say what her role was; tell me if she was a judge, an organizer or a coach")

### 15. Borrowed authority

**Watch for:** `Hünärmenleriň pikiriçe`, `Barlaglar görkezýär`, `Köp adamlar şeýle hasaplaýar`, `Alymlar tassyklaýar` with no one named.
**Problem:** an unnamed authority props up a claim. If the source names the expert or study, name them. Otherwise cut the attribution and either drop the claim or keep it only as plainly uncertain without borrowed weight, and tell the user in your notes that a named source would let it back in. Keeping `Hünärmenleriň pikiriçe` without a name keeps the tell.

> Before: Hünärmenleriň pikiriçe, taslama şäheriň ekologiýasyna oňyn täsir edip biler.
>
> After: (cut; note to the user: "the expert claim was removed; add it back as a quote if you can name the expert")

### 16. Bureaucratic padding

**Watch for:** `amala aşyrylmagy`, `ýerine ýetirilmegi`, `-ýandygyny bellemek bolar`, `durmuşa geçirilmegi maksadyna laýyklykda`, `bolup durýar` in every sentence.
**Problem:** verbal nouns and helper verbs stand where one plain verb would do. Prefer `bar`, `ýok`, `-dyr`, `edýär`, `açyldy`, `geçirildi`. Official documents keep the forms their genre requires; padding that says nothing goes in every register.

> Before: Taslamanyň durmuşa geçirilmegi maksadyna laýyklykda degişli işleriň amala aşyrylýandygyny bellemek gerek.
>
> After: Taslama boýunça işler dowam edýär.

## D. Formatting by rule

### 17. Bold labels, emoji, decorative headings

- Bold labels with colons on every item (`**Esasy pikir:** ...`): turn the list into sentences when the labels carry no information of their own.
- Headings on a text of three paragraphs, headings that capitalize every word, a horizontal rule between every section.
- Arrows in place of a verb (`Tejribe → netije`, `Okuw ➜ iş`): write the sentence. Keep an arrow only in a diagram or a table of changes.
- **Emoji: remove them by default, in every genre, including social posts.** Keep emoji only when the user asks for them or gives a voice sample that uses them, and then at the sample's rate. Never one emoji per line or per sentence.

### 18. A heading repeated in the first sentence

**Problem:** a heading is followed by a sentence that restates it before the real content. Remove the sentence.

> Before:
> ## Tarifler
> Tarifler möhüm.
> Täze tarifler üç topara bölünýär.
>
> After:
> ## Tarifler
> Täze tarifler üç topara bölünýär.

### 19. Quotation marks

`"..."` or `“...”` instead of `«...»`. Turkmen print and media use «». Many people type straight quotes too, so this is *weak alone* as an AI tell, but it is still a fix for publication.

## E. Leftovers from the chat and the draft

Remove these outright, on one sighting.

### 20. Chatbot residue

**Watch for:** `Elbetde!`, `Hökman!`, `Gowy sorag!`, `Ine, siziň üçin ...`, `Size kömek edip bilsem şat bolaryn`, `Umyt edýärin, bu size kömek eder`, `Başga soragyňyz bar bolsa, ýazyň`, `Islän wagtyňyz ýüz tutuň`, and the Russian, English and Turkish equivalents.
**Problem:** the most certain tell. Remove the wrapper and keep the content. A letter's real salutation and closing (`Hormatly ...`, `Hormat bilen`) are not residue.

> Before: Elbetde! Ine, gysgaça maglumat: Mary welaýatynda pagta ýygymy tamamlandy. Umyt edýärin, bu peýdaly bolar!
>
> After: Mary welaýatynda pagta ýygymy tamamlandy.

### 21. Knowledge-limit disclaimers and guesses

**Watch for:** `Elimdäki maglumatlara görä`, `Soňky täzelenmä çenli`, `Bu barada jikme-jik maglumat ýok, ýöne ähtimal ...`, `-dygy çaklanylýar` followed by a guess.
**Problem:** the model talks about its own knowledge, then fills the gap with a guess. State what the source does not show, or delete the sentence. Never keep the guess.

### 22. Writing about the document instead of its subject

**Watch for:** `Aşakdaky tablisada ... görkezilýär`, `Bu bölüm üç bölekden ybarat`, `Bu tekst ... esasynda taýýarlandy`, `Tassyklanmadyk maglumatlar bellendi`, a note on what an earlier version said.
**Problem:** the text describes itself. Keep a source credit the reader can follow and a caveat that changes what the reader should do; cut the rest. *Weak alone* when it is a single sentence.

## F. Writing for the wrong reader

### 23. Re-explaining what the reader knows

Act on this pattern when the text is a reply, a memo or a letter to someone who already knows the background.

**Watch for:** a short message that restates the problem, walks through the diagnosis and only reaches the request in the last line; `Siziň bilşiňiz ýaly, ...` followed by things the reader saw; reminding the reader of what they themselves said or decided (`Siz bu barada geçen ýygnakda hem aýtdyňyz`).
**Problem:** the reader already has the context, so rebuilding it buries the point. Lead with the request or decision; keep only the reasoning that would change whether the reader agrees. Moving the background below the request is not enough: cut what the reader already knows, and above all never tell a reader what they said themselves. Background the reader knows is not a fact the edit must keep.

> Before: Siziň bilşiňiz ýaly, duşenbe güni ýaýlymda ses kesildi. Men bu meseläni barladym: mikrofonyň kabeli könelipdir, ätiýaçlyk mikrofonymyz hem ýok. Şonuň üçin täze kabel satyn almaga rugsat bermegiňizi haýyş edýärin.
>
> After: Täze mikrofon kabelini satyn almaga rugsat bermegiňizi haýyş edýärin. Duşenbe güni ses köne kabel sebäpli kesildi, ätiýaçlyk mikrofonymyz hem ýok.

---

## When not to act

- Pair words with a hyphen are normal Turkmen, not a tell: `gije-gündiz`, `aýal-gyzlar`, `ýygy-ýygydan`, `ep-esli`. Keep them.
- In a file, change the prose only. Table cells, numbers, links, code and names of files stay as they are.

- Quotations, official names, titles of documents and laws, and fixed formulas of the genre stay as they are, even if they contain a tell.
- A specific, unusual detail, a real opinion, a doubt, a joke or an aside is the writer's voice. Keep it.
- Text written before late 2022 was not written by a chatbot. Edit it for grammar only, if asked.
- People who judge by feel do little better than chance, and human writing keeps absorbing AI habits. Several tells together are the evidence; one dash or one `Şeýle hem` is not.
