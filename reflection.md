# PawPal+ Project Reflection

## 1. System Design
- add pet
- schedule walk
- see today's tasks
- request task recomendations
**a. Initial design**

The initial design included four classes:

- **Owner** — holds the owner's name and the total time available for pet care in a day. Responsible for managing which pets belong to the owner.
- **Pet** — holds basic info about the pet: name, species, and age. Has no behavior of its own; it exists to give the scheduler context about who is being cared for.
- **Task** — a dataclass representing a single care activity (e.g., walk, feeding, grooming). Stores the title, duration in minutes, priority level, category, and an optional reason explaining why the task matters.
- **Scheduler** — the core logic class. It holds a reference to the owner and pet, maintains a list of tasks, and is responsible for generating a daily schedule based on available time and task priority, as well as explaining the plan.

**b. Design changes**

Yes. The initial AI-generated UML included `preferences` and `set_available_time` on `Owner`, and a `needs` list with `get_needs()` on `Pet`. These were removed because `needs` was redundant with `Task`, and `preferences` was too vague to be useful without knowing how the scheduler would actually use it. `is_high_priority()` was also removed from `Task` since priority can be checked directly without a dedicated method.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
