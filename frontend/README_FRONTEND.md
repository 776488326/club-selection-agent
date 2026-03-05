# 🎓 校园社团选课智能体 - Web 前端

基于 Streamlit 构建的校园社团选课系统 Web 前端界面。

## 🌟 特性

- 🎨 **现代化 UI**：简洁美观，用户体验流畅
- 💬 **智能对话**：自然语言交互，无需复杂操作
- ⚡ **实时响应**：快速处理用户请求
- 📱 **响应式**：支持 PC 和移动端
- 🎯 **快捷导航**：侧边栏快速功能入口

## 📦 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
pip install -r ../requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 3. 启动应用

```bash
# 方式一：使用启动脚本
./run.sh

# 方式二：直接启动
streamlit run app.py
```

### 4. 访问应用

打开浏览器访问：http://localhost:8501

---

## 🚀 部署到线上

### 方案一：Streamlit Cloud（推荐）

最简单、免费的部署方案。

1. **推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```

2. **部署到 Streamlit Cloud**
   - 访问：https://share.streamlit.io
   - 点击 "New app"
   - 选择你的 GitHub 仓库
   - Main file path: `frontend/app.py`
   - 点击 "Deploy"

3. **配置环境变量**
   在 Streamlit Cloud 的 Settings > Secrets 中添加：
   ```toml
   COZE_WORKSPACE_PATH = "/mount/src"
   COZE_WORKLOAD_IDENTITY_API_KEY = "your_api_key"
   COZE_INTEGRATION_MODEL_BASE_URL = "your_base_url"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ```

**完成！** 你的应用已上线。

---

### 方案二：Docker 部署

1. **构建镜像**
   ```bash
   docker build -t club-selection-app .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e COZE_WORKSPACE_PATH=/app \
     -e COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key \
     -e COZE_INTEGRATION_MODEL_BASE_URL=your_base_url \
     -e SUPABASE_URL=your_supabase_url \
     -e SUPABASE_KEY=your_supabase_key \
     --name club-selection \
     club-selection-app
   ```

3. **配置 Nginx 反向代理**（可选）

4. **配置 HTTPS**（推荐）

---

## 📚 文档

- **[部署指南](DEPLOYMENT_SUMMARY.md)** - 详细的部署方案对比和步骤
- **[使用指南](GUIDE.md)** - 面向学生的使用手册
- **[项目结构](PROJECT_STRUCTURE.md)** - 完整的项目目录说明

---

## 🎯 功能演示

### 查询社团信息

```
你: 有哪些社团？

助手: 📚 社团列表

1. 【文学社】（文艺类）
   - 活动：读书分享会、写作交流会
   - 名额：30人

2. 【篮球社】（运动类）
   - 活动：篮球训练、校队选拔
   - 名额：40人
...
```

### 兴趣测评

```
你: 我想做兴趣测评

助手: 好呀！让我了解一下你的兴趣 😊

问题 1：你平时更喜欢什么类型的活动？
A. 读书、写作、看电影
B. 运动、健身、户外活动
...

你: 我选 A 和 C

助手: 看起来你喜欢思考和创作！

...（继续提问）
```

### 填报志愿

```
你: 我想填报志愿

助手: 好的！让我帮你完成志愿填报 📝

1️⃣ 学号（6 位数字）：
你: 202301

✅ 学号验证通过

2️⃣ 姓名：
你: 张三

...

📋 请确认你的志愿信息：
学号：202301
姓名：张三
年级：高二
志愿顺序：
1. 机器人社
2. 文学社
3. 辩论社

确认提交吗？
你: 确认

✅ 志愿提交成功！🎉
```

---

## 📋 环境变量

应用需要以下环境变量：

```bash
# Coze 工作区配置
COZE_WORKSPACE_PATH=/path/to/project
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key
COZE_INTEGRATION_MODEL_BASE_URL=your_base_url

# Supabase 数据库配置
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# 可选：其他配置
LOG_LEVEL=INFO
```

---

## 🛠️ 开发

### 目录结构

```
frontend/
├── app.py                  # Streamlit 应用主文件
├── requirements.txt        # 前端依赖
├── run.sh                  # 启动脚本
├── .env.example            # 环境变量模板
├── .streamlit/             # Streamlit 配置
│   └── config.toml
├── README_FRONTEND.md      # 前端说明（本文件）
├── DEPLOYMENT_SUMMARY.md   # 部署指南
├── GUIDE.md                # 使用指南
└── PROJECT_STRUCTURE.md    # 项目结构
```

### 自定义样式

编辑 `app.py` 中的 CSS 部分：

```python
st.markdown("""
<style>
    /* 在这里自定义你的样式 */
</style>
""", unsafe_allow_html=True)
```

### 添加新功能

1. 在 `app.py` 中添加新的侧边栏按钮
2. 在 `handle_user_input()` 中处理新的用户输入
3. 在对应的工具中实现功能

---

## 🔧 故障排查

### 问题 1：Agent 初始化失败

**解决：**
- 检查环境变量是否正确
- 确认 Supabase 连接正常
- 查看日志获取详细错误

### 问题 2：样式显示异常

**解决：**
- 清除浏览器缓存
- 检查 `.streamlit/config.toml` 是否存在
- 检查 CSS 代码

### 问题 3：数据库连接超时

**解决：**
- 检查 Supabase URL 和 Key
- 确认网络连接正常
- 检查 Supabase 服务状态

---

## 📊 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 编程语言 |
| Streamlit | 1.28+ | Web 框架 |
| LangChain | 1.0+ | Agent 框架 |
| LangGraph | 1.0+ | 工作流编排 |
| Supabase | - | 数据库 |

---

## 📄 许可证

MIT License

---

## 📞 支持

- 查看 [部署指南](DEPLOYMENT_SUMMARY.md)
- 查看 [使用指南](GUIDE.md)
- 访问 [Streamlit 官方文档](https://docs.streamlit.io)

---

**祝你使用愉快！** 🎉
