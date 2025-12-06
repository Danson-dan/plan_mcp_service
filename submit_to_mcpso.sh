#!/bin/bash

# 快速提交到mcp.so的辅助脚本

echo "🚀 准备提交Plan MCP Service到mcp.so"
echo ""

# 检查必要文件
if [ ! -f "README.md" ]; then
    echo "❌ README.md 不存在"
    exit 1
fi

if [ ! -d "src/plan_mcp_service" ]; then
    echo "❌ 源代码目录不存在"
    exit 1
fi

# 获取仓库信息（需要你手动填写）
echo "📝 请提供以下信息："
read -p "GitHub用户名: " GITHUB_USERNAME
read -p "你的姓名: " AUTHOR_NAME
read -p "联系邮箱: " AUTHOR_EMAIL

# 生成仓库URL
REPO_URL="https://github.com/${GITHUB_USERNAME}/plan-mcp-service"

echo ""
echo "🔍 检查项目状态..."

# 检查是否有git仓库
if [ ! -d ".git" ]; then
    echo "⚠️  当前目录不是git仓库，请先初始化并推送到GitHub"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit: Plan MCP Service'"
    echo "   git branch -M main"
    echo "   git remote add origin ${REPO_URL}"
    echo "   git push -u origin main"
    echo ""
    read -p "按回车继续..."
fi

# 更新pyproject.toml中的作者信息
echo "📝 更新项目信息..."
sed -i.bak "s/Your Name/${AUTHOR_NAME}/" pyproject.toml
sed -i.bak "s/your.email@example.com/${AUTHOR_EMAIL}/" pyproject.toml
sed -i.bak "s/yourusername/${GITHUB_USERNAME}/" pyproject.toml
rm -f pyproject.toml.bak

echo ""
echo "✅ 项目信息已更新"
echo ""

# 生成提交标题
ISSUE_TITLE="SUBMIT MCP SERVER: PLAN MANAGER - Universal Task Planning & Management"

# 生成提交内容
cat > submission_text.md << 'EOF'

## 🏷️ 基本信息

- **服务器名称**: Plan Manager MCP Service
- **简短名称**: plan-mcp-service
- **MCP类型**: Tools
- **分类**: Productivity / Task Management / Planning
- **开发者**: EOF

echo "${GITHUB_USERNAME}" >> submission_text.md
echo "- **许可证**: MIT" >> submission_text.md
echo "- **MCP协议版本**: MCP (FastMCP)" >> submission_text.md
echo "" >> submission_text.md

cat >> submission_text.md << 'EOF'
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

#### PyPI安装（推荐）
```bash
pip install plan-mcp-service
```

#### GitHub安装
```bash
pip install git+EOF

echo "${REPO_URL}.git" >> submission_text.md
echo "" >> submission_text.md

cat >> submission_text.md << 'EOF'
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

- **GitHub仓库**: EOF

echo "${REPO_URL}" >> submission_text.md
echo "- **PyPI包**: https://pypi.org/project/plan-mcp-service/" >> submission_text.md
echo "- **文档**: ${REPO_URL}#readme" >> submission_text.md
echo "- **许可证**: ${REPO_URL}/blob/main/LICENSE" >> submission_text.md
echo "" >> submission_text.md

cat >> submission_text.md << 'EOF'
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

## 📝 备注

- 开源项目，MIT许可证
- 持续维护，欢迎贡献
- 支持中文和英文
- 无需API密钥或外部服务依赖
EOF

echo "📋 已生成提交内容 (submission_text.md)"
echo "📋 Issue标题: ${ISSUE_TITLE}"
echo ""

echo "🌐 提交步骤："
echo "1. 访问: https://github.com/chatmcp/mcpso/issues/new/choose"
echo "2. 选择 'Add MCP Server' 或空白模板"
echo "3. 标题填写: ${ISSUE_TITLE}"
echo "4. 复制 submission_text.md 中的内容并粘贴到正文"
echo "5. 提交Issue"
echo ""

echo "📖 提交前建议："
echo "- 确保代码已推送到GitHub: ${REPO_URL}"
echo "- 检查README.md是否详细完整"
echo "- 考虑先发布到PyPI（可选但推荐）"
echo ""

echo "🔗 有用链接："
echo "- mcp.so首页: https://mcp.so/"
echo "- 直接提交: https://github.com/chatmcp/mcpso/issues/new/choose"
echo "- 你的仓库: ${REPO_URL}"
echo ""

read -p "按回车键打开提交页面..."
open "https://github.com/chatmcp/mcpso/issues/new/choose"

echo "✅ 准备完成！请按上述步骤提交。"