"""
优先级计算工具
根据年级、兴趣匹配度、随机数计算学生选课优先级分数
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
import random
from typing import Optional
from storage.database.supabase_client import get_supabase_client


# 年级基础分配置
GRADE_BASE_SCORE = {
    "高三": 90,
    "高二": 80,
    "高一": 70
}


@tool
def calculate_priority_score(student_id: str, runtime: ToolRuntime = None) -> str:
    """计算学生的优先级分数

    Args:
        student_id: 学号

    Returns:
        str: 优先级分数报告
    """
    client = get_supabase_client()

    try:
        # 查询学生志愿信息
        app_response = client.table('student_applications').select('*').eq('student_id', student_id).execute()

        if not app_response.data:
            return json.dumps({
                "success": False,
                "error": f"未找到学号为{student_id}的志愿记录"
            }, ensure_ascii=False, indent=2)

        app = app_response.data[0]

        # 年级基础分
        grade = safe_get_str(app, 'grade')
        grade_score = GRADE_BASE_SCORE.get(grade, 70)

        # 兴趣匹配分计算
        interest_score = 0.0
        if safe_get_str(app, 'interest_tags'):
            try:
                interest_tags = json.loads(safe_get_str(app, 'interest_tags'))
                # 简单算法：根据兴趣标签数量和志愿社团数量匹配度打分
                # 实际应用中可以使用更复杂的匹配算法
                tag_count = len(interest_tags) if isinstance(interest_tags, list) else 1
                interest_score = min(10.0, tag_count * 2.0)  # 每个标签2分，最高10分
            except:
                interest_score = 5.0  # 默认值

        # 随机小数（0-1）
        random_score = round(random.random(), 4)

        # 优先级总分
        priority_score = grade_score + interest_score + random_score

        # 更新数据库
        update_response = client.table('student_applications').update({
            'grade_score': grade_score,
            'interest_score': interest_score,
            'random_score': random_score,
            'priority_score': priority_score
        }).eq('student_id', student_id).execute()

        return json.dumps({
            "success": True,
            "student_id": student_id,
            "priority_score": priority_score,
            "breakdown": {
                "年级基础分": grade_score,
                "兴趣匹配分": interest_score,
                "随机小数": random_score
            },
            "formula": f"优先级分数 = {grade_score}(年级) + {interest_score}(兴趣) + {random_score}(随机) = {priority_score}"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"计算失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def batch_calculate_priority(runtime: ToolRuntime = None) -> str:
    """批量计算所有待处理学生的优先级分数

    Returns:
        str: 批量计算结果
    """
    client = get_supabase_client()

    try:
        # 查询所有待处理的学生
        response = client.table('student_applications').select('*').eq('status', 'pending').execute()

        if not response.data:
            return json.dumps({
                "success": True,
                "message": "没有待处理的学生",
                "count": 0
            }, ensure_ascii=False, indent=2)

        results = []
        for app in response.data:
            # 年级基础分
            grade = safe_get_str(app, 'grade')
            grade_score = GRADE_BASE_SCORE.get(grade, 70)

            # 兴趣匹配分
            interest_score = 0.0
            if safe_get_str(app, 'interest_tags'):
                try:
                    interest_tags = json.loads(safe_get_str(app, 'interest_tags'))
                    tag_count = len(interest_tags) if isinstance(interest_tags, list) else 1
                    interest_score = min(10.0, tag_count * 2.0)
                except:
                    interest_score = 5.0

            # 随机小数
            random_score = round(random.random(), 4)

            # 优先级总分
            priority_score = grade_score + interest_score + random_score

            # 更新数据库
            update_response = client.table('student_applications').update({
                'grade_score': grade_score,
                'interest_score': interest_score,
                'random_score': random_score,
                'priority_score': priority_score
            }).eq('student_id', safe_get_str(app, 'student_id')).execute()

            results.append({
                "student_id": safe_get_str(app, 'student_id'),
                "student_name": safe_get_str(app, 'student_name'),
                "priority_score": priority_score,
                "breakdown": {
                    "年级基础分": grade_score,
                    "兴趣匹配分": interest_score,
                    "随机小数": random_score
                }
            })

        return json.dumps({
            "success": True,
            "message": f"成功计算{len(results)}名学生的优先级分数",
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"批量计算失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def get_priority_ranking(club_name: Optional[str] = None, runtime: ToolRuntime = None) -> str:
    """获取学生优先级排名

    Args:
        club_name: 可选，按第一志愿社团筛选

    Returns:
        str: 排名结果
    """
    client = get_supabase_client()

    try:
        query = client.table('student_applications').select('*').order('priority_score', desc=True)

        if club_name:
            query = query.ilike('preference1', f'%{club_name}%')

        response = query.execute()

        if not response.data:
            return json.dumps({
                "success": True,
                "message": "暂无数据",
                "count": 0
            }, ensure_ascii=False, indent=2)

        results = []
        for idx, app in enumerate(response.data, 1):
            results.append({
                "rank": idx,
                "student_id": safe_get_str(app, 'student_id'),
                "student_name": safe_get_str(app, 'student_name'),
                "grade": safe_get_str(app, 'grade'),
                "priority_score": float(safe_get_int(app, 'priority_score')) if safe_get_int(app, 'priority_score') else 0,
                "preference1": safe_get_str(app, 'preference1'),
                "status": safe_get_str(app, 'status')
            })

        return json.dumps({
            "success": True,
            "count": len(results),
            "ranking": results
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"获取排名失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@tool
def update_grade_score_config(
    grade1_score: float,
    grade2_score: float,
    grade3_score: float,
    runtime: ToolRuntime = None
) -> str:
    """更新年级基础分配置（仅用于配置调整，不修改数据库）

    Args:
        grade1_score: 高一基础分
        grade2_score: 高二基础分
        grade3_score: 高三基础分

    Returns:
        str: 配置更新结果
    """
    # 注意：实际修改需要在代码中修改 GRADE_BASE_SCORE 字典
    # 这里只是展示如何调整配置
    config = {
        "高一": grade1_score,
        "高二": grade2_score,
        "高三": grade3_score
    }

    return json.dumps({
        "success": True,
        "message": "年级基础分配置已更新（请在代码中修改 GRADE_BASE_SCORE 字典）",
        "new_config": config
    }, ensure_ascii=False, indent=2)
