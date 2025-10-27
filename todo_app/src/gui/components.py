import customtkinter as ctk
from src.models.task import Task, Priority, Status
from src.gui.styles import AppTheme, ComponentStyles


class TaskCard(ctk.CTkFrame):
    """
    Representa visualmente uma única tarefa.
    Recebe callbacks para completar, editar e excluir.
    """
    def __init__(self, master, task: Task, on_complete, on_delete, on_edit, **kwargs):
        super().__init__(master, **ComponentStyles.get_task_card(), **kwargs)
        self.task        = task
        self.on_complete = on_complete
        self.on_delete   = on_delete
        self.on_edit     = on_edit
        self.create_widgets()
    
    def create_widgets(self):
        # Configuração de grid: coluna 1 expande
        self.grid_columnconfigure(1, weight=1)
        
        # Checkbox de conclusão
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            command=self.toggle_complete,
            width=20, height=20,
            checkbox_width=20, checkbox_height=20
        )
        self.checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        
        # Frame de conteúdo (título e descrição)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        # Use getattr to support Task implementations that may use different attribute names (e.g. 'name')
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text=getattr(self.task, "title", getattr(self.task, "name", "")),
            font=("Segoe UI", 14, "bold"),
            text_color=AppTheme.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0,5))
        
        # Descrição (opcional)
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
        
        # Frame de ações (editar, excluir)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=0, column=2, padx=10, pady=10)
        
        # Botão editar
        self.edit_button = ctk.CTkButton(
            self.actions_frame,
            text="✏️",
            width=30, height=30,
            font=("Segoe UI", 12),
            command=lambda: self.on_edit(self.task)
        )
        self.edit_button.pack(side="left", padx=2)
        
        # Botão excluir
        self.delete_button = ctk.CTkButton(
            self.actions_frame,
            text="🗑️",
            width=30, height=30,
            command=lambda: self.on_delete(self.task),
            **ComponentStyles.get_danger_button()
        )
        self.delete_button.pack(side="left", padx=2)
        
        self.update_appearance()
    
    def toggle_complete(self):
        """
        Alterna status da tarefa e atualiza visual.
        Callback no controller faz persitência.
        """
        self.on_complete(self.task)
        self.update_appearance()
    
    def update_appearance(self):
        """
        Ajusta cores e checkbox de acordo com status.
        Tarefas concluídas aparecem esmaecidas.
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
    Janela modal para adicionar nova tarefa.
    Recebe callback on_add_task(title, description, priority).
    """
    def __init__(self, parent, on_add_task):
        super().__init__(parent)
        self.parent = parent
        self.on_add_task = on_add_task
        self.setup_window()
        self.create_widgets()
    def setup_window(self):
        self.title("Nova Tarefa")
        self.geometry("400x300")
        # Use the provided parent reference to avoid type-checker complaints about self.master
        self.transient(self.parent)
        self.grab_set()
    
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
        ctk.CTkButton(btn_frame, text="Adicionar", command=self.add_task, **ComponentStyles.get_main_button()).pack(side="right")
    
    def add_task(self):
        """
        Lê valores dos campos, converte prioridade e chama callback.
        Fecha o modal após adicionar.
        """
        title = self.title_entry.get().strip()
        if not title:
            return  # Não adiciona título vazio
        
        desc = self.desc_textbox.get("1.0", "end-1c").strip() or None
        prio_map = {"Baixa": Priority.LOW, "Média": Priority.MEDIUM, "Alta": Priority.HIGH}
        priority = prio_map[self.priority_var.get()]
        
        self.on_add_task(title, desc, priority)
        self.destroy()
