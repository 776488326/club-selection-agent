import sys
sys.path.insert(0, '/workspace/projects/src')
from storage.database.supabase_client import get_supabase_client

client = get_supabase_client()

# 查询所有学生
students = client.table('student_applications').select('*').execute()
print("所有学生状态：")
for s in students.data:
    print(f"- {s['student_name']}: {s['status']} → {s.get('final_club', '无')}")

# 查询社团名额
print("\n社团录取状态：")
clubs = client.table('clubs').select('*').execute()
status = client.table('admission_status').select('*').execute()
status_map = {s['club_id']: s for s in status.data}

for c in clubs.data:
    s = status_map.get(c['id'])
    print(f"{c['name']}: 总共 {c['total_quota']} 名, 已招 {s['total_used'] if s else 0} 名, 剩余 {c['total_quota'] - (s['total_used'] if s else 0)} 名")
