#!/usr/bin/env python3
"""
barla.py - Turkmen text checker for the humanizer21 skill.

Finds things a careful Turkmen editor would fix:
  * letters that do not exist in the Turkmen Latin alphabet (c, q, v, x, ı, ğ, İ)
  * Cyrillic letters mixed into Latin-script words
  * "y" written where "ý" is needed (y next to another vowel: niyet, peydaly)
  * Turkish words used instead of Turkmen ones
  * front/back vowel harmony errors in plural suffixes (-lar/-ler)
  * stock phrases that make Turkmen text sound machine-written
  * punctuation habits: straight or curly quotes instead of «», dashes,
    spaces before punctuation, invisible Unicode characters

It only points at problems. Fixing them is the editor's job, because many
findings depend on context (a foreign brand name, a quotation, a fixed
official formula).

Usage:
    python3 barla.py text.txt
    python3 barla.py text.txt --fix -o clean.txt   (remove invisible characters)
    python3 barla.py text.txt --json
    cat text.txt | python3 barla.py -
    python3 barla.py text.txt --allow "Coca-Cola,Microsoft"

No third-party packages are needed. Python 3.8+.
"""

import argparse
import json
import re
import sys
import unicodedata

BACK_VOWELS = set("aouy")
FRONT_VOWELS = set("eäiöü")
VOWELS = BACK_VOWELS | FRONT_VOWELS

WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)
SKIP_SPANS_RE = re.compile(
    r"https?://\S+|www\.\S+|\S+@\S+\.\S+|`[^`]*`", re.UNICODE
)

# Turkish word (or stem) -> Turkmen equivalent.
# "stem": True means any word starting with the key is matched.
TURKISH_WORDS = {
    "ve": ("we", False),
    "ile": ("bilen", False),
    "için": ("üçin", False),
    "gibi": ("ýaly", False),
    "değil": ("däl", False),
    "çok": ("köp / örän", False),
    "önemli": ("möhüm", False),
    "önem": ("ähmiýet", True),
    "şimdi": ("häzir", False),
    "sadece": ("diňe", False),
    "ancak": ("emma / ýöne", False),
    "daha": ("has / ýene", False),
    "ama": ("emma / ýöne", False),
    "veya": ("ýa-da", False),
    "olarak": ("hökmünde / bolup", False),
    "tarafından": ("tarapyndan", False),
    "hakkında": ("barada", False),
    "sonra": ("soň / soňra", False),
    "önce": ("öň / ozal", False),
    "şey": ("zat", False),
    "küçük": ("kiçi", False),
    "güzel": ("owadan / gözel", False),
    "bütün": ("bütin / ähli", False),
    "bilgi": ("maglumat", True),
    "durum": ("ýagdaý", True),
    "sorun": ("mesele / kynçylyk", True),
    "çözüm": ("çözgüt", True),
    "hizmet": ("hyzmat", True),
    "ekonomi": ("ykdysadyýet", True),
    "teknoloji": ("tehnologiýa", True),
    "şirket": ("kompaniýa / kärhana", True),
    "üniversite": ("uniwersitet", True),
    "müdür": ("müdir", True),
    "başkan": ("başlyk / prezident", True),
    "bakan": ("ministr", True),
    "proje": ("taslama / proýekt", True),
    "ilgili": ("degişli / bagly", False),
    "gerçek": ("hakyky", True),
    "okul": ("mekdep", True),
    "onun": ("onuň", False),
    "benim": ("meniň", False),
    "senin": ("seniň", False),
    "bizim": ("biziň", False),
    "sizin": ("siziň", False),
    "kullan": ("ulan-", True),
    "çalış": ("işle- / çalyş-", True),
    "konuş": ("gürleş-", True),
    "anla": ("düşün- / aňla-", True),
    "iste": ("isle-", True),
    "söyle": ("aýt-", True),
}

