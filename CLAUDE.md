# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Taskify is an advanced MCP (Model Context Protocol) server that provides AI-driven programming thinking guidance. It serves as an intelligent mentor for large language models, helping them develop systematic and effective programming instruction construction skills through a 5-tool framework.

## ⚡ Major V2.0 Upgrades

### 🚀 Revolutionary Session Management
- **Zero JSON Transfer**: No more complex JSON passing between tools
- **Simple Session IDs**: Use lightweight session_id instead of massive JSON objects  
- **99%+ Success Rate**: Eliminates JSON parsing errors and tool call failures
- **Intelligent State**: Automatic progress tracking and context retention

### 🧠 Smart Learning System
- **Historical Learning**: Learns from previous tasks to provide better guidance
- **Similarity Detection**: Identifies similar past tasks and applies learned insights
- **Adaptive Frameworks**: Dynamically adjusts thinking frameworks based on task patterns
- **Context Memory**: Remembers project contexts and accumulates wisdom over time

### 📊 Enhanced Quality Assessment
- **6-Dimensional Analysis**: Added context alignment evaluation
- **Dynamic Scoring**: Adjusts evaluation criteria based on task type and complexity
- **Personalized Feedback**: Provides specific improvement suggestions
- **Quality Trends**: Tracks quality improvement over time

## Core Philosophy

The system follows a "thinking-first" approach where AI models learn to:
- Analyze programming tasks systematically
- Apply stage-based thinking frameworks
- Validate instruction quality before execution
- Adapt thinking strategies to task complexity

## Tool Architecture (5 Tools)

### 🎓 Smart Programming Coach (Entry Point)
**Tool**: `smart_programming_coach`
**Purpose**: Meta-tool that guides how to use the other tools effectively

**Usage Patterns**:
```python
# For any new programming task, start here
smart_programming_coach("your programming request", project_context="", mode="full_guidance")
```

### 🧠 Core Analysis Engine V2.0
**Tool**: `analyze_programming_context`
**Purpose**: Intelligent task analysis with session management

**Revolutionary Features**:
- ✨ Session-based state management
- 🧠 Historical task learning
- 📊 Similarity analysis and insights
- 🎯 Adaptive framework generation

**V2.0 Workflow**:
```python
# Creates session and returns lightweight session_id
result = analyze_programming_context("implement user authentication", "React + Node.js")
session_id = result["session_id"]  # Simple string like "session_abc123_1234567890"
```

### 🎯 Thinking Process Guide V2.0
**Tool**: `guided_thinking_process`
**Purpose**: Session-driven step-by-step thinking guidance

**Major Improvements**:
- ✅ Uses simple session_id instead of large JSON
- 🧠 Intelligent progress tracking
- 🎯 Context-aware adaptive hints
- 📊 Stage completion monitoring

**Simplified Workflow**:
```python
# No more complex JSON passing!
guided_thinking_process("session_abc123", "understanding")  # Super simple!
guided_thinking_process("session_abc123", "planning")      # Just session_id + stage
guided_thinking_process("session_abc123", "implementation") # No JSON errors!
guided_thinking_process("session_abc123", "validation")    # 99%+ success rate!
```

### ✅ Quality Validator V2.0
**Tool**: `validate_instruction_quality`
**Purpose**: Enhanced multi-dimensional instruction quality assessment

**New Features**:
- 🎯 Context-aware evaluation (uses session_id for precise analysis)
- 📊 6-dimensional quality metrics (added context alignment)
- 🧠 Dynamic scoring weights based on task characteristics
- 📈 Quality trend analysis and historical comparison
- 💡 Personalized improvement recommendations

**Enhanced Usage**:
```python
# Can use with session context for better evaluation
validate_instruction_quality("your instruction", session_id="session_abc123")
# Or standalone for general evaluation
validate_instruction_quality("your instruction")
```

### 🗂️ Session Manager (New!)
**Tool**: `session_manager`
**Purpose**: Intelligent session state management and monitoring

**Capabilities**:
- 📋 List all active sessions with progress tracking
- 🔍 Detailed session information and analytics
- 🗑️ Automatic cleanup of expired sessions
- 📊 Usage statistics and learning insights
- 🔄 Session reset and recovery options

**Usage Examples**:
```python
# List all active sessions
session_manager("list")

# Get detailed info about a specific session  
session_manager("detail", "session_abc123")

# View usage statistics and learning data
session_manager("stats")

# Clean up expired sessions
session_manager("cleanup")

# Reset a session to start over
session_manager("reset", "session_abc123")
```

## Recommended Workflows V2.0

### Simple Tasks (Quick fixes, small functions)
```
1. smart_programming_coach() → get workflow recommendation
2. analyze_programming_context() → get session_id 
3. guided_thinking_process(session_id, "understanding") → quick analysis
4. guided_thinking_process(session_id, "implementation") → direct to implementation
5. validate_instruction_quality(instruction, session_id) → quality check
```

### Medium Tasks (Features, modules, APIs)  
```
1. smart_programming_coach() → get complete workflow
2. analyze_programming_context() → get session_id + intelligent insights
3. guided_thinking_process(session_id, "understanding") → deep comprehension
4. guided_thinking_process(session_id, "planning") → strategy development  
5. guided_thinking_process(session_id, "implementation") → execution guidance
6. validate_instruction_quality(instruction, session_id) → context-aware validation
```

### Complex Tasks (Architecture, systems, optimization)
```
1. smart_programming_coach() → get advanced workflow
2. analyze_programming_context() → comprehensive analysis with learning insights
3. guided_thinking_process(session_id, "understanding") → thorough analysis
4. guided_thinking_process(session_id, "planning") → detailed strategy
5. guided_thinking_process(session_id, "implementation") → phased execution
6. guided_thinking_process(session_id, "validation") → comprehensive testing
7. validate_instruction_quality(instruction, session_id) → final quality check
8. [Optional] session_manager("stats") → review learning insights
```

