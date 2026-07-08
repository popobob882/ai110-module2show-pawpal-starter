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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
