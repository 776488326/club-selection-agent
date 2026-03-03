"""
智能录取与调剂工具
实现按优先级排序、按志愿录取、调剂的完整录取流程
"""

from langchain.tools import tool, ToolRuntime
import json
from typing import Any, Dict
from storage.database.supabase_client import get_supabase_client


def safe_get_int(data: Dict[str, Any], key: str, default: int = 0) -> int:
    """安全地获取整数值"""
    if not isinstance(data, dict):
        return default
    value = data.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_get_str(data: Dict[str, Any], key: str, default: str = "") -> str:
    """安全地获取字符串值"""
    if not isinstance(data, dict):
        return default
    value = data.get(key)
    if value is None:
        return default
    return str(value)


def safe_get_float(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
    """安全地获取浮点数值"""
    if not isinstance(data, dict):
        return default
    value = data.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@tool
def get_club_quota_status(club_name: str, runtime: ToolRuntime = None) -> str:
    """获取社团名额使用情况

    Args:
        club_name: 社团名称

    Returns:
        str: 名额使用情况
    """
    client = get_supabase_client()

    try:
        # 获取社团信息
        club_response = client.table('clubs').select('*').ilike('name', f'%{club_name}%').execute()
        if not club_response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到社团'{club_name}'"
            }, ensure_ascii=False, indent=2)

        club = club_response.data[0]

        # 获取录取状态
        club_id = safe_get_int(club, 'id')
        status_response = client.table('admission_status').select('*').eq('club_id', club_id).execute()
        admission_status = status_response.data[0] if status_response.data else None

        grade1_quota = safe_get_int(club, 'grade1_quota')
        grade2_quota = safe_get_int(club, 'grade2_quota')
        grade3_quota = safe_get_int(club, 'grade3_quota')
        total_quota = safe_get_int(club, 'total_quota')

        if admission_status:
            grade1_used = safe_get_int(admission_status, 'grade1_used')
            grade2_used = safe_get_int(admission_status, 'grade2_used')
            grade3_used = safe_get_int(admission_status, 'grade3_used')
            total_used = safe_get_int(admission_status, 'total_used')
            grade1_remaining = grade1_quota - grade1_used
            grade2_remaining = grade2_quota - grade2_used
            grade3_remaining = grade3_quota - grade3_used
            total_remaining = total_quota - total_used
        else:
            grade1_remaining = grade1_quota
            grade2_remaining = grade2_quota
            grade3_remaining = grade3_quota
            total_remaining = total_quota

        return json.dumps({
            "success": True,
            "club_name": safe_get_str(club, 'name'),
            "quota": {
                "高一名额": {"total": grade1_quota, "used": safe_get_int(admission_status, 'grade1_used') if admission_status else 0, "remaining": grade1_remaining},
                "高二名额": {"total": grade2_quota, "used": safe_get_int(admission_status, 'grade2_used') if admission_status else 0, "remaining": grade2_remaining},
                "高三名额": {"total": grade3_quota, "used": safe_get_int(admission_status, 'grade3_used') if admission_status else 0, "remaining": grade3_remaining},
                "总名额": {"total": total_quota, "used": safe_get_int(admission_status, 'total_used') if admission_status else 0, "remaining": total_remaining}
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"查询失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def check_quota_available(club_name: str, grade: str, runtime: ToolRuntime = None) -> str:
    """检查某年级在某社团是否还有名额

    Args:
        club_name: 社团名称
        grade: 年级（高一/高二/高三）

    Returns:
        str: 名额检查结果
    """
    client = get_supabase_client()

    try:
        # 获取社团信息
        club_response = client.table('clubs').select('*').ilike('name', f'%{club_name}%').execute()
        if not club_response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到社团'{club_name}'"
            }, ensure_ascii=False, indent=2)

        club = club_response.data[0]

        # 获取录取状态
        club_id = safe_get_int(club, 'id')
        status_response = client.table('admission_status').select('*').eq('club_id', club_id).execute()
        admission_status = status_response.data[0] if status_response.data else None

        # 根据年级检查名额
        quota_map = {
            "高一": safe_get_int(club, 'grade1_quota'),
            "高二": safe_get_int(club, 'grade2_quota'),
            "高三": safe_get_int(club, 'grade3_quota')
        }

        used_map = {
            "高一": safe_get_int(admission_status, 'grade1_used') if admission_status else 0,
            "高二": safe_get_int(admission_status, 'grade2_used') if admission_status else 0,
            "高三": safe_get_int(admission_status, 'grade3_used') if admission_status else 0
        }

        total_quota = quota_map.get(grade, 0)
        used = used_map.get(grade, 0)
        remaining = total_quota - used

        # 同时检查总名额
        total_used = safe_get_int(admission_status, 'total_used') if admission_status else 0
        total_quota_all = safe_get_int(club, 'total_quota')
        total_remaining = total_quota_all - total_used

        available = remaining > 0 and total_remaining > 0

        return json.dumps({
            "success": True,
            "available": available,
            "grade": grade,
            "club_name": safe_get_str(club, 'name'),
            "grade_quota": total_quota,
            "grade_used": used,
            "grade_remaining": remaining,
            "total_quota": total_quota_all,
            "total_used": total_used,
            "total_remaining": total_remaining
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"检查失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def run_admission_process(runtime: ToolRuntime = None) -> str:
    """执行完整的录取流程

    流程：
    1. 按优先级排序学生
    2. 按志愿顺序录取
    3. 处理调剂
    4. 更新录取状态

    Returns:
        str: 录取结果统计
    """
    client = get_supabase_client()

    try:
        # 获取所有待处理的学生，按优先级排序
        students_response = client.table('student_applications').select('*').eq('status', 'pending').order('priority_score', desc=True).execute()

        if not students_response.data:
            return json.dumps({
                "success": True,
                "message": "没有待处理的学生",
                "statistics": {
                    "total": 0,
                    "accepted": 0,
                    "adjusted": 0,
                    "rejected": 0
                }
            }, ensure_ascii=False, indent=2)

        statistics = {
            "total": len(students_response.data),
            "first_preference": 0,
            "second_preference": 0,
            "third_preference": 0,
            "adjusted": 0,
            "rejected": 0
        }

        # 逐个处理学生
        for student in students_response.data:
            student_id = safe_get_str(student, 'student_id')
            grade = safe_get_str(student, 'grade')
            preferences = [
                safe_get_str(student, 'preference1'),
                safe_get_str(student, 'preference2'),
                safe_get_str(student, 'preference3')
            ]

            admitted = False
            admission_round = None

            # 按志愿顺序尝试录取
            for idx, pref in enumerate(preferences):
                if not pref:
                    continue

                # 检查名额
                quota_check = json.loads(check_quota_available(pref, grade))
                if quota_check.get('success') and quota_check.get('available'):
                    # 录取学生
                    club_response = client.table('clubs').select('*').ilike('name', f'%{pref}%').execute()
                    if club_response.data:
                        club = club_response.data[0]

                        # 更新学生录取状态
                        round_names = ["第一志愿", "第二志愿", "第三志愿"]
                        admission_round = round_names[idx]
                        statistics[round_names[idx]] += 1

                        client.table('student_applications').update({
                            'status': 'accepted',
                            'final_club': safe_get_str(club, 'name'),
                            'admission_round': admission_round
                        }).eq('student_id', student_id).execute()

                        # 更新社团录取状态
                        club_id = safe_get_int(club, 'id')
                        update_admission_status(club_id, grade)

                        admitted = True
                        break

            # 如果三个志愿都未录取，尝试调剂
            if not admitted:
                # 调剂逻辑：查找还有名额的相似社团
                adjust_result = json.loads(find_adjustment_club(student))
                if adjust_result.get('success') and adjust_result.get('available'):
                    # 调剂录取
                    club_name = adjust_result.get('club_name')
                    club_response = client.table('clubs').select('*').ilike('name', f'%{club_name}%').execute()
                    if club_response.data:
                        club = club_response.data[0]

                        client.table('student_applications').update({
                            'status': 'adjusted',
                            'final_club': safe_get_str(club, 'name'),
                            'admission_round': '调剂'
                        }).eq('student_id', student_id).execute()

                        # 更新社团录取状态
                        club_id = safe_get_int(club, 'id')
                        update_admission_status(club_id, grade)

                        statistics['adjusted'] += 1
                else:
                    # 未录取
                    client.table('student_applications').update({
                        'status': 'rejected',
                        'admission_round': '未录取'
                    }).eq('student_id', student_id).execute()

                    statistics['rejected'] += 1

        return json.dumps({
            "success": True,
            "message": "录取流程执行完成",
            "statistics": statistics
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"录取流程执行失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


def update_admission_status(club_id: int, grade: str):
    """更新社团录取状态（内部函数）"""
    client = get_supabase_client()

    # 获取录取状态
    status_response = client.table('admission_status').select('*').eq('club_id', club_id).execute()

    if status_response.data:
        # 更新现有记录
        status = status_response.data[0]
        update_data = {'total_used': safe_get_int(status, 'total_used') + 1}

        if grade == "高一":
            update_data['grade1_used'] = safe_get_int(status, 'grade1_used') + 1
        elif grade == "高二":
            update_data['grade2_used'] = safe_get_int(status, 'grade2_used') + 1
        elif grade == "高三":
            update_data['grade3_used'] = safe_get_int(status, 'grade3_used') + 1

        client.table('admission_status').update(update_data).eq('club_id', club_id).execute()
    else:
        # 创建新记录
        new_data = {
            'club_id': club_id,
            'grade1_used': 1 if grade == "高一" else 0,
            'grade2_used': 1 if grade == "高二" else 0,
            'grade3_used': 1 if grade == "高三" else 0,
            'total_used': 1
        }
        client.table('admission_status').insert(new_data).execute()


@tool
def find_adjustment_club(student_data: dict, runtime: ToolRuntime = None) -> str:
    """为未录取的学生查找调剂社团

    Args:
        student_data: 学生数据字典，包含grade, interest_tags等信息

    Returns:
        str: 调剂结果
    """
    client = get_supabase_client()

    try:
        grade = safe_get_str(student_data, 'grade')
        interest_tags = safe_get_str(student_data, 'interest_tags')
        preferences = [
            safe_get_str(student_data, 'preference1'),
            safe_get_str(student_data, 'preference2'),
            safe_get_str(student_data, 'preference3')
        ]

        # 获取所有招新中的社团
        clubs_response = client.table('clubs').select('*').eq('is_active', True).execute()

        if not clubs_response.data:
            return json.dumps({
                "success": False,
                "available": False,
                "message": "没有可调剂的社团"
            }, ensure_ascii=False, indent=2)

        # 过滤掉学生已报志愿的社团
        available_clubs = []
        for club in clubs_response.data:
            club_name = safe_get_str(club, 'name')
            if club_name not in preferences:
                available_clubs.append(club)

        if not available_clubs:
            return json.dumps({
                "success": False,
                "available": False,
                "message": "没有可调剂的社团"
            }, ensure_ascii=False, indent=2)

        # 检查每个社团的名额
        for club in available_clubs:
            club_name = safe_get_str(club, 'name')
            quota_check = json.loads(check_quota_available(club_name, grade))
            if quota_check.get('success') and quota_check.get('available'):
                # 如果有兴趣标签，优先匹配兴趣类型相似的社团
                if interest_tags:
                    try:
                        tags = json.loads(interest_tags)
                        if isinstance(tags, list) and tags:
                            # 简单匹配：社团类型与兴趣标签是否有交集
                            club_type = safe_get_str(club, 'club_type')
                            if any(tag in club_type or club_type in tag for tag in tags):
                                return json.dumps({
                                    "success": True,
                                    "available": True,
                                    "club_name": club_name,
                                    "club_type": club_type,
                                    "reason": "根据兴趣标签匹配"
                                }, ensure_ascii=False, indent=2)
                    except:
                        pass

                # 如果没有兴趣匹配，返回第一个有名额的社团
                return json.dumps({
                    "success": True,
                    "available": True,
                    "club_name": club_name,
                    "club_type": safe_get_str(club, 'club_type'),
                    "reason": "有可用名额"
                }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": False,
            "available": False,
            "message": "没有可调剂的社团（所有社团名额已满）"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"调剂查找失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def query_admission_result(student_id: str, runtime: ToolRuntime = None) -> str:
    """查询学生的录取结果

    Args:
        student_id: 学号

    Returns:
        str: 录取结果
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

        # 获取录取社团的活动信息
        activity_info = None
        final_club = safe_get_str(app, 'final_club')
        if final_club:
            club_response = client.table('clubs').select('*').ilike('name', f'%{final_club}%').execute()
            if club_response.data:
                club = club_response.data[0]
                activity_info = {
                    "activity_time": safe_get_str(club, 'activity_time'),
                    "activity_location": safe_get_str(club, 'activity_location')
                }

        priority_score = safe_get_float(app, 'priority_score')

        return json.dumps({
            "success": True,
            "student_id": student_id,
            "student_name": safe_get_str(app, 'student_name'),
            "status": safe_get_str(app, 'status'),
            "final_club": final_club,
            "admission_round": safe_get_str(app, 'admission_round'),
            "activity_info": activity_info,
            "priority_score": priority_score if priority_score > 0 else None,
            "preferences": {
                "第一志愿": safe_get_str(app, 'preference1'),
                "第二志愿": safe_get_str(app, 'preference2'),
                "第三志愿": safe_get_str(app, 'preference3')
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"查询失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def get_admission_statistics(runtime: ToolRuntime = None) -> str:
    """获取录取统计数据

    Returns:
        str: 统计报告
    """
    client = get_supabase_client()

    try:
        # 获取所有学生数据
        response = client.table('student_applications').select('*').execute()

        if not response.data:
            return json.dumps({
                "success": True,
                "message": "暂无数据",
                "statistics": {}
            }, ensure_ascii=False, indent=2)

        # 统计各状态人数
        status_count = {}
        grade_count = {"高一": 0, "高二": 0, "高三": 0}
        club_admission = {}

        for app in response.data:
            # 状态统计
            status = safe_get_str(app, 'status')
            status_count[status] = status_count.get(status, 0) + 1

            # 年级统计
            grade = safe_get_str(app, 'grade')
            grade_count[grade] = grade_count.get(grade, 0) + 1

            # 社团录取统计
            final_club = safe_get_str(app, 'final_club')
            if final_club:
                if final_club not in club_admission:
                    club_admission[final_club] = {
                        "total": 0,
                        "grade1": 0,
                        "grade2": 0,
                        "grade3": 0
                    }
                club_admission[final_club]["total"] += 1
                if grade == "高一":
                    club_admission[final_club]["grade1"] += 1
                elif grade == "高二":
                    club_admission[final_club]["grade2"] += 1
                elif grade == "高三":
                    club_admission[final_club]["grade3"] += 1

        return json.dumps({
            "success": True,
            "statistics": {
                "total_applications": len(response.data),
                "status_distribution": status_count,
                "grade_distribution": grade_count,
                "club_admission": club_admission
            }
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"统计失败：{str(e)}"
        }, ensure_ascii=False, indent=2)
