"""Taskify MCP Server"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("taskify")


@mcp.prompt()
def refine_requirement_prompt():
    """
    Guides a user to refine a high-level software requirement into a detailed specification.
    """
    # 1. 收集基本信息
    high_level_goal = yield "请用一句话描述这个高阶需求的核心目标是什么？"
    target_users = yield f"好的，目标是'{high_level_goal}'。请问这个功能的主要目标用户是谁？"

    # 2. 挖掘功能细节
    key_features = yield "请列出为了实现这个目标，需要包含的关键功能点（3-5个）。"
    inputs = yield "用户需要提供哪些输入信息来使用这些功能？"
    outputs = yield "功能完成后，系统会产生哪些输出或结果？"

    # 3. 定义成功标准
    success_criteria = yield "当满足哪些具体、可衡量的标准时，我们才能认为这个需求已经成功实现了？"
    constraints = yield "是否有任何已知的技术、性能或设计约束？（如果没有请回答“无”）"

    # 4. 整合并生成详细需求
    detailed_spec = f"""
# 详细需求规格说明

## 1. 核心目标
{high_level_goal}

## 2. 目标用户
{target_users}

## 3. 关键功能点
{key_features}

## 4. 输入与输出
- **输入**: {inputs}
- **输出**: {outputs}

## 5. 成功标准 (Acceptance Criteria)
{success_criteria}

## 6. 已知约束
{constraints}
"""
    return detailed_spec


@mcp.tool()
def save_spec_to_file(filename: str, content: str) -> str:
    """Saves the detailed specification to a markdown file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Specification saved to {filename}"
    except IOError as e:
        return f"Error saving file: {e}"


def main():
    """Main entry point to run the MCP server."""
    mcp.run()
