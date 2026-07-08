# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 14%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 28%]
tests/test_pawpal.py::test_sort_by_time_orders_earliest_first PASSED     [ 42%]
tests/test_pawpal.py::test_filter_tasks_by_pet_and_completion PASSED     [ 57%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_times PASSED [ 71%]
tests/test_pawpal.py::test_mark_complete_on_recurring_task_returns_next_occurrence PASSED [ 85%]
tests/test_pawpal.py::test_mark_complete_on_non_recurring_task_returns_none PASSED [100%]

============================== 7 passed in 0.04s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting (by priority) | Scheduler.build_schedule | Sorts by priority (high > medium > low) first, then by preferred time |
| Task sorting (by time) | Scheduler.sort_by_time | Sorts purely by preferred time, ignoring priority |
| Filtering | Scheduler.filter_tasks | Narrows a task list down by pet name and/or completion status |
| Conflict handling | Scheduler.detect_conflicts | Flags any two tasks whose time + duration windows overlap; returns the pairs instead of raising |
| Recurring tasks | Task.mark_complete, Task._next_occurrence | Completing a recurring task returns a new Task due one interval later (daily -> +1 day, weekly -> +7 days)

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
