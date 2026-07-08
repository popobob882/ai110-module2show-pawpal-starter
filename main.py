"""CLI demo: build an owner, some pets and tasks, and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Jordan", "jordan@example.com")

    mochi = Pet("Mochi", "cat")
    rex = Pet("Rex", "dog")
    owner.add_pet(mochi)
    owner.add_pet(rex)

    mochi.add_task(
        Task("Morning feeding", "feeding", 10, "high", "08:00", recurring=True, recurrence_rule="daily")
    )
    rex.add_task(Task("Evening walk", "walk", 30, "medium", "18:00"))
    rex.add_task(Task("Vet checkup", "appointment", 45, "high", "10:00"))

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()
    schedule = scheduler.build_schedule(all_tasks)

    print(scheduler.explain_schedule(schedule))

    conflicts = scheduler.detect_conflicts(all_tasks)
    print()
    if conflicts:
        print("Conflicts found:")
        for task_a, task_b in conflicts:
            print(f"- {task_a.title} overlaps with {task_b.title}")
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()
