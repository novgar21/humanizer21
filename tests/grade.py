#!/usr/bin/env python3
"""Grade a humanizer21 result against a corpus case.

Usage:
    python3 tests/grade.py tests/corpus/olimpiada-habary result.txt

Prints one line per check and exits with code 1 if any check fails.
The checks are substring tests from the case's expected.json:
must_keep lists facts and protected text that have to survive the edit,
must_not lists tells, errors and invented details that must be gone.

Two allowances keep the checks from failing correct Turkmen:
- in must_keep, a count from 2 to 9 may be written in digits or in words,
  with or without `sany` (`3 sany täze seýilgäh`, `üç täze seýilgäh`);
- an entry that starts with `re:` is a regular expression, for a word that
  must not match inside a longer one (`re:\\bi[cç]in\\b` is the Turkish
  `için`, not the Turkmen `içinde`).
"""

import json
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import barla  # noqa: E402

UNITS = {"2": "iki", "3": "üç", "4": "dört", "5": "bäş", "6": "alty", "7": "ýedi", "8": "sekiz", "9": "dokuz"}
WORDS = {w: d for d, w in UNITS.items()}
COUNT = re.compile(r"^(\d|%s)( sany)? (.+)$" % "|".join(UNITS.values()))


def variants(entry):
    """Equally correct spellings of a must_keep entry: 3 / üç, with or without sany."""
    m = COUNT.match(entry)
    if not m or (m.group(1).isdigit() and m.group(1) not in UNITS):
        return [entry]
    n, rest = m.group(1), m.group(3)
    forms = {n, UNITS.get(n, WORDS.get(n))}
    return sorted("%s%s %s" % (f, s, rest) for f in forms for s in ("", " sany"))


def found(entry, text):
    if entry.startswith("re:"):
        return re.search(entry[3:], text) is not None
    return any(v in text for v in variants(entry))


def grade(case_dir, text):
    with open(os.path.join(case_dir, "expected.json"), encoding="utf-8") as fh:
        exp = json.load(fh)
    results = [("keeps %r" % k, found(k, text)) for k in exp["must_keep"]]
    results += [("has no %r" % k, not found(k, text)) for k in exp["must_not"]]
    # Quotes and table rows of a Turkmen source must survive unchanged.
    if exp.get("source_language", "tk") == "tk":
        with open(os.path.join(case_dir, "input.txt"), encoding="utf-8") as fh:
            lost = {i["kind"]: i["items"] for i in barla.compare(fh.read(), text)}
        for q in lost.get("quote", []):
            results.append(("keeps the quote %r" % q, False))
        results.append(("keeps every quote of the source", "quote" not in lost))
        results.append(("keeps every table row of the source", "table" not in lost))
    summary = barla.run(text)["summary"]
    results.append(("barla.py finds no errors or warnings", summary["error"] + summary["warn"] == 0))
    return results


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    with open(argv[2], encoding="utf-8") as fh:
        text = fh.read()
    results = grade(argv[1], text)
    for name, ok in results:
        print("%s %s" % ("OK  " if ok else "FAIL", name))
    passed = sum(ok for _, ok in results)
    print("%d / %d" % (passed, len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
