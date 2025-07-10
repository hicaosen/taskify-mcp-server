# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Taskify is an MCP (Model Context Protocol) server that provides AI-driven code generation capabilities. It acts as a bridge between high-level reasoning AI and specialized coding agents, enabling structured delegation of complex programming tasks.

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
ruff check

# Type checking (configured in pyproject.toml)
pyright

# Format code
ruff format
```

## Architecture

### Core Components

**MCP Server (`src/server.py`)**: The main application using FastMCP framework that exposes the `instruct_coding_agent` tool. This is a minimal implementation with a single tool that serves as a thinking framework for programming instruction construction.

**Project Structure**:
- `src/server.py`: Main MCP server implementation with the single tool
- `pyproject.toml`: Poetry configuration with dependencies and development tools
- `docs/mcp_development_memo.md`: Detailed MCP development documentation in Chinese

### Key Tool

**`instruct_coding_agent`**: A heuristic programming instruction construction tool that provides a thinking framework for analyzing user requests and converting them into clear programming instructions. The tool returns a simple activation message but its real value is in the comprehensive documentation that guides proper instruction construction.

### Framework Details

- **MCP Framework**: Uses FastMCP from the `mcp` library for server implementation
- **Language**: Python 3.12+ (specified in pyproject.toml)
- **Package Management**: Poetry with lockfile for dependency management
- **Development Tools**: Ruff for linting/formatting, Pyright for type checking

### Entry Point

The server is configured with a script entry point `taskify-mcp-server = "server:main"` that calls the `main()` function in `src/server.py`, which starts the MCP server.

## Development Philosophy

The codebase follows a "separation of concerns" approach where high-level AI focuses on understanding and planning while the programming agent handles implementation details. The tool is designed to foster structured communication between AI systems rather than direct code generation.