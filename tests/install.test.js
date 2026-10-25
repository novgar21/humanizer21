"use strict";

// Smoke test for the installer: install, zip, prompt, uninstall in a temp folder.

const assert = require("assert");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const CLI = path.join(__dirname, "..", "bin", "install.js");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "humanizer21-test-"));
const run = (...args) => execFileSync(process.execPath, [CLI, ...args], { cwd: tmp, encoding: "utf8" });

try {
  const skills = path.join(tmp, "skills");
  run("--dir", skills);
  const dest = path.join(skills, "humanizer21");
  for (const f of ["SKILL.md", "LICENSE", "scripts/barla.py", "references/orthography.md"]) {
    assert.ok(fs.existsSync(path.join(dest, f)), `missing ${f}`);
  }
  assert.ok(!fs.existsSync(path.join(dest, "bin")), "bin/ must not be installed");
  assert.ok(!fs.existsSync(path.join(dest, "tests")), "tests/ must not be installed");

  run("--zip", "out.zip");
  const zip = fs.readFileSync(path.join(tmp, "out.zip"));
  assert.strictEqual(zip.readUInt32LE(0), 0x04034b50, "not a zip file");
  assert.ok(zip.includes(Buffer.from("humanizer21/SKILL.md")), "zip lacks humanizer21/SKILL.md");

  run("--prompt");
  assert.ok(fs.readFileSync(path.join(tmp, "humanizer21-prompt.md"), "utf8").includes("humanizer21"));

  run("--uninstall", "--dir", skills);
  assert.ok(!fs.existsSync(dest), "uninstall left files behind");

  console.log("install.test.js: all checks passed");
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
