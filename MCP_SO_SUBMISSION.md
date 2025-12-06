# 📋 提交到 mcp.so 的完整方案

## 🎯 mcp.so GitHub Issue 提交模板

### 📌 标题格式
```
SUBMIT MCP SERVER: PLAN MANAGER - Universal Task Planning & Management
```

### 📋 Issue 内容模板

```markdown
## 🏷️ 基本信息

- **服务器名称**: Plan Manager MCP Service
- **简短名称**: plan-mcp-service
- **MCP类型**: Tools
- **分类**: Productivity / Task Management / Planning
- **开发者**: [你的GitHub用户名]
- **许可证**: MIT
- **MCP协议版本**: MCP (FastMCP)

## 📝 描述

一个通用的计划管理MCP服务，支持AI助手帮助用户创建、管理和跟踪各种类型的计划。采用树形结构设计，支持无限层级嵌套，适用于旅行计划、学习计划、习惯养成、工作项目等场景。

## 🛠️ 支持的工具

| 工具名称 | 功能描述 | 参数 |
|---------|---------|------|
| `create_plan` | 创建顶级计划 | name, description, category, scheduled_at, deadline, metadata |
| `add_step` | 添加子步骤到现有计划 | plan_id, name, description, scheduled_at, metadata |
| `create_plan_batch` | 批量创建包含多步骤的计划 | name, children (JSON), category, description |
| `list_plans` | 列出顶级计划，支持筛选 | category, status |
| `get_plan_details` | 获取完整计划树结构 | plan_id |
| `update_plan_status` | 更新计划状态 | plan_id, status |
| `reschedule_plan` | 重新安排计划时间 | plan_id, new_time |
| `delete_plan` | 删除计划及其子步骤 | plan_id |

## 🚀 服务器配置

### 安装方式

#### PyPI安装（推荐）
```bash
pip install plan-mcp-service
```

#### GitHub安装
```bash
pip install git+https://github.com/yourusername/plan-mcp-service.git
```

### Claude Desktop 配置

#### 基础配置（使用uv - 推荐）
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/plan_mcp_service",
        "run",
        "python",
        "-m",
        "plan_mcp_service.server"
      ]
    }
  }
}
```

#### PyPI安装后的配置
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

#### 直接Python运行配置
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "python3",
      "args": [
        "-m",
        "plan_mcp_service.server"
      ]
    }
  }
}
```

## 🎯 核心特性

- ✅ **无限层级**: 树形任务结构，支持Plan -> Step -> Sub-step无限嵌套
- ✅ **批量操作**: 一次性创建复杂计划（21天挑战、一周计划等）
- ✅ **状态管理**: pending/in_progress/completed/cancelled四种状态
- ✅ **时间管理**: 支持计划时间和截止时间（ISO 8601格式）
- ✅ **灵活元数据**: JSON格式存储自定义数据（预算、地点、资源链接等）
- ✅ **分类系统**: travel/study/habit/work/general多种预设类别
- ✅ **持久存储**: SQLite本地数据库，数据安全可靠
- ✅ **高性能**: 基于FastMCP框架，响应迅速

## 🔗 项目链接

- **GitHub仓库**: https://github.com/yourusername/plan-mcp-service
- **PyPI包**: https://pypi.org/project/plan-mcp-service/
- **文档**: https://github.com/yourusername/plan-mcp-service#readme
- **许可证**: https://github.com/yourusername/plan-mcp-service/blob/main/LICENSE

## 💡 使用场景

- 🗺️ **旅行计划**: 创建包含预算、地点、时间安排的详细旅行计划
- 📚 **学习计划**: 制定结构化的学习进度和打卡系统  
- 🎯 **习惯养成**: 21天挑战或多阶段习惯培养计划
- 💼 **项目管理**: 工作项目的任务分解和进度跟踪
- 🏋️ **健身计划**: 运动计划安排和目标管理

## 🛡️ 技术规格

- **编程语言**: Python 3.10+
- **框架**: FastMCP (Model Context Protocol)
- **数据库**: SQLite3
- **依赖**: mcp[cli]>=1.0.0
- **兼容性**: Claude Desktop, 支持MCP协议的AI助手

## ⚙️ 安装要求

- Python 3.10+
- 网络连接（用于安装依赖）
- 约5MB磁盘空间

## 📊 测试状态

- ✅ 本地测试通过
- ✅ Claude Desktop兼容测试
- ✅ 跨平台兼容性验证（Windows/macOS/Linux）

## 📝 备注

- 开源项目，MIT许可证
- 持续维护，欢迎贡献
- 支持中文和英文
- 无需API密钥或外部服务依赖
```

