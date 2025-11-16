#!/usr/bin/env bash
set -euo pipefail

# Start the To-do app using the repository venv (if present).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

if [ ! -x "$VENV/bin/python" ]; then
  echo "Virtualenv not found. Creating..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --upgrade pip
  echo "Installing requirements..."
  "$VENV/bin/pip" install -r todo_app/requirements.txt
fi

echo "Starting app..."
"$VENV/bin/python" "$ROOT/run_todo_app.py"
