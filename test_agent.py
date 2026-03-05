#!/usr/bin/env python3
"""
测试 Agent 是否能正常构建和运行
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, '/workspace/projects/src')

print("=" * 60)
print("🧪 测试校园社团选课智能体")
print("=" * 60)
print()

# 测试 1: 检查环境变量
print("1️⃣  检查环境变量...")
env_vars = [
    "COZE_WORKLOAD_IDENTITY_API_KEY",
    "COZE_INTEGRATION_MODEL_BASE_URL",
    "SUPABASE_URL",
    "SUPABASE_KEY"
]

all_env_ok = True
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"  ✅ {var}: 已设置")
    else:
        print(f"  ❌ {var}: 未设置")
        all_env_ok = False

if not all_env_ok:
    print("\n❌ 环境变量未完全配置，无法继续测试")
    sys.exit(1)

print()

# 测试 2: 检查配置文件
print("2️⃣  检查配置文件...")
config_path = "/workspace/projects/config/agent_llm_config.json"
if os.path.exists(config_path):
    print(f"  ✅ 配置文件存在: {config_path}")
else:
    print(f"  ❌ 配置文件不存在: {config_path}")
    sys.exit(1)

print()

# 测试 3: 导入 agent
print("3️⃣  导入 agent 模块...")
try:
    from agents.agent import build_agent
    print("  ✅ Agent 模块导入成功")
except Exception as e:
    print(f"  ❌ Agent 模块导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 测试 4: 构建 Agent
print("4️⃣  构建 Agent...")
try:
    agent = build_agent()
    print("  ✅ Agent 构建成功")
except Exception as e:
    print(f"  ❌ Agent 构建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 测试 5: 调用 Agent
print("5️⃣  测试 Agent 调用...")
try:
    from langchain_core.messages import HumanMessage
    
    config = {"configurable": {"thread_id": "test_thread"}}
    response = agent.invoke(
        {"messages": [HumanMessage(content="你好，请介绍一下你自己")]},
        config=config
    )
    
    ai_message = response["messages"][-1]
    print(f"  ✅ Agent 调用成功")
    print(f"  📝 回复内容（前200字符）: {ai_message.content[:200]}...")
except Exception as e:
    print(f"  ❌ Agent 调用失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ 所有测试通过！Agent 工作正常")
print("=" * 60)