# Phrases that read as machine-written in Turkmen.
# Each entry: (regex, category, message, weak)
# weak=True means "only a problem when other tells are present".
AI_PHRASES = [
    (r"\bşuny bellemek (gerek|zerur|möhüm)", "filler",
     "'Şuny bellemek gerek' announces a point instead of making it. State the point.", False),
    (r"\bbellemek gerek(dir)?\b", "filler",
     "'bellemek gerek' is a signpost; usually cut it.", True),
    (r"\bgeliň,?(\s+\S+){0,4}?\s+\w+(?:alyň|eliň|lyň|liň)\b", "staged-opener",
     "'Geliň, ... seredeliň' is a chatbot run-up. Start with the fact.", False),
    (r"\b(gowy|ajaýyp|örän gowy) sorag", "chatbot-residue",
     "Chatbot praise of the question. Remove.", False),
    (r"\b(kömek edip bilsem|size kömek etmäge şat)", "chatbot-residue",
     "Chatbot offer of help. Remove.", False),
    (r"başga sorag(yňyz|laryňyz) (bar bolsa|ýüze çyksa)", "chatbot-residue",
     "Chatbot closing. Remove.", False),
    (r"\bumyt edýärin,?\s+bu (size )?(kömek|peýdaly)", "chatbot-residue",
     "'I hope this helps'. Remove.", False),
    (r"^\s*(elbetde|hökman)\s*[!.,]", "chatbot-residue",
     "Opening 'Elbetde!' is a chatbot wrapper.", False),
    (r"\b(netijede|jemläp aýtsak|gysgaça aýtsak|jemlemek bilen),?", "signpost",
     "Conclusion signpost. Fine once in a long text; in a short one, just end on the last fact.", True),
    (r"\bumuman aýdanyňda\b", "signpost",
     "'Umuman aýdanyňda' is filler.", True),
    (r"\býokarda agzalan(lar|y)dan görnüşi ýaly", "signpost",
     "'As seen from the above' repeats what the reader just read.", False),
    (r"\bdiňe bir\b[^.!?]{1,80}\bdäl\b[^.!?]{0,20}\beýsem\b", "not-x-but-y",
     "'diňe bir ... däl, eýsem ...' contrast. Normal in official news; elsewhere state the point directly.", True),
    (r"\bmöhüm rol(y)? oýna", "calque",
     "'rol oýnamak' is a Russian calque (играть роль). Try 'uly orun eýeleýär', 'täsir edýär', or say what it does.", False),
    (r"\btäze sahypa(ny)? açýar", "cliche",
     "'opens a new page' cliche. Say what changed.", True),
    (r"\bajaýyp mümkinçilik", "sales",
     "Sales language. State the fact.", True),
    (r"\b(deňsiz-taýsyz|gaýtalanmajak|misli görülmedik)", "inflation",
     "Inflated adjective. Acceptable in ceremonial news formulas; otherwise cut.", True),
    (r"\baýratyn ähmiýete eýe", "inflation",
     "'aýratyn ähmiýete eýe' inflates significance. Keep only if the text says why.", True),
    (r"\bmöhüm ädim\b", "inflation",
     "'möhüm ädim' (an important step) is vague. Say what it does.", True),
    (r"\b(hakykatdan hem|aslynda),", "filler",
     "Sentence-opening 'aslynda,' / 'hakykatdan hem,' is usually filler.", True),
]

# Connectors that models overuse; reported when density is high.
CONNECTORS = [
    "şeýle hem", "mundan başga", "bulardan başga", "bu bolsa",
    "şonuň üçin", "netijede", "ýagny", "hususan-da", "şunuň bilen birlikde",
]

INVISIBLE = {
    "\u200b": "zero-width space",
    "\u200c": "zero-width non-joiner",
    "\u200d": "zero-width joiner",
    "\u200e": "left-to-right mark",
    "\u200f": "right-to-left mark",
    "\u2060": "word joiner",
    "\ufeff": "byte order mark / zero-width no-break space",
    "\u00ad": "soft hyphen",
    "\u202f": "narrow no-break space",
    "\u2028": "line separator",
    "\u2029": "paragraph separator",
    "\u180e": "Mongolian vowel separator",
    "\u2061": "invisible function application",
    "\u2062": "invisible times",
    "\u2063": "invisible separator",
    "\u2064": "invisible plus",
    "\u202a": "left-to-right embedding",
    "\u202b": "right-to-left embedding",
    "\u202c": "pop directional formatting",
    "\u202d": "left-to-right override",
    "\u202e": "right-to-left override",
    "\u2066": "left-to-right isolate",
    "\u2067": "right-to-left isolate",
    "\u2068": "first strong isolate",
    "\u2069": "pop directional isolate",
}
# Unicode tag characters (U+E0000 to U+E007F) are invisible and can carry hidden text.
TAG_RE = re.compile("[\U000e0000-\U000e007f]")
# Spaces that look normal but are not U+0020.
ODD_SPACES_RE = re.compile("[\u00a0\u2000-\u200a\u202f\u205f\u3000]")


