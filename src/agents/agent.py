"""
校园社团选课智能体
实现"预选+智能匹配"选课机制，综合志愿优先级、兴趣匹配度、社团容量等因素完成选课录取
"""

import sys
import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers

# 添加路径设置
# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 src 目录
src_dir = os.path.dirname(current_dir)
# 获取项目根目录
project_root = os.path.dirname(src_dir)

# 添加到 sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 导入 storage 模块
from storage.memory.memory_saver import get_memory_saver

# 导入工具
from tools.club_query_tool import (
    query_all_clubs,
    query_club_by_name,
    query_clubs_by_type,
    compare_clubs,
    get_popular_clubs
)
from tools.application_tool import (
    validate_student_id,
    validate_club_name,
    submit_application,
    update_interest_tags,
    query_application
)
from tools.priority_calc_tool import (
    calculate_priority_score,
    batch_calculate_priority,
    get_priority_ranking,
    update_grade_score_config
)
from tools.admission_tool import (
    get_club_quota_status,
    check_quota_available,
    run_admission_process,
    find_adjustment_club,
    query_admission_result,
    get_admission_statistics
)

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:] # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """构建校园社团选课智能体"""
    # 动态获取项目根目录
    # 优先使用环境变量，如果没有则根据当前文件位置计算
    workspace_path = os.getenv("COZE_WORKSPACE_PATH")
    
    if workspace_path and os.path.exists(workspace_path):
        # 使用环境变量指定的路径
        config_path = os.path.join(workspace_path, LLM_CONFIG)
    else:
        # 根据当前文件位置动态计算项目根目录
        # agent.py 在 src/agents/ 目录下
        # 项目根目录应该是 src/ 的上一级
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        project_root = os.path.dirname(src_dir)
        
        # 构建配置文件路径
        config_path = os.path.join(project_root, LLM_CONFIG)
        
        # 如果文件不存在，尝试相对于当前工作目录
        if not os.path.exists(config_path):
            cwd_config = os.path.join(os.getcwd(), LLM_CONFIG)
            if os.path.exists(cwd_config):
                config_path = cwd_config

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 注册所有工具
    tools = [
        # 社团信息查询工具
        query_all_clubs,
        query_club_by_name,
        query_clubs_by_type,
        compare_clubs,
        get_popular_clubs,

        # 志愿填报工具
        validate_student_id,
        validate_club_name,
        submit_application,
        update_interest_tags,
        query_application,

        # 优先级计算工具
        calculate_priority_score,
        batch_calculate_priority,
        get_priority_ranking,
        update_grade_score_config,

        # 录取与调剂工具
        get_club_quota_status,
        check_quota_available,
        run_admission_process,
        find_adjustment_club,
        query_admission_result,
        get_admission_statistics
    ]

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
