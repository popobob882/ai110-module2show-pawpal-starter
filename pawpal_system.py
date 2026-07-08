"""PawPal+ backend logic layer.

Phase 1: class skeletons only (names, attributes, empty method stubs).
Scheduling logic, conflict detection, and recurrence handling are implemented
in later phases.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Task:
    title: str
    task_type: str  # "feeding" | "walk" | "medication" | "appointment"
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    preferred_time: Optional[str] = None  # e.g. "08:00"
    recurring: bool = False
    recurrence_rule: Optional[str] = None  # e.g. "daily", "weekly" - needed once recurring=True
    pet_name: Optional[str] = None
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    owner_name: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, email: Optional[str] = None):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None):
        self.tasks: List[Task] = tasks or []

    def build_schedule(self, tasks: List[Task]) -> List[Task]:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        pass

    def explain_schedule(self, schedule: List[Task]) -> str:
        pass