def clean_text(text):
    """Remove invisible characters and replace unusual spaces with normal ones.

    Returns the cleaned text and a dict of counts. Only characters a reader
    cannot see are touched; letters, punctuation and line breaks stay as they are.
    """
    counts = {"invisible": 0, "tag": 0, "spaces": 0}
    out = []
    for ch in text:
        if ch in ("\u2028", "\u2029"):
            out.append("\n")
            counts["invisible"] += 1
        elif ch == "\u202f":
            out.append(" ")
            counts["spaces"] += 1
        elif ch in INVISIBLE:
            counts["invisible"] += 1
        elif TAG_RE.match(ch):
            counts["tag"] += 1
        elif ODD_SPACES_RE.match(ch):
            out.append(" ")
            counts["spaces"] += 1
        else:
            out.append(ch)
    return "".join(out), counts

PLURAL_TAILS = [
    "", "y", "i", "a", "e", "da", "de", "dan", "den", "dyr", "dir",
    "yň", "iň", "ymyz", "imiz", "yňyz", "iňiz",
    "yny", "ini", "yna", "ine", "ynda", "inde", "yndan", "inden",
    "ynyň", "iniň", "ydyr", "idir",
]


def norm_lower(s):
    # Python lowercases "İ" to "i" + combining dot; handle it first.
    return s.replace("İ", "i").lower()


def masked_text(text):
    """Replace URLs, e-mails and inline code with spaces so they are not checked."""
    return SKIP_SPANS_RE.sub(lambda m: " " * len(m.group(0)), text)


def pos_to_linecol(text, pos):
    line = text.count("\n", 0, pos) + 1
    col = pos - (text.rfind("\n", 0, pos) + 1) + 1
    return line, col


def add(findings, text, pos, sev, cat, msg, snippet, fix=None):
    line, col = pos_to_linecol(text, pos)
    item = {"line": line, "col": col, "severity": sev, "category": cat,
            "text": snippet, "message": msg}
    if fix:
        item["suggestion"] = fix
    findings.append(item)


def last_vowel(s):
    for ch in reversed(s):
        if ch in VOWELS:
            return ch
    return None


