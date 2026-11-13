#!/usr/bin/env python3
"""Ask Codex's real Skill loader to discover this project. No model turns."""
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not shutil.which("codex"):
        raise SystemExit("FAIL: Codex CLI is required for the Skill recognition check.")
    state_root = ROOT / ".local/validation"
    state_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="skill-check-", dir=state_root) as state:
        process = subprocess.Popen([
            "codex", "app-server", "--stdio",
            "-c", "sqlite_home=" + json.dumps(state),
            "-c", "log_dir=" + json.dumps(state),
        ], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        pending = b""

        def send(message):
            process.stdin.write((json.dumps(message) + "\n").encode())
            process.stdin.flush()

        def receive(request_id):
            nonlocal pending
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    try:
                        message = json.loads(line)
                    except ValueError:
                        continue
                    if message.get("id") == request_id:
                        if "error" in message:
                            raise RuntimeError("Codex Skill protocol request failed")
                        return message["result"]
                if not selector.select(max(0, deadline - time.monotonic())):
                    break
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    raise RuntimeError("Codex app-server exited before answering")
                pending += chunk
            raise RuntimeError("Codex Skill discovery timed out")

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "openai-toolkit-skill-check", "version": "1.0.0"},
                "capabilities": {"experimentalApi": True},
            }})
            receive(1)
            send({"method": "initialized"})
            send({"id": 2, "method": "skills/list", "params": {
                "cwds": [str(ROOT)], "forceReload": True,
            }})
            result = receive(2)
            expected = str(ROOT / ".agents/skills/openai-cli/SKILL.md")
            entries = [entry for entry in result["data"] if entry["cwd"] == str(ROOT)]
            matches = [skill for entry in entries for skill in entry["skills"]
                       if skill["name"] == "openai-cli" and skill["path"] == expected]
            errors = [error for entry in entries for error in entry["errors"]
                      if "openai-cli" in error.get("path", "")]
            if len(matches) != 1 or not matches[0]["enabled"] or matches[0]["scope"] != "repo" or errors:
                raise RuntimeError("Official openai-cli Skill is missing, disabled, or invalid")
            safe = {key: matches[0][key] for key in ("name", "path", "scope", "enabled")}
            (state_root / "skill-discovery.json").write_text(
                json.dumps({"method": "Codex skills/list", "skill": safe, "errors": []}, indent=2) + "\n")
            print("PASS: Codex recognizes openai-cli as an enabled project Skill; no loader errors")
        finally:
            selector.close()
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, OSError) as error:
        raise SystemExit("FAIL: " + str(error))
