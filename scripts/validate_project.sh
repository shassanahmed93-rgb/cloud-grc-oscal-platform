#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo " CLOUD GRC PROJECT VALIDATION"
echo "===================================="

echo
echo "[1/5] Generating OSCAL SSP..."
./.venv/bin/python oscal/generate_ssp.py

echo
echo "[2/5] Copying SSP into Trestle workspace..."
mkdir -p system-security-plans/cloud-journal-api
cp oscal/ssp.json \
  system-security-plans/cloud-journal-api/system-security-plan.json

echo
echo "[3/5] Validating OSCAL model structure..."
./.venv/bin/trestle partial-object-validate \
  -f system-security-plans/cloud-journal-api/system-security-plan.json \
  -e system-security-plan \
  -nv

echo
echo "[4/5] Running Ruff lint checks..."
./.venv/bin/python -m ruff check app tests oscal

echo
echo "[5/5] Running automated tests..."
./.venv/bin/python -m pytest -v

echo
echo "===================================="
echo " ALL PROJECT CHECKS PASSED"
echo "===================================="
echo "Note: model validation is not full OSCAL dependency validation."
echo "Note: passing checks does not establish security compliance."
