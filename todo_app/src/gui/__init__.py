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