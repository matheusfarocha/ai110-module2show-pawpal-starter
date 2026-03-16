from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner with 60 minutes available
owner = Owner(name="Jordan", available_minutes=60)

# Create pets
mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", frequency="daily"))
mochi.add_task(Task(title="Grooming", duration_minutes=30, priority="low", frequency="weekly"))

# Add tasks to Luna
luna.add_task(Task(title="Feeding", duration_minutes=5, priority="high", frequency="daily"))
luna.add_task(Task(title="Playtime", duration_minutes=15, priority="medium", frequency="daily"))
luna.add_task(Task(title="Vet checkup", duration_minutes=60, priority="medium", frequency="as needed"))

# Register pets with owner
owner.add_pet(mochi)
owner.add_pet(luna)

# Run scheduler
scheduler = Scheduler(owner=owner)

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)
