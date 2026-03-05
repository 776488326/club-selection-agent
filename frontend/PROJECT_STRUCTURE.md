# 📁 项目结构说明

## 整体目录结构

```
校园社团选课智能体/
├── frontend/                 # 前端应用目录
│   ├── app.py               # Streamlit 应用主文件
│   ├── requirements.txt     # 前端依赖
│   ├── run.sh               # 启动脚本
│   ├── .env.example         # 环境变量模板
│   ├── README.md            # 部署指南
│   ├── GUIDE.md             # 使用指南
│   └── .streamlit/          # Streamlit 配置
│       └── config.toml
├── src/                     # 源代码目录
│   ├── agents/              # Agent 核心
│   │   └── agent.py         # Agent 主逻辑
│   ├── tools/               # 工具定义
│   │   ├── club_query_tool.py       # 社团查询工具
│   │   ├── application_tool.py      # 志愿填报工具
│   │   ├── priority_calc_tool.py    # 优先级计算工具
│   │   └── admission_tool.py        # 录取调剂工具
│   ├── storage/             # 数据存储
│   │   ├── database/        # 数据库
│   │   │   ├── db.py        # 数据库配置
│   │   │   ├── shared/      # 数据模型
│   │   │   │   └── model.py
│   │   │   └── supabase_client.py   # Supabase 客户端
│   │   ├── memory/          # 记忆管理
│   │   └── s3/              # 对象存储
│   ├── utils/               # 工具函数
│   └── main.py              # 入口文件
├── config/                  # 配置目录
│   └── agent_llm_config.json   # Agent 配置
├── assets/                  # 资源目录
│   ├── init_test_data.py    # 初始化测试数据
│   ├── run_admission.py     # 执行录取流程
│   └── check_status.py      # 查询系统状态
├── scripts/                 # 脚本目录
├── tests/                   # 测试目录
├── docs/                    # 文档目录
├── requirements.txt         # 主项目依赖
├── AGENT.md                 # Agent 规范
├── README.md                # 项目说明
└── .coze                    # Coze 配置
```

---

## 📦 核心模块说明

### 1. frontend/（前端模块）

负责用户界面和交互。

| 文件 | 说明 |
|------|------|
| `app.py` | Streamlit 应用主文件，包含 UI 渲染和 Agent 调用逻辑 |
| `requirements.txt` | 前端依赖（Streamlit 等） |
| `run.sh` | 快速启动脚本 |
| `.env.example` | 环境变量模板 |
| `README.md` | 部署指南 |
| `GUIDE.md` | 使用指南 |
| `.streamlit/config.toml` | Streamlit 配置文件（主题、端口等） |

---

### 2. src/agents/（Agent 核心）

Agent 的核心逻辑和状态管理。

| 文件 | 说明 |
|------|------|
| `agent.py` | Agent 主逻辑，包含：
  - `build_agent()`: 构建 Agent 实例
  - `AgentState`: 对话状态管理
  - `_windowed_messages()`: 消息窗口机制 |

---

### 3. src/tools/（工具层）

Agent 的能力封装，分为 4 大类工具。

#### 3.1 club_query_tool.py（社团查询工具）
- `query_all_clubs()` - 查询所有社团
- `query_club_by_name()` - 按名称查社团
- `query_clubs_by_type()` - 按类型查社团
- `compare_clubs()` - 对比多个社团
- `get_popular_clubs()` - 获取热门社团

#### 3.2 application_tool.py（志愿填报工具）
- `validate_student_id()` - 验证学号格式
- `validate_club_name()` - 验证社团名称
- `submit_application()` - 提交志愿
- `update_interest_tags()` - 更新兴趣标签
- `query_application()` - 查询志愿信息

#### 3.3 priority_calc_tool.py（优先级计算工具）
- `calculate_priority_score()` - 计算单个学生优先级
- `batch_calculate_priority()` - 批量计算所有学生优先级
- `get_priority_ranking()` - 获取排名

#### 3.4 admission_tool.py（录取调剂工具）
- `get_club_quota_status()` - 查看名额状态
- `check_quota_available()` - 检查是否有名额
- `run_admission_process()` - 执行录取流程
- `find_adjustment_club()` - 查找调剂社团
- `query_admission_result()` - 查询录取结果
- `get_admission_statistics()` - 获取统计数据

---

### 4. src/storage/（数据存储）

#### 4.1 database/（数据库）
- `db.py` - 数据库配置
- `shared/model.py` - 数据模型定义
- `supabase_client.py` - Supabase 客户端封装

#### 4.2 memory/（记忆管理）
- `memory_saver.py` - LangGraph 记忆保存器

#### 4.3 s3/（对象存储）
- `s3_storage.py` - S3 对象存储封装

---

### 5. config/（配置目录）

| 文件 | 说明 |
|------|------|
| `agent_llm_config.json` | Agent 配置文件，包含：
  - `config`: 模型配置（model、temperature、top_p 等）
  - `sp`: System Prompt（角色定义、任务目标、能力、流程等）
  - `tools`: 工具列表 |

---

### 6. assets/（资源目录）

| 文件 | 说明 |
|------|------|
| `init_test_data.py` | 初始化测试数据（8 个社团） |
| `run_admission.py` | 手动执行录取流程脚本 |
| `check_status.py` | 查询系统状态脚本 |

---

## 🔧 配置文件说明

