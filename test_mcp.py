#!/usr/bin/env python3
"""
MCP 服务器测试脚本
用于验证 list_plans 功能是否正常工作
"""

import sys
import json
from main import list_plans, create_plan, get_plan_details

def test_list_plans():
    """测试 list_plans 函数"""
    print("=" * 50)
    print("🔍 测试 list_plans 功能")
    print("=" * 50)
    
    # 测试1: 无参数调用
    print("\n📋 测试1: 获取所有顶级计划")
    result1 = list_plans()
    print("返回结果:")
    print(result1)
    
    # 测试2: 按类别过滤
    print("\n📋 测试2: 按类别过滤 (学习)")
    result2 = list_plans(category="学习")
    print("返回结果:")
    print(result2)
    
    # 测试3: 按状态过滤
    print("\n📋 测试3: 按状态过滤 (pending)")
    result3 = list_plans(status="pending")
    print("返回结果:")
    print(result3)
    
    # 测试4: 创建一个新计划再查询
    print("\n📋 测试4: 创建测试计划")
    create_result = create_plan(
        name="测试计划-" + str(int(time.time())),
        description="用于测试 list_plans 功能的计划",
        category="测试"
    )
    print("创建结果:", create_result)
    
    print("\n📋 测试5: 再次查询所有计划")
    result5 = list_plans()
    print("返回结果:")
    print(result5)
    
    return True

def test_database_connection():
    """测试数据库连接"""
    print("=" * 50)
    print("🗄️ 测试数据库连接")
    print("=" * 50)
    
    from main import SQLiteDB
    import os
    
    db = SQLiteDB()
    print(f"📁 数据库路径: {os.path.abspath(db.db_path)}")
    
    # 检查顶级计划
    items = db.query_items(parent_id=None)
    print(f"📊 顶级计划数量: {len(items)}")
    
    for item in items:
        print(f"  • [{item['id']}] {item['name']} - {item['category']}")
    
    return len(items) > 0

if __name__ == "__main__":
    import time
    
    print("🚀 开始 MCP 服务器功能测试")
    print("当前时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # 测试数据库连接
        db_ok = test_database_connection()
        
        if db_ok:
            print("\n✅ 数据库连接正常")
            # 测试 list_plans 功能
            test_list_plans()
            print("\n✅ list_plans 功能测试完成")
        else:
            print("\n❌ 数据库连接失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)