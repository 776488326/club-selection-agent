# 🎓 校园社团选课智能体 - 前端部署完整方案

## ✅ 已完成的工作

### 1. 创建前端应用
- ✅ 使用 Streamlit 构建现代化 Web 界面
- ✅ 实现聊天式交互体验
- ✅ 集成 Agent 核心功能
- ✅ 自定义 CSS 样式，界面美观

### 2. 功能模块
- ✅ 侧边栏快速导航（4 个快捷按钮）
- ✅ 聊天界面（支持历史对话）
- ✅ 使用说明和规则展示
- ✅ 清空对话功能

### 3. 配置文件
- ✅ Streamlit 配置（`.streamlit/config.toml`）
- ✅ 环境变量模板（`.env.example`）
- ✅ 依赖清单（`requirements.txt`）
- ✅ 启动脚本（`run.sh`）

### 4. 文档
- ✅ 部署指南（`README.md`）
- ✅ 使用指南（`GUIDE.md`）
- ✅ 项目结构说明（`PROJECT_STRUCTURE.md`）

---

## 🚀 部署方案对比

### 方案一：Streamlit Cloud（推荐 ⭐⭐⭐⭐⭐）

**优点：**
- ✅ 完全免费
- ✅ 一键部署，无需运维
- ✅ 自动 HTTPS
- ✅ 自动扩容
- ✅ 适合个人和小型项目

**缺点：**
- ❌ 资源有限（免费版）
- ❌ 自定义程度较低

**适用场景：**
- 个人项目
- 学校内部系统
- 测试和演示

**部署时间：** 5-10 分钟

---

### 方案二：Docker + 云服务器（推荐 ⭐⭐⭐⭐）

**优点：**
- ✅ 资源可控
- ✅ 可自定义配置
- ✅ 适合中大型项目
- ✅ 可扩展性强

**缺点：**
- ❌ 需要运维成本
- ❌ 需要购买服务器
- ❌ 需要配置域名和 SSL

**适用场景：**
- 正式生产环境
- 需要高可用性
- 多租户系统

**部署时间：** 30-60 分钟

---

### 方案三：云服务器直接部署（推荐 ⭐⭐⭐）

**优点：**
- ✅ 成本低
- ✅ 灵活性高
- ✅ 适合有运维经验

**缺点：**
- ❌ 需要手动配置
- ❌ 缺少容器化隔离

**适用场景：**
- 预算有限
- 有运维团队

**部署时间：** 20-40 分钟

---

## 📋 快速部署检查清单

### 前置准备

- [ ] Python 3.11+ 已安装
- [ ] Git 已安装
- [ ] GitHub 账号已创建
- [ ] Supabase 数据库已创建
- [ ] API Key 和数据库凭证已获取

### 代码准备

- [ ] 代码已推送到 GitHub
- [ ] `frontend/app.py` 文件存在
- [ ] `requirements.txt` 文件完整
- [ ] 环境变量已配置

### Streamlit Cloud 部署

- [ ] 登录 https://share.streamlit.io
- [ ] 创建新应用
- [ ] 配置仓库和分支
- [ ] 配置环境变量
- [ ] 部署成功
- [ ] 测试访问

### Docker 部署

- [ ] Docker 已安装
- [ ] Dockerfile 已创建
- [ ] 镜像已构建
- [ ] 容器已运行
- [ ] Nginx 已配置
- [ ] 域名已解析
- [ ] HTTPS 已配置

---

## 🎯 推荐部署流程（Streamlit Cloud）

### 步骤 1：准备代码（5 分钟）

