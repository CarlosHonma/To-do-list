import customtkinter as ctk
from typing import cast
from src.models.task import Status, Task, Priority
from src.utils.database import TaskDatabase
from src.gui.components import TaskCard, AddTaskDialog
from src.gui.styles import AppTheme, ComponentStyles


class TodoApp(ctk.CTk):
    """
    To-Do List application main window.
    Responsible for initializing GUI, database and callbacks.
    """
    def __init__(self):
        super().__init__()
        AppTheme.configure_appearance()
        
        self.db = TaskDatabase()  # Initializes or loads tasks
        self.setup_window()
        self.create_widgets()
        self.refresh_tasks()
    
    def setup_window(self):
        """
        Basic window settings:
        title, size, minimum, icon (optional).
        """
        self.title("Lista de Tarefas")
        self.geometry("800x600")
        self.minsize(600, 400)
    
    def create_widgets(self):
        """
        Creates main containers: header, filters and task area.
        """
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_header()
        self._create_filters()
        self._create_task_list()
    
    def _create_header(self):
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))
        # Split emoji and title into separate labels so we can set an
        # emoji-capable font for the emoji glyph and keep the UI font for text.
        from src.gui.styles import emoji_font

        emoji_lbl = ctk.CTkLabel(
            header,
            text="📋",
            font=emoji_font(28, "normal"),
            text_color=AppTheme.TEXT_PRIMARY
        )
        emoji_lbl.pack(side="left", padx=(0,8))

        ctk.CTkLabel(
            header,
            text="Minhas Tarefas",
            font=("Segoe UI", 24, "bold"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(side="left")
        
        ctk.CTkButton(
            header,
            text="+ Nova Tarefa",
            command=self.show_add_dialog,
            **ComponentStyles.get_main_button()
        ).pack(side="right")
    
    def _create_filters(self):
        filters = ctk.CTkFrame(self.main_container, fg_color="transparent")
        filters.pack(fill="x", pady=(0,15))
        
        self.filter_var = ctk.StringVar(value="Todas")
        for label in ["Todas", "Pendentes", "Concluídas"]:
            ctk.CTkRadioButton(
                filters,
                text=label,
                variable=self.filter_var,
                value=label,
                command=self.refresh_tasks,
                font=("Segoe UI", 12)
            ).pack(side="left", padx=(0,15))
    
    def _create_task_list(self):
        """
        Scrollable area that will display TaskCards or empty list message.
        """
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_container,
            corner_radius=AppTheme.CORNER_RADIUS
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
    
    def show_add_dialog(self):
        """Displays the modal to add a new task."""
        AddTaskDialog(self, self.add_task)
    
    def add_task(self, title, description, priority):
        """Callback: adds a task to the database and updates the list."""
        self.db.add_task(title, description, priority)
        self.refresh_tasks()
    
    def complete_task(self, task):
        """
        Callback: switches task status and saves it to the database.
        Called by TaskCard.
        """
        if task.status == Status.PENDING:
            task.mark_completed()
        else:
            task.mark_pending()
        self.db.save_tasks()
        self.refresh_tasks()
    
    def delete_task(self, task):
        """
        Callback: confirms deletion and removes from the database.
        Uses simple input modal for confirmation.
        """
        dialog = ctk.CTkInputDialog(
            text=f"Excluir '{task.title}'?",
            title="Confirmar Exclusão"
        )
        if dialog.get_input():  # User confirmed
            self.db.delete_task(task.id)
            self.refresh_tasks()
    
    def edit_task(self, task):
        """
        Edit callback (not implemented yet).
        Could reuse AddTaskDialog to edit fields.
        """
        pass
    
    def refresh_tasks(self):
        """
		Refreshes the displayed list:
		- Clears existing widgets
		- Filters by status (All/Pending/Completed)
		- Displays TaskCard for each empty task or message
        """
        # Clean scroll area
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Select tasks according to filter
        fv = self.filter_var.get()
        if fv == "Pendentes":
            tasks = self.db.get_tasks(Status.PENDING)
        elif fv == "Concluídas":
            tasks = self.db.get_tasks(Status.COMPLETED)
        else:
            tasks = self.db.get_tasks()

        # If there are no tasks, show a composed empty message using an
        # emoji-capable font for the emoji and the UI font for the text.
        if not tasks:
            from src.gui.styles import emoji_font
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            empty_frame.pack(expand=True, pady=50)
            emoji_lbl = ctk.CTkLabel(
                empty_frame,
                text="🎉",
                font=emoji_font(28),
                text_color=AppTheme.TEXT_MUTED,
            )
            emoji_lbl.pack(side="left", padx=(0,8))
            ctk.CTkLabel(
                empty_frame,
                text="Nenhuma tarefa encontrada!\nClique em 'Nova Tarefa'.",
                font=("Segoe UI", 14),
                text_color=AppTheme.TEXT_MUTED,
            ).pack(side="left")
            return
        # Ensure each item is a Task-like object (some DB implementations may return dicts)
        def _to_task(obj):
                from src.models.task import Task
                if isinstance(obj, dict):
                    # Normalize dict data into proper Task fields (convert
                    # priority/status to Enum values and parse datetimes) before
                    # constructing a Task instance.
                    try:
                        data = dict(obj)
                        # Priority: could be stored as int (value) or str
                        p = data.get("priority")
                        if p is None or p == "None":
                            priority = None
                        else:
                            try:
                                # try integer value
                                priority = Priority(int(p))
                            except Exception:
                                # try name or string mapping
                                try:
                                    priority = Priority[p]
                                except Exception:
                                    priority = Priority.MEDIUM

                        # Status: could be stored as value string (e.g. 'Pending')
                        s = data.get("status")
                        if s is None:
                            status = Status.PENDING
                        else:
                            try:
                                status = Status(s)
                            except Exception:
                                # try matching by name
                                try:
                                    status = Status[s]
                                except Exception:
                                    status = Status.PENDING

                        # created_at may be an ISO string
                        ca = data.get("created_at")
                        if isinstance(ca, str):
                            try:
                                from datetime import datetime
                                created_at = datetime.fromisoformat(ca)
                            except Exception:
                                created_at = None
                        else:
                            created_at = ca

                        from uuid import uuid4
                        id_val = data.get("id") or str(uuid4())
                        title_val = data.get("title") or ""
                        task_obj = Task(
                            id=id_val,
                            title=title_val,
                            description=data.get("description"),
                            priority=priority if priority is not None else Priority.MEDIUM,
                            status=status,
                            created_at=created_at,
                            completed_at=data.get("completed_at"),
                        )
                        return task_obj
                    except Exception:
                        # Fallback: lightweight wrapper that exposes expected attributes and methods
                        class _TaskWrapper:
                            def __init__(self, data):
                                self.__dict__.update(data)

                            def mark_completed(self):
                                self.status = Status.COMPLETED

                            def mark_pending(self):
                                self.status = Status.PENDING

                        return _TaskWrapper(obj)
                return obj
        task_objs = [cast(Task, _to_task(t)) for t in tasks]
        for task in sorted(task_objs, key=lambda t: getattr(t, "created_at", 0), reverse=True):
                TaskCard(
                    self.scrollable_frame,
                    task,
                    self.complete_task,
                    self.delete_task,
                    self.edit_task
                ).pack(fill="x", padx=10, pady=5)


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
