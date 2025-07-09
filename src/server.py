"""Taskify MCP Server"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("taskify")


@mcp.prompt()
def refine_requirement_prompt():
    """
    Guides a user to refine a high-level software requirement into a detailed specification
    by focusing on the underlying intent and problem space.
    """
    # --- 阶段一：探索问题与价值 (The "Why") ---
    intro = yield """你好！我将引导您一起发掘需求的深层价值。让我们从高阶目标开始。
请用一句话描述您希望通过这个需求达成什么效果？"""

    problem_to_solve = yield f"""了解，目标是“{intro}”。
那么，这个需求主要是为了解决当前存在的什么核心问题？或者说，是为了抓住什么样的机遇？"""

    pain_points = yield """说得好。那在没有这个功能的情况下，您的用户或团队正在经历哪些具体的痛点或不便之处？
（例如：流程繁琐、耗时过长、容易出错、信息不透明等）"""

    # --- 阶段二：定义用户与成功 (The "Who" and "How") ---
    user_persona = yield """非常具体，谢谢。接下来我们聚焦于“人”。
这个功能的核心用户是谁？可以简单描述一下典型的用户画像吗？（例如：他们的角色、目标、技术熟练度）"""

    success_metrics = yield f"""好的，我们为“{user_persona}”设计。
那么，当功能上线后，我们如何从数据或行为上客观地判断它是否成功了？
（请提供可衡量的指标，例如：将XX任务的完成时间从2小时缩短到15分钟）"""

    # --- 阶段三：构思解决方案 (The "What") ---
    user_journey = yield """清晰的成功指标很重要。现在让我们构思一下解决方案。
请描述一下用户在使用这个功能时的理想流程或用户旅程是怎样的？（从开始到结束的关键步骤）"""

    # --- 阶段四：明确边界与风险 (The "What If") ---
    constraints_and_risks = yield """谢谢，这让我们对功能有了更立体的认识。
最后，关于此功能，是否存在任何已知的技术限制、业务红线、或者您预见到的最大风险？"""

    # --- 阶段五：整合输出 ---
    final_spec = f"""
# 深度需求规格说明书 (DRD - Deep Requirement Document)

## 1. 背景与价值 (The "Why")
- **核心目标**: {intro}
- **待解决的问题/机遇**: {problem_to_solve}
- **主要痛点**: {pain_points}

## 2. 用户与成功 (The "Who" & "How")
- **核心用户画像**: {user_persona}
- **关键成功指标 (KPIs)**: {success_metrics}

## 3. 解决方案构思 (The "What")
- **理想用户旅程**: {user_journey}

## 4. 边界与风险 (The "What If")
- **已知约束与风险**: {constraints_and_risks}

"""
    return final_spec


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
