"""
校园社团选课智能体 - Web 前端界面
使用 Streamlit 构建
"""

import sys
import os
import json
import asyncio
from typing import Dict, List

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# 配置页面
st.set_page_config(
    page_title="🎓 校园社团选课助手",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 2rem 0;
    }
    
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        color: white;
    }
    
    .assistant-message {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        height: 3rem;
        font-weight: bold;
    }
    
    .sidebar-section {
        padding: 1rem;
        border-radius: 0.5rem;
        background: #f8f9fa;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = build_agent()
        except Exception as e:
            st.error(f"Agent 初始化失败: {str(e)}")
            st.session_state.agent = None


def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🎯 选课助手")
        
        # 功能导航
        st.subheader("快速导航")
        
        if st.button("📚 查询社团信息", use_container_width=True):
            st.session_state.suggested_input = "有哪些社团？"
        
        if st.button("🎮 兴趣测评", use_container_width=True):
            st.session_state.suggested_input = "我想做兴趣测评，帮我推荐社团"
        
        if st.button("📝 填报志愿", use_container_width=True):
            st.session_state.suggested_input = "我想填报志愿"
        
        if st.button("📊 查询录取结果", use_container_width=True):
            st.session_state.suggested_input = "查询录取结果"
        
        st.divider()
        
        # 使用说明
        with st.expander("📖 使用说明"):
            st.markdown("""
            **功能介绍：**
            - 📚 查询社团：了解所有社团的详细信息
            - 🎮 兴趣测评：根据你的兴趣推荐社团
            - 📝 填报志愿：提交三个志愿选择
            - 📊 查询结果：查看录取状态
            
            **选课规则：**
            - 不拼手速，只拼兴趣
            - 按优先级智能匹配
            - 第一志愿优先录取
            
            **优先级计算：**
            - 年级基础分：高三90 / 高二80 / 高一70
            - 兴趣匹配分：0-10分
            - 随机因子：0-1分（解决同分）
            """)
        
        st.divider()
        
        # 系统信息
        st.info("💡 提示：点击上方的快捷按钮可以快速发起对话")
        
        # 清空对话
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def render_chat():
    """渲染聊天界面"""
    st.markdown('<div class="main-header">🎓 校园社团选课助手</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">不拼手速，只拼兴趣 | 智能匹配，公平选课</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # 显示历史消息
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2>👋 你好！我是你的社团选课助手</h2>
                <p>我可以帮你：</p>
                <ul style="display: inline-block; text-align: left;">
                    <li>📚 查询社团信息</li>
                    <li>🎮 进行兴趣测评，推荐社团</li>
                    <li>📝 填报志愿</li>
                    <li>📊 查询录取结果</li>
                </ul>
                <p style="margin-top: 1rem;">选择左侧的快捷按钮开始吧！</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)


def handle_user_input():
    """处理用户输入"""
    # 获取建议输入
    if 'suggested_input' in st.session_state:
        user_input = st.session_state.suggested_input
        del st.session_state.suggested_input
        st.chat_input("输入你的问题...", key="auto_input", value=user_input)
    else:
        user_input = st.chat_input("输入你的问题...", key="chat_input")
    
    if user_input:
        # 显示用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
        # 调用 Agent
        if st.session_state.agent:
            try:
                with st.spinner("🤖 思考中..."):
                    # 创建配置
                    config = {"configurable": {"thread_id": "default_thread"}}
                    
                    # 调用 agent
                    response = st.session_state.agent.invoke(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=config
                    )
                    
                    # 获取 AI 回复
                    ai_message = response["messages"][-1]
                    assistant_response = ai_message.content
                    
                    # 显示助手消息
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    st.rerun()
                    
            except Exception as e:
                error_msg = f"❌ 抱歉，处理你的请求时出错了：{str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()
        else:
            error_msg = "❌ Agent 未初始化，请检查配置"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()


def main():
    """主函数"""
    # 初始化会话状态
    init_session_state()
    
    # 渲染侧边栏
    render_sidebar()
    
    # 渲染聊天界面
    render_chat()
    
    # 处理用户输入
    handle_user_input()


if __name__ == "__main__":
    main()
