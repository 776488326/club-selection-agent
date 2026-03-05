# 🎓 校园社团选课智能体 - Web 前端

基于 Streamlit 构建的校园社团选课系统前端界面。

## ✨ 功能特性

- 🎨 **现代化 UI 设计**：简洁美观的界面，流畅的用户体验
- 💬 **智能对话交互**：自然语言交流，无需复杂操作
- ⚡ **实时响应**：快速处理用户请求
- 📱 **响应式设计**：支持 PC 和移动端访问
- 🎯 **快捷功能**：侧边栏快速导航常用功能

## 🚀 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
# 方式一：直接运行
streamlit run app.py

# 方式二：指定端口
streamlit run app.py --server.port 8501

# 方式三：允许外部访问
streamlit run app.py --server.address 0.0.0.0
```

### 3. 访问应用

打开浏览器访问：`http://localhost:8501`

## 🌐 部署到线上

### 方案一：Streamlit Cloud（推荐，免费）

Streamlit Cloud 是官方提供的免费托管平台，非常适合快速部署。

#### 步骤：

1. **准备代码**
   ```bash
   # 确保项目结构如下
   project/
   ├── frontend/
   │   ├── app.py
   │   ├── requirements.txt
   │   └── .streamlit/
   │       └── config.toml
   ├── src/
   │   ├── agents/
   │   ├── tools/
   │   └── storage/
   ├── config/
   └── requirements.txt (主项目依赖)
   ```

2. **推送到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```

3. **部署到 Streamlit Cloud**
   - 访问：https://share.streamlit.io
   - 点击 "New app"
   - 填写信息：
     - **Repository**: 选择你的 GitHub 仓库
     - **Branch**: main
     - **Main file path**: frontend/app.py
   - 点击 "Deploy"
   - 等待部署完成（通常 1-2 分钟）

4. **配置环境变量**（重要！）
   
   在 Streamlit Cloud 的 Settings > Secrets 中添加以下配置：
   ```toml
   COZE_WORKSPACE_PATH = "/mount/src"
   COZE_WORKLOAD_IDENTITY_API_KEY = "your_api_key"
   COZE_INTEGRATION_MODEL_BASE_URL = "your_base_url"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ```

5. **完成！** 
   - 你的应用已上线，可以通过 Streamlit 提供的 URL 访问
   - 示例 URL: `https://your-app-name.streamlit.app`

---

### 方案二：Docker 部署

适合需要更多控制权和自定义配置的场景。

#### 1. 创建 Dockerfile

```dockerfile
# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY .. /app
COPY requirements.txt /app/frontend/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r /app/frontend/requirements.txt

# 暴露端口
EXPOSE 8501

# 启动应用
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. 构建镜像

```bash
cd frontend
docker build -t club-selection-app .
```

#### 3. 运行容器

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

#### 4. 部署到云服务器

```bash
# SSH 连接到服务器
ssh user@your-server

# 拉取镜像（如果推送到 Docker Hub）
docker pull your-username/club-selection-app

# 运行容器
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  --name club-selection \
  your-username/club-selection-app

# 配置 Nginx 反向代理（可选）
# 配置域名和 SSL 证书
```

---

### 方案三：云服务器部署

适合需要完全控制服务器的场景（如阿里云、腾讯云、AWS 等）。

#### 1. 服务器准备

```bash
# 安装 Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-venv

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r frontend/requirements.txt
```

#### 2. 安装 Supervisor（进程管理）

```bash
sudo apt install supervisor

# 创建配置文件
sudo nano /etc/supervisor/conf.d/club-selection.conf
```

配置内容：
```ini
[program:club-selection]
directory=/path/to/your/project/frontend
command=/path/to/venv/bin/streamlit run app.py --server.port=8501
user=your-username
autostart=true
autorestart=true
stderr_logfile=/var/log/club-selection.err.log
stdout_logfile=/var/log/club-selection.out.log
environment=COZE_WORKSPACE_PATH="/path/to/project"
```

启动服务：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start club-selection
```

#### 3. 配置 Nginx 反向代理

```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/club-selection
```

配置内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/club-selection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. 配置 HTTPS（使用 Let's Encrypt）

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 📋 部署清单

部署前请确保以下事项已完成：

- [ ] 所有依赖已添加到 `requirements.txt`
- [ ] Supabase 数据库已创建并配置好表结构
- [ ] 环境变量已正确配置
- [ ] 本地测试通过，功能正常
- [ ] 代码已推送到 GitHub（如使用 Streamlit Cloud）
- [ ] 已准备好 API Key 和数据库凭证

## 🔧 环境变量配置

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

## 🐛 常见问题

### 1. Agent 初始化失败

**问题**：显示 "Agent 初始化失败"

**解决**：
- 检查环境变量是否正确配置
- 确认 Supabase 连接正常
- 查看日志获取详细错误信息

### 2. 数据库连接超时

**问题**：查询社团信息时提示连接超时

**解决**：
- 检查 Supabase URL 和 Key 是否正确
- 确认网络连接正常
- 检查 Supabase 服务状态

### 3. Streamlit Cloud 部署失败

**问题**：Streamlit Cloud 部署时提示错误

**解决**：
- 确保项目根目录有 `frontend/app.py`
- 检查 `requirements.txt` 文件格式
- 查看 Streamlit Cloud 的部署日志

### 4. 样式显示异常

**问题**：界面样式不正常

**解决**：
- 清除浏览器缓存
- 确认 `.streamlit/config.toml` 文件存在
- 检查 CSS 样式代码

## 📊 性能优化建议

1. **使用缓存**：对于频繁查询的数据使用 Streamlit 的缓存功能
2. **异步处理**：对于耗时操作使用异步处理
3. **CDN 加速**：使用 CDN 加速静态资源加载
4. **数据库优化**：为常用查询字段添加索引
5. **负载均衡**：高并发场景下使用负载均衡

## 🔐 安全建议

1. **环境变量**：敏感信息（API Key、数据库凭证）使用环境变量
2. **HTTPS**：生产环境必须使用 HTTPS
3. **访问控制**：添加用户认证和授权
4. **日志脱敏**：日志中不输出敏感信息
5. **定期备份**：定期备份数据库

## 📞 技术支持

如遇到问题，可以：
1. 查看 Streamlit 官方文档：https://docs.streamlit.io
2. 查看 Streamlit Cloud 文档：https://docs.streamlit.io/streamlit-cloud
3. 提交 Issue 到项目仓库

## 📄 许可证

MIT License
