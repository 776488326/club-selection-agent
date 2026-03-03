"""
志愿填报工具
支持学生提交社团志愿，包含数据校验和存储
"""


def safe_get_int(data, key, default=0):
    """安全地获取整数值"""
    value = data.get(key) if hasattr(data, 'get') else default
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def safe_get_str(data, key, default=""):
    """安全地获取字符串值"""
    value = data.get(key) if hasattr(data, 'get') else default
    if value is None:
        return default
    return str(value)


from langchain.tools import tool, ToolRuntime
import json
import re
from typing import Optional
from storage.database.supabase_client import get_supabase_client


@tool
def validate_student_id(student_id: str, runtime: ToolRuntime = None) -> str:
    """验证学号格式是否正确（6位数字）

    Args:
        student_id: 学号

    Returns:
        str: 验证结果
    """
    # 验证学号格式：6位数字
    if not re.match(r'^\d{6}$', student_id):
        return json.dumps({
            "success": False,
            "error": "学号格式错误，请输入6位数字"
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "success": True,
        "message": "学号格式正确"
    }, ensure_ascii=False, indent=2)


@tool
def validate_club_name(club_name: str, runtime: ToolRuntime = None) -> str:
    """验证社团名称是否存在

    Args:
        club_name: 社团名称

    Returns:
        str: 验证结果
    """
    client = get_supabase_client()
    try:
        response = client.table('clubs').select('*').ilike('name', club_name).eq('is_active', True).execute()

        if not response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到社团'{club_name}'，请检查社团名称是否正确"
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": True,
            "message": f"社团'{club_name}'存在",
            "club": safe_get_str(response.data[0], 'name')
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"验证失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def submit_application(
    student_id: str,
    student_name: str,
    grade: str,
    preference1: str,
    preference2: Optional[str] = None,
    preference3: Optional[str] = None,
    interest_tags: Optional[str] = None,
    runtime: ToolRuntime = None
) -> str:
    """提交社团志愿

    Args:
        student_id: 学号（6位数字）
        student_name: 学生姓名
        grade: 年级（高一/高二/高三）
        preference1: 第一志愿社团
        preference2: 第二志愿社团（可选）
        preference3: 第三志愿社团（可选）
        interest_tags: 兴趣标签，JSON字符串格式（可选）

    Returns:
        str: 提交结果
    """
    client = get_supabase_client()

    try:
        # 验证学号格式
        if not re.match(r'^\d{6}$', student_id):
            return json.dumps({
                "success": False,
                "error": "学号格式错误，请输入6位数字"
            }, ensure_ascii=False, indent=2)

        # 验证年级
        if grade not in ["高一", "高二", "高三"]:
            return json.dumps({
                "success": False,
                "error": "年级必须为：高一、高二或高三"
            }, ensure_ascii=False, indent=2)

        # 验证第一志愿是否存在
        pref1_response = client.table('clubs').select('*').ilike('name', preference1).eq('is_active', True).execute()
        if not pref1_response.data:
            return json.dumps({
                "success": False,
                "error": f"第一志愿社团'{preference1}'不存在，请检查社团名称"
            }, ensure_ascii=False, indent=2)

        # 验证第二志愿是否存在（如果提供）
        if preference2:
            pref2_response = client.table('clubs').select('*').ilike('name', preference2).eq('is_active', True).execute()
            if not pref2_response.data:
                return json.dumps({
                    "success": False,
                    "error": f"第二志愿社团'{preference2}'不存在，请检查社团名称"
                }, ensure_ascii=False, indent=2)

        # 验证第三志愿是否存在（如果提供）
        if preference3:
            pref3_response = client.table('clubs').select('*').ilike('name', preference3).eq('is_active', True).execute()
            if not pref3_response.data:
                return json.dumps({
                    "success": False,
                    "error": f"第三志愿社团'{preference3}'不存在，请检查社团名称"
                }, ensure_ascii=False, indent=2)

        # 检查学号是否已存在
        existing_response = client.table('student_applications').select('*').eq('student_id', student_id).execute()
        if existing_response.data:
            return json.dumps({
                "success": False,
                "error": f"学号{student_id}已提交过志愿，如需修改请联系教务"
            }, ensure_ascii=False, indent=2)

        # 插入志愿记录
        application_data = {
            'student_id': student_id,
            'student_name': student_name,
            'grade': grade,
            'preference1': safe_get_str(pref1_response.data[0], 'name'),
            'preference2': safe_get_str(pref2_response.data[0], 'name') if preference2 else None,
            'preference3': safe_get_str(pref3_response.data[0], 'name') if preference3 else None,
            'interest_tags': interest_tags,
            'status': 'pending'
        }

        response = client.table('student_applications').insert(application_data).execute()

        return json.dumps({
            "success": True,
            "message": "志愿提交成功！请等待录取结果",
            "application_id": safe_get_str(response.data[0], 'id'),
            "summary": {
                "学号": student_id,
                "姓名": student_name,
                "年级": grade,
                "第一志愿": safe_get_str(pref1_response.data[0], 'name'),
                "第二志愿": safe_get_str(pref2_response.data[0], 'name') if preference2 else "未填写",
                "第三志愿": safe_get_str(pref3_response.data[0], 'name') if preference3 else "未填写"
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"提交失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def update_interest_tags(student_id: str, interest_tags: str, runtime: ToolRuntime = None) -> str:
    """更新学生兴趣标签

    Args:
        student_id: 学号
        interest_tags: 兴趣标签，JSON字符串格式，例如：["文学", "写作", "阅读"]

    Returns:
        str: 更新结果
    """
    client = get_supabase_client()
    try:
        response = client.table('student_applications').update({
            'interest_tags': interest_tags
        }).eq('student_id', student_id).execute()

        if not response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到学号为{student_id}的志愿记录"
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": True,
            "message": "兴趣标签更新成功",
            "interest_tags": interest_tags
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"更新失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def query_application(student_id: str, runtime: ToolRuntime = None) -> str:
    """查询学生的志愿信息

    Args:
        student_id: 学号

    Returns:
        str: 志愿信息
    """
    client = get_supabase_client()
    try:
        response = client.table('student_applications').select('*').eq('student_id', student_id).execute()

        if not response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到学号为{student_id}的志愿记录"
            }, ensure_ascii=False, indent=2)

        app = response.data[0]

        return json.dumps({
            "success": True,
            "application": {
                "学号": safe_get_str(app, 'student_id'),
                "姓名": safe_get_str(app, 'student_name'),
                "年级": safe_get_str(app, 'grade'),
                "兴趣标签": json.loads(safe_get_str(app, 'interest_tags')) if safe_get_str(app, 'interest_tags') else None,
                "第一志愿": safe_get_str(app, 'preference1'),
                "第二志愿": safe_get_str(app, 'preference2'),
                "第三志愿": safe_get_str(app, 'preference3'),
                "优先级分数": float(safe_get_int(app, 'priority_score')) if safe_get_int(app, 'priority_score') else None,
                "状态": safe_get_str(app, 'status'),
                "最终录取社团": safe_get_str(app, 'final_club')
            }
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"查询失败：{str(e)}"
        }, ensure_ascii=False, indent=2)
