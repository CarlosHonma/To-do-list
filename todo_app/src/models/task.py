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

    def to_dict(self) -> dict:
        """Serialize Task to a JSON-serializable dict.

        - Enum fields are converted to their `.value`.
        - datetimes are converted to ISO strings (or None).
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": (self.priority.value if isinstance(self.priority, Priority) else self.priority),
            "status": (self.status.value if isinstance(self.status, Status) else self.status),
            "created_at": (self.created_at.isoformat() if self.created_at is not None else None),
            "completed_at": (self.completed_at.isoformat() if self.completed_at is not None else None),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dict loaded from storage.

        The loader is forgiving: it accepts priority/status as names,
        int values, or stored .value strings. For datetime values we try
        to parse ISO strings and fall back to None.
        """
        # Priority
        pr = data.get("priority")
        priority = None
        if pr is None or pr == "None":
            priority = Priority.MEDIUM
        else:
            try:
                priority = Priority(int(pr))
            except Exception:
                try:
                    priority = Priority[pr]
                except Exception:
                    # If it's already a Priority instance or unknown, default
                    if isinstance(pr, Priority):
                        priority = pr
                    else:
                        priority = Priority.MEDIUM

        # Status
        st = data.get("status")
        status = Status.PENDING
        if st is None:
            status = Status.PENDING
        else:
            try:
                status = Status(st)
            except Exception:
                try:
                    status = Status[st]
                except Exception:
                    # Leave as PENDING on failure
                    status = Status.PENDING

        # created_at / completed_at
        def _parse_dt(v):
            if v is None:
                return None
            if isinstance(v, datetime):
                return v
            if isinstance(v, str):
                try:
                    return datetime.fromisoformat(v)
                except Exception:
                    return None
            return None

        created_at = _parse_dt(data.get("created_at"))
        completed_at = _parse_dt(data.get("completed_at"))

        return cls(
            id=str(data.get("id") or ""),
            title=str(data.get("title") or ""),
            description=data.get("description"),
            priority=priority,
            status=status,
            created_at=created_at,
            completed_at=completed_at,
        )
