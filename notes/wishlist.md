have the `/re*` commands that redo the ongoing constitution/spec/plan/tasks/implementation with the feedback

/reconstitution
/respecify
/replan
/retasks
/reimplement

---

store the specify state in the folder and allow switching of state using command. currently the highest spec number is taken for things like /plan, /tasks, /implement commands. if i want to switch from ongoing spec to other spec, i should be able to using a command

/switch <spec-id/spec-name>

for this, we can store the states in `.specify` folder as json/yaml

/status

to get you the current status of spec-kit


---

sub-agent based execution of tasks
- have tasks broken down into logical phases or batches, and executed/implemented by sub-agent, passing - correctness, completeness, agent log, agent ctx files

---

have `/next` command that auto-matically runs the next due command.
- if there are clarifications sorted in:
  - constitution, runs `/clarify-constitution`
  - in spec, runs `/clarify-spec`
  - in plan, runs `/clarify-plan`
  - in tasks, runs `/clarify-tasks`
- if currently developing a feature and
  - spec.md is generated, runs `/plan`
  - plan.md is generated, runs `/tasks`
  - tasks.md is generated, runs `/implement`

---

remove sequence numbers from Functional Requirements FR-1234
helps with replan being simpler
or we can have format FR-<EPIC>-<SEQUENCE>, where EPIC is like high level area, e.g. UI, AUTH etc.

---

have the process scale based on the changes required
if only bug fixes, should not require elaborate process
should scale adapt (source: bmad v6 https://www.youtube.com/watch?v=6LtrJD5Dz40)

---
keep all the user inputs as logs in the spec folder along with the phase, so if information about future phase provided can be passed and valuable information extracted

---
have the constitution changelog in separate files/folder

---

have the specs high level overview extracted and put in specs/CLAUDE.md so future specs can refer to if required

---

have a final review for best practices before /implement

---

have /explain that exlpains you the plan in phases using multi-turn conversations, and generates the explanation of next phase dynamically using the ongoing and conversation history

 we have generated the plan to implement adding local mode to spec-kit.  all the files generated are in git-staged. \
 \
 they are very hard to follow. Thoroughly analyze these files and conversationally explain to me the implementation plan
 without bogging me down with all the details. A few things you can do is have a holistic overview of the implementation
 plan, remove the duplicates, and cover the most core details while ignoring the details that are not applicable or are
not that important.  \
 \
ultrathink \
 \
 instead of explaining to me in one go, we will do it in phases. Divide the whole plan into logical phases. And present 
to me one phase at a time. Once I completely understand a phase that is presented, I will say "next". You will then
present me the next phase, incorporating the conversation we had in the previous phases and updating the next phase
accordingly.

---

