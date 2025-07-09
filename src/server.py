"""Taskify MCP Server"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("taskify")


@mcp.tool()
def instruct_coding_agent() -> str:
    """
    This tool serves as a capability declaration for instructing a programming agent.
    Its value lies entirely in this documentation, which provides a mental framework
    for the calling model on how to construct a high-quality `agent_prompt`.

    **## Core Philosophy: A Framework for Thought, Not a Rigid Template ##**

    The calling model (you, the assistant) is responsible for all reasoning. You must
    autonomously adapt the detail and structure of the `agent_prompt` based on the
    context and complexity of the user's request. A simple request demands a simple
    instruction; a complex request requires a detailed blueprint. Do not rigidly
    apply a verbose structure to a simple problem.

    **## Recommended Reasoning Process for the Calling Model ##**

    Before calling this tool, you should follow this thought process:

    **1. Assess Complexity & Intent:**
    - First, deeply analyze the user's request. Is it a simple, self-contained task
      (e.g., "write a function to add two numbers"), or a complex, multi-component
      system (e.g., "build a task management API")?
    - What is the user's true underlying intent?

    **2. Select an Appropriate Level of Detail:**
    - **For simple requests:** A direct, concise instruction is best. For example:
      `"Write a Python function named 'add' that takes two integers and returns their sum."`
    - **For complex requests:** A more structured approach is necessary to guide the
      coding agent effectively. In this case, consider generating a prompt that includes
      some of the following sections, as needed.

    **3. (For Complex Requests) Key Sections to Consider:**
    - **Inferred Application Type & Tech Stack:** Briefly state the most logical type of
      application (e.g., Web API, CLI Tool) and a recommended technology stack
      (e.g., FastAPI, argparse). This sets a clear direction.
    - **Core Logic or Feature Breakdown:** Deconstruct the request into a list of
      specific, actionable features, functions, or classes to be implemented.
    - **Key Data Structures:** If applicable, define the essential data models or objects.
    - **Critical Constraints:** Mention any important constraints or non-negotiable
      requirements (e.g., "must not use external libraries", "must run on Python 3.8").

    **## Final Goal ##**
    Your goal is to generate the most effective and efficient `agent_prompt` possible.
    Efficiency means not over-engineering the instruction for a simple task. Effectiveness
    means providing sufficient detail for a complex task. This tool simply registers
    your final, reasoned instruction.
    """
    # This tool's implementation is intentionally trivial.
    # It trusts the calling model to have performed the necessary reasoning.
    return "Agent instruction registered. The programming agent can now proceed with the provided prompt."



def main():
    """Main entry point to run the MCP server."""
    mcp.run()