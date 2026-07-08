# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

- User can add a pet (and who owns it)
- Can add a care task for a pet, such as feeding, walking, medication, or vet appointment
- Allow user to see a prioritized to-do list for today

**a. Initial design**

I ended up with 4 classes:

- **Owner** - the class that represents a person with their name/email and a list of their pets
- **Pet** - the class that represents the pet with its name, species, which owner it belongs to, and a list of its tasks
- **Task** - one task that needs to happen (feed, walk, meds, appointment). Has a duration, priority, preferred time, and whether it repeats
- **Scheduler** - the class that actually does the work: takes all the tasks and figures out the order, checks for conflicts, and explains the plan

Owner has Pets, Pets have Tasks, and Scheduler just works on top of whatever tasks it's given - it doesn't belong to Owner or Pet, it's more of a helper class.

**b. Design changes**

- I originally just had a recurring true/false field on Task, but that doesn't actually tell you how often it repeats (daily? weekly?). So I added a  field to say the frequency instead of just yes/no. Rest of the design stayed the same for now.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler mainly looks at priority and time. build_schedule sorts high priority tasks first, then breaks ties by preferred time. I went with priority first because things like meds usually matter more than something like grooming, even if grooming happens earlier in the day. Time still matters though, so I added sort_by_time as a separate method for when someone just wants to see the day in order, not by importance.

**b. Tradeoffs**

detect_conflicts only checks if two tasks' time + duration windows overlap at all. As a result, it doesn't know or care if the tasks are for the same pet or different pets. So two tasks for two different pets at the same time still count as a "conflict," even though in real life a friend or family member could handle one of them. I think that's a fair tradeoff for now, since the owner is probably the one doing everything themselves, and it keeps the conflict check simple (just compare start/end times) instead of having to model who else is available.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI the whole way through, but for different things at each stage. I used it to help me draw the UML at the start, as helping me write my pytest tests. I kept the testing phase in its own chat instead of continuing the implementation chat, which helped as it forced me to describe behaviors in plain English ("what happens if a pet has no tasks?") instead of just pointing at code, and that ended up surfacing edge cases I hadn't thought of yet such as the fact that adjacent tasks that shouldn't count as conflicts. I felt that the most useful prompts to me were specific ones describing a specific scenario rahter than vague ones like "make this better."

**b. Judgment and verification**

One thing I rejected from AI was when it suggested the recurring tasks to just have a true/false recurring flag. I realized that completing a task would just leave it marked done. That's not actually useful as the app has no way to know if "recurring" means every day or every week. So I pushed back and added a recurrence_rule field and a due_date so completing a task can actually compute the next one. I verified this by writing tests for the exact edge cases I was worried about instead of trusting that the code "looked right."

---

## 4. Testing and Verification

**a. What you tested**

I tested the two "happy path" things I cared about most which were tasks getting sorted correctly (by priority and separately by time) and completing a recurring task creating the next one. Then I added edge cases: a pet with zero tasks, an owner with zero pets, every Scheduler method given an empty list, and two tasks that are back-to-back but shouldn't count as a conflict. I thought these mattered because the sorting/conflict/recurrence logic is the whole point of the app.

**b. Confidence**

Pretty confident - 13 tests pass and they cover both normal cases and the edge cases I could think of. If I had more time I'd want to test conflicts that cross midnight (like a task at 23:45 running into the next day) as it was something I didn't think about yet.

---

## 5. Reflection

**a. What went well**

I think the whole project went well. I think the part that went the best in my opinion was the testing portion as it didn't have huge errors that I needed to fix.

**b. What you would improve**
What I would probably improve on would be the due date as it exists on Task but the UI doesn't really use it as everything is framed as "today.If I had more time, I'd want the app to actually look at due dates, so recurring tasks show up on the right day instead of just accumulating.

**c. Key takeaway**

I think that what I would take away would be that I'm the main person designing the project and that I should be the main person making the decisions and not the AI. It should just be a tool to help me write code and brainstorm but I should be someone who still udnerstands whats going on and the person that makes all the choices.