```bash
# 1. 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit: 校园社团选课智能体"

# 2. 推送到 GitHub
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 步骤 2：部署到 Streamlit Cloud（5 分钟）

1. 访问：https://share.streamlit.io
2. 点击 "New app"
3. 填写信息：
   - **Repository**: 选择你的 GitHub 仓库
   - **Branch**: main
   - **Main file path**: frontend/app.py
4. 点击 "Deploy"
5. 等待部署完成（1-2 分钟）

### 步骤 3：配置环境变量（3 分钟）

1. 进入应用设置
2. 找到 "Secrets" 或 "Environment Variables"
3. 添加以下配置：

```toml
COZE_WORKSPACE_PATH = "/mount/src"
COZE_WORKLOAD_IDENTITY_API_KEY = "your_api_key"
COZE_INTEGRATION_MODEL_BASE_URL = "your_base_url"
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
```

### 步骤 4：测试访问（2 分钟）

- 访问 Streamlit 提供的 URL
- 测试基本功能：
  - 查询社团
  - 填报志愿
  - 查询结果

---

## 🔧 Docker 部署流程

### 步骤 1：创建 Dockerfile

已在 `frontend/Dockerfile` 中创建。

### 步骤 2：构建镜像

```bash
cd frontend
docker build -t club-selection-app .
```

### 步骤 3：运行容器

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

### 步骤 4：配置 Nginx（可选）

创建 Nginx 配置文件 `/etc/nginx/sites-available/club-selection`：

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

### 步骤 5：配置 HTTPS

```bash
sudo certbot --nginx -d your-domain.com
```

---

## 💰 成本估算

### Streamlit Cloud
- **费用**: 免费
- **资源**:
  - 1 GB 内存
  - 10 GB 存储
  - 3 个应用

### 云服务器（阿里云/腾讯云）
- **服务器**: ¥30-100/月（1核2G）
- **带宽**: ¥10-30/月
- **域名**: ¥60-100/年
- **SSL证书**: 免费（Let's Encrypt）
- **总计**: ¥40-130/月

### Docker 部署
- **服务器**: 同上
- **Docker Hub**: 免费（公共仓库）
- **总计**: ¥40-130/月

---

## 📊 性能优化建议

### 1. 前端优化
- 使用 Streamlit 的缓存功能 `@st.cache_data`
- 压缩静态资源
- 使用 CDN 加速

### 2. 后端优化
- 数据库索引优化
- 异步处理耗时操作
- 使用连接池

### 3. 架构优化
- 负载均衡
- 水平扩展
- 缓存层（Redis）

---

## 🔐 安全建议

### 1. 环境变量
- ✅ 所有敏感信息使用环境变量
- ✅ 不要在代码中硬编码
- ✅ 定期更换 API Key

### 2. 访问控制
- ✅ 添加用户认证
- ✅ IP 白名单
- ✅ 访问限流

### 3. 数据安全
- ✅ 数据库定期备份
- ✅ 敏感数据脱敏
- ✅ 日志脱敏

### 4. HTTPS
- ✅ 生产环境必须使用 HTTPS
- ✅ 使用 Let's Encrypt 免费证书

---

## 🐛 常见问题排查

### 1. 部署失败

**问题**: Streamlit Cloud 部署失败

**解决**:
- 检查 `requirements.txt` 格式
- 检查 `frontend/app.py` 路径
- 查看部署日志

### 2. 环境变量未生效

**问题**: Agent 初始化失败

**解决**:
- 检查环境变量名称是否正确
- 检查变量值是否包含特殊字符
- 重新部署应用

### 3. 数据库连接失败

**问题**: 查询超时

**解决**:
- 检查 Supabase URL 和 Key
- 检查网络连接
- 检查 Supabase 服务状态

### 4. 页面样式异常

**问题**: 样式显示不正常

**解决**:
- 清除浏览器缓存
- 检查 `.streamlit/config.toml` 是否存在
- 检查 CSS 代码

---

## 📈 监控和维护

### 1. 日志监控

```bash
# Streamlit Cloud
- 在应用设置中查看日志

# Docker
docker logs -f club-selection

# 服务器
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 性能监控

- 使用 Streamlit 自带的监控
- 使用 Prometheus + Grafana
- 使用云服务商的监控工具

### 3. 备份策略

```bash
# 数据库备份
pg_dump -U user -h host -d database > backup.sql

# 定时备份（使用 cron）
0 2 * * * pg_dump ... > /backup/daily_$(date +\%Y\%m\%d).sql
```

---

## 🎓 学习资源

- [Streamlit 官方文档](https://docs.streamlit.io)
- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-cloud)
- [Docker 官方文档](https://docs.docker.com)
- [Supabase 官方文档](https://supabase.com/docs)
- [Nginx 官方文档](https://nginx.org/en/docs/)

---

## 📞 技术支持

如有问题，可以：
1. 查看 `frontend/README.md` 部署指南
2. 查看 `frontend/GUIDE.md` 使用指南
3. 查看 Streamlit 社区论坛
4. 提交 Issue 到 GitHub

---

## ✨ 总结

### 最推荐方案：Streamlit Cloud

**理由：**
1. 完全免费，零成本
2. 一键部署，无需运维
3. 自动 HTTPS，安全可靠
4. 适合校园社团选课场景

**部署时间：** 15 分钟内完成

### 推荐方案：Docker + 云服务器

**理由：**
1. 资源可控，可扩展
2. 适合正式生产环境
3. 技术栈成熟稳定

**部署时间：** 1 小时内完成

---

**现在就开始部署吧！** 🚀

选择一个方案，按照步骤操作，你的社团选课智能体很快就能上线了！
