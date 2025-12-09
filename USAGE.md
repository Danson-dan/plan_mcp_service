# PlanManager MCP Server

基于FastMCP框架和SQLite数据库的通用计划管理系统。

## 功能特性

### 📋 核心功能
- ✅ 创建计划（支持父子层级结构）
- ✅ 添加子计划/步骤
- ✅ 批量创建计划
- ✅ 更新计划状态
- ✅ 查看计划详情
- ✅ 搜索计划
- ✅ 删除计划
- ✅ 获取统计信息

### 🚀 快速模板
- ✈️ 旅行计划模板
- 📚 学习计划模板

## 安装和运行

```bash
# 安装依赖
uv sync

# 运行服务器
uv run main.py
```

## 使用示例

### 创建旅行计划
```python
create_travel_plan(
    destination="云南",
    start_date="2025-01-15",
    end_date="2025-01-25",
    budget=5000,
    description="云南昆明、大理、丽江深度游"
)
```

### 创建学习计划
```python
create_study_plan(
    subject="Python编程",
    duration_weeks=4,
    start_date="2025-01-01",
    description="系统学习Python编程基础"
)
```

### 创建自定义计划
```python
create_plan(
    name="健身计划",
    description="三个月减重10公斤",
    category="健康",
    scheduled_at="2025-01-01",
    deadline="2025-03-31",
    metadata='{"target_weight": 65, "current_weight": 75}'
)
```

### 添加子计划
```python
add_step(
    plan_id=1,
    name="有氧运动",
    description="每周3次慢跑，每次30分钟",
    scheduled_at="2025-01-01"
)
```

### 批量创建计划步骤
```python
create_plan_batch(
    name="一周学习计划",
    children='[
        {"name": "第1天", "scheduled_at": "2025-01-01", "description": "Python基础语法"},
        {"name": "第2天", "scheduled_at": "2025-01-02", "description": "数据类型和控制流"},
        {"name": "第3天", "scheduled_at": "2025-01-03", "description": "函数和模块"}
    ]',
    category="学习"
)
```

### 更新计划状态
```python
update_plan_status(plan_id=1, status="in_progress")
```

### 查看计划详情
```python
get_plan_details(plan_id=1)
```

### 搜索计划
```python
search_plans(keyword="旅行")
```

### 获取统计信息
```python
get_plan_statistics()
```

### 删除计划
```python
delete_plan(plan_id=1)
```

## 🎯 引导式创建功能

### 使用引导创建计划
```python
# 获取创建指南
guided_plan_creation(plan_type="travel")

# 可选类型:
# - general: 通用计划
# - travel: 旅行计划
# - study: 学习计划
```

### 验证并保存计划
```python
validate_and_save_plan(
    name="我的新计划",
    plan_data='{"description": "这是一个测试计划", "category": "工作"}',
    auto_save=True
)
```

### 备份数据
```python
backup_plans()
```

## 数据库

系统使用SQLite数据库，数据文件自动创建在项目目录下的 `plans.db`。

### 数据表结构
```sql
CREATE TABLE plans (
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
);
```

## 状态说明

- `pending`: 待开始
- `in_progress`: 进行中  
- `completed`: 已完成
- `cancelled`: 已取消

## 类别说明

- `general`: 通用
- `旅行`: 旅行相关
- `学习`: 学习计划
- `工作`: 工作任务
- `健康`: 健康管理
- `习惯`: 习惯培养

## 技术栈

- **框架**: FastMCP
- **数据库**: SQLite3
- **语言**: Python 3.14+
- **包管理**: UV

## 开发

```bash
# 开发模式运行
python main.py

# 代码检查
uv run python -m py_compile main.py
```