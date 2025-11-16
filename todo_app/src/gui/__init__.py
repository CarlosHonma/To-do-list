"""Simplified GUI package API.

Expose main GUI classes from a single import location so callers can use
`from src.gui import TodoApp` instead of importing from multiple files.
This file re-exports the classes implemented in `main_window.py` and
`components.py` for convenience.
"""
from .main_window import TodoApp
from .components import TaskCard, AddTaskDialog

__all__ = ["TodoApp", "TaskCard", "AddTaskDialog"]
"""
Graphical interface module.
Contains the main window, components, and styles.
"""

from src.gui.main_window import TodoApp
from src.gui.components import TaskCard, AddTaskDialog
from src.gui.styles import AppTheme, ComponentStyles

__all__ = [
    "TodoApp",
    "TaskCard",
    "AddTaskDialog",
    "AppTheme",
    "ComponentStyles"
]