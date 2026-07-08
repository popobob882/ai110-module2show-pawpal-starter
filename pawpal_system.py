"""PawPal+ backend logic layer.

Owner -> Pet -> Task, with Scheduler as a standalone helper that
sorts, filters, checks, and explains a set of tasks.
"""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional, Tuple

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    """A single pet care activity (feeding, walk, medication, appointment, etc.)."""

    title: str
    task_type: str  # "feeding" | "walk" | "medication" | "appointment"
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    preferred_time: Optional[str] = None  # e.g. "08:00"
    recurring: bool = False
    recurrence_rule: Optional[str] = None  # "daily" | "weekly" - used when recurring=True
    pet_name: Optional[str] = None
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task done. If it's recurring, return the next occurrence."""
        self.completed = True
        if not self.recurring:
            return None
        return self._next_occurrence()

    def _next_occurrence(self) -> "Task":
        """Build the next copy of this task, due one interval after this one."""
        interval = RECURRENCE_INTERVALS.get(self.recurrence_rule, timedelta(days=1))
        return replace(self, due_date=self.due_date + interval, completed=False)


@dataclass
class Pet:
    """A pet and the list of care tasks it needs."""

    name: str
    species: str
    owner_name: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name: str, email: Optional[str] = None):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        pet.owner_name = self.name
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Sorts, filters, checks, and explains a set of tasks."""

    def __init__(self, tasks: Optional[List[Task]] = None):
        self.tasks: List[Task] = tasks or []

    def build_schedule(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority (high first), then by preferred time."""

        def sort_key(task: Task) -> Tuple[int, str]:
            rank = PRIORITY_RANK.get(task.priority, len(PRIORITY_RANK))
            return (rank, task.preferred_time or "23:59")

        return sorted(tasks, key=sort_key)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted purely by their preferred time, ignoring priority."""
        return sorted(tasks, key=lambda task: task.preferred_time or "23:59")

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return tasks narrowed down by pet name and/or completion status."""
        result = tasks
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Return pairs of tasks whose time windows overlap (a lightweight warning,
        not an exception - callers decide what to do with the pairs)."""

        def to_minutes(hhmm: str) -> int:
            hours, minutes = hhmm.split(":")
            return int(hours) * 60 + int(minutes)

        timed = [t for t in tasks if t.preferred_time]
        intervals = [
            (to_minutes(t.preferred_time), to_minutes(t.preferred_time) + t.duration_minutes, t)
            for t in timed
        ]

        conflicts: List[Tuple[Task, Task]] = []
        for i in range(len(intervals)):
            start_a, end_a, task_a = intervals[i]
            for start_b, end_b, task_b in intervals[i + 1 :]:
                if start_a < end_b and start_b < end_a:
                    conflicts.append((task_a, task_b))
        return conflicts

    def explain_schedule(self, schedule: List[Task]) -> str:
        """Return a readable, line-by-line summary of a schedule."""
        lines = ["Today's Schedule:"]
        for task in schedule:
            time_str = task.preferred_time or "anytime"
            pet_str = f" for {task.pet_name}" if task.pet_name else ""
            lines.append(
                f"- [{task.priority.upper()}] {time_str} - {task.title}{pet_str} "
                f"({task.duration_minutes} min)"
            )
        return "\n".join(lines)
