from datetime import timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


# --- Happy paths ---

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


def test_mark_complete_on_weekly_recurring_task_adds_seven_days():
    task = Task(
        "Flea treatment", "medication", 5, "medium", recurring=True, recurrence_rule="weekly"
    )
    original_due_date = task.due_date

    next_task = task.mark_complete()

    assert next_task.due_date == original_due_date + timedelta(weeks=1)


def test_mark_complete_on_non_recurring_task_returns_none():
    task = Task("One-time vet visit", "appointment", 45, "high")
    assert task.mark_complete() is None


# --- Edge cases ---

def test_pet_with_no_tasks_has_empty_task_list():
    pet = Pet("Ghost", "hamster")
    assert pet.tasks == []


def test_owner_with_no_pets_has_no_tasks():
    owner = Owner("Alex")
    assert owner.get_all_tasks() == []


def test_scheduler_handles_empty_task_list():
    scheduler = Scheduler()
    assert scheduler.build_schedule([]) == []
    assert scheduler.sort_by_time([]) == []
    assert scheduler.filter_tasks([]) == []
    assert scheduler.detect_conflicts([]) == []


def test_adjacent_back_to_back_tasks_do_not_conflict():
    scheduler = Scheduler()
    first = Task("Morning walk", "walk", 30, "medium", preferred_time="08:00")
    second = Task("Feeding", "feeding", 10, "high", preferred_time="08:30")
    assert scheduler.detect_conflicts([first, second]) == []


def test_tasks_without_a_preferred_time_sort_last():
    scheduler = Scheduler()
    anytime = Task("Play time", "walk", 15, "low")
    timed = Task("Feed", "feeding", 10, "high", preferred_time="08:00")
    assert scheduler.sort_by_time([anytime, timed]) == [timed, anytime]
