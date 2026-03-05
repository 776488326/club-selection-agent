# 🚀 部署到 Streamlit Cloud - 操作步骤

## 📋 部署清单

- ✅ 本地代码已完成
- ✅ Git 仓库已初始化
- ✅ 代码已提交到本地
- ⏳ 需要配置 GitHub 远程仓库
- ⏳ 需要推送到 GitHub
- ⏳ 需要在 Streamlit Cloud 部署

---

## 🎯 完整部署步骤

### 第一步：创建 GitHub 仓库

#### 方式 A：通过 GitHub 网页创建（推荐）

1. **访问 GitHub**
   - 打开 https://github.com
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角的 "+" 图标
   - 选择 "New repository"

3. **填写仓库信息**
   - **Repository name**: `club-selection-agent`（或你喜欢的名字）
   - **Description**: 校园社团选课智能体
   - **Public/Private**: 选择 Public（推荐）或 Private
   - **Initialize this repository**: ❌ 不要勾选（我们已经有了）
   - **Add a README file**: ❌ 不要勾选

4. **创建仓库**
   - 点击 "Create repository"

5. **获取仓库地址**
   - 创建后会显示仓库地址，格式如：
     ```
     https://github.com/your-username/club-selection-agent.git
     ```

---

#### 方式 B：使用 GitHub CLI（gh）

```bash
# 安装 GitHub CLI（如果没有安装）
# Ubuntu/Debian:
sudo apt install gh

# macOS:
brew install gh

# 登录 GitHub
gh auth login

# 创建仓库
gh repo create club-selection-agent --public --description "校园社团选课智能体"

# 配置远程仓库
git remote add origin https://github.com/your-username/club-selection-agent.git
```

---

### 第二步：配置远程仓库并推送

执行以下命令：

```bash
cd /workspace/projects

# 添加远程仓库（请替换为你的 GitHub 仓库地址）
git remote add origin https://github.com/your-username/club-selection-agent.git

# 验证远程仓库
git remote -v

# 推送到 GitHub
git push -u origin main
```

**如果遇到错误**：
- 如果提示 "failed to push some refs"，使用强制推送：
  ```bash
  git push -u origin main --force
  ```
- 如果提示认证错误，使用 SSH 方式：
  ```bash
  git remote set-url origin git@github.com:your-username/club-selection-agent.git
  git push -u origin main
  ```

---

### 第三步：部署到 Streamlit Cloud

#### 1. 访问 Streamlit Cloud

打开浏览器访问：https://share.streamlit.io

#### 2. 登录

- 使用你的 GitHub 账号登录
- 授权 Streamlit 访问你的 GitHub 仓库

#### 3. 创建新应用

1. 点击右上角的 **"New app"** 按钮

2. 填写应用信息：
   - **Repository**: 从下拉菜单选择你刚创建的仓库（如 `your-username/club-selection-agent`）
   - **Branch**: 选择 `main`
   - **Main file path**: 输入 `frontend/app.py`

3. 点击 **"Deploy"** 按钮

4. 等待部署完成（通常 1-3 分钟）

5. 部署成功后，你会看到：
   - 应用访问地址：`https://your-app-name.streamlit.app`
   - 部署日志

---

### 第四步：配置环境变量（重要！）

#### 1. 进入应用设置

在 Streamlit Cloud 的应用页面：
1. 点击右上角的 "Settings"（齿轮图标）
2. 在左侧菜单找到 "Secrets" 或 "Environment variables"

#### 2. 添加环境变量

点击 "New secret" 或 "Add variable"，添加以下变量：

```toml
# 1. Coze 工作区路径
COZE_WORKSPACE_PATH = "/mount/src"

# 2. API Key（请替换为你的实际值）
COZE_WORKLOAD_IDENTITY_API_KEY = "your_actual_api_key_here"

# 3. 模型 Base URL（请替换为你的实际值）
COZE_INTEGRATION_MODEL_BASE_URL = "your_actual_base_url_here"

# 4. Supabase URL（请替换为你的实际值）
SUPABASE_URL = "https://your-project.supabase.co"

# 5. Supabase Key（请替换为你的实际值）
SUPABASE_KEY = "your_supabase_key_here"
```

