import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Setup ---
st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=60)

if st.button("Save Owner"):
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    st.success(f"Owner '{owner_name}' saved.")

if st.session_state.owner is None:
    st.info("Save an owner to get started.")
    st.stop()

owner = st.session_state.owner

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(pet)
    st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Your pets:", [p.name for p in owner.pets])

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])

    if st.button("Add Task"):
        task = Task(title=task_title, duration_minutes=int(duration), priority=priority, frequency=frequency)
        selected_pet.add_task(task)
        st.success(f"Added '{task_title}' to {selected_pet_name}.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([
            {"pet": p.name, "task": t.title, "duration": t.duration_minutes, "priority": t.priority, "frequency": t.frequency}
            for p in owner.pets for t in p.get_tasks()
        ])

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    if not owner.get_all_tasks():
        st.warning("No tasks added yet.")
    else:
        scheduler = Scheduler(owner=owner)
        st.text(scheduler.explain_plan())
