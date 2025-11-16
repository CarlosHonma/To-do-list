import customtkinter as ctk
import tkinter as tk
from src.models.task import Task, Priority, Status
from src.gui.styles import AppTheme, ComponentStyles


class TaskCard(ctk.CTkFrame):
    """
    Visually represents a single task.
    Receives callbacks for completion, editing, and deletion.
    """
    def __init__(self, master, task: Task, on_complete, on_delete, on_edit, **kwargs):
        super().__init__(master, **ComponentStyles.get_task_card(), **kwargs)
        self.task        = task
        self.on_complete = on_complete
        self.on_delete   = on_delete
        self.on_edit     = on_edit
        self.create_widgets()
    
    def create_widgets(self):
        # Grid configuration: it expands column 1
        self.grid_columnconfigure(1, weight=1)
        
        # Conclusion checkbox
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            command=self.toggle_complete,
            width=20, height=20,
            checkbox_width=20, checkbox_height=20
        )
        self.checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        # The content frame (title and description)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        # Use getattr to support Task implementations that may use different attribute names (e.g. 'name')
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text=getattr(self.task, "title", getattr(self.task, "name", "")),
            font=("Segoe UI", 14, "bold"),
            text_color=AppTheme.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0,5))
        
        # Description (optional)
        desc = getattr(self.task, "description", None)
        if desc:
            self.desc_label = ctk.CTkLabel(
                self.content_frame,
                text=desc,
                font=("Segoe UI", 11),
                text_color=AppTheme.TEXT_SECONDARY,
                anchor="w"
            )
            self.desc_label.grid(row=1, column=0, sticky="w", pady=(0,5))
        
        # Action frames (edit and delete)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=0, column=2, padx=10, pady=10)
        
        # Edit button
        self.edit_button = ctk.CTkButton(
            self.actions_frame,
            text="✏️",
            width=30, height=30,
            font=("Segoe UI", 12),
            command=lambda: self.on_edit(self.task)
        )
        self.edit_button.pack(side="left", padx=2)
        
        # Delete button
        # Note: ComponentStyles.get_danger_button() already provides a 'height'
        # key, so avoid passing 'height' here to prevent multiple values for
        # the same keyword argument.
        self.delete_button = ctk.CTkButton(
            self.actions_frame,
            text="🗑️",
            width=30,
            command=lambda: self.on_delete(self.task),
            **ComponentStyles.get_danger_button()
        )
        self.delete_button.pack(side="left", padx=2)
        
        self.update_appearance()
    
    def toggle_complete(self):
        """
        Toggles task status and updates the visuals.
        Callback in the controller ensures persistence.
        """
        self.on_complete(self.task)
        self.update_appearance()
    
    def update_appearance(self):
        """
        Adjusts colors and checkboxes according to status.
        Completed tasks appear dimmed.
        """
        # Support multiple Task shapes:
        # - Enum status attribute (Status.COMPLETED)
        # - Boolean flags: is_completed or completed
        status = getattr(self.task, "status", None)
        is_completed_flag = getattr(self.task, "is_completed", None)
        completed_prop = getattr(self.task, "completed", None)

        if status is not None:
            is_completed = (status == Status.COMPLETED)
        elif isinstance(is_completed_flag, bool):
            is_completed = is_completed_flag
        else:
            is_completed = bool(completed_prop)

        if is_completed:
            self.checkbox.select()
            self.title_label.configure(text_color=AppTheme.TEXT_MUTED)
            if hasattr(self, 'desc_label'):
                self.desc_label.configure(text_color=AppTheme.TEXT_MUTED)
        else:
            self.checkbox.deselect()
            self.title_label.configure(text_color=AppTheme.TEXT_PRIMARY)
            if hasattr(self, 'desc_label'):
                self.desc_label.configure(text_color=AppTheme.TEXT_SECONDARY)


