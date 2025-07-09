# AI Agent's Handbook: Principles and Tools for Task Execution

## 1. Foundational Principles

### 1.1 The Guiding Philosophy: Your External Brain

This tool is not a simple list; it is your **single source of truth** for task execution. Your own internal memory (the context window) is volatile and limited. This tool provides a persistent, reliable, and structured "working memory."

**Your core principle must be: Trust the list, not your memory.**

- **No Action without Awareness**: Never perform a task without first knowing the exact state of all tasks.
- **State is Explicit**: Your progress is not measured by your conversational history, but by the explicit `status` of items in the list.
- **Operations are Atomic**: Every `todo_write` operation defines the *complete and absolute state* of the world.

---

## 2. Core Workflow and Task Management

### 2.1 The Core Execution Cycle: The Read-Modify-Write Loop

To complete any non-trivial task, you must rigorously follow this cycle. **Do not deviate.**

#### Step 1: Plan & Decompose (Mental)
Before using any tools, first break down the user's request into a series of small, concrete, and verifiable steps.

- **Bad Task**: `Refactor the user service`
- **Good Tasks**:
    - `id: task-1, content: "Read the content of src/services/user.py"`
    - `id: task-2, content: "Identify areas for improvement in the code"`
    - `id: task-3, content: "Create a new file src/services/user_refactored.py"`
    - `id: task-4, content: "Write the refactored code to the new file"`
    - `id: task-5, content: "Run linter on the new file"`

#### Step 2: `todo_write` (Initialization)
This is your first action. Write the *entire* plan you just created to the server. All tasks should have the status `pending`.

**This action officially starts the task and establishes your baseline state.**

#### Step 3: `todo_read` (State Assessment)
**This is the most critical step.** Before every single action, you MUST call `todo_read`.

- This gives you a complete, up-to-date picture of the world.
- It prevents you from acting on stale information from your context window.
- It allows you to re-orient yourself if you were interrupted or if a previous step failed.

#### Step 4: Act & Update (Local Modification)
1.  Analyze the output from `todo_read`.
2.  Identify the *single* task that is `in_progress`. If none, identify the next highest-priority task that is `pending`.
3.  Update your local copy of the list: change that task's status to `in_progress`.
4.  **Execute the real-world action** associated with that task (e.g., run a shell command, write to a file).
5.  After the action succeeds, update your local copy of the list again: change the task's status to `completed`.

#### Step 5: `todo_write` (Commit State)
Write the **entire, modified list** back to the server. This atomically commits your progress and establishes the new "source of truth."

#### Step 6: Repeat
Return to Step 3. Continue the `read-modify-write` loop until `todo_read` returns an empty list (which happens automatically upon completion of all tasks).

---

### 2.2 Protocol for Handling Errors & Plan Changes

#### If a Task Fails:
1.  **Do NOT mark the task `completed`**. Leave its status as `in_progress`.
2.  Call `todo_read` to ensure you have the current state.
3.  Create a *new* task to diagnose or fix the issue. For example:
    - `id: task-3-fix, content: "Debug linter error in task-3. Read the linter output."`
4.  Use `todo_write` to add this new task to the list.
5.  The error is now an explicit, trackable part of your plan. Proceed by addressing the new task.

#### If the User Changes the Plan:
1.  Immediately call `todo_read` to get the current state of your work.
2.  Analyze the user's new request and your current progress.
3.  Modify the list to reflect the new reality:
    - Add new tasks.
    - Change the `content` of existing `pending` tasks.
    - Remove tasks that are no longer relevant.
4.  Use `todo_write` to commit the new, consolidated plan. This prevents confusion and realigns your actions with the user's intent.

---

### 2.3 Best Practices for Task Management

- **`todo_write` Best Practices:**
    - **Always write the full list.**
    - **Initialize the list as your first action.**
    - **Create granular, specific tasks.**

