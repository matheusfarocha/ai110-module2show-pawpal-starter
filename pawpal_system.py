from dataclasses import dataclass, field
from typing import List
from datetime import date, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", "high"
    frequency: str = "daily"  # "daily", "weekly", "as needed"
    scheduled_time: str = ""  # "HH:MM" format, e.g. "08:30"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Return a fresh copy of this task with due_date advanced by frequency interval."""
        delta = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        next_due = self.due_date + delta.get(self.frequency, timedelta(days=0))
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_time=self.scheduled_time,
            due_date=next_due,
            completed=False,
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> List[Task]:
        """Return tasks sorted by priority that fit within available time."""
        all_tasks = self.owner.get_all_tasks()
        pending = [t for t in all_tasks if not t.completed]
        sorted_tasks = sorted(pending, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

        schedule = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                schedule.append(task)
                time_used += task.duration_minutes

        return schedule

    def complete_task(self, task: Task, pet: Pet) -> None:
        """Mark a task complete and schedule the next occurrence if it recurs."""
        task.mark_complete()
        if task.frequency in ("daily", "weekly"):
            pet.add_task(task.next_occurrence())

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any tasks that share the same scheduled_time."""
        schedule = self.generate_schedule()
        timed = [t for t in schedule if t.scheduled_time]
        warnings = []
        for i, a in enumerate(timed):
            for b in timed[i + 1:]:
                if a.scheduled_time == b.scheduled_time:
                    warnings.append(
                        f"WARNING: '{a.title}' and '{b.title}' are both scheduled at {a.scheduled_time}."
                    )
        return warnings

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        results = []
        for pet in self.owner.pets:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def sort_by_time(self) -> List[Task]:
        """Sort scheduled tasks by their scheduled_time (HH:MM), putting unscheduled tasks last."""
        schedule = self.generate_schedule()
        return sorted(schedule, key=lambda t: t.scheduled_time if t.scheduled_time else "99:99")

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated schedule."""
        schedule = self.generate_schedule()
        if not schedule:
            return "No tasks could be scheduled within the available time."

        total = sum(t.duration_minutes for t in schedule)
        lines = [f"Schedule for {self.owner.name} ({total} min of {self.owner.available_minutes} min available):\n"]
        for task in schedule:
            lines.append(f"- {task.title} ({task.duration_minutes} min, {task.priority} priority, {task.frequency})")

        skipped = [t for t in self.owner.get_all_tasks() if t not in schedule and not t.completed]
        if skipped:
            lines.append("\nSkipped (not enough time):")
            for task in skipped:
                lines.append(f"- {task.title} ({task.duration_minutes} min)")

        return "\n".join(lines)
