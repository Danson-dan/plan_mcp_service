from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from . import db
import json

# Create the MCP server
mcp = FastMCP("PlanManager")

@mcp.tool()
def create_plan(
    name: str,
    description: Optional[str] = None,
    category: str = "general",
    scheduled_at: Optional[str] = None,
    deadline: Optional[str] = None,
    metadata: Optional[str] = None
) -> str:
    """
    Create a new top-level plan.
    
    Args:
        name: The name of the plan (e.g., "Trip to Japan", "Learn Python").
        description: Detailed description of the plan.
        category: The category (e.g., "travel", "study", "habit", "work").
        scheduled_at: When the plan starts (ISO 8601 format: YYYY-MM-DD).
        deadline: When the plan should be finished (ISO 8601 format).
        metadata: JSON string containing extra data (e.g., '{"budget": 500}').
    """
    meta_dict = {}
    if metadata:
        try:
            meta_dict = json.loads(metadata)
        except json.JSONDecodeError:
            return "Error: metadata must be a valid JSON string."

    item_id = db.create_item(
        name=name,
        description=description,
        category=category,
        scheduled_at=scheduled_at,
        deadline=deadline,
        metadata=meta_dict
    )
    return f"Plan created successfully. ID: {item_id}"

@mcp.tool()
def add_step(
    plan_id: int,
    name: str,
    description: Optional[str] = None,
    scheduled_at: Optional[str] = None,
    metadata: Optional[str] = None
) -> str:
    """
    Add a step (sub-task) to an existing plan.
    
    Args:
        plan_id: The ID of the parent plan.
        name: The name of the step.
        description: Details about this step.
        scheduled_at: When this step should be done (ISO 8601).
        metadata: JSON string for extra data.
    """
    # Verify parent exists
    parent = db.get_item(plan_id)
    if not parent:
        return f"Error: Plan with ID {plan_id} not found."

    meta_dict = {}
    if metadata:
        try:
            meta_dict = json.loads(metadata)
        except json.JSONDecodeError:
            return "Error: metadata must be a valid JSON string."

    item_id = db.create_item(
        name=name,
        parent_id=plan_id,
        description=description,
        category=parent['category'], # Inherit category
        scheduled_at=scheduled_at,
        metadata=meta_dict
    )
    return f"Step added to plan {plan_id}. Step ID: {item_id}"

@mcp.tool()
def create_plan_batch(
    name: str,
    children: str,
    category: str = "general",
    description: Optional[str] = None
) -> str:
    """
    Create a plan with multiple steps in one go. 
    Useful for generating full schedules like "Weekly Study Plan" or "21-Day Challenge".
    
    Args:
        name: Name of the main plan.
        children: A JSON string representing a LIST of step objects.
                  Example: '[{"name": "Day 1", "scheduled_at": "2023-10-01"}, {"name": "Day 2"}]'
        category: Category for the plan and all children.
    """
    try:
        steps = json.loads(children)
        if not isinstance(steps, list):
            return "Error: 'children' must be a JSON list of objects."
    except json.JSONDecodeError:
        return "Error: 'children' must be a valid JSON string."

    # Create parent
    parent_id = db.create_item(name=name, description=description, category=category)
    
    # Create children
    created_count = 0
    for step in steps:
        db.create_item(
            name=step.get('name', 'Untitled Step'),
            parent_id=parent_id,
            description=step.get('description'),
            category=category,
            scheduled_at=step.get('scheduled_at'),
            metadata=step.get('metadata', {})
        )
        created_count += 1
        
    return f"Plan '{name}' created with {created_count} steps. Parent ID: {parent_id}"

@mcp.tool()
def list_plans(
    category: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    List top-level plans (items without a parent).
    
    Args:
        category: Filter by category (e.g., "travel", "study").
        status: Filter by status (e.g., "pending", "completed").
    """
    items = db.query_items(parent_id=None, category=category, status=status) # parent_id=None means top-level
    if not items:
        return "No plans found matching criteria."
        
    result = "Found plans:\n"
    for item in items:
        result += f"- [{item['id']}] {item['name']} ({item['status']}) - {item['scheduled_at'] or 'No date'}\n"
    return result

@mcp.tool()
def get_plan_details(plan_id: int) -> str:
    """
    Get the full details and structure of a plan, including all its steps.
    """
    tree = db.get_tree(plan_id)
    if not tree:
        return f"Plan with ID {plan_id} not found."
    
    return json.dumps(tree, indent=2, ensure_ascii=False)

@mcp.tool()
def update_plan_status(plan_id: int, status: str) -> str:
    """
    Update the status of a plan or step.
    
    Args:
        plan_id: The ID of the item.
        status: New status ('pending', 'in_progress', 'completed', 'cancelled').
    """
    valid_statuses = {'pending', 'in_progress', 'completed', 'cancelled'}
    if status not in valid_statuses:
        return f"Error: Invalid status. Must be one of {valid_statuses}"
        
    success = db.update_item(plan_id, status=status)
    if success:
        return f"Item {plan_id} status updated to '{status}'."
    return f"Item {plan_id} not found."

@mcp.tool()
def reschedule_plan(plan_id: int, new_time: str) -> str:
    """
    Change the scheduled time for a plan or step.
    
    Args:
        plan_id: The ID of the item.
        new_time: New ISO 8601 date string (e.g., "2025-12-25").
    """
    success = db.update_item(plan_id, scheduled_at=new_time)
    if success:
        return f"Item {plan_id} rescheduled to {new_time}."
    return f"Item {plan_id} not found."

@mcp.tool()
def delete_plan(plan_id: int) -> str:
    """
    Delete a plan and all its steps.
    """
    success = db.delete_item(plan_id)
    if success:
        return f"Plan {plan_id} deleted."
    return f"Plan {plan_id} not found."

if __name__ == "__main__":
    mcp.run()
