"""
Launcher script to run the To-do app from the repository root.

This script ensures the `todo_app` package is on sys.path and calls the
application entrypoint. Use it from the repository root (recommended):

    source .venv/bin/activate
    python run_todo_app.py

It is safe to import (it will only start the app when executed as __main__).
"""
from pathlib import Path
import sys

ROOT = Path(__file__).parent.resolve()
TODO_APP = ROOT / "todo_app"

if str(TODO_APP) not in sys.path:
    sys.path.insert(0, str(TODO_APP))

def main():
    # import and call the application's main() function
    from src.main import main as app_main
    app_main()


if __name__ == "__main__":
    main()
