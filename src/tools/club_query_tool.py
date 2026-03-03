"""
社团信息查询工具
支持查询社团信息、按类型或名称搜索、对比多个社团
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
from typing import Optional, List
from storage.database.supabase_client import get_supabase_client


@tool
def query_all_clubs(runtime: ToolRuntime = None) -> str:
    """查询所有社团的基本信息列表

    Returns:
        str: JSON格式的社团列表
    """
    client = get_supabase_client()
    try:
        response = client.table('clubs').select('*').eq('is_active', True).execute()
        clubs = response.data

        # 格式化输出
        result = []
        for club in clubs:
            result.append({
                "name": safe_get_str(club, 'name'),
                "type": safe_get_str(club, 'club_type'),
                "total_quota": safe_get_int(club, 'total_quota'),
                "activity_time": safe_get_str(club, 'activity_time'),
                "activity_location": safe_get_str(club, 'activity_location')
            })

        return json.dumps({
            "success": True,
            "count": len(result),
            "clubs": result
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@tool
def query_club_by_name(club_name: str, runtime: ToolRuntime = None) -> str:
    """根据社团名称查询详细信息

    Args:
        club_name: 社团名称

    Returns:
        str: JSON格式的社团详细信息
    """
    client = get_supabase_client()
    try:
        response = client.table('clubs').select('*').ilike('name', f'%{club_name}%').execute()
        clubs = response.data

        if not clubs:
            return json.dumps({
                "success": False,
                "error": f"未找到名称包含'{club_name}'的社团"
            }, ensure_ascii=False, indent=2)

        # 格式化输出
        result = []
        for club in clubs:
            if not isinstance(club, dict):
                continue
            established_date = club.get('established_date') if isinstance(club, dict) else None
            result.append({
                "name": safe_get_str(club, 'name'),
                "type": safe_get_str(club, 'club_type'),
                "established_date": str(established_date) if established_date else None,
                "department": safe_get_str(club, 'department'),
                "activities": safe_get_str(club, 'activities'),
                "activity_time": safe_get_str(club, 'activity_time'),
                "activity_location": safe_get_str(club, 'activity_location'),
                "requirements": safe_get_str(club, 'requirements'),
                "target_audience": safe_get_str(club, 'target_audience'),
                "total_quota": safe_get_int(club, 'total_quota'),
                "grade1_quota": safe_get_int(club, 'grade1_quota'),
                "grade2_quota": safe_get_int(club, 'grade2_quota'),
                "grade3_quota": safe_get_int(club, 'grade3_quota'),
                "description": safe_get_str(club, 'description')
            })

        return json.dumps({
            "success": True,
            "count": len(result),
            "clubs": result
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@tool
def query_clubs_by_type(club_type: str, runtime: ToolRuntime = None) -> str:
    """根据社团类型查询社团

    Args:
        club_type: 社团类型（学术/文艺/运动/公益等）

    Returns:
        str: JSON格式的社团列表
    """
    client = get_supabase_client()
    try:
        response = client.table('clubs').select('*').eq('club_type', club_type).eq('is_active', True).execute()
        clubs = response.data

        # 格式化输出
        result = []
        for club in clubs:
            result.append({
                "name": safe_get_str(club, 'name'),
                "type": safe_get_str(club, 'club_type'),
                "activities": safe_get_str(club, 'activities'),
                "total_quota": safe_get_int(club, 'total_quota'),
                "activity_time": safe_get_str(club, 'activity_time'),
                "activity_location": safe_get_str(club, 'activity_location'),
                "target_audience": safe_get_str(club, 'target_audience')
            })

        return json.dumps({
            "success": True,
            "count": len(result),
            "clubs": result,
            "type": club_type
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@tool
def compare_clubs(club_names: str, runtime: ToolRuntime = None) -> str:
    """对比两个或多个社团的信息

    Args:
        club_names: 社团名称列表，用逗号分隔，例如："文学社,话剧社,辩论社"

    Returns:
        str: JSON格式的对比结果
    """
    client = get_supabase_client()
    try:
        # 解析社团名称列表
        names = [name.strip() for name in club_names.split(',')]

        results = []
        for name in names:
            response = client.table('clubs').select('*').ilike('name', f'%{name}%').execute()
            if response.data:
                club = response.data[0]
                results.append({
                    "name": safe_get_str(club, 'name'),
                    "type": safe_get_str(club, 'club_type'),
                    "activities": safe_get_str(club, 'activities'),
                    "activity_time": safe_get_str(club, 'activity_time'),
                    "activity_location": safe_get_str(club, 'activity_location'),
                    "requirements": safe_get_str(club, 'requirements'),
                    "target_audience": safe_get_str(club, 'target_audience'),
                    "total_quota": safe_get_int(club, 'total_quota'),
                    "grade1_quota": safe_get_int(club, 'grade1_quota'),
                    "grade2_quota": safe_get_int(club, 'grade2_quota'),
                    "grade3_quota": safe_get_int(club, 'grade3_quota')
                })

        if not results:
            return json.dumps({
                "success": False,
                "error": "未找到匹配的社团"
            }, ensure_ascii=False, indent=2)

        # 生成对比信息
        comparison = {
            "success": True,
            "count": len(results),
            "clubs": results,
            "comparison_summary": {
                "types": list(set([safe_get_str(c, 'type') for c in results])),
                "max_quota": max([safe_get_int(c, 'total_quota') for c in results]),
                "min_quota": min([safe_get_int(c, 'total_quota') for c in results])
            }
        }

        return json.dumps(comparison, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@tool
def get_popular_clubs(limit: int = 5, runtime: ToolRuntime = None) -> str:
    """获取热门社团（按名额排序）

    Args:
        limit: 返回数量，默认5

    Returns:
        str: JSON格式的热门社团列表
    """
    client = get_supabase_client()
    try:
        response = client.table('clubs').select('*').eq('is_active', True).order('total_quota', desc=True).limit(limit).execute()
        clubs = response.data

        result = []
        for club in clubs:
            result.append({
                "name": safe_get_str(club, 'name'),
                "type": safe_get_str(club, 'club_type'),
                "activities": safe_get_str(club, 'activities'),
                "total_quota": safe_get_int(club, 'total_quota'),
                "target_audience": safe_get_str(club, 'target_audience')
            })

        return json.dumps({
            "success": True,
            "count": len(result),
            "popular_clubs": result
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)