## Best Practices for AI Models V2.0

### 1. Always Start with the Coach
- Use `smart_programming_coach` as your entry point
- It will recommend the optimal workflow for your specific task
- Follow the suggested tool sequence and session-based calls

### 2. Embrace Session-Based Workflow  
- Always save the session_id from `analyze_programming_context`
- Use session_id for all subsequent `guided_thinking_process` calls
- Pass session_id to `validate_instruction_quality` for context-aware evaluation
- Use `session_manager` to track progress and manage sessions

### 3. Leverage Intelligent Features
- Pay attention to similarity analysis and learning insights
- Use adaptive hints provided in each thinking stage
- Review quality trends to improve instruction writing over time
- Check session statistics to understand your task patterns

### 4. Maintain Session Continuity
- Don't lose session_ids - they contain valuable context
- Use `session_manager("list")` to find active sessions
- Use `session_manager("detail", session_id)` to resume interrupted work
- Sessions auto-expire after 1 hour for security

### 5. Quality-First Mindset
- Always validate your final instructions with session context
- Aim for scores above 0.8 in all quality dimensions
- Use personalized recommendations to improve specific weak areas
- Track quality trends to see improvement over time

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

# Test the tools functionality
python test_tools.py
```

## Architecture Details

### Core Components

**MCP Server (`src/server.py`)**: Advanced implementation with 5 intelligent tools using FastMCP framework.

**Tools Structure**:
- `smart_programming_coach`: Meta-orchestrator and workflow guide
- `analyze_programming_context`: Task analysis with session management and learning
- `guided_thinking_process`: Session-driven stage-by-stage thinking guidance  
- `validate_instruction_quality`: Enhanced multi-dimensional quality assessment
- `session_manager`: Intelligent session state management and analytics

**V2.0 State Management**:
- `_session_cache`: Active session storage with automatic cleanup
- `_context_memory`: Project context learning and familiarity tracking
- `_analysis_history`: Task history for similarity analysis and learning

### Framework Details

- **MCP Framework**: Uses FastMCP from the `mcp` library for server implementation
- **Language**: Python 3.12+ (specified in pyproject.toml)
- **Package Management**: Poetry with lockfile for dependency management
- **Development Tools**: Ruff for linting/formatting, Pyright for type checking

### Entry Point

The server is configured with a script entry point `taskify-mcp-server = "server:main"` that calls the `main()` function in `src/server.py`, which starts the MCP server with all 5 tools available.

## Advanced Usage Examples V2.0

### Example 1: Feature Development with Learning
```python
# Step 1: Get intelligent workflow guidance
coach_result = smart_programming_coach("Implement real-time chat feature")

# Step 2: Analyze with learning insights
analysis = analyze_programming_context("Implement real-time chat", "React + Socket.io")
session_id = analysis["session_id"]

# Step 3: Session-driven thinking (no JSON passing!)
understanding = guided_thinking_process(session_id, "understanding")
planning = guided_thinking_process(session_id, "planning") 
implementation = guided_thinking_process(session_id, "implementation")

# Step 4: Context-aware quality validation
quality_report = validate_instruction_quality(final_instruction, session_id)

# Step 5: Review learning insights
session_manager("detail", session_id)
```

### Example 2: Performance Optimization with History
```python
# Complex task with iterative approach
coach_result = smart_programming_coach("Optimize database queries for 10x performance", mode="expert_mode")

# Analysis with similarity detection
analysis = analyze_programming_context("Optimize database performance", "MySQL + 1M+ records")
session_id = analysis["session_id"]

# Check if similar tasks provide insights
if analysis["intelligent_insights"]["similarity_analysis"] != "未发现相似的历史任务":
    print("Found similar tasks with lessons learned!")

# Follow complete workflow with adaptive hints
# Multiple rounds of guided_thinking_process with session continuity
# Context-aware quality validation and refinement
```

### Example 3: Session Management and Recovery
```python
# List all active sessions to resume work
sessions = session_manager("list")

# Get detailed information about a specific session
details = session_manager("detail", "session_abc123")

# Check overall usage statistics and learning patterns
stats = session_manager("stats")

# Reset a session if needed to start over
reset_result = session_manager("reset", "session_abc123")
```

## Key Success Metrics V2.0

- **Tool Call Success Rate**: Target >99% (vs ~70% in V1.0)
- **Session Management Efficiency**: Lightweight session_id vs heavy JSON
- **Instruction Quality Score**: Target >0.8 overall with context awareness
- **Learning Effectiveness**: Similarity detection and adaptive improvements
- **Context Retention**: Project familiarity and accumulated insights
- **User Experience**: Simple session-based workflow vs complex JSON handling

## Migration from V1.0

### What Changed
- ❌ No more passing large JSON between tools
- ✅ Simple session_id based workflow  
- ❌ No more `task_analysis_json` parameter
- ✅ Enhanced quality evaluation with 6 dimensions
- ✅ New `session_manager` tool for state management
- ✅ Historical learning and similarity analysis

### Migration Steps
1. Replace `guided_thinking_process(large_json, stage)` with `guided_thinking_process(session_id, stage)`
2. Add session_id parameter to `validate_instruction_quality` for better evaluation
3. Use `session_manager` to track and manage sessions
4. Leverage new intelligent insights and adaptive features

The goal is to develop AI models that can think like experienced technical leads: systematic, thorough, quality-focused, and continuously learning from experience.