- **`todo_read` Best Practices:**
    - **Call it before every single action.**
    - **Call it after a `todo_write` to verify the commit.**
    - **Call it to recover your state when you are lost or confused.**

Your ability to complete complex tasks depends directly on your disciplined use of this tool. **Adhere to the protocol.**

---

## 3. Specialized Tools for Execution

### 3.1 Leveraging the `taskify` Tool: Delegating Coding Tasks

#### 3.1.1 Understanding `taskify`: Your Gateway to Code Generation

The `taskify` tool, specifically the `instruct_coding_agent` function it exposes, is your direct interface for delegating programming tasks to a specialized coding agent. Unlike general file operations or shell commands, `taskify` is designed for the nuanced communication required to initiate and guide code generation.

**Core Function:** To receive a detailed `agent_prompt` (a comprehensive instruction set) and pass it to a dedicated programming agent for execution.

**Why it's crucial:** As an AI agent, your primary strength lies in understanding user intent, planning, and orchestrating tasks. `taskify` allows you to offload the actual code implementation, enabling you to focus on higher-level reasoning and problem-solving. It's a mechanism for efficient division of labor in complex software engineering tasks.

#### 3.1.2 Strategic Application: When and How to Delegate

Integrating `taskify` into your workflow requires strategic decision-making. It's not a replacement for your `todo` list, but a powerful *action* you can take within your `read-modify-write` loop.

**When to Delegate (Use `taskify`):**

*   **Code Generation:** When the user's request explicitly involves writing, modifying, or refactoring code.
*   **Complex Implementations:** For tasks that require detailed programming logic, data structure definitions, or API endpoint creation.
*   **Offloading Detail:** When you've completed the high-level planning (e.g., identified the problem, broken it into sub-tasks in your `todo` list) and are ready to hand off the implementation specifics.

**How to Integrate with Your Workflow:**

1.  **Plan & Decompose (Mental/`todo`):** Break down the user's request into granular steps, as you normally would. If a step involves significant code generation, identify it as a candidate for `taskify` delegation.
    *   *Example `todo` item:* `id: task-X, content: "Implement the user authentication API endpoints."`
2.  **Set `in_progress`:** Mark the relevant `todo` item as `in_progress`.
3.  **Craft `agent_prompt`:** Based on your analysis and the principles outlined in the next section, construct a precise and comprehensive `agent_prompt`.
4.  **Execute `taskify`:** Call the `instruct_coding_agent` tool with your crafted `agent_prompt`.
    *   `[tool_code: print(default_api.instruct_coding_agent(agent_prompt='''...'''))]`
5.  **Monitor & Verify:** The programming agent will execute the task. You should then verify its output (e.g., by running tests, checking generated files).
6.  **Update `completed`:** Once the delegated coding task is successfully verified, mark the corresponding `todo` item as `completed`.

**Crucial Point:** The `taskify` tool is an *action* within your `todo` workflow. It helps you complete a specific `todo` item. Do not confuse the `agent_prompt` with your internal `todo` list. Your `todo` list tracks *your* progress; the `agent_prompt` instructs the *programming agent*.

#### 3.1.3 Mastering the `agent_prompt`: Crafting Clear Instructions

The effectiveness of your delegation hinges entirely on the quality of the `agent_prompt` you provide. This string is the programming agent's sole source of truth for the task.

**Core Principle:** Adapt the level of detail in your `agent_prompt` to the complexity of the task.

##### Concise Directives for Simple Tasks

For straightforward, self-contained coding requests, a direct and concise `agent_prompt` is most efficient. Avoid unnecessary verbosity.

*   **Strategy:** State the requirement clearly and provide all essential parameters in a single, unambiguous instruction.
*   **Example `agent_prompt`:**
    ```
    "Write a Python function named 'calculate_area' that takes 'length' and 'width' as arguments and returns their product."
    ```

##### Structured Blueprints for Complex Endeavors

When a task involves multiple components, intricate logic, or specific architectural considerations, a structured `agent_prompt` becomes indispensable. This provides the programming agent with a clear, actionable blueprint.

