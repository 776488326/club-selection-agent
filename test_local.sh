#!/bin/bash

# 本地测试脚本

echo "🧪 开始本地测试校园社团选课智能体"
echo "=================================="
echo ""

# 检查环境变量
echo "1️⃣  检查环境变量..."
if [ -z "$COZE_WORKLOAD_IDENTITY_API_KEY" ]; then
    echo "❌ 缺少 COZE_WORKLOAD_IDENTITY_API_KEY"
else
    echo "✅ COZE_WORKLOAD_IDENTITY_API_KEY 已设置"
fi

if [ -z "$COZE_INTEGRATION_MODEL_BASE_URL" ]; then
    echo "❌ 缺少 COZE_INTEGRATION_MODEL_BASE_URL"
else
    echo "✅ COZE_INTEGRATION_MODEL_BASE_URL 已设置"
fi

if [ -z "$SUPABASE_URL" ]; then
    echo "❌ 缺少 SUPABASE_URL"
else
    echo "✅ SUPABASE_URL 已设置"
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "❌ 缺少 SUPABASE_KEY"
else
    echo "✅ SUPABASE_KEY 已设置"
fi

echo ""

# 检查文件
echo "2️⃣  检查文件..."
files=(
    "frontend/app.py"
    "src/agents/agent.py"
    "config/agent_llm_config.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 不存在"
    fi
done

echo ""

# 启动测试
echo "3️⃣  启动测试应用..."
echo "=================================="
echo ""
echo "🚀 启动 Streamlit 应用..."
echo "📍 访问地址: http://localhost:8501"
echo ""
echo "测试清单："
echo "- [ ] 查询社团信息"
echo "- [ ] 兴趣测评"
echo "- [ ] 填报志愿"
echo "- [ ] 查询录取结果"
echo "- [ ] 对话历史"
echo ""
echo "按 Ctrl+C 停止应用"
echo ""
echo "=================================="
echo ""

cd /workspace/projects
streamlit run frontend/app.py --server.port 8501
