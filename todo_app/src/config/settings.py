"""
Application settings.
Centralize constants, paths, and preferences here.
"""

from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent.parent.parent  
DATA_DIR = BASE_DIR / "data"

# Database
DEFAULT_DB_PATH = "tasks.json"

# Interface
DEFAULT_WINDOW_SIZE = "800x600"
MIN_WINDOW_SIZE = (600, 400)

# Behavior
AUTO_SAVE_INTERVAL = 30  # seconds (if you implement auto-save)
MAX_TASKS_DISPLAY = 100  # limit of displayed tasks
