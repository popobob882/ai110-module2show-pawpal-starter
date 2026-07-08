import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Add your pets and their care tasks below, then generate today's schedule.
"""
)

# Streamlit reruns this whole script top-to-bottom on every click, so the Owner
# has to live in st.session_state or it would be recreated (and emptied) each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="")

owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.email = st.text_input("Owner email (optional)", value=owner.email or "")

st.divider()

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name} the {species}.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    st.write("Pets:")
    st.table(
        [{"name": p.name, "species": p.species, "tasks": len(p.tasks)} for p in owner.pets]
    )

st.divider()

st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling a task.")
else:
    pet_names = [p.name for p in owner.pets]
    col1, col2, col3 = st.columns(3)
    with col1:
        task_pet = st.selectbox("Pet", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_type = st.selectbox("Type", ["feeding", "walk", "medication", "appointment"])
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        preferred_time = st.text_input("Preferred time (HH:MM)", value="08:00")

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == task_pet)
        pet.add_task(
            Task(
                title=task_title,
                task_type=task_type,
                duration_minutes=int(duration),
                priority=priority,
                preferred_time=preferred_time,
            )
        )
        st.success(f"Added '{task_title}' for {task_pet}.")

all_tasks = owner.get_all_tasks()
scheduler = Scheduler()

if all_tasks:
    st.write("All tasks:")

    pet_filter_options = ["All pets"] + [p.name for p in owner.pets]
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.selectbox("Filter by pet", pet_filter_options)
    with col2:
        status_filter = st.selectbox("Filter by status", ["All", "Incomplete", "Completed"])

    filtered_tasks = scheduler.filter_tasks(
        all_tasks,
        pet_name=None if pet_filter == "All pets" else pet_filter,
        completed=None if status_filter == "All" else status_filter == "Completed",
    )

    def _as_row(task: Task) -> dict:
        return {
            "pet": task.pet_name,
            "title": task.title,
            "time": task.preferred_time,
            "duration": task.duration_minutes,
            "priority": task.priority,
            "completed": task.completed,
        }

    if filtered_tasks:
        st.table([_as_row(t) for t in scheduler.sort_by_time(filtered_tasks)])
    else:
        st.info("No tasks match that filter.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = scheduler.build_schedule(all_tasks)
        st.table(
            [
                {
                    "priority": task.priority.upper(),
                    "time": task.preferred_time or "anytime",
                    "title": task.title,
                    "pet": task.pet_name,
                    "duration": task.duration_minutes,
                }
                for task in schedule
            ]
        )

        conflicts = scheduler.detect_conflicts(all_tasks)
        if conflicts:
            conflict_lines = "\n".join(
                f"- **{task_a.title}** ({task_a.pet_name}) overlaps with "
                f"**{task_b.title}** ({task_b.pet_name}) at {task_a.preferred_time}"
                for task_a, task_b in conflicts
            )
            st.warning(f"⚠️ Scheduling conflicts found:\n\n{conflict_lines}")
        else:
            st.success("No conflicts found. This schedule is good to go!")
