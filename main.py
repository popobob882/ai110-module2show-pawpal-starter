"""CLI demo: build an owner, some pets and tasks, and exercise the scheduling logic."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan", "jordan@example.com")

    mochi = Pet("Mochi", "cat")
    rex = Pet("Rex", "dog")
    owner.add_pet(mochi)
    owner.add_pet(rex)

    # Added out of time order on purpose, to prove sort_by_time actually sorts.
    rex.add_task(Task("Evening walk", "walk", 30, "medium", "18:00"))
    mochi.add_task(
        Task("Morning feeding", "feeding", 10, "high", "08:00", recurring=True, recurrence_rule="daily")
    )
    rex.add_task(Task("Vet checkup", "appointment", 45, "high", "10:00"))
    # Same time as the vet checkup, on purpose, so detect_conflicts has something to catch.
    mochi.add_task(Task("Grooming", "appointment", 30, "medium", "10:00"))

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()

    print(scheduler.explain_schedule(scheduler.build_schedule(all_tasks)))

    print("\nSorted purely by time:")
    for task in scheduler.sort_by_time(all_tasks):
        print(f"- {task.preferred_time} {task.title} ({task.pet_name})")

    print("\nRex's tasks only (filter by pet):")
    for task in scheduler.filter_tasks(all_tasks, pet_name="Rex"):
        print(f"- {task.title}")

    print()
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        print("Conflicts found:")
        for task_a, task_b in conflicts:
            print(f"- {task_a.title} overlaps with {task_b.title}")
    else:
        print("No conflicts found.")

    print("\nCompleting the recurring feeding task...")
    feeding_task = mochi.tasks[0]
    next_occurrence = feeding_task.mark_complete()
    if next_occurrence:
        mochi.add_task(next_occurrence)
        print(
            f"'{feeding_task.title}' done for {feeding_task.due_date}; "
            f"next one scheduled for {next_occurrence.due_date}."
        )

    print("\nIncomplete tasks for Mochi (filter by completion status):")
    for task in scheduler.filter_tasks(mochi.tasks, completed=False):
        print(f"- {task.title} (due {task.due_date})")


if __name__ == "__main__":
    main()
