# Plan Manager MCP Service 规划文档

## 1. 核心理念

本服务旨在提供一个**通用的计划容器 (Universal Plan Container)**，支持用户通过语音（自然语言）交互来管理各种类型的计划。

**核心设计哲学**:
*   **万物皆任务 (Everything is a Task)**: 无论是宏大的“21天习惯养成”，还是微小的“买牛奶”，在底层都是统一的数据节点。
*   **灵活的元数据 (Flexible Metadata)**: 通过 JSON 字段存储特定场景的数据（如旅游的地点、学习的资源链接），实现“一个模型，无限形态”。

## 2. 数据模型 (Schema)

采用单表树形结构，实现无限层级和灵活扩展。

**表名**: `items` (或 `nodes`)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | INTEGER | 主键，自增 ID |
| `parent_id` | INTEGER | 父节点 ID (可为空)，指向父任务，实现层级关系 |
| `name` | TEXT | 任务/计划名称 |
| `description` | TEXT | 详细描述 |
| `status` | TEXT | 状态: `pending`, `in_progress`, `completed`, `cancelled` |
| `scheduled_at` | TEXT | 计划执行时间 (ISO 8601 格式) |
| `deadline` | TEXT | 截止时间 (ISO 8601 格式) |
| `category` | TEXT | 分类标签: `travel`, `study`, `habit`, `work`, `general` |
| `metadata` | TEXT | JSON 字符串，存储自定义字段 (如 `{"location": "Tokyo", "budget": 20000}`) |
| `created_at` | TEXT | 创建时间 |
| `updated_at` | TEXT | 更新时间 |

## 3. MCP 工具 (Tools) 规划

提供一套原子化的操作工具，供 LLM 灵活组合使用。

### 3.1 基础操作
*   **`create_item`**: 创建单个任务/计划节点。
    *   参数: `name`, `parent_id`, `category`, `scheduled_at`, `metadata`, `description`
*   **`delete_item`**: 删除任务（及其子任务）。
    *   参数: `item_id`
*   **`update_item`**: 更新任务属性（改名、改时间、改状态、更新元数据）。
    *   参数: `item_id`, `name`, `status`, `scheduled_at`, `metadata`, ...
*   **`get_item`**: 获取单个任务详情。
    *   参数: `item_id`

### 3.2 高级/批量操作
*   **`add_sub_items`**: 批量添加子任务（适用于生成“一周计划”或“21天打卡”）。
    *   参数: `parent_id`, `items` (List of objects)
*   **`query_items`**: 通用查询接口。
    *   参数: `category`, `status`, `start_date`, `end_date`
*   **`get_tree`**: 获取结构化视图（查看整个计划树）。
    *   参数: `root_id`

## 4. 场景演示

### 场景 A: 21天习惯养成
*   **LLM 操作**:
    1.  `create_item(name="21天早起挑战", category="habit", metadata={"target": 21})` -> 得到 `id=100`
    2.  `add_sub_items(parent_id=100, items=[{"name": "Day 1", "scheduled_at": "2025-12-01"}, ...])`

### 场景 B: 旅游计划
*   **LLM 操作**:
    1.  `create_item(name="日本游", category="travel")` -> `id=200`
    2.  `add_sub_items(parent_id=200, items=[{"name": "东京站", "metadata": {"hotel": "Hilton"}}, {"name": "大阪站"}])`

### 场景 C: 一周学习计划
*   **LLM 操作**:
    1.  `create_item(name="Python 进阶周", category="study")` -> `id=300`
    2.  `add_sub_items(parent_id=300, items=[{"name": "周一：装饰器", "scheduled_at": "2025-12-08"}, ...])`

## 5. 技术栈 (Python)

*   **Runtime**: Python 3.10+
*   **Framework**: `mcp[cli]` (FastMCP)
*   **Database**: SQLite3 (标准库)
*   **Environment**: `uv` 或 `venv` 管理虚拟环境
