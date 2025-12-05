import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = "plans.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the items table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create items table with flexible metadata support
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            scheduled_at TEXT,
            deadline TEXT,
            category TEXT DEFAULT 'general',
            metadata TEXT DEFAULT '{}',
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (parent_id) REFERENCES items (id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for common queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_parent_id ON items(parent_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON items(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON items(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_scheduled_at ON items(scheduled_at)")
    
    conn.commit()
    conn.close()

def create_item(
    name: str,
    parent_id: Optional[int] = None,
    description: Optional[str] = None,
    category: str = "general",
    scheduled_at: Optional[str] = None,
    deadline: Optional[str] = None,
    metadata: Dict[str, Any] = None
) -> int:
    """Create a new item (plan/task/step)."""
    if metadata is None:
        metadata = {}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute(
        """
        INSERT INTO items (
            name, parent_id, description, category, 
            scheduled_at, deadline, metadata, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name, parent_id, description, category,
            scheduled_at, deadline, json.dumps(metadata), now, now
        )
    )
    
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def get_item(item_id: int) -> Optional[Dict[str, Any]]:
    """Get a single item by ID."""
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    
    if item:
        return dict(item)
    return None

def update_item(item_id: int, **kwargs) -> bool:
    """Update an item's fields."""
    allowed_fields = {
        'name', 'description', 'status', 'scheduled_at', 
        'deadline', 'category', 'metadata', 'parent_id'
    }
    
    updates = {}
    for k, v in kwargs.items():
        if k in allowed_fields:
            if k == 'metadata' and isinstance(v, dict):
                updates[k] = json.dumps(v)
            else:
                updates[k] = v
                
    if not updates:
        return False
        
    updates['updated_at'] = datetime.now().isoformat()
    
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [item_id]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE items SET {set_clause} WHERE id = ?", values)
    rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows > 0

def delete_item(item_id: int) -> bool:
    """Delete an item and its children (via cascade if supported, or manual)."""
    # Note: SQLite foreign key cascade needs to be enabled per connection, 
    # or we can manually delete children. For simplicity/robustness here, 
    # let's trust SQLite but enable foreign keys.
    conn = get_db_connection()
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    rows = cursor.rowcount
    conn.commit()
    conn.close()
    return rows > 0

def query_items(
    parent_id: Optional[int] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    date_range: Optional[tuple] = None # (start, end)
) -> List[Dict[str, Any]]:
    """Query items with flexible filters."""
    query = "SELECT * FROM items WHERE 1=1"
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
        
    if date_range:
        start, end = date_range
        query += " AND scheduled_at BETWEEN ? AND ?"
        params.extend([start, end])
        
    query += " ORDER BY scheduled_at ASC, created_at ASC"
    
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_tree(root_id: int) -> Dict[str, Any]:
    """Get a recursive tree view of a plan."""
    root = get_item(root_id)
    if not root:
        return None
        
    children = query_items(parent_id=root_id)
    root['children'] = [get_tree(child['id']) for child in children]
    return root

# Initialize on module load
init_db()
