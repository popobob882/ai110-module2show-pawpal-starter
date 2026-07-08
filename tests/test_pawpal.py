from pawpal_system import Task, Pet


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
