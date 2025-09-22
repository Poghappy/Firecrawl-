# 🐳 Docker Hub配置指南

## 概述

本指南将帮助您配置Docker Hub集成，实现自动构建和推送Docker镜像。

## 1. Docker Hub账户设置

### 1.1 创建Docker Hub账户
1. 访问 [Docker Hub](https://hub.docker.com/)
2. 注册新账户或登录现有账户
3. 验证邮箱地址

### 1.2 创建仓库
1. 点击 **Create Repository**
2. 填写仓库信息：
- **Repository Name**: `firecrawl`
- **Description**: `Firecrawl数据采集器 - 智能网页内容监控和采集系统`
   - **Visibility**: 选择 Public 或 Private
3. 点击 **Create**

## 2. GitHub Secrets配置

### 2.1 添加Docker Hub Secrets
在GitHub仓库中添加以下Secrets：

1. 进入仓库：https://github.com/Poghappy/Firecrawl-
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 添加以下Secrets：

| Secret名称        | 描述                     | 获取方式                              |
| ----------------- | ------------------------ | ------------------------------------- |
| `DOCKER_USERNAME` | Docker Hub用户名         | 您的Docker Hub用户名                  |
| `DOCKER_PASSWORD` | Docker Hub密码或访问令牌 | Docker Hub密码或Personal Access Token |

### 2.2 创建Personal Access Token（推荐）
1. 登录Docker Hub
2. 进入 **Account Settings** → **Security**
3. 点击 **New Access Token**
4. 填写Token信息：
   - **Access Token Description**: `GitHub Actions`
   - **Access Permissions**: `Read, Write, Delete`
5. 复制生成的Token并保存到GitHub Secrets

## 3. 验证Docker构建

### 3.1 检查GitHub Actions
1. 进入仓库的 **Actions** 标签
2. 查看 **Docker Build and Push** 工作流
3. 确认构建成功并推送到Docker Hub

### 3.2 本地测试Docker镜像
```bash
# 拉取最新镜像
docker pull denzhile/firecrawl:latest

# 运行容器
docker run -d \
  --name firecrawl-collector \
  -p 8000:8000 \
  -e FIRECRAWL_API_KEY=your_api_key_here \
  denzhile/firecrawl:latest

# 检查容器状态
docker ps

# 查看日志
docker logs firecrawl-collector

# 测试API
curl http://localhost:8000/health
```

## 4. 多架构支持

### 4.1 更新Dockerfile
确保Dockerfile支持多架构构建：

```dockerfile
# 使用多架构基础镜像
FROM --platform=$BUILDPLATFORM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["python", "src/api_server.py"]
```

### 4.2 更新GitHub Actions
修改 `.github/workflows/docker-build.yml`：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: ./config/deployment/Dockerfile
    platforms: linux/amd64,linux/arm64
    push: true
    tags: |
      poghappy/firecrawl-collector:latest
      poghappy/firecrawl-collector:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 5. 镜像标签策略

### 5.1 标签命名规范
- `latest`: 最新稳定版本
- `v1.0.0`: 语义化版本标签
- `main`: 主分支构建
- `develop`: 开发分支构建
- `sha-abc123`: 提交哈希标签

### 5.2 自动标签
GitHub Actions会自动创建以下标签：
- 每次推送到main分支 → `latest`
- 每次Git标签 → `v{version}`
- 每次提交 → `sha-{commit_hash}`

## 6. 镜像使用指南

### 6.1 基本使用
```bash
# 拉取最新版本
docker pull poghappy/firecrawl-collector:latest

# 运行容器
docker run -d \
  --name firecrawl-collector \
  -p 8000:8000 \
  -e FIRECRAWL_API_KEY=your_api_key \
  poghappy/firecrawl-collector:latest
```

### 6.2 使用Docker Compose
创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  firecrawl-collector:
    image: poghappy/firecrawl-collector:latest
    container_name: firecrawl-collector
    ports:
      - "8000:8000"
    environment:
      - FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
      - DATABASE_URL=${DATABASE_URL:-sqlite:///data/firecrawl.db}
      - REDIS_URL=${REDIS_URL:-redis://redis:6379}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: firecrawl-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### 6.3 生产环境配置
```bash
# 使用生产环境镜像
docker run -d \
  --name firecrawl-collector-prod \
  -p 8000:8000 \
  -e FIRECRAWL_API_KEY=your_prod_api_key \
  -e DATABASE_URL=postgresql://user:pass@host:port/db \
  -e REDIS_URL=redis://redis-host:6379 \
  -e LOG_LEVEL=INFO \
  --restart=unless-stopped \
  poghappy/firecrawl-collector:latest
```

## 7. 监控和维护

### 7.1 镜像大小优化
```dockerfile
# 使用多阶段构建
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY config/ ./config/

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["python", "src/api_server.py"]
```

### 7.2 安全扫描
```bash
# 使用Trivy扫描镜像
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image poghappy/firecrawl-collector:latest

# 使用Snyk扫描
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  snyk/snyk:docker poghappy/firecrawl-collector:latest
```

### 7.3 镜像清理
```bash
# 清理未使用的镜像
docker image prune -f

# 清理特定镜像的旧版本
docker images poghappy/firecrawl-collector --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}" | \
  grep -v latest | \
  awk '{print $1":"$2}' | \
  xargs docker rmi
```

## 8. 故障排除

### 8.1 常见问题

#### 构建失败
- 检查Dockerfile语法
- 确认基础镜像可用
- 查看构建日志中的具体错误

#### 推送失败
- 验证Docker Hub凭据
- 检查仓库权限
- 确认网络连接

#### 镜像运行失败
- 检查环境变量配置
- 查看容器日志
- 确认端口映射

### 8.2 调试命令
```bash
# 查看镜像信息
docker inspect poghappy/firecrawl-collector:latest

# 查看镜像历史
docker history poghappy/firecrawl-collector:latest

# 进入容器调试
docker run -it --rm poghappy/firecrawl-collector:latest /bin/bash

# 查看容器日志
docker logs -f firecrawl-collector
```

## 9. 最佳实践

### 9.1 镜像管理
- 定期更新基础镜像
- 使用特定版本标签
- 定期清理旧镜像

### 9.2 安全考虑
- 使用非root用户运行
- 定期扫描安全漏洞
- 最小化镜像大小

### 9.3 性能优化
- 使用多阶段构建
- 优化Dockerfile层
- 使用.dockerignore文件

## 10. 相关链接

- [Docker Hub仓库](https://hub.docker.com/r/denzhile/firecrawl)
- [GitHub Actions](https://github.com/Poghappy/Firecrawl-/actions)
- [Docker文档](https://docs.docker.com/)
- [GitHub Actions文档](https://docs.github.com/en/actions)

---

**注意**: 请确保在生产环境中使用强密码和安全的配置设置。
