"""
Entry point for the To-Do List application.
Run this file to start the application:
    python -m src.main
"""

from src.gui.main_window import TodoApp


def main():
    """
    Main function that initializes and runs the application.
    """
    app = TodoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
