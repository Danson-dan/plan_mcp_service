#!/usr/bin/env python3
"""
MCP 客户端测试脚本
用于测试 MCP 服务器连接和 list_plans 功能
"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_connection():
    """测试 MCP 连接和 list_plans 功能"""
    print("🚀 开始测试 MCP 服务器连接")
    
    try:
        # 创建服务器参数
        server_params = StdioServerParameters(
            command="python",
            args=["main.py"],
            env=None
        )
        
        print("📡 正在连接到 MCP 服务器...")
        
        # 创建客户端会话
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化连接
                await session.initialize()
                print("✅ MCP 服务器连接成功")
                
                # 获取可用工具列表
                response = await session.list_tools()
                print(f"🔧 可用工具数量: {len(response.tools)}")
                
                # 查找 list_plans 工具
                list_plans_tool = None
                for tool in response.tools:
                    if tool.name == "list_plans":
                        list_plans_tool = tool
                        break
                
                if not list_plans_tool:
                    print("❌ 未找到 list_plans 工具")
                    return False
                
                print("✅ 找到 list_plans 工具")
                
                # 调用 list_plans 工具
                print("\n🔍 调用 list_plans 工具...")
                result = await session.call_tool("list_plans", {})
                
                print("📋 list_plans 调用结果:")
                print(result.content[0].text if result.content else "无内容")
                
                # 测试带参数的调用
                print("\n🔍 调用 list_plans (category='学习')...")
                result2 = await session.call_tool("list_plans", {"category": "学习"})
                
                print("📋 带类别过滤的结果:")
                print(result2.content[0].text if result2.content else "无内容")
                
                return True
                
    except Exception as e:
        print(f"❌ MCP 连接测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("=" * 60)
    print("🧪 MCP 客户端功能测试")
    print("=" * 60)
    
    success = await test_mcp_connection()
    
    if success:
        print("\n✅ MCP 客户端测试成功")
        print("💡 如果在您的环境中 list_plans 不工作，请检查:")
        print("  1. MCP 服务器是否正确启动")
        print("  2. 客户端连接配置是否正确")
        print("  3. 是否有防火墙或网络问题")
    else:
        print("\n❌ MCP 客户端测试失败")
        print("💡 请检查 MCP 服务器是否正常运行")

if __name__ == "__main__":
    asyncio.run(main())