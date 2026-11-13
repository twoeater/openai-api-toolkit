#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
python3 scripts/install.py
source scripts/activate.sh
python3 scripts/verify.py