def check_words(text, masked, allow, findings):
    for m in WORD_RE.finditer(masked):
        word = m.group(0)
        if word.lower() in allow:
            continue
        pos = m.start()
        low = norm_lower(word)
        is_cap = word[0].isupper()

        # Cyrillic mixed with Latin
        has_cyr = any("CYRILLIC" in unicodedata.name(ch, "") for ch in word)
        has_lat = any("LATIN" in unicodedata.name(ch, "") for ch in word)
        if has_cyr and has_lat:
            add(findings, text, pos, "error", "mixed-script",
                "Word mixes Cyrillic and Latin letters (often invisible to the eye).", word)
            continue
        if has_cyr:
            continue  # a Cyrillic word: not checked by Latin rules

        # Letters outside the Turkmen alphabet
        if "İ" in word or "ı" in word or "ğ" in low:
            add(findings, text, pos, "error", "turkish-letter",
                "Turkish letter (ı, İ or ğ). Turkmen uses y / i / g.", word)
        else:
            foreign = sorted(set(ch for ch in low if ch in "cqvx"))
            if foreign:
                add(findings, text, pos, "info" if is_cap else "warn", "foreign-letter",
                    "Letter(s) %s are not in the Turkmen alphabet (c→ç/s, v→w, x→ks/h, q→k). "
                    "Fine only in a foreign name kept in its original spelling." % ", ".join(foreign),
                    word)

        # y next to another vowel -> almost always ý. "y" is itself a vowel, and
        # Turkmen does not put two vowels side by side: niyet -> niýet,
        # peydaly -> peýdaly, bay -> baý.
        ym = (re.search(r"y(?=[aeäioöuü])", low)
              or re.search(r"(?<=[aeäioöuü])y(?=[^aeäioöuüyý]|$)", low))
        if ym:
            add(findings, text, pos + ym.start(), "info" if is_cap else "warn", "y-vs-ý",
                "'y' next to another vowel: Turkmen writes ý here (ýa, ýe, ýo, peýda, baý).", word,
                word[:ym.start()] + ("Ý" if word[ym.start()] == "Y" else "ý") + word[ym.start() + 1:])

        # Turkish vocabulary
        for tr, (tk, is_stem) in TURKISH_WORDS.items():
            if (is_stem and low.startswith(tr) and len(low) >= len(tr)) or low == tr:
                add(findings, text, pos, "warn", "turkish-word",
                    "Looks like a Turkish word, not Turkmen.", word, tk)
                break

        # Genitive written with n instead of ň (e.g. Türkmenistanyn)
        if len(low) > 5 and re.search(r"(nyn|nin)$", low):
            add(findings, text, pos, "info", "n-vs-ň",
                "Genitive ending is written -nyň/-niň (with ň). Check this word.", word,
                word[:-1] + "ň")

        # Vowel harmony in the plural suffix
        for sfx in ("lar", "ler"):
            for tail in PLURAL_TAILS:
                ending = sfx + tail
                if low.endswith(ending) and len(low) > len(ending) + 1:
                    stem = low[: -len(ending)]
                    v = last_vowel(stem)
                    if v is None:
                        continue
                    if sfx == "lar" and v in FRONT_VOWELS:
                        add(findings, text, pos, "warn", "harmony",
                            "Stem ends in a front vowel (%s), so the plural is -ler, not -lar." % v,
                            word)
                    elif sfx == "ler" and v in BACK_VOWELS:
                        add(findings, text, pos, "warn", "harmony",
                            "Stem ends in a back vowel (%s), so the plural is -lar, not -ler." % v,
                            word)
                    break
            else:
                continue
            break


# Spoken form of the last word of a number, for ordinal suffixes (2026-njy, 2025-nji).
UNIT_WORDS = {1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "bäş", 6: "alty", 7: "ýedi", 8: "sekiz", 9: "dokuz"}
TEN_WORDS = {1: "on", 2: "ýigrimi", 3: "otuz", 4: "kyrk", 5: "elli", 6: "altmyş", 7: "ýetmiş", 8: "segsen", 9: "togsan"}
NUMBER_WORDS = set(UNIT_WORDS.values()) | set(TEN_WORDS.values()) | {"ýüz", "müň", "million", "milliard"}
PLURAL_OK_AFTER_NUMBER = {"dollar", "dollary", "dollara", "dollarda", "dollardan"}
# Words that may stand between a number and its noun (12 sany täze kompýuter).
BETWEEN_NUMBER_AND_NOUN = {
    "sany", "täze", "köne", "uly", "kiçi", "häzirki", "zaman", "gowy", "ýaş", "ak", "gara",
    "gyzyl", "ýaşyl", "gök", "sary", "beýik", "giň", "uzyn", "gysga", "agyr", "ýeňil",
    "ýokary", "pes", "daşary", "ýerli", "halkara", "tejribeli", "ökde", "hünärli", "zehinli",
    "owadan", "arassa", "hususy", "umumy", "esasy", "goşmaça", "ätiýaçlyk", "elektron", "sanly",
}


