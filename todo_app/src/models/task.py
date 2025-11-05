from dataclasses import dataclass
from datetime import datetime
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    """Possible task statuses."""
    PENDING = "Pending"
    COMPLETED = "Completed"


@dataclass
class Task:
    """Represents an individual task in the to-do list."""

    id: str
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Ensure created_at is set when a Task is instantiated."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def mark_completed(self):
        """Marks the task as completed and sets the completed_at timestamp."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()

    def mark_pending(self):
        """Marks the task as pending and clears the completed_at timestamp."""
        self.status = Status.PENDING
        self.completed_at = None
