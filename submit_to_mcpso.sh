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

# 生成提交文本
cat > submission_text.txt << 'EOF'
## 服务器信息
- **名称**: Plan Manager MCP Service
- **描述**: 通用计划管理MCP服务，支持无限层级的任务管理和时间规划
- **分类**: Productivity / Task Management
- **GitHub**: EOF

echo "${REPO_URL}" >> submission_text.txt
echo "" >> submission_text.txt
echo '- **PyPI**: https://pypi.org/project/plan-mcp-service/' >> submission_text.txt
echo "" >> submission_text.txt

cat >> submission_text.txt << 'EOF'
## 核心功能
- 8个完整的计划管理工具（create_plan, add_step, create_plan_batch等）
- 支持树形任务结构和批量操作（21天挑战、一周计划等）
- SQLite持久化存储，数据安全可靠
- 完整的状态管理（pending/in_progress/completed/cancelled）
- 灵活的时间管理（计划时间、截止时间）
- 支持多种分类（travel/study/habit/work/general）
- JSON元数据系统，适应各种使用场景

## 技术特性
- 轻量级：基于SQLite，无需外部依赖
- 高性能：使用FastMCP框架，响应迅速
- 易扩展：灵活的元数据系统，支持自定义场景
- 跨平台：支持Windows、macOS、Linux

## 安装方式

### PyPI安装（推荐）
```bash
pip install plan-mcp-service
```

### GitHub安装
```bash
pip install git+EOF

echo "${REPO_URL}.git" >> submission_text.txt
echo "" >> submission_text.txt

cat >> submission_text.txt << 'EOF'
```

## Claude Desktop配置
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

## 使用场景
- 🗺️ **旅行计划**: 创建包含预算、地点、时间安排的详细旅行计划
- 📚 **学习计划**: 制定结构化的学习进度和打卡系统
- 🎯 **习惯养成**: 21天挑战或多阶段习惯培养计划
- 💼 **项目管理**: 工作项目的任务分解和进度跟踪

## 技术栈
- Python 3.10+
- FastMCP (Model Context Protocol)
- SQLite3 (持久存储)

## 许可证
MIT License - 开源免费使用
EOF

echo "📋 已生成提交文本 (submission_text.txt)"
echo ""

echo "🌐 提交步骤："
echo "1. 访问: https://github.com/chatmcp/mcpso/issues/new/choose"
echo "2. 选择 'Add MCP Server' 模板"
echo "3. 复制 submission_text.txt 中的内容并粘贴"
echo "4. 填写标题: Add Plan Manager MCP Service"
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