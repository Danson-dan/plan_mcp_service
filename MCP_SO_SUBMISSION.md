# 📋 提交到 mcp.so 的完整方案

## 🎯 提交信息模板

### 基本信息
- **服务器名称**: Plan Manager MCP Service
- **英文名称**: plan-mcp-service
- **分类**: Productivity / Task Management
- **开发者**: [你的姓名/团队名]
- **许可证**: MIT

### 简要描述
一个通用的计划管理MCP服务，支持AI助手帮助用户创建、管理和跟踪各种类型的计划，包括旅行计划、学习计划、习惯养成和工作项目等。

### 核心功能
- ✅ **创建计划**: 支持无限层级的树形任务结构
- ✅ **批量操作**: 一次性创建复杂的多步骤计划
- ✅ **状态管理**: pending/in_progress/completed/cancelled
- ✅ **时间管理**: 支持计划时间和截止时间
- ✅ **灵活元数据**: JSON格式存储自定义数据
- ✅ **分类系统**: travel/study/habit/work/general
- ✅ **持久存储**: SQLite本地数据库

### 支持的工具
1. `create_plan` - 创建顶级计划
2. `add_step` - 添加子步骤
3. `create_plan_batch` - 批量创建计划
4. `list_plans` - 列出计划
5. `get_plan_details` - 获取计划详情
6. `update_plan_status` - 更新状态
7. `reschedule_plan` - 重新安排时间
8. `delete_plan` - 删除计划

### 项目链接
- **GitHub仓库**: https://github.com/yourusername/plan-mcp-service
- **PyPI包**: https://pypi.org/project/plan-mcp-service/
- **文档**: https://github.com/yourusername/plan-mcp-service#readme

### 安装和配置

#### PyPI安装
```bash
pip install plan-mcp-service
```

#### Claude Desktop配置
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

#### GitHub安装
```bash
pip install git+https://github.com/yourusername/plan-mcp-service.git
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