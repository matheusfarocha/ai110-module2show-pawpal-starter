from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Evening walk", duration_minutes=20, priority="medium", scheduled_time="18:00"))
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="07:00"))
    pet.add_task(Task(title="Playtime", duration_minutes=15, priority="medium", scheduled_time="12:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times)


def test_complete_daily_task_creates_next_occurrence():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog", age=3)
    today = date.today()
    task = Task(title="Morning walk", duration_minutes=20, priority="high", frequency="daily", due_date=today)
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    scheduler.complete_task(task, pet)

    tasks = pet.get_tasks()
    assert len(tasks) == 2
    assert tasks[1].completed is False
    assert tasks[1].due_date == today + timedelta(days=1)


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", scheduled_time="08:00"))
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
