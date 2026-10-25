#!/usr/bin/env node
"use strict";

// humanizer21 installer. No dependencies; Node 16+.

const fs = require("fs");
const os = require("os");
const path = require("path");
const zlib = require("zlib");

const NAME = "humanizer21";
const ROOT = path.resolve(__dirname, "..");
const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));
const SKILL_ITEMS = ["SKILL.md", "LICENSE", "references", "scripts"];

const HELP = `
humanizer21 ${PKG.version} - Turkmen language humanizer

Usage:
  npx humanizer21                 install for Claude Code (all projects)
  npx humanizer21 --project       install into ./.claude/skills of this project
  npx humanizer21 --dir <path>    install into any skills folder (other agents)
  npx humanizer21 --zip [file]    build humanizer21.zip to upload on claude.ai
  npx humanizer21 --prompt [file] save the one-file prompt for ChatGPT, Grok, Gemini...
  npx humanizer21 --uninstall     remove it (combine with --project or --dir)
  npx humanizer21 --help | --version
`;

function parseArgs(argv) {
  const opts = { mode: "install", target: null, out: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => (argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : null);
    switch (a) {
      case "--project": opts.target = path.join(process.cwd(), ".claude", "skills"); break;
      case "--dir": {
        const d = next();
        if (!d) fail("--dir needs a folder path");
        opts.target = path.resolve(d);
        break;
      }
      case "--zip": opts.mode = "zip"; opts.out = next(); break;
      case "--prompt": opts.mode = "prompt"; opts.out = next(); break;
      case "--uninstall": opts.mode = "uninstall"; break;
      case "--help": case "-h": opts.mode = "help"; break;
      case "--version": case "-v": opts.mode = "version"; break;
      default: fail(`unknown option: ${a}\n${HELP}`);
    }
  }
  if (!opts.target) opts.target = path.join(os.homedir(), ".claude", "skills");
  return opts;
}

function fail(msg) {
  process.stderr.write(`humanizer21: ${msg}\n`);
  process.exit(1);
}

function listFiles(rel) {
  const abs = path.join(ROOT, rel);
  if (!fs.existsSync(abs)) return [];
  if (fs.statSync(abs).isFile()) return [rel];
  return fs.readdirSync(abs).flatMap((n) =>
    n === "__pycache__" || n.startsWith(".") ? [] : listFiles(path.join(rel, n))
  );
}

function skillFiles() {
  return SKILL_ITEMS.flatMap(listFiles);
}

function install(targetRoot) {
  const dest = path.join(targetRoot, NAME);
  if (fs.existsSync(dest)) fs.rmSync(dest, { recursive: true, force: true });
  for (const rel of skillFiles()) {
    const to = path.join(dest, rel);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(path.join(ROOT, rel), to);
  }
  const script = path.join(dest, "scripts", "barla.py");
  if (fs.existsSync(script)) fs.chmodSync(script, 0o755);
  console.log(`Installed ${NAME} ${PKG.version} to ${dest}`);
  console.log("Start a new Claude Code session; the skill loads when you work with Turkmen text.");
}

function uninstall(targetRoot) {
  const dest = path.join(targetRoot, NAME);
  if (!fs.existsSync(dest)) {
    console.log(`Nothing to remove: ${dest} does not exist.`);
    return;
  }
  fs.rmSync(dest, { recursive: true, force: true });
  console.log(`Removed ${dest}`);
}

// Minimal ZIP writer (deflate), enough for a skill upload.
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function dosTime(d) {
  const time = (d.getHours() << 11) | (d.getMinutes() << 5) | Math.floor(d.getSeconds() / 2);
  const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
  return { time, date };
}

function buildZip(entries) {
  const locals = [];
  const centrals = [];
  let offset = 0;
  const { time, date } = dosTime(new Date());
  for (const { name, data } of entries) {
    const nameBuf = Buffer.from(name, "utf8");
    const comp = zlib.deflateRawSync(data);
    const crc = crc32(data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6); // UTF-8 names
    local.writeUInt16LE(8, 8);
    local.writeUInt16LE(time, 10);
    local.writeUInt16LE(date, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(comp.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    locals.push(local, nameBuf, comp);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(8, 10);
    central.writeUInt16LE(time, 12);
    central.writeUInt16LE(date, 14);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(comp.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBuf.length, 28);
    central.writeUInt32LE(offset, 42);
    centrals.push(central, nameBuf);
    offset += local.length + nameBuf.length + comp.length;
  }
  const centralBuf = Buffer.concat(centrals);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(centralBuf.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, centralBuf, end]);
}

function makeZip(out) {
  const file = path.resolve(out || `${NAME}.zip`);
  const entries = skillFiles().map((rel) => ({
    name: `${NAME}/${rel.split(path.sep).join("/")}`,
    data: fs.readFileSync(path.join(ROOT, rel)),
  }));
  fs.writeFileSync(file, buildZip(entries));
  console.log(`Created ${file} (${entries.length} files).`);
  console.log("Upload it on claude.ai: Settings > Capabilities > Skills > Upload skill.");
}

function savePrompt(out) {
  const file = path.resolve(out || `${NAME}-prompt.md`);
  fs.copyFileSync(path.join(ROOT, "prompts", "system-prompt.md"), file);
  console.log(`Saved ${file}`);
  console.log("Paste it into custom instructions (ChatGPT, Grok, Gemini, DeepSeek...).");
  console.log("For better results also attach the files from references/ as knowledge files.");
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  switch (opts.mode) {
    case "help": process.stdout.write(HELP); break;
    case "version": console.log(PKG.version); break;
    case "zip": makeZip(opts.out); break;
    case "prompt": savePrompt(opts.out); break;
    case "uninstall": uninstall(opts.target); break;
    default: install(opts.target);
  }
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    fail(err.message);
  }
}

module.exports = { buildZip, crc32, skillFiles };
