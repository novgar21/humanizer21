#!/usr/bin/env python3
"""Grade a humanizer21 result against a corpus case.

Usage:
    python3 tests/grade.py tests/corpus/olimpiada-habary result.txt

Prints one line per check and exits with code 1 if any check fails.
The checks are plain substring tests from the case's expected.json:
must_keep lists facts and protected text that have to survive the edit,
must_not lists tells, errors and invented details that must be gone.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import barla  # noqa: E402


def grade(case_dir, text):
    with open(os.path.join(case_dir, "expected.json"), encoding="utf-8") as fh:
        exp = json.load(fh)
    results = [("keeps %r" % k, k in text) for k in exp["must_keep"]]
    results += [("has no %r" % k, k not in text) for k in exp["must_not"]]
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
