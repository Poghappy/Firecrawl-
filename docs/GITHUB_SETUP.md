# 🔧 GitHub仓库配置指南

## 📋 配置概览

本指南将帮助您完成GitHub仓库的完整配置，包括Secrets设置、Actions启用、Docker Hub集成等。

## 🔐 1. GitHub Secrets配置

### 1.1 访问Secrets设置
1. 进入仓库：https://github.com/Poghappy/Firecrawl-
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 添加新的密钥

### 1.2 必需的Secrets

#### 核心API密钥
| Secret名称          | 描述                   | 获取方式                                   | 示例值            |
| ------------------- | ---------------------- | ------------------------------------------ | ----------------- |
| `FIRECRAWL_API_KEY` | Firecrawl API密钥      | [Firecrawl控制台](https://firecrawl.dev/)  | `fc-xxxxxxxxxxxx` |
| `OPENAI_API_KEY`    | OpenAI API密钥（可选） | [OpenAI平台](https://platform.openai.com/) | `sk-xxxxxxxxxxxx` |

#### Docker Hub配置
| Secret名称        | 描述                    | 获取方式                              | 示例值         |
| ----------------- | ----------------------- | ------------------------------------- | -------------- |
| `DOCKER_USERNAME` | Docker Hub用户名        | [Docker Hub](https://hub.docker.com/) | `yourusername` |
| `DOCKER_PASSWORD` | Docker Hub密码/访问令牌 | Docker Hub设置                        | `yourpassword` |

#### 数据库配置（可选）
| Secret名称     | 描述          | 获取方式     | 示例值                                |
| -------------- | ------------- | ------------ | ------------------------------------- |
| `DATABASE_URL` | 生产数据库URL | 数据库提供商 | `postgresql://user:pass@host:port/db` |
| `REDIS_URL`    | Redis连接URL  | Redis提供商  | `redis://user:pass@host:port`         |

#### 通知配置（可选）
| Secret名称            | 描述               | 获取方式          | 示例值                                 |
| --------------------- | ------------------ | ----------------- | -------------------------------------- |
| `SLACK_WEBHOOK_URL`   | Slack通知Webhook   | Slack应用设置     | `https://hooks.slack.com/...`          |
| `DISCORD_WEBHOOK_URL` | Discord通知Webhook | Discord服务器设置 | `https://discord.com/api/webhooks/...` |

### 1.3 环境变量配置
创建 `.env.example` 文件作为模板：

```bash
# Firecrawl配置
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
FIRECRAWL_BASE_URL=https://api.firecrawl.dev

# 数据库配置
DATABASE_URL=sqlite:///data/firecrawl.db
REDIS_URL=redis://localhost:6379

# 服务器配置
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO

# 可选：AI服务配置
OPENAI_API_KEY=your_openai_api_key_here

# 可选：通知配置
SLACK_WEBHOOK_URL=your_slack_webhook_here
DISCORD_WEBHOOK_URL=your_discord_webhook_here
```

## 🚀 2. GitHub Actions启用

### 2.1 启用Actions
1. 进入仓库 **Settings** → **Actions** → **General**
2. 在 **Workflow permissions** 部分选择：
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. 点击 **Save**

### 2.2 验证工作流
1. 进入 **Actions** 标签
2. 查看工作流状态：
   - `CI/CD Pipeline` - 代码质量检查和测试
   - `Docker Build and Push` - Docker镜像构建

### 2.3 手动触发测试
```bash
# 推送测试提交
git commit --allow-empty -m "test: trigger GitHub Actions"
git push origin main
```

## 🐳 3. Docker Hub集成

### 3.1 创建Docker Hub仓库
1. 访问 [Docker Hub](https://hub.docker.com/)
2. 创建新仓库：`firecrawl-collector`
3. 设置为公开或私有

### 3.2 配置Docker Hub Secrets
在GitHub仓库中添加以下Secrets：
- `DOCKER_USERNAME`: Docker Hub用户名
- `DOCKER_PASSWORD`: Docker Hub密码或访问令牌

### 3.3 验证Docker构建
1. 推送代码到main分支
2. 查看Actions中的Docker构建日志
3. 确认镜像成功推送到Docker Hub

### 3.4 使用Docker镜像
```bash
# 拉取最新镜像
docker pull poghappy/firecrawl-collector:latest

# 运行容器
docker run -d \
  --name firecrawl-collector \
  -p 8000:8000 \
  -e FIRECRAWL_API_KEY=your_api_key \
  poghappy/firecrawl-collector:latest
```

## 📚 4. 文档完善

### 4.1 API文档
- 自动生成API文档：`http://localhost:8000/docs`
- 交互式API测试：`http://localhost:8000/redoc`

### 4.2 使用示例
参考 `docs/examples/` 目录中的示例代码

### 4.3 快速开始
```bash
# 1. 克隆仓库
git clone https://github.com/Poghappy/Firecrawl-.git
cd Firecrawl-

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境
cp .env.example .env
# 编辑.env文件，填入API密钥

# 4. 运行服务
python src/api_server.py
```

## 👥 5. 社区建设

### 5.1 贡献指南
- 查看 [CONTRIBUTING.md](CONTRIBUTING.md)
- 遵循代码规范和提交流程

### 5.2 问题报告
- 使用 [Bug报告模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 提供详细的复现步骤

### 5.3 功能请求
- 使用 [功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)
- 描述使用场景和预期效果

## 🔍 6. 监控和调试

### 6.1 Actions监控
- 查看构建状态：https://github.com/Poghappy/Firecrawl-/actions
- 设置通知：Settings → Notifications → Actions

### 6.2 日志查看
```bash
# 查看容器日志
docker logs firecrawl-collector

# 查看应用日志
tail -f logs/app/app.log
```

### 6.3 健康检查
```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查API状态
curl http://localhost:8000/api/v1/status
```

## 🛠️ 7. 故障排除

### 7.1 常见问题

#### Actions失败
- 检查Secrets是否正确配置
- 查看详细错误日志
- 确认仓库权限设置

#### Docker构建失败
- 检查Dockerfile语法
- 确认基础镜像可用
- 查看构建日志中的具体错误

#### 服务启动失败
- 检查环境变量配置
- 确认端口未被占用
- 查看应用日志

### 7.2 获取帮助
- 查看 [GitHub Issues](https://github.com/Poghappy/Firecrawl-/issues)
- 阅读 [文档](README.md)
- 提交新的Issue

## ✅ 配置检查清单

- [ ] 配置所有必需的GitHub Secrets
- [ ] 启用GitHub Actions工作流
- [ ] 设置Docker Hub集成
- [ ] 验证CI/CD流程
- [ ] 测试Docker镜像构建
- [ ] 完善项目文档
- [ ] 设置社区贡献指南
- [ ] 配置监控和通知

---

**注意**: 请确保所有敏感信息都通过GitHub Secrets管理，不要直接提交到代码仓库中。