def last_number_word(n):
    if n == 0:
        return None
    if n % 10:
        return UNIT_WORDS[n % 10]
    if n % 100:
        return TEN_WORDS[(n // 10) % 10]
    if n % 1000:
        return "ýüz"
    if n % 1000000:
        return "müň"
    return "million"


def check_numbers(text, masked, findings):
    # Ordinals written with digits
    for m in re.finditer(r"\b(\d+)-(n[cj][yiı]|ynjy|inji|unjy|ünji|nci|ncı|njy|nji)\b", masked):
        word = last_number_word(int(m.group(1)))
        if not word:
            continue
        v = last_vowel(word)
        right = "njy" if v in BACK_VOWELS else "nji"
        if m.group(2) != right:
            add(findings, text, m.start(), "error", "ordinal",
                "Ordinal suffix follows the spoken last word (%s): write %s-%s." % (word, m.group(1), right),
                m.group(0), "%s-%s" % (m.group(1), right))
    # Plural noun right after a cardinal number (üç kitaplar -> üç kitap)
    num = r"(?:\d[\d\s.,]*|%s)" % "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
    between = r"(?:(?:%s)\s+){0,3}" % "|".join(sorted(BETWEEN_NUMBER_AND_NOUN, key=len, reverse=True))
    for m in re.finditer(r"(?<![\w-])" + num + r"\s+(?:(?:müň|million|milliard)\s+)?" + between + r"([^\W\d_]+)",
                         masked, re.IGNORECASE):
        noun = m.group(1)
        low = norm_lower(noun)
        if low in PLURAL_OK_AFTER_NUMBER or low in NUMBER_WORDS:
            continue
        # "bir" is also an article or part of a phrase: diňe bir, her bir, hiç bir, ýene bir.
        before = norm_lower(masked[max(0, m.start() - 12):m.start()])
        if norm_lower(m.group(0)).startswith("bir") and re.search(r"(diňe|her|hiç|ýene|haýsy)\s+$", before):
            continue
        if re.search(r"(lar|ler)(y|i|a|e|da|de|dan|den|yň|iň|y?n?y?)?$", low) and len(low) > 4:
            stem = re.sub(r"(lar|ler).*$", "", low)
            if last_vowel(stem):
                add(findings, text, m.start(1), "warn", "plural-after-number",
                    "A noun after a number stays singular (üç kitap, 40 talyp).", noun)


def check_phrases(text, findings):
    low = norm_lower(text)
    # Words inside «...» belong to someone else; never flag them as AI phrases.
    taken = [(m.start(), m.end()) for m in re.finditer(r"«[^»]*»", text)]
    for pattern, cat, msg, weak in sorted(AI_PHRASES, key=lambda e: e[3]):
        for m in re.finditer(pattern, low, re.MULTILINE):
            if any(m.start() < e and m.end() > b for b, e in taken):
                continue
            taken.append((m.start(), m.end()))
            add(findings, text, m.start(), "info" if weak else "warn", cat, msg,
                text[m.start():m.end()])


def check_connectors(text, findings, word_count):
    low = norm_lower(text)
    total = 0
    used = {}
    for c in CONNECTORS:
        n = len(re.findall(r"\b" + re.escape(c) + r"\b", low))
        if n:
            used[c] = n
            total += n
    if word_count and total >= 3 and total / word_count > 0.02:
        add(findings, text, 0, "warn", "connectors",
            "Many linking phrases (%d in %d words): %s. Models chain sentences with them; "
            "people let most sentences follow on without one." %
            (total, word_count, ", ".join("%s×%d" % kv for kv in used.items())), "")


def check_punctuation(text, findings, word_count):
    for ch, name in INVISIBLE.items():
        for m in re.finditer(re.escape(ch), text):
            add(findings, text, m.start(), "error", "invisible-char",
                "Invisible character: %s (U+%04X). Delete it." % (name, ord(ch)), repr(ch))

    tags = TAG_RE.findall(text)
    if tags:
        add(findings, text, TAG_RE.search(text).start(), "error", "invisible-char",
            "%d Unicode tag character(s): invisible, and able to carry hidden text. Run with --fix." % len(tags), "")

    odd = [m for m in ODD_SPACES_RE.finditer(text) if m.group(0) != "\u202f"]
    if odd:
        add(findings, text, odd[0].start(), "info", "invisible-char",
            "%d unusual space(s) (non-breaking, thin, wide...). Usually harmless; --fix turns them into normal spaces." % len(odd),
            "")

    for m in re.finditer(r"[“”„]|(?<![\w])\"|\"(?![\w])", text):
        add(findings, text, m.start(), "warn", "quotes",
            "Turkmen uses «...» quotation marks, not \"...\" or “...”.", text[m.start()])
        break  # one report is enough; the editor fixes all of them

    dashes = len(re.findall("[\u2014\u2013]", text))
    if word_count and ((dashes >= 3 and dashes / word_count > 0.015)
                       or (dashes >= 2 and dashes / word_count > 0.03)):
        add(findings, text, text.find("\u2014") if "\u2014" in text else text.find("\u2013"),
            "warn", "dashes",
            "%d long dashes in %d words. Turkmen uses the dash for specific jobs (dialogue, "
            "subject-predicate, apposition); elsewhere a comma, colon or full stop reads more naturally." %
            (dashes, word_count), "")

    for m in re.finditer(r"[^\S\n]+[,.;:!?](?!\S*://)", text):
        add(findings, text, m.start(), "warn", "spacing",
            "Space before a punctuation mark.", text[m.start():m.end()].strip())

    for m in re.finditer(r"(?<=\S)  +(?=\S)", text):
        add(findings, text, m.start(), "info", "spacing", "Double space.", "")
        break

    if re.search(r"\*\*[^*\n]{1,40}:\*\*", text):
        m = re.search(r"\*\*[^*\n]{1,40}:\*\*", text)
        add(findings, text, m.start(), "info", "formatting",
            "Bold labels with colons ('**Title:**') are a chatbot formatting habit.", m.group(0))

    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text)
    if emoji:
        add(findings, text, text.find(emoji[0]), "info", "formatting",
            "%d emoji found. Remove unless the genre (social post) calls for them." % len(emoji), "")


def run(text, allow=()):
    allow = {a.strip().lower() for a in allow if a.strip()}
    findings = []
    masked = masked_text(text)
    word_count = len(WORD_RE.findall(masked))
    check_words(text, masked, allow, findings)
    check_numbers(text, masked, findings)
    check_phrases(text, findings)
    check_connectors(text, findings, word_count)
    check_punctuation(text, findings, word_count)
    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (f["line"], f["col"], order[f["severity"]]))
    summary = {s: sum(1 for f in findings if f["severity"] == s) for s in order}
    summary["words"] = word_count
    return {"summary": summary, "findings": findings}


