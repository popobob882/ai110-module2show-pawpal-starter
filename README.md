# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- Add owners, pets, and care tasks (feeding, walks, meds, appointments) right from the app
- Smart scheduling: tasks are sorted by priority first, then by time, so the important stuff shows up first
- Time-only sorting, for when you just want to see the day in order
- Filter tasks by pet or by whether they're done yet
- Conflict warnings: if two tasks overlap in time, the app flags it instead of quietly double-booking you
- Recurring tasks: mark a daily or weekly task complete and the next one gets scheduled automatically

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule:
- [HIGH] 08:00 - Morning feeding for Mochi (10 min)
- [HIGH] 10:00 - Vet checkup for Rex (45 min)
- [MEDIUM] 10:00 - Grooming for Mochi (30 min)
- [MEDIUM] 18:00 - Evening walk for Rex (30 min)

Sorted purely by time:
- 08:00 Morning feeding (Mochi)
- 10:00 Grooming (Mochi)
- 10:00 Vet checkup (Rex)
- 18:00 Evening walk (Rex)

Rex's tasks only (filter by pet):
- Evening walk
- Vet checkup

Conflicts found:
- Grooming overlaps with Vet checkup

Completing the recurring feeding task...
'Morning feeding' done for 2026-07-07; next one scheduled for 2026-07-08.

Incomplete tasks for Mochi (filter by completion status):
- Grooming (due 2026-07-07)
- Morning feeding (due 2026-07-08)
```

## 🧪 Testing PawPal+

Run the suite with:

```bash
python -m pytest
```

`tests/test_pawpal.py` covers both the "happy path" behaviors and a handful of edge cases:

- Marking a task complete updates its status
- Adding a task to a pet increases that pet's task count
- `sort_by_time` puts tasks in chronological order, and pushes tasks with no preferred time to the end
- `filter_tasks` narrows a task list down by pet name and by completion status
- `detect_conflicts` flags two tasks that overlap in time, but does *not* flag two tasks that are simply back-to-back
- Completing a recurring task returns the next occurrence, one day later for `daily` and seven days later for `weekly`; a non-recurring task returns `None`
- Empty-input edge cases: a pet with no tasks, an owner with no pets, and every `Scheduler` method given an empty list

Sample test output:

```
tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 15%]
tests/test_pawpal.py::test_sort_by_time_orders_earliest_first PASSED     [ 23%]
tests/test_pawpal.py::test_filter_tasks_by_pet_and_completion PASSED     [ 30%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_times PASSED [ 38%]
tests/test_pawpal.py::test_mark_complete_on_recurring_task_returns_next_occurrence PASSED [ 46%]
tests/test_pawpal.py::test_mark_complete_on_weekly_recurring_task_adds_seven_days PASSED [ 53%]
tests/test_pawpal.py::test_mark_complete_on_non_recurring_task_returns_none PASSED [ 61%]
tests/test_pawpal.py::test_pet_with_no_tasks_has_empty_task_list PASSED  [ 69%]
tests/test_pawpal.py::test_owner_with_no_pets_has_no_tasks PASSED        [ 76%]
tests/test_pawpal.py::test_scheduler_handles_empty_task_list PASSED      [ 84%]
tests/test_pawpal.py::test_adjacent_back_to_back_tasks_do_not_conflict PASSED [ 92%]
tests/test_pawpal.py::test_tasks_without_a_preferred_time_sort_last PASSED [100%]

============================= 13 passed in 0.06s ==============================
```

**Confidence level:** ⭐⭐⭐⭐☆ (4/5) — the core sorting, filtering, conflict, and recurrence logic is well covered and passing. What would push this to a 5: tests around the `app.py`/`st.session_state` wiring itself, and conflict detection across midnight (e.g. a task at 23:45 running past 00:00).

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (by priority) | Scheduler.build_schedule | Sorts by priority (high > medium > low) first, then by preferred time |
| Task sorting (by time) | Scheduler.sort_by_time | Sorts purely by preferred time, ignoring priority |
| Filtering | Scheduler.filter_tasks | Narrows a task list down by pet name and/or completion status |
| Conflict handling | Scheduler.detect_conflicts | Flags any two tasks whose time + duration windows overlap; returns the pairs instead of raising |
| Recurring tasks | Task.mark_complete, Task._next_occurrence | Completing a recurring task returns a new Task due one interval later (daily -> +1 day, weekly -> +7 days)

## 📸 Demo Walkthrough

1. Set the owner's name (and optional email) at the top of the page.
2. Add a pet: type a name, pick a species, and click "Add pet." Add a second pet too - they both show up in a table right away.
3. Add a task for a pet: title, type, duration, priority, and a preferred time, then click "Add task." Add a few tasks across your pets, including two at the same time, so there's something for the conflict check to catch later.
4. Use the "Filter by pet" and "Filter by status" dropdowns above the task table to narrow down what you're looking at - the table underneath is also sorted by time automatically.
5. Click "Generate schedule" to see the full day sorted by priority-then-time. If any tasks overlap, a warning lists exactly which ones and when; otherwise you get a success message saying the schedule is conflict-free.

This walkthrough shows off the main Scheduler behaviors: priority+time sorting (`build_schedule`), time-only sorting (`sort_by_time`), pet/status filtering (`filter_tasks`), and conflict warnings (`detect_conflicts`). Recurring tasks (completing a daily/weekly task to generate its next occurrence) are demonstrated in `main.py` rather than the UI - see the CLI output below.

Sample CLI output from `python main.py`:

```
Today's Schedule:
- [HIGH] 08:00 - Morning feeding for Mochi (10 min)
- [HIGH] 10:00 - Vet checkup for Rex (45 min)
- [MEDIUM] 10:00 - Grooming for Mochi (30 min)
- [MEDIUM] 18:00 - Evening walk for Rex (30 min)

Sorted purely by time:
- 08:00 Morning feeding (Mochi)
- 10:00 Grooming (Mochi)
- 10:00 Vet checkup (Rex)
- 18:00 Evening walk (Rex)

Rex's tasks only (filter by pet):
- Evening walk
- Vet checkup

Conflicts found:
- Grooming overlaps with Vet checkup

Completing the recurring feeding task...
'Morning feeding' done for 2026-07-07; next one scheduled for 2026-07-08.

Incomplete tasks for Mochi (filter by completion status):
- Grooming (due 2026-07-07)
- Morning feeding (due 2026-07-08)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