class AddTaskDialog(ctk.CTkToplevel):
    """
    Modal window for adding a new task.
    Receives the on_add_task(title, description, priority) callback.
    """
    def __init__(self, parent, on_add_task, task=None):
        """Create the add/edit dialog.

        Args:
            parent: parent window
            on_add_task: callback with signature (title, description, priority, task)
            task: optional Task instance to edit
        """
        super().__init__(parent)
        self.parent = parent
        self.on_add_task = on_add_task
        self.task = task
        self.setup_window()
        self.create_widgets()
    def setup_window(self):
        self.title("Nova Tarefa")
        self.geometry("400x300")
        # Use the provided parent reference to avoid type-checker complaints about self.master
        self.transient(self.parent)
        # Ensure the window is realized/visible before taking the grab. In some
        # environments tkinter raises TclError: "grab failed: window not viewable"
        # if grab_set is called too early. Attempt grab_set and if it fails,
        # deiconify/update and retry.
        try:
            self.grab_set()
        except tk.TclError:
            try:
                self.deiconify()
                self.update_idletasks()
                self.grab_set()
            except Exception:
                # If grabbing still fails, continue without modal grab to avoid
                # crashing the whole app; dialog will still appear.
                pass
    
    def create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Adicionar Nova Tarefa", font=("Segoe UI", 16, "bold")).pack(pady=(0,20))
        
        ctk.CTkLabel(frame, text="Título:", font=("Segoe UI", 12)).pack(anchor="w")
        self.title_entry = ctk.CTkEntry(frame, placeholder_text="Digite o título...", height=35)
        self.title_entry.pack(fill="x", pady=(5,15))
        
        ctk.CTkLabel(frame, text="Descrição:", font=("Segoe UI", 12)).pack(anchor="w")
        self.desc_textbox = ctk.CTkTextbox(frame, height=80)
        self.desc_textbox.pack(fill="x", pady=(5,15))
        
        ctk.CTkLabel(frame, text="Prioridade:", font=("Segoe UI", 12)).pack(anchor="w")
        self.priority_var = ctk.StringVar(value="Média")
        self.priority_combo = ctk.CTkComboBox(
            frame,
            values=["Baixa", "Média", "Alta"],
            variable=self.priority_var,
            height=35
        )
        self.priority_combo.pack(fill="x", pady=(5,20))
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy, fg_color=AppTheme.SECONDARY_COLOR).pack(side="right", padx=(10,0))
        action_text = "Salvar" if self.task is not None else "Adicionar"
        ctk.CTkButton(btn_frame, text=action_text, command=self.add_task, **ComponentStyles.get_main_button()).pack(side="right")

        # If editing an existing task, prefill fields
        if self.task is not None:
            try:
                self.title_entry.insert(0, getattr(self.task, "title", ""))
                desc = getattr(self.task, "description", None)
                if desc:
                    self.desc_textbox.insert("1.0", desc)
                # map Priority to label
                pr = getattr(self.task, "priority", None)
                if pr is not None:
                    # Priority may be an Enum or numeric; derive label
                    try:
                        from src.models.task import Priority
                        if isinstance(pr, Priority):
                            val = pr
                        else:
                            try:
                                val = Priority(int(pr))
                            except Exception:
                                val = Priority.MEDIUM
                        label_map = {Priority.LOW: "Baixa", Priority.MEDIUM: "Média", Priority.HIGH: "Alta"}
                        self.priority_var.set(label_map.get(val, "Média"))
                    except Exception:
                        self.priority_var.set("Média")
            except Exception:
                pass
    
    def add_task(self):
        """
        Reads field values, converts priority, and calls a callback.
        Closes the modal after adding.
        """
        title = self.title_entry.get().strip()
        if not title:
            return  # Don't add empty title

        desc = self.desc_textbox.get("1.0", "end-1c").strip() or None
        prio_map = {"Baixa": Priority.LOW, "Média": Priority.MEDIUM, "Alta": Priority.HIGH}
        priority = prio_map.get(self.priority_var.get(), Priority.MEDIUM)

        # Pass the original task object (or None) so the caller can update
        # an existing task instead of creating a new one.
        try:
            self.on_add_task(title, desc, priority, self.task)
        finally:
            self.destroy()
