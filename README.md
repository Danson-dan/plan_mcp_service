# Plan Manager MCP Service

A powerful, universal plan management service for LLMs, built with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io).

This service allows AI agents to create, manage, and track any kind of plan—from travel itineraries and study schedules to 21-day habit challenges—using a flexible, tree-based task structure.

## Features

*   **Universal Schema**: "Everything is a Task". Supports infinite nesting (Plan -> Step -> Sub-step).
*   **Flexible Metadata**: Store structured JSON data for specific domains (e.g., travel budgets, resource URLs).
*   **Batch Operations**: Create complex schedules (like a weekly plan) in a single turn.
*   **Persistent Storage**: Uses SQLite (`plans.db`) for reliable, local data storage.

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install plan-mcp-service
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/yourusername/plan-mcp-service.git
```

### Option 3: Install from Source

```bash
git clone https://github.com/yourusername/plan-mcp-service.git
cd plan-mcp-service
pip install -e .
```

### Option 4: Run directly with `uv`

```bash
uv run src/plan_mcp_service/server.py
```

## Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/plan_mcp_service",
        "run",
        "plan-mcp-service"
      ]
    }
  }
}
```

*(Note: Replace `/ABSOLUTE/PATH/TO/plan_mcp_service` with the actual path on your machine)*

## Tools Available

*   `create_plan(name, ...)`: Create a new top-level plan.
*   `add_step(plan_id, ...)`: Add a sub-task to a plan.
*   `create_plan_batch(name, children, ...)`: Create a plan with multiple steps at once.
*   `list_plans(category, status)`: List all plans.
*   `get_plan_details(plan_id)`: Get the full tree structure of a plan.
*   `update_plan_status(plan_id, status)`: Mark tasks as completed/in_progress.
*   `reschedule_plan(plan_id, new_time)`: Change dates.
*   `delete_plan(plan_id)`: Remove a plan.

## Development

1.  Install dependencies:
    ```bash
    uv pip install -e .
    ```
2.  Run tests:
    ```bash
    python test_db.py
    ```
