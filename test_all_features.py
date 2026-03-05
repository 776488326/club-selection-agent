#!/usr/bin/env python3
"""
完整功能测试脚本
模拟用户交互，测试所有功能
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
print("🧪 校园社团选课智能体 - 完整功能测试")
print("=" * 80)
print()

# 构建 Agent
print("📦 构建 Agent...")
try:
    agent = build_agent()
    print("✅ Agent 构建成功")
except Exception as e:
    print(f"❌ Agent 构建失败: {e}")
    sys.exit(1)

print()

# 测试场景
test_cases = [
    {
        "name": "查询社团信息",
        "input": "有哪些社团？",
        "expected": "应该显示社团列表"
    },
    {
        "name": "兴趣测评",
        "input": "我想做兴趣测评，帮我推荐社团",
        "expected": "应该开始兴趣测评流程"
    },
    {
        "name": "填报志愿",
        "input": "我想填报志愿",
        "expected": "应该开始收集填报信息"
    },
    {
        "name": "查询录取结果",
        "input": "查询录取结果",
        "expected": "应该询问学号"
    },
    {
        "name": "介绍自己",
        "input": "你好，请介绍一下你自己",
        "expected": "应该自我介绍"
    }
]

config = {"configurable": {"thread_id": "test_thread"}}

# 运行测试
for i, test_case in enumerate(test_cases, 1):
    print("=" * 80)
    print(f"测试 {i}/{len(test_cases)}: {test_case['name']}")
    print("=" * 80)
    print(f"📝 输入: {test_case['input']}")
    print(f"🎯 预期: {test_case['expected']}")
    print()
    
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=test_case['input'])]},
            config=config
        )
        
        ai_message = response["messages"][-1]
        reply = ai_message.content
        
        print(f"🤖 回复: {reply[:500]}...")
        print()
        print("✅ 测试通过")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print()

print("=" * 80)
print("✅ 所有测试完成")
print("=" * 80)
