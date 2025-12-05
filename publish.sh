#!/bin/bash

# Plan MCP Service 发布脚本
# 使用方法: ./publish.sh [test|prod]

set -e  # 遇到错误就退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查参数
if [ $# -eq 0 ]; then
    print_error "请指定发布目标: test 或 prod"
    echo "使用方法: ./publish.sh [test|prod]"
    exit 1
fi

TARGET=$1

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ] || [ ! -d "src/plan_mcp_service" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

print_info "开始发布 Plan MCP Service 到 $TARGET..."

# 1. 清理旧的构建文件
print_info "清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info/

# 2. 运行测试
print_info "运行测试..."
if [ -f "test_db.py" ]; then
    python3 test_db.py
    print_success "测试通过"
else
    print_warning "未找到测试文件，跳过测试"
fi

# 3. 构建包
print_info "构建包..."
python3 setup.py sdist bdist_wheel

# 检查构建结果
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    print_error "构建失败"
    exit 1
fi

print_success "构建完成，生成的文件："
ls -la dist/

# 4. 检查包
print_info "检查包完整性..."
python3 -m pip install twine
twine check dist/*

# 5. 上传包
if [ "$TARGET" = "test" ]; then
    print_info "上传到 TestPyPI..."
    twine upload --repository testpypi dist/*
    print_success "已上传到 TestPyPI"
    print_info "测试安装命令: pip install --index-url https://test.pypi.org/simple/ plan-mcp-service"
elif [ "$TARGET" = "prod" ]; then
    print_warning "准备上传到正式 PyPI..."
    read -p "确认要上传到正式 PyPI 吗？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "上传到 PyPI..."
        twine upload dist/*
        print_success "已上传到 PyPI"
        print_info "安装命令: pip install plan-mcp-service"
    else
        print_info "取消上传"
        exit 0
    fi
else
    print_error "无效的目标，请使用 test 或 prod"
    exit 1
fi

print_success "发布完成！"