### 安装和配置

#### 方式一：使用uv（推荐）
```bash
# 克隆仓库
git clone https://github.com/yourusername/plan-mcp-service.git
cd plan-mcp-service
# 使用uv运行
uv run python -m plan_mcp_service.server
```

#### 方式二：PyPI安装
```bash
pip install plan-mcp-service
```

#### 方式三：GitHub安装
```bash
pip install git+https://github.com/yourusername/plan-mcp-service.git
```

#### Claude Desktop配置（推荐 - uv方式）
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/plan_mcp_service",
        "run",
        "python",
        "-m",
        "plan_mcp_service.server"
      ]
    }
  }
}
```

### 使用示例
- 🗺️ **旅行计划**: 创建包含预算、地点、时间安排的详细旅行计划
- 📚 **学习计划**: 制定结构化的学习进度和打卡系统
- 🎯 **习惯养成**: 21天挑战或多阶段习惯培养计划
- 💼 **项目管理**: 工作项目的任务分解和进度跟踪

### 技术特性
- **轻量级**: 基于SQLite，无需外部依赖
- **高性能**: 使用FastMCP框架，响应迅速
- **易扩展**: 灵活的元数据系统，支持自定义场景
- **跨平台**: 支持Windows、macOS、Linux

## 🚀 提交步骤

### 第一步：访问提交页面
1. 打开 https://mcp.so/
2. 点击导航栏的 **"提交"** 按钮
3. 或直接访问：https://github.com/chatmcp/mcpso/issues/new/choose

### 第二步：创建GitHub Issue
1. 选择合适的Issue模板（通常是"Add MCP Server"）
2. 按照以下格式填写：

```
## 服务器信息
- **名称**: Plan Manager MCP Service
- **描述**: 通用计划管理MCP服务，支持无限层级的任务管理和时间规划
- **GitHub**: https://github.com/yourusername/plan-mcp-service
- **PyPI**: https://pypi.org/project/plan-mcp-service/

## 核心功能
- 8个完整的计划管理工具
- 支持树形任务结构和批量操作
- SQLite持久化存储
- 完整的状态和时间管理

## 安装方式
pip install plan-mcp-service

## Claude Desktop配置
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

### 第三步：等待审核
- mcp.so团队会在1-3个工作日内审核
- 审核通过后，你的服务会出现在网站上
- 用户可以直接从网站发现和安装你的服务

## 📊 优化建议

### 提交前检查清单
- [ ] GitHub仓库已创建并推送代码
- [ ] README.md文档完整
- [ ] 已发布到PyPI（可选但推荐）
- [ ] 项目有清晰的许可证
- [ ] 代码质量良好，有基本测试

### 提高收录概率
1. **完善文档**: 确保README详细说明使用方法
2. **添加徽章**: 在README中添加build status、license等徽章
3. **提供示例**: 包含具体的使用案例和截图
4. **及时回复**: 保持对GitHub Issues的快速响应

## 🎉 后续维护

### 更新服务信息
- 版本更新时，通过GitHub Issue通知mcp.so团队
- 添加新功能时，及时更新描述信息

### 社区建设
- 关注用户反馈，持续改进功能
- 分享使用案例，扩大影响力

---

**🎊 提交成功后，你的Plan MCP Service将被全球MCP用户发现和使用！**