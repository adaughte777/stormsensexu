#!/usr/bin/env bash
# setup.sh — macOS / Linux
set -e

# Create virtual environment in .venv
python3 -m venv .venv

# Activate venv for this script (note: activation won't persist outside this script)
source .venv/bin/activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete. To run the app:"
echo "  source .venv/bin/activate"
echo "  streamlit run app.py"
