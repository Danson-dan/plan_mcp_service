# 🚀 快速提交到 mcp.so

## 📌 Issue 标题（复制使用）
```
SUBMIT MCP SERVER: PLAN MANAGER - Universal Task Planning & Management
```

## 📋 Issue 内容（直接复制粘贴）

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

| 工具名称 | 功能描述 |
|---------|---------|
| `create_plan` | 创建顶级计划 |
| `add_step` | 添加子步骤到现有计划 |
| `create_plan_batch` | 批量创建包含多步骤的计划 |
| `list_plans` | 列出顶级计划，支持筛选 |
| `get_plan_details` | 获取完整计划树结构 |
| `update_plan_status` | 更新计划状态 |
| `reschedule_plan` | 重新安排计划时间 |
| `delete_plan` | 删除计划及其子步骤 |

## 🚀 服务器配置

### 安装方式

```bash
pip install plan-mcp-service
```

### Claude Desktop 配置

#### 推荐配置（使用uv）
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

## 💡 使用场景

- 🗺️ **旅行计划**: 创建包含预算、地点、时间安排的详细旅行计划
- 📚 **学习计划**: 制定结构化的学习进度和打卡系统  
- 🎯 **习惯养成**: 21天挑战或多阶段习惯培养计划
- 💼 **项目管理**: 工作项目的任务分解和进度跟踪

## 🛡️ 技术规格

- **编程语言**: Python 3.10+
- **框架**: FastMCP (Model Context Protocol)
- **数据库**: SQLite3
- **依赖**: mcp[cli]>=1.0.0
- **兼容性**: Claude Desktop, 支持MCP协议的AI助手

## 📝 备注

- 开源项目，MIT许可证
- 持续维护，欢迎贡献
- 支持中文和英文
- 无需API密钥或外部服务依赖
```

## 🔗 提交链接

点击这里直接访问：https://github.com/chatmcp/mcpso/issues/new/choose

## 📋 提交步骤

1. **复制标题**：上方的Issue标题
2. **复制内容**：上方的Issue内容（从```markdown到```）
3. **访问链接**：点击上方链接或手动访问
4. **填写提交**：
   - 粘贴标题到 "Title" 字段
   - 粘贴内容到 "Leave a comment" 字段
   - 选择合适的Label（如果有）
5. **提交Issue**：点击 "Submit new issue"

## ⚠️ 提交前检查

- [ ] GitHub仓库已创建
- [ ] README.md文档完整
- [ ] 已发布到PyPI（可选）
- [ ] 代码已测试通过

---

**🎊 提交成功后等待审核，通常1-3个工作日！**