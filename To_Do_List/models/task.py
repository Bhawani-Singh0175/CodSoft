from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    title: str
    description: str
    due_date: str
    priority: str
    labels: str
    completed: bool = False
    id: Optional[int] = None
    created_at: Optional[str] = None
