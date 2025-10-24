import json
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from src.models.task import Priority, Status

class TaskDatabase:
    """It manages task storage and retrieval using a JSON file.
    
    Attributes:
    	db_path: Path to the JSON file storing tasks.
     	tasks: In-memory list of tasks."""
      
    def __init__(self, db_path: str = "tasks.json"):
        """It starts the database and loads existing tasks from the JSON file.
        
        Args:
			db_path: Path to the JSON file storing tasks."""
   
        self.db_path = Path(db_path)
        self.tasks = []
        self.load_tasks()
        
    def load_tasks(self):
        """It loads tasks from the JSON file into memory if it exists."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [self._dict_to_task(task_dict) for task_dict in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
                
    def save_tasks(self):
        """It saves all the tasks to the JSON file."""
        try:
            data = [self._task_to_dict(task) for task in self.tasks]
            # Use Path.open to write text; use lowercase 'w' for write mode
            with self.db_path.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    def add_task(self, title: str, description: Optional[str] = None, priority: Priority = Priority.MEDIUM) -> dict:
        """It creates a new task and adds it to the database.
        
        Args:
            title: Title of the task.
            description: Detailed description of the task.
            priority: Priority level of the task."""
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "priority": priority.value if isinstance(priority, Priority) else str(priority),
            "status": Status.PENDING.value,
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """It deletes a task by its ID.
        
        Args:
            task_id: Unique identifier of the task to delete.
            
        Returns:
            True if the task was found and deleted, False otherwise."""
        for i, task in enumerate(self.tasks):
            if task.get("id") == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def update_task(self, task: dict):
        """It updates an existing task in the database.

        Args:
            task: The task dict with updated information.
        """
        for i, existing_task in enumerate(self.tasks):
            if existing_task.get("id") == task.get("id"):
                self.tasks[i] = task
                self.save_tasks()
                return

    def get_tasks(self, status: Optional[Status] = None) -> List[dict]:
        """It retrieves all tasks, optionally filtered by status.

        Args:
            status: If provided, filters tasks by this status."""
        if status is not None:
            target = status.value
            return [task for task in self.tasks if task.get("status") == target]
        return self.tasks.copy()
    
    def _task_to_dict(self, task: dict) -> dict:
        """Convert task dict to dictionary (JSON serializable)."""
        # tasks are stored as dicts already; return a shallow copy to avoid mutation
        return dict(task)
    
    
    def _dict_to_task(self, data: dict) -> dict:
        """Normalize loaded dictionary to task dict."""
        # Ensure expected keys exist and return as-is (saved format uses simple primitives)
        return {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "priority": data.get("priority"),
            "status": data.get("status"),
            "created_at": data.get("created_at"),
            "completed_at": data.get("completed_at")
        }