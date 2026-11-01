"""Run the corpus through a model and grade every answer.

    uv run --with anthropic tests/run_corpus.py               # all cases, 3 runs each
    uv run --with anthropic tests/run_corpus.py --runs 1 --case olimpiada-habary
    python3 tests/run_corpus.py --variant prompt --dry-run    # show what would be sent
    python3 tests/run_corpus.py --answers DIR                 # grade saved answers, no API

The model gets SKILL.md and every file of references/ as its instructions
(or, with --variant prompt, prompts/system-prompt.md plus references/, as a
ChatGPT project would). Each case sends its `request` and `input.txt`. The
finished text is taken from between the markers the harness asks for, so
the list of changes after it is not graded, and checked with tests/grade.py.

A case passes when at least --need of its --runs answers pass every check.
Requests go out --jobs at a time. The script exits with code 1 if any case
fails, and with code 2 if the API stops answering (a bad key, for example);
the report then covers the answers received so far. It needs ANTHROPIC_API_KEY
unless --dry-run or --answers is given. Answers and a report go to --out.
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(HERE, "corpus")
sys.path.insert(0, HERE)
import grade  # noqa: E402

MODEL = "claude-opus-5-5"
START = "<<<TEXT"
END = "TEXT>>>"
HARNESS_NOTE = (
    "Test harness note: you cannot run scripts here, so skip the automatic "
    "check. Put the finished text, and nothing else, between a line "
    "'%s' and a line '%s'. Write your list of changes and notes after it." % (START, END)
)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def cases():
    return sorted(d for d in os.listdir(CORPUS) if os.path.isdir(os.path.join(CORPUS, d)))


def system_prompt(variant):
    first = "SKILL.md" if variant == "skill" else os.path.join("prompts", "system-prompt.md")
    parts = ["<file name=%r>\n%s\n</file>" % (first.replace(os.sep, "/"), read(os.path.join(ROOT, first)))]
    refs = os.path.join(ROOT, "references")
    for name in sorted(os.listdir(refs)):
        if name.endswith(".md"):
            parts.append("<file name='references/%s'>\n%s\n</file>" % (name, read(os.path.join(refs, name))))
    return "\n\n".join(parts) + "\n\n" + HARNESS_NOTE


def user_message(case):
    exp = json.loads(read(os.path.join(CORPUS, case, "expected.json")))
    return "%s\n\n%s" % (exp["request"], read(os.path.join(CORPUS, case, "input.txt")))


def final_text(answer):
    """The text between the markers, or None when the answer has none."""
    start = answer.find(START)
    if start < 0:
        return None
    start += len(START)
    end = answer.find(END, start)
    if end < 0:
        return None
    return answer[start:end].strip("\n")


def check(case, answer):
    """Names of the failed checks for one answer."""
    text = final_text(answer)
    if text is None:
        return ["answer has the %s ... %s markers" % (START, END)]
    return [name for name, ok in grade.grade(os.path.join(CORPUS, case), text) if not ok]


def ask(client, system, message, model, effort):
    import anthropic

    for attempt in range(4):
        try:
            with client.beta.messages.stream(
                model=model,
                max_tokens=32000,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": message}],
                output_config={"effort": effort},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                msg = stream.get_final_message()
            if msg.stop_reason == "refusal":
                return "", msg.usage
            return "".join(b.text for b in msg.content if b.type == "text"), msg.usage
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError):
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 2))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--case", action="append", help="run only this case (repeatable)")
    p.add_argument("--runs", type=int, default=3, help="answers per case (default 3)")
    p.add_argument("--need", type=int, help="passing answers a case needs (default: runs - 1, at least 1)")
    p.add_argument("--jobs", type=int, default=6, help="requests sent at the same time (default 6)")
    p.add_argument("--variant", choices=["skill", "prompt"], default="skill")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--out", default=os.path.join(ROOT, "corpus-results"), help="folder for answers and report")
    p.add_argument("--answers", help="grade saved answers from this folder (<case>/<n>.txt) instead of asking a model")
    p.add_argument("--dry-run", action="store_true", help="print sizes and the first request, send nothing")
    args = p.parse_args(argv)

    selected = args.case or cases()
    unknown = [c for c in selected if c not in cases()]
    if unknown:
        p.error("unknown case: %s" % ", ".join(unknown))
    need = args.need if args.need is not None else max(1, args.runs - 1)
    system = system_prompt(args.variant)

    if args.dry_run:
        print("variant %s: system prompt %d characters, %d cases x %d runs" % (args.variant, len(system), len(selected), args.runs))
        print("--- first message ---\n" + user_message(selected[0]))
        return 0

    client = None
    if not args.answers:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
            return 2
        import anthropic

        client = anthropic.Anthropic()

    jobs = [(case, n) for case in selected for n in range(1, args.runs + 1)]
    totals = {"input": 0, "cache_read": 0, "cache_write": 0, "output": 0}
    results = {}

    def one(job):
        case, n = job
        if args.answers:
            path = os.path.join(args.answers, case, "%d.txt" % n)
            return job, (read(path) if os.path.exists(path) else ""), None
        answer, usage = ask(client, system, user_message(case), args.model, args.effort)
        os.makedirs(os.path.join(args.out, case), exist_ok=True)
        with open(os.path.join(args.out, case, "%d.txt" % n), "w", encoding="utf-8") as fh:
            fh.write(answer)
        return job, answer, usage

    fatal = None
    with ThreadPoolExecutor(max_workers=1 if args.answers else args.jobs) as pool:
        pending = [pool.submit(one, job) for job in jobs]
        for future in as_completed(pending):
            try:
                (case, n), answer, usage = future.result()
            except Exception as exc:  # a bad key or a dead API: stop, keep what we have
                if fatal is None:
                    fatal = exc
                    for f in pending:
                        f.cancel()
                continue
            if usage is not None:
                totals["input"] += usage.input_tokens
                totals["cache_read"] += usage.cache_read_input_tokens or 0
                totals["cache_write"] += usage.cache_creation_input_tokens or 0
                totals["output"] += usage.output_tokens
            failed = check(case, answer)
            results[case, n] = failed
            print("%-24s run %d: %s" % (case, n, "OK" if not failed else "FAIL (%d)" % len(failed)), flush=True)

    rows = []
    for case in selected:
        failures = [results[case, n] for n in range(1, args.runs + 1) if (case, n) in results]
        passed = sum(not f for f in failures)
        rows.append({"case": case, "passed": passed, "runs": len(failures), "ok": passed >= need, "failures": failures})

    report = render(rows, need, args, totals)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "report.md"), "w", encoding="utf-8") as fh:
        fh.write(report)
    with open(os.path.join(args.out, "report.json"), "w", encoding="utf-8") as fh:
        json.dump({"variant": args.variant, "model": args.model, "need": need, "tokens": totals, "cases": rows}, fh, ensure_ascii=False, indent=2)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(report)
    print("\n" + report)
    if fatal is not None:
        print("Stopped early: %s" % fatal, file=sys.stderr)
        return 2
    return 0 if all(r["ok"] for r in rows) else 1


def render(rows, need, args, totals):
    ok = sum(r["ok"] for r in rows)
    lines = [
        "## Corpus run: %s, %s" % (args.variant, "saved answers" if args.answers else args.model),
        "",
        "%d of %d cases pass (a case needs %d of %d answers to pass every check)." % (ok, len(rows), need, args.runs),
        "",
        "| Case | Passed | Result |",
        "|---|---|---|",
    ]
    lines += ["| %s | %d / %d | %s |" % (r["case"], r["passed"], r["runs"], "OK" if r["ok"] else "FAIL") for r in rows if r["runs"]]
    skipped = [r["case"] for r in rows if not r["runs"]]
    if skipped:
        lines += ["", "Not run (stopped early): %s." % ", ".join(skipped)]
    if not args.answers:
        lines += ["", "Tokens: %(input)d input, %(cache_read)d cache read, %(cache_write)d cache write, %(output)d output." % totals]
    failed = [(r["case"], i + 1, f) for r in rows for i, f in enumerate(r["failures"]) if f]
    if failed:
        lines += ["", "### Failed checks", ""]
        for case, n, names in failed:
            lines.append("- **%s**, run %d: %s" % (case, n, "; ".join(names)))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
