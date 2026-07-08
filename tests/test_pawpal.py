from datetime import timedelta

from pawpal_system import Task, Pet, Scheduler


def test_mark_complete_changes_status():
    task = Task("Walk", "walk", 20, "medium")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "cat")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feed", "feeding", 10, "high"))
    assert len(pet.tasks) == 1


def test_sort_by_time_orders_earliest_first():
    scheduler = Scheduler()
    late = Task("Walk", "walk", 20, "medium", preferred_time="18:00")
    early = Task("Feed", "feeding", 10, "high", preferred_time="08:00")
    result = scheduler.sort_by_time([late, early])
    assert result == [early, late]


def test_filter_tasks_by_pet_and_completion():
    scheduler = Scheduler()
    mochi_task = Task("Feed", "feeding", 10, "high", pet_name="Mochi")
    rex_task = Task("Walk", "walk", 20, "medium", pet_name="Rex", completed=True)

    assert scheduler.filter_tasks([mochi_task, rex_task], pet_name="Mochi") == [mochi_task]
    assert scheduler.filter_tasks([mochi_task, rex_task], completed=True) == [rex_task]


def test_detect_conflicts_flags_overlapping_times():
    scheduler = Scheduler()
    task_a = Task("Vet checkup", "appointment", 45, "high", preferred_time="10:00")
    task_b = Task("Grooming", "appointment", 30, "medium", preferred_time="10:00")
    conflicts = scheduler.detect_conflicts([task_a, task_b])
    assert conflicts == [(task_a, task_b)]


def test_mark_complete_on_recurring_task_returns_next_occurrence():
    task = Task(
        "Morning feeding", "feeding", 10, "high", recurring=True, recurrence_rule="daily"
    )
    original_due_date = task.due_date

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == original_due_date + timedelta(days=1)


def test_mark_complete_on_non_recurring_task_returns_none():
    task = Task("One-time vet visit", "appointment", 45, "high")
    assert task.mark_complete() is None