### 1. agent_llm_config.json

```json
{
  "config": {
    "model": "doubao-seed-1-6-251015",      // 模型 ID
    "temperature": 0.7,                      // 温度参数
    "top_p": 0.9,                           // Top-p 采样
    "max_completion_tokens": 10000,         // 最大生成长度
    "timeout": 600,                         // 超时时间
    "thinking": "disabled"                  // 思考模式
  },
  "sp": "...",                               // System Prompt
  "tools": [...]                            // 工具列表
}
```

### 2. .streamlit/config.toml

```toml
[theme]
primaryColor = "#667eea"                    # 主题色
backgroundColor = "#ffffff"                 # 背景色
secondaryBackgroundColor = "#f8f9fa"        # 次要背景色
textColor = "#262730"                       # 文字颜色

[client]
showErrorDetails = true                     # 显示错误详情
maxUploadSize = 200                         # 最大上传大小

[runner]
fastReruns = true                           # 快速重运行

[logger]
level = "info"                              # 日志级别
```

### 3. .env.example

```bash
COZE_WORKSPACE_PATH=/path/to/project        # 工作区路径
COZE_WORKLOAD_IDENTITY_API_KEY=xxx          # API Key
COZE_INTEGRATION_MODEL_BASE_URL=xxx         # 模型 Base URL
SUPABASE_URL=xxx                            # Supabase URL
SUPABASE_KEY=xxx                            # Supabase Key
LOG_LEVEL=INFO                              # 日志级别
```

---

## 🔄 数据流说明

### 1. 用户查询社团信息

```
用户 → Streamlit 界面 → Agent → query_club_by_name()
                          ↓
                      Supabase 数据库
                          ↓
                      返回社团信息
                          ↓
                      Agent 格式化输出
                          ↓
                      Streamlit 展示
```

### 2. 用户填报志愿

```
用户 → Streamlit 界面 → 收集信息（学号、姓名、年级、志愿）
                          ↓
                      Agent 验证（validate_student_id、validate_club_name）
                          ↓
                      submit_application()
                          ↓
                      Supabase 插入数据
                          ↓
                      返回成功提示
```

### 3. 教务执行录取

```
教务 → run_admission.py 脚本
        ↓
    batch_calculate_priority()  // 计算所有学生优先级
        ↓
    run_admission_process()     // 执行录取流程
        ↓
    - 按优先级排序
    - 按志愿录取
    - 智能调剂
        ↓
    更新录取状态
        ↓
    生成统计报告
```

### 4. 学生查询结果

```
学生 → Streamlit 界面 → Agent → query_admission_result()
                              ↓
                          Supabase 查询
                              ↓
                          返回录取状态
                              ↓
                          Agent 格式化输出
                              ↓
                          Streamlit 展示
```

---

## 🗄️ 数据库表结构

### clubs（社团表）
```sql
- id: 主键
- name: 社团名称
- type: 社团类型
- description: 描述
- advisor: 指导老师
- established_date: 成立时间
- activity_time: 活动时间
- location: 活动地点
- requirements: 招募要求
- total_quota: 总名额
- grade1_quota: 高一名额
- grade2_quota: 高二名额
- grade3_quota: 高三名额
```

### student_applications（学生志愿表）
```sql
- id: 主键
- student_id: 学号
- student_name: 姓名
- grade: 年级
- preference1: 第一志愿
- preference2: 第二志愿
- preference3: 第三志愿
- interest_tags: 兴趣标签
- priority_score: 优先级分数
- status: 状态（pending/accepted/rejected）
- final_club: 最终录取社团
- admission_round: 录取轮次
```

### admission_status（录取状态表）
```sql
- id: 主键
- club_id: 社团 ID
- grade1_used: 高一已用名额
- grade2_used: 高二已用名额
- grade3_used: 高三已用名额
- total_used: 总已用名额
```

---

## 🚀 快速开始

### 1. 初始化环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r frontend/requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp frontend/.env.example frontend/.env

# 编辑 .env 文件，填入你的配置
nano frontend/.env
```

### 3. 初始化数据库

```bash
# 在 Supabase 中创建数据库和表
# 或运行初始化脚本
python assets/init_test_data.py
```

### 4. 启动前端

```bash
# 方式一：使用启动脚本
cd frontend
./run.sh

# 方式二：直接启动
streamlit run frontend/app.py
```

### 5. 访问应用

打开浏览器访问：http://localhost:8501

---

## 📚 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.11+ | 编程语言 |
| LangChain | Agent 框架 |
| LangGraph | 工作流编排 |
| Streamlit | 前端框架 |
| Supabase | 数据库 |
| PostgreSQL | 数据库引擎 |
| 豆包大模型 | LLM |

---

## 🔧 开发规范

### 1. 代码风格
- 遵循 PEP 8 规范
- 使用类型注解
- 添加文档字符串

### 2. 工具开发
- 使用 `@tool` 装饰器
- 返回字符串类型
- 添加详细注释

### 3. 错误处理
- 使用 try-except 捕获异常
- 返回友好的错误信息
- 记录日志

### 4. 数据安全
- 使用环境变量存储敏感信息
- 不在前端暴露 API Key
- 数据脱敏处理

---

## 📞 支持

如有问题，请查看：
- 部署指南：`frontend/README.md`
- 使用指南：`frontend/GUIDE.md`
- 项目说明：`README.md`
