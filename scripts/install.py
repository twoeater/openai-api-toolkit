#!/usr/bin/env python3
"""Install the locked official Linux x86_64 release without root or API keys."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "config/openai-cli.lock.json").read_text())


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "amd64"):
        raise SystemExit("This lock targets Codex Cloud Linux x86_64 only.")
    if not shutil.which("curl"):
        raise SystemExit("curl is required, with the platform's proxy and CA trust.")
    binary = ROOT / ".local/openai-cli" / LOCK["version"] / "openai"
    link = ROOT / ".local/bin/openai"
    if link.exists() and not link.is_symlink():
        raise SystemExit("Refusing to replace an unrelated .local/bin/openai file.")
    if not binary.is_file() or digest(binary) != LOCK["binary_sha256"]:
        binary.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="install-", dir=binary.parent) as work:
            work = Path(work)
            archive = work / "release.tar.gz"
            subprocess.run([
                "curl", "--fail", "--show-error", "--silent", "--location",
                "--proto", "=https", "--proto-redir", "=https", "--retry", "2",
                "--connect-timeout", "15", "--max-time", "120",
                "--output", str(archive), LOCK["archive"]["url"],
            ], check=True)
            if digest(archive) != LOCK["archive"]["sha256"]:
                raise SystemExit("Official release archive checksum mismatch; installation stopped.")
            staged = work / "openai"
            with tarfile.open(archive, "r:gz") as bundle:
                member = bundle.getmember("openai")
                if not member.isfile():
                    raise SystemExit("The release binary is not a regular file.")
                with bundle.extractfile(member) as source, staged.open("wb") as output:
                    shutil.copyfileobj(source, output)
            if digest(staged) != LOCK["binary_sha256"]:
                raise SystemExit("Release binary checksum mismatch; installation stopped.")
            staged.chmod(0o755)
            os.replace(staged, binary)
        print("Installed checksum-verified official OpenAI CLI " + LOCK["version"])
    else:
        print("Already installed; binary checksum verified: " + LOCK["version"])
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink():
        link.unlink()
    link.symlink_to(os.path.relpath(binary, link.parent))
    subprocess.run([str(ROOT / "bin/openai"), "--version"], check=True)


if __name__ == "__main__":
    main()
