#!/usr/bin/env python3
"""Check humanizer21's package files. Standard library only."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def read(rel):
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except OSError as exc:
        errors.append("cannot read %s: %s" % (rel, exc))
        return ""


def load_json(rel):
    try:
        return json.loads(read(rel) or "{}")
    except json.JSONDecodeError as exc:
        errors.append("fix the JSON in %s: %s" % (rel, exc))
        return {}


skill = read("SKILL.md")
meta = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
if not meta:
    errors.append("SKILL.md must begin with YAML metadata")
    meta_text = ""
else:
    meta_text = meta.group(1)

name = re.search(r"(?m)^name:\s*(\S+)\s*$", meta_text)
if not name or name.group(1) != "humanizer21":
    errors.append("SKILL.md name must be humanizer21")

desc_match = re.search(r"(?m)^description:\s*(.+)$", meta_text)
description = desc_match.group(1).strip() if desc_match else ""
if not description:
    errors.append("SKILL.md needs a description")
if len(description) > 1024:
    errors.append("SKILL.md description has %d characters; the limit is 1024" % len(description))
if "<" in description or ">" in description:
    errors.append("SKILL.md description must not contain angle brackets")

version = re.search(r'(?m)^\s+version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', meta_text)
skill_version = version.group(1) if version else None
if not skill_version:
    errors.append("add metadata.version to SKILL.md")

changelog = re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)\s*$", read("CHANGELOG.md"))
package = load_json("package.json")
plugin = load_json(".claude-plugin/plugin.json")
cursor = load_json(".cursor-plugin/plugin.json")
market = load_json(".claude-plugin/marketplace.json")

versions = {
    "SKILL.md": skill_version,
    "CHANGELOG.md": changelog.group(1) if changelog else None,
    "package.json": package.get("version"),
    ".claude-plugin/plugin.json": plugin.get("version"),
    ".cursor-plugin/plugin.json": cursor.get("version"),
}
if len(set(versions.values())) != 1:
    errors.append("use one version everywhere: %s" % versions)

first_two = " ".join(re.split(r"(?<=\.)\s+", description)[:2])
manifest_descs = [plugin.get("description"), cursor.get("description")]
manifest_descs += [p.get("description") for p in market.get("plugins", [])]
for d in manifest_descs:
    if d != first_two:
        errors.append("plugin descriptions must equal the first two sentences of the SKILL.md description")
        break

if plugin.get("skills") != ["./"]:
    errors.append("point the Claude plugin skill loader at the repo root")

# Files that SKILL.md tells the agent to read must exist.
for ref in sorted(set(re.findall(r"`((?:references|scripts)/[\w.-]+)`", skill))):
    if not (ROOT / ref).is_file():
        errors.append("SKILL.md points at a missing file: %s" % ref)
if not (ROOT / "THIRD_PARTY_NOTICES.md").is_file():
    errors.append("THIRD_PARTY_NOTICES.md is missing")

# Pattern numbering and section references.
patterns_md = read("references/ai-patterns.md")
numbers = [int(n) for n in re.findall(r"(?m)^### ([0-9]+)\. ", patterns_md)]
if not numbers or numbers != list(range(1, len(numbers) + 1)):
    errors.append("number the patterns in ai-patterns.md from 1 without gaps: %s" % numbers)
count = len(numbers)
for rel in ["SKILL.md"] + ["references/%s" % p.name for p in sorted((ROOT / "references").glob("*.md"))]:
    for ref in re.findall(r"§([0-9]+)", read(rel)):
        if not 1 <= int(ref) <= count:
            errors.append("%s refers to §%s, but there are %d patterns" % (rel, ref, count))
if "%d patterns" % count not in skill:
    errors.append("SKILL.md should state the pattern count (%d patterns)" % count)

# Sizes.
words = len(skill.split())
if words > 2500:
    errors.append("SKILL.md has %d words; keep it at 2,500 or fewer" % words)
prompt_chars = len(read("prompts/system-prompt.md"))
if prompt_chars > 8000:
    errors.append("prompts/system-prompt.md has %d characters; keep it under 8,000" % prompt_chars)

# No invisible characters anywhere in text files.
invisible = re.compile("[\u200b-\u200f\u2060\ufeff\u00ad\u202f\u00a0\u2028\u2029]")
for path in ROOT.rglob("*"):
    if ".git" in path.parts or "node_modules" in path.parts or not path.is_file():
        continue
    if path.suffix not in {".md", ".py", ".js", ".json", ".yml", ".yaml", ".txt"}:
        continue
    if path.name == "input.txt" and "corpus" in path.parts:
        continue  # test inputs carry hidden characters on purpose
    if invisible.search(path.read_text(encoding="utf-8")):
        errors.append("invisible character in %s" % path.relative_to(ROOT))

if errors:
    for e in errors:
        print("error: " + e)
    sys.exit(1)
print("humanizer21 package v%s is valid (%d patterns, SKILL.md %d words, prompt %d characters)"
      % (skill_version, count, words, prompt_chars))
