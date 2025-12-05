# Plan MCP Service 发布指南

## 🚀 发布方式

### 方式一：PyPI发布（推荐）

#### 1. 准备工作
```bash
# 安装构建工具
pip install build twine

# 测试本地安装
pip install -e .
```

#### 2. 构建包
```bash
# 清理旧构建
rm -rf dist/ build/ *.egg-info/

# 构建包
python -m build
```

#### 3. 上传到PyPI
```bash
# 测试上传到TestPyPI
twine upload --repository testpypi dist/*

# 正式上传到PyPI
twine upload dist/*
```

#### 4. 用户安装使用
```bash
# 安装
pip install plan-mcp-service

# Claude Desktop配置
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

---

### 方式二：GitHub直接安装

#### 1. 推送到GitHub
```bash
git add .
git commit -m "Add MCP service for plan management"
git tag v0.1.0
git push origin main --tags
```

#### 2. 用户安装使用
```bash
# 直接从GitHub安装
pip install git+https://github.com/yourusername/plan-mcp-service.git

# 或指定版本
pip install git+https://github.com/yourusername/plan-mcp-service.git@v0.1.0
```

---

### 方式三：CloudStudio部署

如果你需要将服务部署到云端供团队使用：

1. 在CloudStudio中创建项目
2. 上传代码文件
3. 配置Python环境
4. 安装依赖：`pip install mcp[cli]`
5. 启动服务：`python -m plan_mcp_service.server`

---

## 📦 发布前检查清单

- [ ] 代码测试通过
- [ ] 文档完整（README.md）
- [ ] 版本号更新（pyproject.toml）
- [ ] 许可证文件存在
- [ ] .gitignore配置正确
- [ ] 依赖关系明确
- [ ] 脚本可执行权限

## 🧪 测试命令

```bash
# 运行测试
python test_db.py

# 本地测试MCP服务
python -m plan_mcp_service.server

# 测试安装
pip install -e .
plan-mcp-service --help
```

## 📝 用户使用指南

用户安装后需要在Claude Desktop的配置文件中添加：

```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

或者使用uv运行：

```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/plan_mcp_service",
        "run",
        "python",
        "-m",
        "plan_mcp_service.server"
      ]
    }
  }
}
```