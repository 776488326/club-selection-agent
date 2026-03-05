#!/bin/bash

# Streamlit 启动脚本

echo "🚀 启动校园社团选课助手..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本: $python_version"

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  未检测到虚拟环境，建议先创建虚拟环境"
    echo "💡 运行: python3 -m venv venv && source venv/bin/activate"
fi

# 检查依赖
echo "📦 检查依赖..."
pip install -q -r requirements.txt
pip install -q -r ../requirements.txt

# 设置环境变量（如果不存在）
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，使用系统环境变量"
else
    export $(cat .env | xargs)
fi

# 启动 Streamlit
echo "🎯 启动应用..."
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --browser.gatherUsageStats=false \
    --logger.level=info

echo "✅ 应用已启动！"
echo "🌐 访问地址: http://localhost:8501"
