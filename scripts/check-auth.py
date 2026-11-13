#!/usr/bin/env python3
"""GET /v1/models only. Never print or persist credentials or raw error text."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if not os.environ.get("OPENAI_API_KEY"):
    print("SKIP: OPENAI_API_KEY is not available in this process.")
    sys.exit(2)

try:
    result = subprocess.run(
        [str(ROOT / "bin/openai"), "models", "list", "--format", "json"],
        capture_output=True, text=True, timeout=30,
    )
except subprocess.TimeoutExpired:
    print("FAIL: model listing timed out; check the applied network policy.")
    sys.exit(1)
if result.returncode:
    # API authentication errors may echo key fragments. Never return raw stderr.
    error = result.stderr.lower()
    category = "API or network error"
    if "401" in error or "invalid_api_key" in error:
        category = "authentication rejected"
    elif "403" in error or "forbidden" in error or "blocked" in error:
        category = "access or network policy denied"
    print(f"FAIL: {category}; CLI exit {result.returncode}. Raw error text withheld.")
    sys.exit(1)
try:
    payload = json.loads(result.stdout)
    models = payload.get("data") if isinstance(payload, dict) else payload
    if not isinstance(models, list) or not all(isinstance(m, dict) and isinstance(m.get("id"), str) for m in models):
        raise ValueError("Unexpected model-list structure")
except (ValueError, TypeError):
    print("FAIL: models list did not return the expected JSON records.")
    sys.exit(1)

# Store only selected model metadata, never the raw response or error body.
os.umask(0o077)
output = ROOT / "results/models.json"
output.parent.mkdir(parents=True, exist_ok=True)
safe_models = [{key: model[key] for key in ("id", "object", "created", "owned_by") if key in model}
               for model in models]
output.write_text(json.dumps({"data": safe_models}, indent=2) + "\n")
output.chmod(0o600)
print(f"PASS: authenticated model listing; {len(models)} models; saved to results/models.json")
