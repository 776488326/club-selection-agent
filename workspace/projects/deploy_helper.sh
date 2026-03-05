#!/bin/bash

# 部署辅助脚本 - 帮助快速配置和推送代码

set -e

echo "🚀 校园社团选课智能体 - 部署辅助脚本"
echo "======================================"
echo ""

# 检查是否在项目根目录
if [ ! -f "src/agents/agent.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

echo "✅ 已确认在项目根目录"
echo ""

# 显示当前 Git 状态
echo "📋 当前 Git 状态："
git status --short
echo ""

# 显示最近的提交
echo "📝 最近的提交："
git log --oneline -3
echo ""

# 检查远程仓库
echo "🔍 检查远程仓库配置..."
if git remote get-url origin &>/dev/null; then
    echo "✅ 已配置远程仓库："
    git remote -v
else
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请按照以下步骤操作："
    echo ""
    echo "1️⃣  在 GitHub 上创建新仓库："
    echo "   访问 https://github.com/new"
    echo "   仓库名：club-selection-agent"
    echo "   描述：校园社团选课智能体"
    echo ""
    echo "2️⃣  复制仓库地址，格式如："
    echo "   https://github.com/your-username/club-selection-agent.git"
    echo ""
    echo "3️⃣  运行以下命令配置远程仓库："
    echo ""
    echo "   git remote add origin YOUR_REPOSITORY_URL"
    echo "   git remote -v"
    echo ""
    echo "4️⃣  推送代码："
    echo ""
    echo "   git push -u origin main"
    echo ""
    echo "5️⃣  访问 https://share.streamlit.io 部署应用"
    echo ""
    echo "详细步骤请查看：DEPLOY_STEPS.md"
    exit 0
fi

echo ""
echo "======================================"
echo "📦 远程仓库已配置"
echo "======================================"
echo ""

# 询问是否要推送
read -p "是否要推送到远程仓库？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📤 正在推送代码到远程仓库..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 代码推送成功！"
        echo ""
        echo "🎯 下一步操作："
        echo "1. 访问 https://share.streamlit.io"
        echo "2. 使用 GitHub 账号登录"
        echo "3. 点击 'New app' 创建新应用"
        echo "4. 选择你的仓库和 main 分支"
        echo "5. Main file path 填写：frontend/app.py"
        echo "6. 点击 Deploy"
        echo "7. 在 Settings 中配置环境变量（见 DEPLOY_STEPS.md）"
        echo ""
        echo "📚 详细文档："
        echo "- DEPLOY_STEPS.md - 完整部署步骤"
        echo "- frontend/DEPLOYMENT_SUMMARY.md - 部署方案对比"
        echo "- frontend/GUIDE.md - 使用手册"
    else
        echo ""
        echo "❌ 推送失败，请检查："
        echo "1. 网络连接是否正常"
        echo "2. GitHub 凭证是否正确"
        echo "3. 远程仓库地址是否正确"
    fi
else
    echo "❌ 已取消推送"
fi

echo ""