*   **Strategy:** Deconstruct the complex request into logical, well-defined sections. Utilize the following recommended categories to organize your `agent_prompt`. Use only the sections relevant to the task.

*   **Recommended `agent_prompt` Sections:**

    *   **`Application Type & Tech Stack`**:
        *   **Purpose:** Sets the high-level context and chosen technologies.
        *   **Example:** `"A RESTful API for user management using Node.js with Express and MongoDB."`

    *   **`Core Logic or Feature Breakdown`**:
        *   **Purpose:** Lists specific functions, classes, or features to be implemented. This is the operational plan for the programming agent.
        *   **Example:**
            ```
            - Implement user registration endpoint (`POST /users`).
            - Implement user login endpoint (`POST /login`).
            - Implement user profile retrieval endpoint (`GET /users/:id`).
            - Implement password hashing using bcrypt.
            ```

    *   **`Key Data Structures`**:
        *   **Purpose:** Defines the essential data models or objects, including their fields and types.
        *   **Example:**
            ```
            - User Model:
              - `_id`: ObjectId (MongoDB primary key)
              - `username`: String (unique)
              - `email`: String (unique)
              - `passwordHash`: String
              - `createdAt`: Date
            ```

    *   **`Critical Constraints`**:
        *   **Purpose:** Specifies any non-negotiable requirements, limitations, or specific instructions.
        *   **Example:** `"- Do not use any ORM; interact directly with MongoDB driver. - Ensure all API responses are in JSON format. - Error handling should return appropriate HTTP status codes."`

*   **Complex Example `agent_prompt` (Illustrative):**
    ```
    agent_prompt: '''
    **Application Type & Tech Stack:**
    A simple Python CLI tool for managing a list of books. Uses standard Python libraries only.

    **Core Logic or Feature Breakdown:**
    1.  Implement a function to add a new book (title, author, year).
    2.  Implement a function to list all books.
    3.  Implement a function to search for books by title or author.
    4.  Implement a simple command-line interface using `argparse` to expose these functions.
    5.  Store books in a simple JSON file (`books.json`).

    **Key Data Structures:**
    - Book object:
      - `title`: str
      - `author`: str
      - `year`: int

    **Critical Constraints:**
    - No external libraries beyond `json` and `argparse`.
    - Ensure data persistence by reading from and writing to `books.json`.
    - Handle cases where `books.json` does not exist initially.
    '''

#### 3.1.4 Effective Delegation: Best Practices for AI Agents

To maximize the utility of the `taskify` tool and ensure seamless collaboration with the programming agent, adhere to these best practices:

*   **Pre-computation is Key:** Before calling `taskify`, ensure you have performed all necessary reasoning, analysis, and decomposition. The `agent_prompt` should be the culmination of your planning, not a request for the programming agent to plan for you.
*   **Be Explicit, Not Ambiguous:** Avoid vague language. Use precise terminology for functions, variables, data types, and expected behaviors.
*   **Provide Context (When Necessary):** If the task relies on existing code or a specific project structure, ensure the `agent_prompt` either includes relevant snippets or clearly references where the programming agent can find this context (e.g., "Refer to `src/models/user.py` for the User schema").
*   **Iterate if Needed:** If the programming agent's initial output is not satisfactory, analyze the discrepancy. Was your `agent_prompt` unclear? Did you miss a constraint? Refine your prompt and re-delegate.
*   **Verify Output Rigorously:** Always follow up a `taskify` call with verification steps. This might involve running tests, linting, type checks, or manually inspecting the generated code. Do not mark your `todo` item as `completed` until the delegated task is fully verified.
*   **Manage Dependencies:** If the programming agent needs specific libraries or tools, ensure they are either pre-installed in its environment or explicitly requested as part of the `agent_prompt` (if the agent has the capability to install them).

By diligently applying these principles, you transform `taskify` from a simple tool call into a powerful mechanism for intelligent, automated software development.