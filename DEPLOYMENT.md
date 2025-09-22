# 🚀 部署指南

## 📋 部署概览

本项目支持多种部署方式，包括本地开发、Docker容器化部署和生产环境部署。

## 🛠️ 部署方式

### 1. 本地开发部署

#### 环境要求
- Python 3.9+
- pip 或 conda
- Git

#### 快速开始
```bash
# 1. 克隆仓库
git clone https://github.com/Poghappy/Firecrawl-.git
cd Firecrawl-

# 2. 创建虚拟环境
python -m venv firecrawl_env
source firecrawl_env/bin/activate  # Linux/Mac
# 或
firecrawl_env\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp config_example.json config.json
# 编辑config.json，填入Firecrawl API密钥

# 5. 运行应用
python src/api_server.py
```

### 2. Docker部署

#### 使用Docker Compose（推荐）
```bash
# 1. 克隆仓库
git clone https://github.com/Poghappy/Firecrawl-.git
cd Firecrawl-

# 2. 配置环境变量
cp .env.example .env
# 编辑.env文件，配置必要的环境变量

# 3. 启动服务
docker-compose -f config/deployment/docker-compose.yml up -d

# 4. 查看服务状态
docker-compose -f config/deployment/docker-compose.yml ps
```

#### 使用Docker镜像
```bash
# 1. 拉取镜像
docker pull ghcr.io/poghappy/firecrawl-:latest

# 2. 运行容器
docker run -d \
  --name firecrawl-collector \
  -p 8000:8000 \
  -e FIRECRAWL_API_KEY=your_api_key \
  ghcr.io/poghappy/firecrawl-:latest
```

### 3. 生产环境部署

#### 使用Docker Compose生产配置
```bash
# 1. 配置生产环境变量
cp .env.production.example .env.production

# 2. 启动生产服务
docker-compose -f config/deployment/docker-compose.production.yml up -d

# 3. 配置Nginx反向代理
# 参考 config/nginx/nginx.conf
```

#### 使用Kubernetes
```bash
# 1. 应用Kubernetes配置
kubectl apply -f k8s/

# 2. 检查部署状态
kubectl get pods -l app=firecrawl-collector
```

## 🔧 配置说明

### 环境变量配置

| 变量名              | 描述              | 默认值                      | 必需 |
| ------------------- | ----------------- | --------------------------- | ---- |
| `FIRECRAWL_API_KEY` | Firecrawl API密钥 | -                           | ✅    |
| `DATABASE_URL`      | 数据库连接URL     | sqlite:///data/firecrawl.db | ❌    |
| `REDIS_URL`         | Redis连接URL      | redis://localhost:6379      | ❌    |
| `PORT`              | 服务端口          | 8000                        | ❌    |
| `LOG_LEVEL`         | 日志级别          | INFO                        | ❌    |

### 配置文件

#### config.json
```json
{
  "firecrawl": {
    "api_key": "your_firecrawl_api_key",
    "base_url": "https://api.firecrawl.dev"
  },
  "database": {
    "url": "sqlite:///data/firecrawl.db"
  },
  "redis": {
    "url": "redis://localhost:6379"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

## 📊 监控和日志

### 健康检查
```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 检查API状态
curl http://localhost:8000/api/v1/status
```

### 日志查看
```bash
# Docker容器日志
docker logs firecrawl-collector

# 应用日志
tail -f logs/app/app.log

# Nginx日志
tail -f logs/nginx/access.log
```

### 监控面板
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **应用Dashboard**: http://localhost:8000/dashboard

## 🔒 安全配置

### 1. API密钥管理
```bash
# 使用环境变量
export FIRECRAWL_API_KEY=your_api_key

# 或使用密钥管理服务
# AWS Secrets Manager, Azure Key Vault, etc.
```

### 2. 网络安全
```bash
# 配置防火墙
ufw allow 8000/tcp
ufw allow 22/tcp

# 使用HTTPS
# 配置SSL证书和反向代理
```

### 3. 数据安全
```bash
# 数据库加密
# 配置数据库连接加密

# 备份策略
# 定期备份数据库和配置文件
```

## 🚨 故障排除

### 常见问题

#### 1. 服务无法启动
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 检查日志
docker logs firecrawl-collector
```

#### 2. API连接失败
```bash
# 检查API密钥
echo $FIRECRAWL_API_KEY

# 测试API连接
curl -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  https://api.firecrawl.dev/v1/health
```

#### 3. 数据库连接问题
```bash
# 检查数据库状态
docker ps | grep postgres

# 检查连接字符串
echo $DATABASE_URL
```

### 性能优化

#### 1. 资源限制
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

#### 2. 缓存配置
```python
# 配置Redis缓存
CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://localhost:6379/0"
}
```

## 📈 扩展部署

### 水平扩展
```bash
# 使用Docker Swarm
docker service create \
  --name firecrawl-collector \
  --replicas 3 \
  --publish 8000:8000 \
  ghcr.io/poghappy/firecrawl-:latest
```

### 负载均衡
```nginx
# Nginx配置
upstream firecrawl_backend {
    server firecrawl-collector-1:8000;
    server firecrawl-collector-2:8000;
    server firecrawl-collector-3:8000;
}
```

## 📞 支持

如果遇到部署问题，请：

1. 查看[GitHub Issues](https://github.com/Poghappy/Firecrawl-/issues)
2. 检查[文档](https://github.com/Poghappy/Firecrawl-/blob/main/README.md)
3. 提交新的Issue描述问题

---

**注意**: 请确保在生产环境中使用强密码和安全的配置设置。