**注意**：
- 每个变量单独添加
- 不要使用引号包裹值（除非值中包含空格）
- 确保所有值都是正确的

#### 3. 保存并重启

- 点击 "Save" 保存配置
- 应用会自动重启
- 等待重启完成（通常 1-2 分钟）

---

### 第五步：测试应用

#### 1. 访问应用

打开 Streamlit 提供的 URL，如：
```
https://your-app-name.streamlit.app
```

#### 2. 测试基本功能

✅ **测试 1：查询社团**
- 点击侧边栏 "📚 查询社团信息"
- 应该显示社团列表

✅ **测试 2：填报志愿**
- 点击侧边栏 "📝 填报志愿"
- 尝试提交一个测试志愿

✅ **测试 3：查询结果**
- 点击侧边栏 "📊 查询录取结果"
- 输入学号查询

#### 3. 查看日志

如果遇到问题，在 Streamlit Cloud：
1. 点击应用页面的 "Logs" 标签
2. 查看错误信息
3. 根据错误信息调整配置

---

## 🔧 常见问题排查

### 问题 1：推送失败 - 认证错误

**错误信息**：
```
fatal: Authentication failed
```

**解决方案**：
- 使用 GitHub Personal Access Token
  1. 访问 https://github.com/settings/tokens
  2. 点击 "Generate new token" → "Classic"
  3. 选择权限（repo 全选）
  4. 生成 token
  5. 使用 token 作为密码

```bash
git push -u origin main
# Username: your_github_username
# Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 问题 2：部署失败 - 找不到文件

**错误信息**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'frontend/app.py'
```

**解决方案**：
- 确认 `frontend/app.py` 文件存在
- 确认文件路径正确（相对于项目根目录）
- 重新推送代码

---

### 问题 3：Agent 初始化失败

**错误信息**：
```
Agent 初始化失败: ...
```

**解决方案**：
1. 检查环境变量是否正确配置
2. 检查 API Key 是否有效
3. 检查 Supabase 连接是否正常
4. 查看 Streamlit Cloud 日志

---

### 问题 4：数据库连接失败

**错误信息**：
```
Supabase connection error
```

**解决方案**：
1. 检查 SUPABASE_URL 和 SUPABASE_KEY 是否正确
2. 确认 Supabase 项目是否正常运行
3. 检查数据库表是否已创建
4. 在 Supabase 控制台测试连接

---

## 📊 部署成功标志

✅ **部署成功后，你应该看到**：

1. **应用可访问**
   - URL 格式：`https://your-app-name.streamlit.app`
   - 页面正常加载，显示标题和侧边栏

2. **功能正常**
   - 侧边栏按钮可以点击
   - 输入框可以输入
   - 对话正常进行

3. **无错误日志**
   - Streamlit Cloud 日志无 ERROR 级别信息
   - 应用正常运行

---

## 🎉 恭喜！

部署完成后，你的应用已经上线了！

**分享给他人**：
- 复制 Streamlit 提供的 URL
- 发送给同学、老师或用户
- 他们可以直接访问使用

**自定义域名**（可选）：
- 在 Streamlit Cloud 的 Settings 中配置自定义域名
- 需要购买域名并配置 DNS

---

## 📞 需要帮助？

- 查看 `frontend/DEPLOYMENT_SUMMARY.md`
- 查看 `frontend/GUIDE.md`
- 访问 Streamlit 社区：https://discuss.streamlit.io

---

## ✨ 下一步

部署成功后，你可以：
1. ✅ 分享给同学使用
2. ✅ 添加更多社团数据
3. ✅ 优化界面和交互
4. ✅ 添加用户认证
5. ✅ 配置自定义域名

**祝你部署顺利！** 🚀
