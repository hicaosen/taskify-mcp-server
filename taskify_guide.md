# Taskify AI Agent Usage Guide

## 1. Introduction

**What is Taskify?**
Taskify is a specialized MCP (Multi-purpose Co-pilot Protocol) server designed to act as an interface to a powerful programming agent. Its purpose is to receive structured instructions and delegate them to an agent capable of executing complex coding tasks.

**Who is this guide for?**
This guide is written for AI models and assistants who will interact with the Taskify system. It outlines how to effectively formulate instructions for the programming agent.

**What is the goal?**
The goal of this guide is to enable you, the AI assistant, to craft the most effective and efficient instructions possible, ensuring the programming agent can understand and execute the user's requests with precision.

## 2. The Core Tool: `instruct_coding_agent`

The primary and only tool you need to interact with Taskify is `instruct_coding_agent`.

**Function Signature:**
```python
instruct_coding_agent(agent_prompt: str) -> str
```

**Core Concept:**
The power of this tool lies entirely within the `agent_prompt` string. You can think of the tool itself as a simple registration mechanism; it formally passes your detailed instructions to the programming agent. The agent's success is therefore entirely dependent on the quality and clarity of the `agent_prompt` you provide.

## 3. Guiding Philosophy: You Are the Thinker

It is critical to understand that the Taskify system views you, the calling model, as the primary reasoning engine. The programming agent is an executor of well-defined plans; it does not perform the initial analysis or task decomposition.

**A Framework for Thought, Not a Rigid Template**
The instructions provided by the `instruct_coding_agent` tool's documentation are a "framework for thought." You must autonomously adapt your approach based on the user's request. Do not treat the recommendations as a rigid, unchangeable template.

**Adapt Detail to Complexity**
The core principle is to match the level of detail in your `agent_prompt` to the complexity of the task at hand.
*   A simple, self-contained request (e.g., "write a function to add two numbers") requires only a simple, direct instruction.
*   A complex, multi-component request (e.g., "build a task management API") requires a detailed, structured blueprint to guide the agent effectively.

Your ability to assess the user's intent and choose the appropriate level of detail is paramount to success.

## 4. How to Craft the `agent_prompt`

This section details the two primary approaches for constructing your `agent_prompt`, based on the task's complexity.

**A. For Simple, Self-Contained Tasks**

When the user's request is straightforward and can be accomplished with a single, clear action, your prompt should be direct and concise. Avoid over-engineering the instruction.

*   **Strategy:** State the requirement clearly and provide all necessary information in a single instruction.
*   **Example:**
    ```
    "Write a Python function named 'add' that takes two integers and returns their sum."
    ```

**B. For Complex, Multi-Component Tasks**

When the request involves multiple steps, components, or logical considerations, a structured and detailed blueprint is required. This approach ensures the agent has a clear and unambiguous plan to follow.

*   **Strategy:** Deconstruct the request into logical parts. Use the following recommended sections to structure your `agent_prompt`. These sections are recommendations, not rigid requirements; use them as needed to provide clarity.

*   **Recommended Sections:**

    *   **`Inferred Application Type & Tech Stack`**:
        *   **Purpose:** To set the high-level context for the agent.
        *   **Example:** `"I will build a simple Task Management Web API using Python and FastAPI."`

    *   **`Core Logic or Feature Breakdown`**:
        *   **Purpose:** To deconstruct the application into a list of specific, actionable features, functions, or classes. This is the heart of your instruction.
        *   **Example:**
            ```
            - A main.py file to set up the FastAPI app.
            - A GET endpoint at /tasks/ to list all tasks.
            - A POST endpoint at /tasks/ to create a new task.
            - An in-memory list to store the tasks.
            ```

    *   **`Key Data Structures`**:
        *   **Purpose:** To define the essential data models or objects the agent will need to work with.
        *   **Example:**
            ```
            - Task model should contain:
              - id: int (unique identifier)
              - title: str (the task description)
              - completed: bool (status of the task)
            ```

    *   **`Critical Constraints`**:
        *   **Purpose:** To mention any important constraints or non-negotiable requirements.
        *   **Example:** `"- Must not use any external database libraries; use a simple Python list for storage. - Must run on Python 3.9."`

*   **Complex Example (Putting it all together):**
    ```
    agent_prompt: '''
    **Application Type:**
    A simple Task Management Web API using Python and FastAPI.

    **Core Logic & Features:**
    1.  Create a `main.py` file.
    2.  Set up a basic FastAPI application instance.
    3.  Implement an in-memory list to serve as the database for tasks.
    4.  Define a `GET` endpoint at `/tasks` that returns the list of all tasks.
    5.  Define a `POST` endpoint at `/tasks` that accepts a new task, adds it to the list, and returns the newly created task.

    **Data Structures:**
    - The `Task` model should be a Pydantic model containing:
      - `id`: `int`
      - `title`: `str`
      - `completed`: `bool`

    **Constraints:**
    - Use only the `fastapi` and `uvicorn` libraries.
    - The ID for new tasks should be generated by incrementing the ID of the last task in the list.
    '''
    ```

## 5. Conclusion: Your Goal

Your primary objective when using Taskify is to generate the most effective and efficient `agent_prompt` possible for the given task.

*   **Efficiency** means not over-engineering your prompt. For simple tasks, a direct instruction is faster and clearer.
*   **Effectiveness** means providing sufficient detail for complex tasks. A well-structured prompt with a clear breakdown of logic, data structures, and constraints is the key to success on complex requests.

By mastering this balance, you will enable the programming agent to function at its highest capacity, delivering accurate and robust solutions.
