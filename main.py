"""
FastMCP Plan Manager - 通用计划管理系统

基于SQLite的MCP服务器，支持创建、管理、更新和删除各类计划。
支持旅行计划、学习计划等多层级项目管理。

运行方式:
    uv run main.py
"""

from mcp.server.fastmcp import FastMCP
import json
import sqlite3
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# SQLite数据库管理类
class SQLiteDB:
    def __init__(self, db_path: str = "plans.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建计划表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'general',
                parent_id INTEGER,
                scheduled_at DATE,
                deadline DATE,
                status TEXT DEFAULT 'pending',
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES plans (id) ON DELETE CASCADE
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_parent_id ON plans(parent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON plans(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON plans(status)')
        
        conn.commit()
        conn.close()
    
    def create_item(self, name: str, description: Optional[str] = None, 
                   category: str = "general", parent_id: Optional[int] = None,
                   scheduled_at: Optional[str] = None, 
                   deadline: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> int:
        """创建新计划项"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute('''
            INSERT INTO plans (name, description, category, parent_id, 
                              scheduled_at, deadline, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, category, parent_id, 
              scheduled_at, deadline, metadata_json))
        
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return item_id
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """获取单个计划项"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM plans WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if not row:
            return None
            
        columns = ['id', 'name', 'description', 'category', 'parent_id', 
                  'scheduled_at', 'deadline', 'status', 'metadata', 
                  'created_at', 'updated_at']
        
        item = dict(zip(columns, row))
        if item['metadata']:
            item['metadata'] = json.loads(item['metadata'])
        
        return item
    
    def query_items(self, parent_id: Optional[int] = None, 
                   category: Optional[str] = None,
                   status: Optional[str] = None) -> list:
        """查询计划项"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM plans WHERE 1=1"
        params = []
        
        if parent_id is not None:
            query += " AND parent_id = ?"
            params.append(parent_id)
        
        if category:
            query += " AND category = ?"
            params.append(category)
            
        if status:
            query += " AND status = ?"
            params.append(status)
            
        query += " ORDER BY created_at"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'name', 'description', 'category', 'parent_id', 
                  'scheduled_at', 'deadline', 'status', 'metadata', 
                  'created_at', 'updated_at']
        
        results = []
        for row in rows:
            item = dict(zip(columns, row))
            if item['metadata']:
                item['metadata'] = json.loads(item['metadata'])
            results.append(item)
            
        return results
    
    def get_tree(self, item_id: int) -> Optional[Dict[str, Any]]:
        """获取计划树形结构"""
        item = self.get_item(item_id)
        if not item:
            return None
        
        # 递归获取子项
        children = self.query_items(parent_id=item_id)
        if children:
            item['children'] = [self.get_tree(child['id']) for child in children]
        
        return item
    
    def update_item(self, item_id: int, **kwargs) -> bool:
        """更新计划项"""
        if not self.get_item(item_id):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 准备更新字段
        update_fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ['name', 'description', 'category', 'parent_id', 
                      'scheduled_at', 'deadline', 'status']:
                update_fields.append(f"{key} = ?")
                params.append(value)
            elif key == 'metadata':
                update_fields.append("metadata = ?")
                params.append(json.dumps(value) if value else None)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            params.append(item_id)
            
            query = f"UPDATE plans SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_item(self, item_id: int) -> bool:
        """删除计划项（级联删除子项）"""
        if not self.get_item(item_id):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM plans WHERE id = ?", (item_id,))
        affected_rows = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return affected_rows > 0

# 创建数据库实例
db = SQLiteDB()

# 创建 MCP server
mcp = FastMCP("PlanManager", json_response=True)

@mcp.tool()
def create_plan(
    name: str,
    description: str | None = None,
    category: str = "general",
    scheduled_at: str | None = None,
    deadline: str | None = None,
    metadata: str | None = None
) -> str:
    """
    创建一个通用计划.
    
    Args:
        
        name: 计划的名称（例如，“我要去云南旅行”、“学习计划一周的Python课程安排”）.
        description: 计划的详细描述.
        category: 类别（例如，“旅行”、“学习”、“习惯”、“工作”）.
        scheduled_at: 计划开始时（ISO 8601格式：YYYY-MM-DD）.
        deadline: 计划应何时完成（ISO 8601格式：YYYY-MM-DD）.
        metadata: 包含额外数据的JSON字符串（例如，“{“budget”：500}”）.
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
    description: str | None = None,
    scheduled_at: str | None = None,
    metadata: str | None = None
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
    description: str | None = None
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
    category: str | None = None,
    status: str | None = None
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

@mcp.tool()
def create_travel_plan(
    destination: str,
    start_date: str,
    end_date: str,
    budget: float | None = None,
    description: str | None = None
) -> str:
    """
    快速创建旅行计划模板.
    
    Args:
        destination: 目的地（例如，"云南"、"日本"、"欧洲"）
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        budget: 预算金额
        description: 旅行描述
    """
    metadata = {"destination": destination, "budget": budget}
    if budget:
        metadata["budget"] = budget
    
    parent_id = db.create_item(
        name=f"{destination}旅行计划",
        description=description or f"前往{destination}的精彩旅程",
        category="旅行",
        scheduled_at=start_date,
        deadline=end_date,
        metadata=metadata
    )
    
    # 添加默认步骤
    default_steps = [
        {"name": "行前准备", "description": "办理签证、预订机票酒店"},
        {"name": "行程规划", "description": "制定详细行程安排"},
        {"name": "行李打包", "description": "准备必需物品"},
        {"name": "出发", "scheduled_at": start_date},
        {"name": "返程", "scheduled_at": end_date}
    ]
    
    created_count = 0
    for step in default_steps:
        db.create_item(
            name=step["name"],
            description=step.get("description"),
            parent_id=parent_id,
            category="旅行",
            scheduled_at=step.get("scheduled_at")
        )
        created_count += 1
    
    return f"✈️ 旅行计划创建成功！目的地: {destination}, ID: {parent_id}, 包含 {created_count} 个步骤"

@mcp.tool()
def create_study_plan(
    subject: str,
    duration_weeks: int,
    start_date: str,
    description: str | None = None
) -> str:
    """
    快速创建学习计划模板.
    
    Args:
        subject: 学习主题（例如，"Python编程"、"英语口语"、"数据分析"）
        duration_weeks: 学习周期（周数）
        start_date: 开始日期 (YYYY-MM-DD)
        description: 学习计划描述
    """
    from datetime import datetime, timedelta
    
    parent_id = db.create_item(
        name=f"{subject}学习计划",
        description=description or f"系统学习{subject}，计划{duration_weeks}周完成",
        category="学习",
        scheduled_at=start_date,
        metadata={"subject": subject, "duration_weeks": duration_weeks}
    )
    
    # 按周创建学习步骤
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    created_count = 0
    
    for week in range(1, duration_weeks + 1):
        week_date = (start_dt + timedelta(weeks=week-1)).strftime("%Y-%m-%d")
        db.create_item(
            name=f"第{week}周学习",
            description=f"{subject}第{week}周学习内容",
            parent_id=parent_id,
            category="学习",
            scheduled_at=week_date
        )
        created_count += 1
    
    return f"📚 学习计划创建成功！主题: {subject}, ID: {parent_id}, 共{duration_weeks}周, {created_count}个步骤"

@mcp.tool()
def search_plans(keyword: str) -> str:
    """
    搜索计划（按名称或描述）.
    
    Args:
        keyword: 搜索关键词
    """
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM plans 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY created_at DESC
    ''', (f'%{keyword}%', f'%{keyword}%'))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"未找到包含关键词 '{keyword}' 的计划。"
    
    columns = ['id', 'name', 'description', 'category', 'parent_id', 
              'scheduled_at', 'deadline', 'status', 'metadata', 
              'created_at', 'updated_at']
    
    result = f"🔍 搜索结果 ({len(rows)}个):\n"
    for row in rows:
        item = dict(zip(columns, row))
        result += f"- [{item['id']}] {item['name']} ({item['category']}) - {item['status']}\n"
        if item['description']:
            result += f"  📝 {item['description'][:100]}...\n"
    
    return result

@mcp.tool()
def get_plan_statistics() -> str:
    """
    获取计划统计信息.
    """
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    # 总计划数
    cursor.execute("SELECT COUNT(*) FROM plans")
    total_plans = cursor.fetchone()[0]
    
    # 按状态统计
    cursor.execute("SELECT status, COUNT(*) FROM plans GROUP BY status")
    status_stats = dict(cursor.fetchall())
    
    # 按类别统计
    cursor.execute("SELECT category, COUNT(*) FROM plans GROUP BY category")
    category_stats = dict(cursor.fetchall())
    
    # 本月创建的计划
    cursor.execute('''
        SELECT COUNT(*) FROM plans 
        WHERE created_at >= date('now', 'start of month')
    ''')
    monthly_plans = cursor.fetchone()[0]
    
    conn.close()
    
    stats = f"""
📊 计划统计信息
==================
📈 总计划数: {total_plans}
📅 本月新增: {monthly_plans}

🎯 状态分布:
{chr(10).join([f"  • {status}: {count}" for status, count in status_stats.items()])}

📂 类别分布:
{chr(10).join([f"  • {category}: {count}" for category, count in category_stats.items()])}
    """.strip()
    
    return stats

# 运行服务器
if __name__ == "__main__":
    print("🚀 PlanManager MCP Server 启动中...")
    print("💾 数据库位置:", os.path.abspath(db.db_path))
    print("🛠️  可用功能:")
    print("  • 创建通用计划 (create_plan)")
    print("  • 添加子计划 (add_step)")
    print("  • 批量创建计划 (create_plan_batch)")
    print("  • 快速创建旅行计划 (create_travel_plan)")
    print("  • 快速创建学习计划 (create_study_plan)")
    print("  • 列出计划 (list_plans)")
    print("  • 查看计划详情 (get_plan_details)")
    print("  • 更新状态 (update_plan_status)")
    print("  • 搜索计划 (search_plans)")
    print("  • 获取统计 (get_plan_statistics)")
    print("  • 删除计划 (delete_plan)")
    print("=" * 50)
    
    
    mcp.run(transport="stdio")