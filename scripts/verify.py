#!/usr/bin/env python3
"""Offline checks of the CLI, official Skill, and Git exclusions. No API calls."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "config/openai-cli.lock.json").read_text())


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def check_hash(path, expected):
    require(path.is_file(), "Missing " + str(path.relative_to(ROOT)))
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == expected,
                "Checksum mismatch: " + str(path.relative_to(ROOT)))


check_hash(ROOT / ".local/bin/openai", LOCK["binary_sha256"])
skill = ROOT / LOCK["skill"]["path"]
check_hash(skill, LOCK["skill"]["sha256"])
check_hash(ROOT / LOCK["skill"]["license_path"], LOCK["skill"]["license_sha256"])
require(skill.read_text().startswith("---\nname: openai-cli\ndescription: "),
        "Missing official Skill frontmatter")
for args, marker in [
    (["--version"], "openai version " + LOCK["version"]),
    (["--help"], "OpenAI CLI"),
    (["models", "list", "--help"], "List accessible model IDs"),
]:
    result = subprocess.run([str(ROOT / "bin/openai"), *args],
                            capture_output=True, text=True, timeout=15)
    require(result.returncode == 0 and marker in result.stdout,
            "CLI check failed: " + " ".join(args))
    print("PASS: openai " + " ".join(args))
print("PASS: official Skill and Apache-2.0 license match pinned upstream bytes")
for path in [".env", ".env.production", "nested/.env", "auth.json", "credentials.json",
             "private/key.pem", "logs/run.log", "results/models.json", ".local/bin/openai"]:
    result = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT)
    require(result.returncode == 0, "Not ignored: " + path)
for path in ["README.md", "AGENTS.md", "config/openai-cli.lock.json", LOCK["skill"]["path"]]:
    result = subprocess.run(["git", "check-ignore", "--no-index", "-q", path], cwd=ROOT)
    require(result.returncode == 1, "Public setup file is unexpectedly ignored: " + path)
print("PASS: secret/result exclusions and public setup file visibility")
