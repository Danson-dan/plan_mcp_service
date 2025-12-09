# PlanManager MCP Server

🚀 **基于FastMCP框架和SQLite的通用计划管理系统**

一个功能强大的MCP服务器，支持创建、管理和追踪各类计划，特别适合旅行计划、学习计划、工作任务等多层级项目管理。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.14+-green.svg)
![Framework](https://img.shields.io/badge/framework-FastMCP-purple.svg)

## ✨ 特性

### 📋 核心功能
- 🏗️ **层级管理** - 支持父子计划的层级结构
- 🗄️ **数据持久化** - 基于SQLite的可靠数据存储
- 🔍 **智能搜索** - 按名称和描述搜索计划
- 📊 **统计分析** - 实时查看计划完成情况
- 🔄 **状态管理** - 完整的计划生命周期管理

### 🎯 快速模板
- ✈️ **旅行计划模板** - 一键创建完整的旅行计划
- 📚 **学习计划模板** - 自动生成学习进度安排
- 💼 **工作计划模板** - 灵活的任务分解

### 🛠️ 高级功能
- 📝 **批量创建** - 支持一次性创建多个子计划
- 🏷️ **分类管理** - 多种类别标签支持
- 📅 **时间管理** - 灵活的开始时间和截止日期
- 💾 **元数据扩展** - JSON格式的自定义数据支持

## 🚀 快速开始

### 环境要求
- Python 3.14+
- UV (推荐) 或 pip

### 安装

```bash
# 克隆项目
git clone <your-repo-url>
cd plan-server-mcp

# 安装依赖
uv sync

# 或者使用pip
pip install -e .
```

### 运行

```bash
# 启动MCP服务器
uv run main.py

# 或者
python main.py
```

## 📖 使用指南

### 基础操作

#### 创建计划
```python
# 创建通用计划
create_plan(
    name="我的新项目",
    description="这是一个重要的项目",
    category="工作",
    scheduled_at="2025-01-01",
    deadline="2025-03-31"
)
```

#### 添加子计划
```python
# 添加子步骤
add_step(
    plan_id=1,
    name="需求分析",
    description="完成项目需求文档",
    scheduled_at="2025-01-05"
)
```

### 快速模板

#### 🌍 创建旅行计划
```python
create_travel_plan(
    destination="日本",
    start_date="2025-04-01",
    end_date="2025-04-10",
    budget=15000,
    description="东京、大阪、京都文化之旅"
)
```

#### 📖 创建学习计划
```python
create_study_plan(
    subject="机器学习",
    duration_weeks=8,
    start_date="2025-01-15",
    description="深入学习机器学习算法和实践"
)
```

### 查询和管理

#### 查看计划
```python
# 列出所有计划
list_plans()

# 按类别筛选
list_plans(category="旅行")

# 查看详情
get_plan_details(plan_id=1)
```

#### 更新状态
```python
# 更新计划状态
update_plan_status(plan_id=1, status="in_progress")
```

#### 搜索和统计
```python
# 搜索计划
search_plans(keyword="学习")

# 获取统计信息
get_plan_statistics()
```

## 📊 数据库设计

### 表结构
```sql
CREATE TABLE plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- 计划名称
    description TEXT,                       -- 描述
    category TEXT DEFAULT 'general',       -- 类别
    parent_id INTEGER,                     -- 父计划ID
    scheduled_at DATE,                     -- 开始时间
    deadline DATE,                         -- 截止时间
    status TEXT DEFAULT 'pending',         -- 状态
    metadata TEXT,                         -- 元数据(JSON)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES plans (id) ON DELETE CASCADE
);
```

### 状态说明
- `pending` - 待开始
- `in_progress` - 进行中
- `completed` - 已完成
- `cancelled` - 已取消

### 类别标签
- `general` - 通用
- `旅行` - 旅行相关
- `学习` - 学习计划
- `工作` - 工作任务
- `健康` - 健康管理
- `习惯` - 习惯培养

## 🏗️ 架构设计

```
PlanManager MCP Server
├── FastMCP Framework      # MCP协议层
├── SQLiteDB              # 数据持久化层
├── Plan Management       # 业务逻辑层
└── Template System       # 模板系统
```

### 核心组件

#### 1. SQLiteDB 类
- 数据库连接管理
- CRUD操作封装
- 事务支持

#### 2. MCP Tools
- `create_plan` - 创建计划
- `add_step` - 添加子步骤
- `update_plan_status` - 更新状态
- `get_plan_details` - 获取详情
- `list_plans` - 列出计划
- `delete_plan` - 删除计划

#### 3. 模板系统
- `create_travel_plan` - 旅行计划模板
- `create_study_plan` - 学习计划模板
- `create_plan_batch` - 批量创建

## 🔧 开发

### 项目结构
```
plan-server-mcp/
├── main.py              # 主程序文件
├── pyproject.toml       # 项目配置
├── uv.lock             # 依赖锁定文件
├── README.md           # 项目文档
└── USAGE.md            # 使用指南
```

### 本地开发

```bash
# 开发模式运行
python main.py

# 代码检查
python -m py_compile main.py

# 测试数据库
sqlite3 plans.db ".schema"
```

## 📝 API 参考

### 核心工具

| 工具名 | 功能描述 | 参数 |
|--------|----------|------|
| `create_plan` | 创建计划 | name, description, category, scheduled_at, deadline, metadata |
| `add_step` | 添加子步骤 | plan_id, name, description, scheduled_at, metadata |
| `update_plan_status` | 更新状态 | plan_id, status |
| `get_plan_details` | 获取详情 | plan_id |
| `list_plans` | 列出计划 | category, status |
| `delete_plan` | 删除计划 | plan_id |

### 模板工具

| 工具名 | 功能描述 | 参数 |
|--------|----------|------|
| `create_travel_plan` | 创建旅行计划 | destination, start_date, end_date, budget, description |
| `create_study_plan` | 创建学习计划 | subject, duration_weeks, start_date, description |
| `create_plan_batch` | 批量创建 | name, children, category, description |

### 实用工具

| 工具名 | 功能描述 | 参数 |
|--------|----------|------|
| `search_plans` | 搜索计划 | keyword |
| `get_plan_statistics` | 获取统计 | 无 |
| `reschedule_plan` | 重新安排时间 | plan_id, new_time |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastMCP](https://github.com/modelcontextprotocol/python-sdk) - 强大的MCP框架
- [SQLite](https://www.sqlite.org/) - 可靠的嵌入式数据库

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](../../issues)
- 查看 [USAGE.md](USAGE.md) 详细使用指南

---

**Made with ❤️ using FastMCP**