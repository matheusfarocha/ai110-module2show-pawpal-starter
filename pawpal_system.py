from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    category: str = ""
    reason: str = ""


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = []
        self.total_minutes: int = 0

    def add_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass
