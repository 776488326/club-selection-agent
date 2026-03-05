# 🚀 部署到 Streamlit Cloud - 操作步骤

## 📋 当前状态

- ✅ 本地代码已完成
- ✅ Git 仓库已初始化
- ✅ 代码已提交到本地
- ⏳ 需要配置 GitHub 远程仓库
- ⏳ 需要推送到 GitHub
- ⏳ 需要在 Streamlit Cloud 部署

---

## 🎯 完整部署步骤

### 第一步：创建 GitHub 仓库

#### 通过 GitHub 网页创建（推荐）

1. **访问 GitHub**
   - 打开 https://github.com
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角的 "+" 图标
   - 选择 "New repository"

3. **填写仓库信息**
   - **Repository name**: `club-selection-agent`（或你喜欢的名字）
   - **Description**: 校园社团选课智能体
   - **Public/Private**: 选择 Public（推荐）
   - **Initialize**: 不要勾选任何选项（我们已经有了）

4. **创建仓库**
   - 点击 "Create repository"

5. **复制仓库地址**
   - 页面会显示仓库地址，格式如：
     ```
     https://github.com/your-username/club-selection-agent.git
     ```

---

### 第二步：配置远程仓库并推送

执行以下命令（替换 YOUR_REPOSITORY_URL）：

```bash
# 1. 添加远程仓库
git remote add origin YOUR_REPOSITORY_URL

# 2. 验证远程仓库
git remote -v

# 3. 推送到 GitHub
git push -u origin main
```

**示例**：
```bash
git remote add origin https://github.com/johndoe/club-selection-agent.git
git push -u origin main
```

**如果需要身份验证**：
- GitHub 会提示输入用户名和密码
- 密码使用 Personal Access Token（不是登录密码）
- 获取 Token: https://github.com/settings/tokens

---

### 第三步：部署到 Streamlit Cloud

#### 1. 访问 Streamlit Cloud

打开浏览器访问：https://share.streamlit.io

#### 2. 登录

- 使用你的 GitHub 账号登录
- 授权 Streamlit 访问你的仓库

#### 3. 创建新应用

1. 点击右上角的 **"New app"** 按钮

2. 填写应用信息：
   - **Repository**: 选择你刚创建的仓库
   - **Branch**: 选择 `main`
   - **Main file path**: 输入 `frontend/app.py`

3. 点击 **"Deploy"** 按钮

4. 等待部署完成（通常 1-3 分钟）

---

### 第四步：配置环境变量（重要！）

#### 1. 进入应用设置

在 Streamlit Cloud 的应用页面：
1. 点击右上角的 "Settings"（齿轮图标）
2. 在左侧菜单找到 "Secrets"

#### 2. 添加环境变量

点击 "New secret"，添加以下变量：

```toml
COZE_WORKSPACE_PATH = "/mount/src"
COZE_WORKLOAD_IDENTITY_API_KEY = "your_actual_api_key"
COZE_INTEGRATION_MODEL_BASE_URL = "your_actual_base_url"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_supabase_key"
```

**注意**：
- 每个变量单独添加
- 替换为你的实际值
- 不要使用引号（除非值中有空格）

#### 3. 保存并重启

- 点击 "Save" 保存
- 应用会自动重启
- 等待重启完成

---

### 第五步：测试应用

#### 访问应用

打开 Streamlit 提供的 URL，如：
```
https://your-app-name.streamlit.app
```

#### 测试功能

✅ 点击侧边栏 "📚 查询社团信息"
✅ 点击侧边栏 "📝 填报志愿"
✅ 点击侧边栏 "📊 查询录取结果"

---

## 🔧 常见问题

### 问题 1：推送失败 - 认证错误

**解决方案**：使用 GitHub Personal Access Token
1. 访问 https://github.com/settings/tokens
2. 生成新 token（选择 repo 权限）
3. 使用 token 作为密码

### 问题 2：部署失败 - 找不到文件

**解决方案**：
- 确认 `frontend/app.py` 文件存在
- 路径正确（相对于项目根目录）

### 问题 3：Agent 初始化失败

**解决方案**：
- 检查环境变量是否正确
- 检查 API Key 是否有效
- 查看 Streamlit Cloud 日志

---

## 📚 相关文档

- `frontend/DEPLOYMENT_SUMMARY.md` - 部署方案对比
- `frontend/GUIDE.md` - 使用手册
- `frontend/README_FRONTEND.md` - 前端快速指南

---

## 🎉 部署成功标志

✅ 应用可访问
✅ 功能正常
✅ 无错误日志

**祝你部署顺利！** 🚀