def print_report(result, out=sys.stdout):
    s = result["summary"]
    out.write("words: %d | errors: %d | warnings: %d | notes: %d\n"
              % (s["words"], s["error"], s["warn"], s["info"]))
    if not result["findings"]:
        out.write("No problems found by the automatic check. Still read the text yourself.\n")
        return
    for f in result["findings"]:
        tag = {"error": "ERROR", "warn": "WARN ", "info": "note "}[f["severity"]]
        loc = "%d:%d" % (f["line"], f["col"])
        snippet = (" «%s»" % f["text"]) if f["text"] else ""
        sug = (" → %s" % f["suggestion"]) if f.get("suggestion") else ""
        out.write("%s %-7s [%s]%s%s  %s\n" % (tag, loc, f["category"], snippet, sug, f["message"]))


def main(argv=None):
    p = argparse.ArgumentParser(description="Check Turkmen text for spelling slips and AI tells.")
    p.add_argument("file", help="text file to check, or - for standard input")
    p.add_argument("--json", action="store_true", help="print the result as JSON")
    p.add_argument("--allow", default="", help="comma-separated words to skip (names, brands)")
    p.add_argument("--strict", action="store_true", help="exit with code 1 if any error is found")
    p.add_argument("--fix", action="store_true",
                   help="remove invisible characters and unusual spaces; write the cleaned text to -o or standard output")
    p.add_argument("-o", "--output", help="file for the cleaned text (with --fix)")
    a = p.parse_args(argv)

    if a.file == "-":
        text = sys.stdin.read()
    else:
        with open(a.file, encoding="utf-8") as fh:
            text = fh.read()

    report_out = sys.stdout
    if a.fix:
        text, counts = clean_text(text)
        if a.output:
            with open(a.output, "w", encoding="utf-8") as fh:
                fh.write(text)
        else:
            sys.stdout.write(text)
            report_out = sys.stderr
        report_out.write("cleaned: %d invisible character(s), %d tag character(s), %d unusual space(s)\n"
                         % (counts["invisible"], counts["tag"], counts["spaces"]))

    result = run(text, a.allow.split(","))
    if a.json:
        json.dump(result, report_out, ensure_ascii=False, indent=2)
        report_out.write("\n")
    else:
        print_report(result, report_out)
    if a.strict and result["summary"]["error"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
