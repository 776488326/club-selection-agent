"""
初始化测试数据
向数据库中插入社团信息供测试使用
"""

import sys
import os
sys.path.insert(0, '/workspace/projects/src')

from storage.database.supabase_client import get_supabase_client
import datetime

def init_clubs():
    """初始化社团数据"""
    client = get_supabase_client()

    clubs = [
        {
            "name": "文学社",
            "club_type": "文艺",
            "established_date": "2015-09-01",
            "department": "语文组-王老师",
            "activities": "每周读书分享会、写作交流会、文学沙龙、校刊编辑",
            "activity_time": "每周三下午4:30-6:00",
            "activity_location": "图书馆二楼活动室",
            "requirements": "热爱阅读和写作，每月至少读一本书",
            "target_audience": "对文学、写作感兴趣的学生",
            "total_quota": 30,
            "grade1_quota": 10,
            "grade2_quota": 10,
            "grade3_quota": 10,
            "description": "文学社是喜爱阅读和写作的学生的聚集地，在这里你可以与志同道合的朋友分享读书心得，提升写作能力。",
            "is_active": True
        },
        {
            "name": "话剧社",
            "club_type": "文艺",
            "established_date": "2016-09-01",
            "department": "艺术组-李老师",
            "activities": "话剧排练、舞台表演、剧本创作、校园艺术节",
            "activity_time": "每周二和周五下午4:30-6:00",
            "activity_location": "学校小剧场",
            "requirements": "热爱表演，敢于展示自己，能按时参加排练",
            "target_audience": "对表演艺术感兴趣的学生",
            "total_quota": 25,
            "grade1_quota": 8,
            "grade2_quota": 8,
            "grade3_quota": 9,
            "description": "话剧社培养表演人才，每年举办多场话剧演出，是展示自我的绝佳平台。",
            "is_active": True
        },
        {
            "name": "辩论社",
            "club_type": "学术",
            "established_date": "2014-09-01",
            "department": "政治组-张老师",
            "activities": "辩论技巧训练、模拟辩论赛、校外辩论比赛、思维训练",
            "activity_time": "每周一和周四下午4:30-6:00",
            "activity_location": "教学楼306教室",
            "requirements": "思维敏捷，口齿伶俐，善于思辨",
            "target_audience": "对辩论、思辨感兴趣的学生",
            "total_quota": 20,
            "grade1_quota": 6,
            "grade2_quota": 7,
            "grade3_quota": 7,
            "description": "辩论社锻炼逻辑思维和表达能力，每年参加市级辩论赛并多次获奖。",
            "is_active": True
        },
        {
            "name": "机器人社",
            "club_type": "科技",
            "established_date": "2017-09-01",
            "department": "物理组-陈老师",
            "activities": "机器人编程、机械组装、创客项目、机器人竞赛",
            "activity_time": "每周三和周五下午4:30-6:30",
            "activity_location": "科技楼实验室",
            "requirements": "对编程和机械感兴趣，有较强动手能力",
            "target_audience": "对科技、编程、机器人感兴趣的学生",
            "total_quota": 15,
            "grade1_quota": 5,
            "grade2_quota": 5,
            "grade3_quota": 5,
            "description": "机器人社培养创新精神和实践能力，每年参加全国青少年机器人竞赛。",
            "is_active": True
        },
        {
            "name": "篮球社",
            "club_type": "运动",
            "established_date": "2013-09-01",
            "department": "体育组-刘教练",
            "activities": "篮球训练、校队选拔、校内比赛、校外交流赛",
            "activity_time": "每周一、三、五下午4:30-6:00",
            "activity_location": "学校篮球场",
            "requirements": "热爱篮球，具备基本篮球技能，能坚持训练",
            "target_audience": "篮球爱好者",
            "total_quota": 40,
            "grade1_quota": 15,
            "grade2_quota": 12,
            "grade3_quota": 13,
            "description": "篮球社提高篮球技能，培养团队合作精神，每年参加市级高中篮球联赛。",
            "is_active": True
        },
        {
            "name": "羽毛球社",
            "club_type": "运动",
            "established_date": "2015-09-01",
            "department": "体育组-王教练",
            "activities": "羽毛球技术训练、双打比赛、校内联赛",
            "activity_time": "每周二和周四下午4:30-6:00",
            "activity_location": "学校体育馆",
            "requirements": "热爱羽毛球，具备基本技术",
            "target_audience": "羽毛球爱好者",
            "total_quota": 30,
            "grade1_quota": 10,
            "grade2_quota": 10,
            "grade3_quota": 10,
            "description": "羽毛球社提供专业的训练指导，提高羽毛球技能，丰富课余生活。",
            "is_active": True
        },
        {
            "name": "志愿者协会",
            "club_type": "公益",
            "established_date": "2012-09-01",
            "department": "德育处-赵老师",
            "activities": "社区服务、公益活动、环保宣传、慈善义卖",
            "activity_time": "每周六上午9:00-11:00（具体活动时间另行通知）",
            "activity_location": "校内及校外社区",
            "requirements": "热心公益，有爱心，愿意奉献时间",
            "target_audience": "热心公益、乐于助人的学生",
            "total_quota": 50,
            "grade1_quota": 20,
            "grade2_quota": 15,
            "grade3_quota": 15,
            "description": "志愿者协会培养社会责任感，组织各类公益活动，传递温暖与爱心。",
            "is_active": True
        },
        {
            "name": "环保社",
            "club_type": "公益",
            "established_date": "2016-09-01",
            "department": "生物组-孙老师",
            "activities": "环保知识讲座、垃圾分类宣传、校园绿化、环保调研",
            "activity_time": "每周三下午4:30-6:00",
            "activity_location": "生物实验室",
            "requirements": "关注环境保护，愿意参与环保行动",
            "target_audience": "对环境保护感兴趣的学生",
            "total_quota": 25,
            "grade1_quota": 8,
            "grade2_quota": 8,
            "grade3_quota": 9,
            "description": "环保社宣传环保知识，组织环保活动，共建绿色校园。",
            "is_active": True
        }
    ]

    # 插入数据
    for club in clubs:
        response = client.table('clubs').insert(club).execute()
        print(f"已插入社团: {club['name']}")

    print("\n社团数据初始化完成！")

if __name__ == "__main__":
    init_clubs()
