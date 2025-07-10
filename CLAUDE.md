# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Taskify is an advanced MCP (Model Context Protocol) server that provides AI-driven programming thinking guidance. It serves as an intelligent mentor for large language models, helping them develop systematic and effective programming instruction construction skills through a 4-tool framework.

## Core Philosophy

The system follows a "thinking-first" approach where AI models learn to:
- Analyze programming tasks systematically
- Apply stage-based thinking frameworks
- Validate instruction quality before execution
- Adapt thinking strategies to task complexity

## Tool Architecture

### 🎓 Smart Programming Coach (Entry Point)
**Tool**: `smart_programming_coach`
**Purpose**: Meta-tool that guides how to use the other tools effectively

**Usage Patterns**:
```python
# For any new programming task, start here
smart_programming_coach("your programming request", project_context="", mode="full_guidance")
```

### 🧠 Core Analysis Engine
**Tool**: `analyze_programming_context`
**Purpose**: Intelligent task analysis and framework generation

**Key Features**:
- Auto-detects 7 task types (new_feature, bug_fix, refactor, performance, testing, documentation, maintenance)
- Evaluates complexity (simple/medium/complex)
- Generates 4-stage thinking frameworks (understanding → planning → implementation → validation)

### 🎯 Thinking Process Guide
**Tool**: `guided_thinking_process`
**Purpose**: Step-by-step thinking guidance for each stage

**Workflow**:
1. Use `analyze_programming_context` first
2. Pass the JSON result to this tool
3. Progress through: understanding → planning → implementation → validation
4. Each stage provides specific questions, considerations, and examples

### ✅ Quality Validator
**Tool**: `validate_instruction_quality`
**Purpose**: Multi-dimensional instruction quality assessment

**Evaluation Criteria**:
- Clarity (0-1): Clear goals and actions
- Completeness (0-1): All necessary information included
- Specificity (0-1): Concrete technical details
- Actionability (0-1): Clear executable steps
- Risk Awareness (0-1): Considers testing, errors, compatibility

## Recommended Workflows

### Simple Tasks (Quick fixes, small functions)
```
1. smart_programming_coach() → get workflow recommendation
2. analyze_programming_context() → understand task
3. [develop your instruction based on analysis]
4. validate_instruction_quality() → ensure quality
```

### Medium Tasks (Features, modules, APIs)
```
1. smart_programming_coach() → get complete workflow
2. analyze_programming_context() → get analysis framework
3. guided_thinking_process(json, "understanding") → deep comprehension
4. guided_thinking_process(json, "planning") → strategy development
5. guided_thinking_process(json, "implementation") → execution guidance
6. [develop your instruction]
7. validate_instruction_quality() → final check
```

### Complex Tasks (Architecture, systems, optimization)
```
1. smart_programming_coach() → get advanced workflow
2. analyze_programming_context() → comprehensive analysis
3. guided_thinking_process() → all 4 stages with deep thinking
4. [develop initial instruction]
5. validate_instruction_quality() → first quality check
6. [iterate and refine based on feedback]
7. validate_instruction_quality() → final validation
```

## Best Practices for AI Models

### 1. Always Start with the Coach
- Use `smart_programming_coach` as your entry point
- It will recommend the optimal workflow for your specific task
- Follow the suggested tool sequence and sample calls

### 2. Maintain Data Flow Integrity
- Always pass complete JSON results between tools
- Don't summarize or truncate the JSON when passing to next tool
- Each tool builds upon the previous tool's complete output

### 3. Think Before Acting
- Don't rush through the thinking stages
- Each stage should produce genuine insights
- Use the guiding questions to explore different angles

### 4. Quality-First Mindset
- Always validate your final instructions
- Aim for scores above 0.8 in all quality dimensions
- Iterate based on improvement suggestions

### 5. Adapt to Context
- Consider task complexity when choosing depth of analysis
- Learning scenarios need more explanation
- Production tasks need more risk assessment

## Development Commands

### Setup and Installation
```bash
# Install dependencies using Poetry
poetry install

# Run the MCP server
poetry run taskify

# Alternative using Poetry run
poetry run python src/server.py
```

### Development Tools
```bash
# Code linting (configured in pyproject.toml)
poetry run ruff check

# Type checking (configured in pyproject.toml)
poetry run pyright

# Format code
poetry run ruff format
```

## Architecture Details

### Core Components

**MCP Server (`src/server.py`)**: Advanced implementation with 4 intelligent tools using FastMCP framework.

**Tools Structure**:
- `smart_programming_coach`: Meta-orchestrator and workflow guide
- `analyze_programming_context`: Task analysis and framework generation engine
- `guided_thinking_process`: Stage-by-stage thinking guidance system
- `validate_instruction_quality`: Multi-dimensional quality assessment engine

**Project Structure**:
- `src/server.py`: Complete MCP server with 4 intelligent tools
- `pyproject.toml`: Poetry configuration with dependencies and development tools
- `docs/mcp_development_memo.md`: Detailed MCP development documentation in Chinese

### Framework Details

- **MCP Framework**: Uses FastMCP from the `mcp` library for server implementation
- **Language**: Python 3.12+ (specified in pyproject.toml)
- **Package Management**: Poetry with lockfile for dependency management
- **Development Tools**: Ruff for linting/formatting, Pyright for type checking

### Entry Point

The server is configured with a script entry point `taskify-mcp-server = "server:main"` that calls the `main()` function in `src/server.py`, which starts the MCP server with all 4 tools available.

## Advanced Usage Examples

### Example 1: Feature Development
```python
# Step 1: Get workflow guidance
coach_result = smart_programming_coach("Implement user authentication with JWT tokens")

# Step 2: Analyze the task
analysis = analyze_programming_context("Implement user authentication with JWT tokens", "Express.js REST API")

# Step 3: Deep thinking through stages
understanding = guided_thinking_process(analysis, "understanding")
planning = guided_thinking_process(analysis, "planning") 
implementation = guided_thinking_process(analysis, "implementation")

# Step 4: Develop instruction based on insights
instruction = "Based on the analysis: implement JWT authentication..."

# Step 5: Validate quality
quality_report = validate_instruction_quality(instruction)
```

### Example 2: Performance Optimization
```python
# Complex task requiring iterative approach
coach_result = smart_programming_coach("Optimize database queries for 10x performance improvement", mode="expert_mode")

# Follow the recommended complex workflow...
# Multiple rounds of guided_thinking_process
# Quality validation and refinement
```

## Key Success Metrics

- **Instruction Quality Score**: Target >0.8 overall
- **Thinking Completeness**: All 4 stages thoroughly explored
- **Context Awareness**: Project constraints and technical requirements considered
- **Risk Mitigation**: Testing, error handling, and compatibility addressed

The goal is to develop AI models that can think like experienced technical leads: systematic, thorough, and quality-focused.