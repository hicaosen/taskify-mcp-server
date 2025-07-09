# A Strategic Guide for AI Agents: Mastering Task Execution with `todo_read` and `todo_write`

## 1. The Guiding Philosophy: Your External Brain

This tool is not a simple list; it is your **single source of truth** for task execution. Your own internal memory (the context window) is volatile and limited. This tool provides a persistent, reliable, and structured "working memory."

**Your core principle must be: Trust the list, not your memory.**

- **No Action without Awareness**: Never perform a task without first knowing the exact state of all tasks.
- **State is Explicit**: Your progress is not measured by your conversational history, but by the explicit `status` of items in the list.
- **Operations are Atomic**: Every `todo_write` operation defines the *complete and absolute state* of the world.

---

## 2. The Core Execution Cycle: The Read-Modify-Write Loop

To complete any non-trivial task, you must rigorously follow this cycle. **Do not deviate.**

### **Step 1: Plan & Decompose (Mental)**
Before using any tools, first break down the user's request into a series of small, concrete, and verifiable steps.

- **Bad Task**: `Refactor the user service`
- **Good Tasks**:
    - `id: task-1, content: "Read the content of src/services/user.py"`
    - `id: task-2, content: "Identify areas for improvement in the code"`
    - `id: task-3, content: "Create a new file src/services/user_refactored.py"`
    - `id: task-4, content: "Write the refactored code to the new file"`
    - `id: task-5, content: "Run linter on the new file"`

### **Step 2: `todo_write` (Initialization)**
This is your first action. Write the *entire* plan you just created to the server. All tasks should have the status `pending`.

**This action officially starts the task and establishes your baseline state.**

### **Step 3: `todo_read` (State Assessment)**
**This is the most critical step.** Before every single action, you MUST call `todo_read`.

- This gives you a complete, up-to-date picture of the world.
- It prevents you from acting on stale information from your context window.
- It allows you to re-orient yourself if you were interrupted or if a previous step failed.

### **Step 4: Act & Update (Local Modification)**
1.  Analyze the output from `todo_read`.
2.  Identify the *single* task that is `in_progress`. If none, identify the next highest-priority task that is `pending`.
3.  Update your local copy of the list: change that task's status to `in_progress`.
4.  **Execute the real-world action** associated with that task (e.g., run a shell command, write to a file).
5.  After the action succeeds, update your local copy of the list again: change the task's status to `completed`.

### **Step 5: `todo_write` (Commit State)**
Write the **entire, modified list** back to the server. This atomically commits your progress and establishes the new "source of truth."

### **Step 6: Repeat**
Return to Step 3. Continue the `read-modify-write` loop until `todo_read` returns an empty list (which happens automatically upon completion of all tasks).

---

## 3. Protocol for Handling Errors & Plan Changes

### If a Task Fails:
1.  **Do NOT mark the task `completed`**. Leave its status as `in_progress`.
2.  Call `todo_read` to ensure you have the current state.
3.  Create a *new* task to diagnose or fix the issue. For example:
    - `id: task-3-fix, content: "Debug linter error in task-3. Read the linter output."`
4.  Use `todo_write` to add this new task to the list.
5.  The error is now an explicit, trackable part of your plan. Proceed by addressing the new task.

### If the User Changes the Plan:
1.  Immediately call `todo_read` to get the current state of your work.
2.  Analyze the user's new request and your current progress.
3.  Modify the list to reflect the new reality:
    - Add new tasks.
    - Change the `content` of existing `pending` tasks.
    - Remove tasks that are no longer relevant.
4.  Use `todo_write` to commit the new, consolidated plan. This prevents confusion and realigns your actions with the user's intent.

---

## 4. Summary of Best Practices

- **`todo_write` Best Practices:**
    - **Always write the full list.**
    - **Initialize the list as your first action.**
    - **Create granular, specific tasks.**

- **`todo_read` Best Practices:**
    - **Call it before every single action.**
    - **Call it after a `todo_write` to verify the commit.**
    - **Call it to recover your state when you are lost or confused.**

Your ability to complete complex tasks depends directly on your disciplined use of this tool. **Adhere to the protocol.**