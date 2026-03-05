"""
手动执行录取流程脚本

使用方法：
python run_admission.py
"""

import sys
sys.path.insert(0, '/workspace/projects/src')

from storage.database.supabase_client import get_supabase_client
import json

def main():
    """主函数：执行录取流程"""
    client = get_supabase_client()

    print("=" * 60)
    print("🎯 开始执行录取流程")
    print("=" * 60)

    # 获取所有待处理的学生
    students_response = client.table('student_applications').select('*').eq('status', 'pending').order('priority_score', desc=True).execute()

    if not students_response.data:
        print("\n✅ 没有待处理的学生，所有录取已完成！")
        return

    print(f"\n📊 待处理学生数量: {len(students_response.data)}")

    # 逐个处理学生并录取
    for idx, student in enumerate(students_response.data, 1):
        student_id = student['student_id']
        student_name = student['student_name']
        grade = student['grade']
        priority_score = student['priority_score']
        preferences = [
            student['preference1'],
            student['preference2'],
            student['preference3']
        ]

        print(f"\n👤 处理学生 {idx}: {student_name} ({student_id})")
        print(f"   年级: {grade} | 优先级分数: {priority_score}")
        print(f"   志愿: {preferences}")

        admitted = False

        # 按志愿顺序尝试录取
        for pref_idx, pref in enumerate(preferences):
            if not pref:
                continue

            print(f"\n   🔍 检查第{pref_idx+1}志愿: {pref}")

            # 检查名额
            club_response = client.table('clubs').select('*').ilike('name', f'%{pref}%').execute()
            if not club_response.data:
                continue

            club = club_response.data[0]
            club_id = club['id']

            # 获取录取状态
            status_response = client.table('admission_status').select('*').eq('club_id', club_id).execute()
            admission_status = status_response.data[0] if status_response.data else None

            # 计算剩余名额
            grade_quota_map = {"高一": club['grade1_quota'], "高二": club['grade2_quota'], "高三": club['grade3_quota']}
            grade_used_map = {
                "高一": admission_status['grade1_used'] if admission_status else 0,
                "高二": admission_status['grade2_used'] if admission_status else 0,
                "高三": admission_status['grade3_used'] if admission_status else 0
            }
            total_used = admission_status['total_used'] if admission_status else 0

            grade_quota = grade_quota_map.get(grade, 0)
            grade_used = grade_used_map.get(grade, 0)
            grade_remaining = grade_quota - grade_used
            total_remaining = club['total_quota'] - total_used

            available = grade_remaining > 0 and total_remaining > 0

            if available:
                # 录取学生
                round_names = ["第一志愿", "第二志愿", "第三志愿"]

                print(f"   ✅ 录取成功！录取轮次: {round_names[pref_idx]}")

                # 更新学生录取状态
                client.table('student_applications').update({
                    'status': 'accepted',
                    'final_club': club['name'],
                    'admission_round': round_names[pref_idx]
                }).eq('student_id', student_id).execute()

                # 更新社团录取状态
                if admission_status:
                    update_data = {'total_used': total_used + 1}
                    if grade == "高一":
                        update_data['grade1_used'] = grade_used + 1
                    elif grade == "高二":
                        update_data['grade2_used'] = grade_used + 1
                    elif grade == "高三":
                        update_data['grade3_used'] = grade_used + 1
                    client.table('admission_status').update(update_data).eq('club_id', club_id).execute()
                else:
                    new_data = {
                        'club_id': club_id,
                        'grade1_used': 1 if grade == "高一" else 0,
                        'grade2_used': 1 if grade == "高二" else 0,
                        'grade3_used': 1 if grade == "高三" else 0,
                        'total_used': 1
                    }
                    client.table('admission_status').insert(new_data).execute()

                admitted = True
                break
            else:
                print(f"   ❌ 名额不足")

    print("\n✅ 录取流程执行完毕！")

if __name__ == "__main__":
    main()
