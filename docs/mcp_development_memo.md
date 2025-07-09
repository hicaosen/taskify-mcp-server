### **MCP (Model Context Protocol) Python SDK 开发备忘录**

#### **1. 核心目标与理念**

*   **目标**: MCP 旨在为大语言模型 (LLM) 与外部应用/工具的交互提供一个标准化的协议。它将“提供上下文”的逻辑与“LLM 交互”的逻辑解耦。
*   **核心理念**: 应用通过一个 MCP "服务器" 暴露其能力（如函数调用、数据查询），而 LLM 或其代理作为 "客户端" 来消费这些能力。这使得工具的定义和 LLM 的使用可以独立进行。
*   **Python SDK**: `mcp-sdk` 这个库简化了创建 MCP 服务器的流程，让我可以专注于实现工具的具体逻辑，而无需关心底层协议的细节。

#### **2. 关键概念**

*   **Server (`mcp.FastMCP`)**: MCP 应用的核心，用于注册和暴露工具和资源。
*   **Tool (`@mcp.tool()`)**: 一个可被 LLM 调用的函数。使用装饰器 `@mcp.tool()` 来定义。SDK 会自动根据函数的签名和文档字符串生成工具的元数据（schema）。
*   **Resource (`@mcp.resource()`)**: 一种可被 LLM 查询的数据源。使用装饰器 `@mcp.resource()` 定义，通常使用 URI 模板来标识资源。
*   **Prompt (`@mcp.prompt()`)**: 一个结构化的对话模板，用于引导模型完成多轮交互任务。

#### **3. 开发环境搭建**

1.  **创建项目目录**:
    ```bash
    mkdir my-mcp-tool && cd my-mcp-tool
    ```
2.  **初始化 Python 环境 (推荐使用 uv)**:
    ```bash
    uv init
    ```
3.  **安装 MCP SDK**:
    ```bash
    # 安装核心库和命令行工具
    uv add "mcp[cli]"
    ```
    如果使用 pip，则运行 `pip install "mcp[cli]"`。

#### **4. 详细开发步骤：创建一个简单的文件操作工具**

为了备忘，我将创建一个名为 `file_tool.py` 的工具，它将提供两个基本功能：`read_file` 和 `write_file`。

**步骤 1: 创建 `file_tool.py` 文件**

**步骤 2: 编写工具代码**

```python
# file_tool.py
import os
from mcp.server.fastmcp import FastMCP

# 1. 初始化 MCP 服务器
# 参数是此 MCP 应用的名称，会显示在客户端。
mcp = FastMCP("FileOperator")

# 2. 定义第一个工具：读取文件
@mcp.tool()
def read_file(path: str) -> str:
    """
    Reads the content of a file at the specified path.

    :param path: The absolute path to the file.
    :return: The content of the file.
    """
    if not os.path.exists(path):
        return f"Error: File not found at {path}"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

# 3. 定义第二个工具：写入文件
@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file at the specified path. Overwrites if the file exists.

    :param path: The absolute path to the file.
    :param content: The content to write to the file.
    :return: A success or error message.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file: {e}"

# 4. (可选) 添加一个资源示例
@mcp.resource("file://{path}/metadata")
def get_file_metadata(path: str) -> dict:
    """
    Get metadata for a file.
    """
    if not os.path.exists(path):
        return {"error": "File not found"}
    stat = os.stat(path)
    return {
        "size": stat.st_size,
        "modified_time": stat.st_mtime,
        "created_time": stat.st_ctime,
    }

```

**步骤 3: 运行 MCP 服务器**

在终端中，使用 `mcp` 命令行工具来运行这个文件。

```bash
# 'dev' 表示以开发模式运行，提供交互式检查器
# 'file_tool.py' 是我们的源文件
uv run mcp dev file_tool.py
```

**步骤 4: 如何与工具交互 (备忘)**

当服务器运行时，作为客户端，我会像下面这样发送请求来调用工具。

*   **调用 `read_file`**:
    *   **请求**:
        ```json
        {
          "tool": "read_file",
          "parameters": {
            "path": "/home/caosen/GitHub/taskify/README.md"
          }
        }
        ```
    *   **预期响应 (成功时)**:
        ```json
        {
          "result": "# Taskify
..."
        }
        ```

*   **调用 `write_file`**:
    *   **请求**:
        ```json
        {
          "tool": "write_file",
          "parameters": {
            "path": "/tmp/mcp_test.txt",
            "content": "Hello from MCP!"
          }
        }
        ```
    *   **预期响应 (成功时)**:
        ```json
        {
          "result": "Successfully wrote to /tmp/mcp_test.txt"
        }
        ```

#### **5. 总结与要点**

*   **装饰器是关键**: `@mcp.tool` 和 `@mcp.resource` 是将普通 Python 函数暴露为 MCP 能力的核心。
*   **类型提示很重要**: SDK 使用 Python 的类型提示 (e.g., `path: str`) 来自动生成工具的输入参数 schema。
*   **文档字符串是文档**: 函数的 docstring 会被用作工具的 `description`，这对于客户端（我）理解如何使用该工具至关重要。
*   **`mcp dev` 命令**: 这是开发和调试的利器，可以快速启动服务并提供一个交互式环境来测试工具。

---

#### **6. 进阶概念：`@mcp.prompt` - 定义交互式提示**

`@mcp.prompt` 是一个更高级的装饰器，用于定义结构化的、多轮的交互式对话模板。可以将其理解为一个“对话表单”或“引导式工作流”。

**核心特征**:
*   **引导式对话**: 定义一系列步骤（通常是问题），引导模型收集完成任务所需的所有信息。
*   **状态管理**: 在 Prompt 的生命周期内维护一个状态，跟踪已收集和待收集的信息。
*   **结构化输出**: 任务完成后，通常返回一个结构化的数据对象，可供其他 Tool 使用。

**适合场景**:
*   **复杂对象创建**: 如创建日历事件，需要依次询问标题、时间、参与人等。
*   **引导式工作流**: 如故障排查、用户注册等。
*   **需要澄清和确认的交互**: 在调用一个参数复杂的 Tool 前，用 Prompt 来澄清用户的意图。

**概念示例**:

```python
# 这是一个概念性的例子，具体实现可能略有不同
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Scheduler")

@mcp.prompt()
def create_event_prompt():
    """
    A prompt to guide the user in creating a new calendar event.
    """
    # 第一步：获取标题
    title = yield "What is the title of the event?"

    # 第二步：获取日期
    date = yield "What is the date of the event?"

    # 所有信息收集完毕，返回结构化结果
    return {"title": title, "date": date, "status": "confirmed"}

@mcp.tool()
def save_event_to_calendar(event_data: dict) -> str:
    """Saves the event to the calendar."""
    # ... 在这里调用日历API ...
    return f"Event '{event_data['title']}' saved successfully!"
```