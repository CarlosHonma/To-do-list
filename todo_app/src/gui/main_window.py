# todo_app/src/gui/main_window.py

import customtkinter as ctk
from typing import cast
from src.models.task import Status, Task
from src.utils.database import TaskDatabase
from src.gui.components import TaskCard, AddTaskDialog
from src.gui.styles import AppTheme, ComponentStyles


class TodoApp(ctk.CTk):
    """
    Janela principal da aplicação To-Do List.
    Responsável por inicializar GUI, banco de dados e callbacks.
    """
    def __init__(self):
        super().__init__()
        AppTheme.configure_appearance()
        
        self.db = TaskDatabase()  # Inicializa ou carrega tarefas
        self.setup_window()
        self.create_widgets()
        self.refresh_tasks()
    
    def setup_window(self):
        """
        Configurações básicas da janela:
        título, tamanho, mínimo, ícone (opcional).
        """
        self.title("Lista de Tarefas")
        self.geometry("800x600")
        self.minsize(600, 400)
    
    def create_widgets(self):
        """
        Cria containers principais: header, filtros e área de tarefas.
        """
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_header()
        self._create_filters()
        self._create_task_list()
    
    def _create_header(self):
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))
        
        ctk.CTkLabel(
            header,
            text="📋 Minhas Tarefas",
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
        Área rolável que exibirá TaskCards ou mensagem de lista vazia.
        """
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_container,
            corner_radius=AppTheme.CORNER_RADIUS
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        self.empty_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="🎉 Nenhuma tarefa encontrada!\nClique em 'Nova Tarefa'.",
            font=("Segoe UI", 14),
            text_color=AppTheme.TEXT_MUTED
        )
    
    def show_add_dialog(self):
        """Exibe o modal para adicionar nova tarefa."""
        AddTaskDialog(self, self.add_task)
    
    def add_task(self, title, description, priority):
        """Callback: adiciona tarefa no banco e atualiza lista."""
        self.db.add_task(title, description, priority)
        self.refresh_tasks()
    
    def complete_task(self, task):
        """
        Callback: alterna status da tarefa e salva no banco.
        Chamado pelo TaskCard.
        """
        if task.status == Status.PENDING:
            task.mark_completed()
        else:
            task.mark_pending()
        self.db.save_tasks()
        self.refresh_tasks()
    
    def delete_task(self, task):
        """
        Callback: confirma exclusão e remove do banco.
        Usa modal simples de input para confirmação.
        """
        dialog = ctk.CTkInputDialog(
            text=f"Excluir '{task.title}'?",
            title="Confirmar Exclusão"
        )
        if dialog.get_input():  # Usuário confirmou
            self.db.delete_task(task.id)
            self.refresh_tasks()
    
    def edit_task(self, task):
        """
        Callback de edição (ainda não implementado).
        Poderia reutilizar AddTaskDialog para editar campos.
        """
        pass
    
    def refresh_tasks(self):
        """
        Atualiza a lista exibida:
        - Limpa widgets existentes
        - Filtra por status (Todas/Pendentes/Concluídas)
        - Exibe TaskCard para cada tarefa ou mensagem vazia
        """
        # Limpa área de scroll
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Seleciona tarefas conforme filtro
        fv = self.filter_var.get()
        if fv == "Pendentes":
            tasks = self.db.get_tasks(Status.PENDING)
        elif fv == "Concluídas":
            tasks = self.db.get_tasks(Status.COMPLETED)
        else:
            tasks = self.db.get_tasks()
        
        # Exibe
        if not tasks:
            self.empty_label.pack(expand=True, pady=50)
        else:
            # Ensure each item is a Task-like object (some DB implementations may return dicts)
            def _to_task(obj):
                from src.models.task import Task
                if isinstance(obj, dict):
                    try:
                        return Task(**obj)
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
