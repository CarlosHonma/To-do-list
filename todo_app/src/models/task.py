from dataclasses import dataclass
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
    """It represents an individual task in the to=do list
    
    Attrbutes:
    	id: Unique identifier for the task.
     	title: Title of the task.
      	description: Detailed description of the task.
        priority: Priority level of the task.
        status: Current status of the task.(PENDING or COMPLETED)
        created_at: Timestamp when the task was created.
        completed_at: Timestamp when the task was completed (None if pending)."""
        

id: str
title: str
description: Optional[str] = None
priority: Priority = Priority.MEDIUM
status: Status = Status.PENDING
created_at: Optional[datetime] = None
completed_at: Optional[datetime] = None


def __post_init__(self):
    """Executed after __init__"""
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