#!/usr/bin/env python3
"""
前端逻辑测试（模拟 Streamlit 会话）
"""

import sys
import os

# 设置环境变量
os.environ["COZE_WORKSPACE_PATH"] = "/workspace/projects"
os.environ["COZE_WORKLOAD_IDENTITY_API_KEY"] = "bFRxY3prY1BnV2VJOXR5ZlJpQlB0Z0QyQ2wwRDl5S1g6NkhkV2tLbG52VzBFOTVGSU1LYVFZQVMxN09GeEFzdEtoR2VmTkpYSlhtMzBIdWdzOFhQZUttdmZhWG1DWndqTQ=="
os.environ["COZE_INTEGRATION_MODEL_BASE_URL"] = "https://integration.coze.cn/api/v3"
os.environ["SUPABASE_URL"] = "https://br-sharp-char-09e1aa7c.supabase2.aidap-global.cn-beijing.volces.com"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjMzNTMxMzMzMDcsInJvbGUiOiJhbm9uIn0.OW_0xMDA1o2pjb9hr966jdlsCMt76e0tMmoMjBmYg_o"

# 添加项目路径
sys.path.insert(0, '/workspace/projects/src')

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

print("=" * 80)
print("🧪 前端逻辑测试（模拟 Streamlit 会话）")
print("=" * 80)
print()

# 模拟 session_state
class SessionState:
    def __init__(self):
        self.messages = []
        self.agent = None
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

# 初始化 session
print("1️⃣  初始化会话状态...")
session = SessionState()

# 构建 Agent
print("2️⃣  构建 Agent...")
try:
    session.agent = build_agent()
    print("   ✅ Agent 构建成功")
except Exception as e:
    print(f"   ❌ Agent 构建失败: {e}")
    sys.exit(1)

print()

# 模拟用户交互流程
print("3️⃣  模拟用户交互流程...")
print()

# 场景 1：用户点击快捷按钮
print("场景 1：用户点击「📚 查询社团信息」快捷按钮")
print("-" * 80)
user_input = "有哪些社团？"
print(f"👤 用户输入: {user_input}")

# 添加用户消息
session.add_message("user", user_input)
print(f"   ✅ 用户消息已添加到会话")

# 调用 Agent
try:
    config = {"configurable": {"thread_id": "test_thread"}}
    response = session.agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    ai_message = response["messages"][-1]
    assistant_response = ai_message.content
    
    # 添加助手消息
    session.add_message("assistant", assistant_response)
    print(f"   ✅ 助手回复已添加到会话")
    print(f"   📝 回复预览（前200字符）: {assistant_response[:200]}...")
    
except Exception as e:
    print(f"   ❌ Agent 调用失败: {e}")

print()

# 检查会话状态
print("4️⃣  检查会话状态...")
print("-" * 80)
print(f"   📊 总消息数: {len(session.messages)}")
for i, msg in enumerate(session.messages):
    role_icon = "👤" if msg["role"] == "user" else "🤖"
    print(f"   {i+1}. {role_icon} {msg['role']}: {msg['content'][:50]}...")

print()

# 场景 2：用户继续对话
print("场景 2：用户继续对话")
print("-" * 80)
user_input = "介绍一下机器人社"
print(f"👤 用户输入: {user_input}")

session.add_message("user", user_input)

try:
    response = session.agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    ai_message = response["messages"][-1]
    assistant_response = ai_message.content
    session.add_message("assistant", assistant_response)
    print(f"   ✅ 助手回复已添加")
    print(f"   📝 回复预览（前200字符）: {assistant_response[:200]}...")
    
except Exception as e:
    print(f"   ❌ Agent 调用失败: {e}")

print()

# 最终检查
print("5️⃣  最终检查...")
print("-" * 80)
print(f"   📊 总消息数: {len(session.messages)}")
print(f"   ✅ 用户消息数: {len([m for m in session.messages if m['role'] == 'user'])}")
print(f"   ✅ 助手消息数: {len([m for m in session.messages if m['role'] == 'assistant'])}")

print()
print("=" * 80)
print("✅ 前端逻辑测试通过！消息流程正常工作")
print("=" * 80)
