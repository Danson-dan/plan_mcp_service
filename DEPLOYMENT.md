# 🚀 Plan MCP Service 发布完整指南

## 📦 发布方式总结

### 1️⃣ PyPI发布（推荐给开源项目）

**优点：**
- 全球用户可直接 `pip install` 安装
- 自动化依赖管理
- 版本控制和更新通知

**发布步骤：**
```bash
# 1. 测试本地构建
./publish.sh test

# 2. 发布到PyPI
./publish.sh prod
```

### 2️⃣ GitHub源码安装

**优点：**
- 用户可以获取最新代码
- 适合开发者和测试用户

**用户安装：**
```bash
pip install git+https://github.com/yourusername/plan-mcp-service.git
```

### 3️⃣ Docker镜像发布

**优点：**
- 隔离环境，无依赖问题
- 适合企业内部部署

## 🔧 准备工作清单

### ✅ 已完成的配置
- [x] pyproject.toml（现代Python包配置）
- [x] setup.py（兼容旧版pip）
- [x] MANIFEST.in（文件包含清单）
- [x] LICENSE（MIT许可证）
- [x] .gitignore（忽略不必要文件）
- [x] publish.sh（半自动发布脚本）
- [x] GitHub Actions（自动化发布）
- [x] README.md（完整文档）

### 📝 需要你填写的信息
1. **PyPI账号：** 注册 https://pypi.org/account/register/
2. **API Token：** 在PyPI账户设置中生成
3. **GitHub仓库：** 推送代码到GitHub
4. **仓库信息：** 更新pyproject.toml中的作者信息和链接

## 🎯 推荐发布流程

### 第一步：测试发布
```bash
# 1. 安装发布工具
pip3 install build twine

# 2. 测试发布到TestPyPI
./publish.sh test
```

### 第二步：正式发布
```bash
# 1. 确认版本号（pyproject.toml）
# 2. 创建Git标签
git tag v0.1.0
git push origin main --tags

# 3. 发布到PyPI
./publish.sh prod
```

### 第三步：验证发布
```bash
# 用户安装测试
pip install plan-mcp-service

# 测试命令行工具
plan-mcp-service --help
```

## 🌍 用户使用方式

### Claude Desktop配置
```json
{
  "mcpServers": {
    "plan-manager": {
      "command": "plan-mcp-service"
    }
  }
}
```

### 手动运行
```bash
# 直接运行
python3 -m plan_mcp_service.server

# 或使用uv
uv run python3 -m plan_mcp_service.server
```

## 🔄 自动化更新

设置GitHub Actions后，每次推送新标签时会自动：
1. 在多个Python版本上测试
2. 构建包
3. 发布到PyPI

## 📞 技术支持

用户可以通过以下方式获取帮助：
- GitHub Issues：报告问题和建议
- PyPI页面：查看文档和更新日志
- README文档：详细使用说明

## 🎉 发布后检查

发布完成后，请验证：
- [ ] PyPI页面显示正确信息
- [ ] `pip install` 可以正常安装
- [ ] MCP服务可以正常启动
- [ ] Claude Desktop可以正常连接

---

**🎊 恭喜！你的MCP服务现在可以被全世界的用户使用了！**