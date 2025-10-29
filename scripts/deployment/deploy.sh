#!/bin/bash

# 火鸟门户系统 Firecrawl 集成部署脚本
# Deploy Script for Firecrawl Integration with Huoniao Portal System

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统要求
check_requirements() {
    log_info "检查系统要求..."
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    # 检查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    # 检查 Git
    if ! command -v git &> /dev/null; then
        log_error "Git 未安装，请先安装 Git"
        exit 1
    fi
    
    log_success "系统要求检查通过"
}

# 创建环境配置文件
create_env_file() {
    log_info "创建环境配置文件..."
    
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Firecrawl API 配置
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
FIRECRAWL_BASE_URL=https://api.firecrawl.dev

# 数据库配置
POSTGRES_PASSWORD=firecrawl_secure_password_$(openssl rand -hex 16)
REDIS_PASSWORD=redis_secure_password_$(openssl rand -hex 16)

# Grafana 配置
GRAFANA_USER=admin
GRAFANA_PASSWORD=grafana_admin_password_$(openssl rand -hex 8)

# 应用配置
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# 安全配置
JWT_SECRET_KEY=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# 火鸟门户系统集成配置
HUONIAO_API_URL=https://your-huoniao-portal.com/api
HUONIAO_API_KEY=your_huoniao_api_key_here
HUONIAO_WEBHOOK_SECRET=webhook_secret_$(openssl rand -hex 16)
EOF
        log_success "环境配置文件已创建: .env"
        log_warning "请编辑 .env 文件，填入正确的 API 密钥和配置信息"
    else
        log_info "环境配置文件已存在，跳过创建"
    fi
}

# 创建配置目录和文件
create_config_files() {
    log_info "创建配置文件..."
    
    # 创建配置目录
    mkdir -p config/{nginx,grafana/{provisioning,dashboards},prometheus}
    mkdir -p logs/{nginx,app}
    mkdir -p data/{postgres,redis,grafana,prometheus}
    mkdir -p backups
    mkdir -p scripts
    
    # 创建 Nginx 配置
    if [ ! -f "config/nginx.conf" ]; then
        cat > config/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream firecrawl_api {
        server firecrawl-api:8000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        location / {
            proxy_pass http://firecrawl_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF
        log_success "Nginx 配置文件已创建"
    fi
    
    # 创建 Prometheus 配置
    if [ ! -f "config/prometheus.yml" ]; then
        cat > config/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'firecrawl-api'
    static_configs:
      - targets: ['firecrawl-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
    
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF
        log_success "Prometheus 配置文件已创建"
    fi
    
    # 创建数据库初始化脚本
    if [ ! -f "scripts/init-db.sql" ]; then
        cat > scripts/init-db.sql << 'EOF'
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_crawl_jobs_status ON crawl_jobs(status);
CREATE INDEX IF NOT EXISTS idx_crawl_jobs_created_at ON crawl_jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_crawled_pages_job_id ON crawled_pages(job_id);
CREATE INDEX IF NOT EXISTS idx_crawled_pages_url ON crawled_pages USING gin(url gin_trgm_ops);
EOF
        log_success "数据库初始化脚本已创建"
    fi
    
    # 创建备份脚本
    if [ ! -f "scripts/backup.sh" ]; then
        cat > scripts/backup.sh << 'EOF'
#!/bin/bash
set -e

BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/firecrawl_backup_$DATE.sql"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行数据库备份
pg_dump -h postgres -U firecrawl -d firecrawl > $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "备份完成: ${BACKUP_FILE}.gz"
EOF
        chmod +x scripts/backup.sh
        log_success "备份脚本已创建"
    fi
}

# 构建和启动服务
deploy_services() {
    log_info "构建和启动服务..."
    
    # 构建镜像
    log_info "构建 Docker 镜像..."
    docker-compose build
    
    # 启动服务
    log_info "启动服务..."
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    log_info "检查服务状态..."
    docker-compose ps
}

# 运行数据库迁移
run_migrations() {
    log_info "运行数据库迁移..."
    
    # 等待数据库就绪
    log_info "等待数据库就绪..."
    docker-compose exec -T postgres pg_isready -U firecrawl -d firecrawl
    
    # 运行迁移
    log_info "执行数据库迁移..."
    docker-compose exec -T firecrawl-api python -m alembic upgrade head
    
    log_success "数据库迁移完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查 API 服务
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "API 服务运行正常"
    else
        log_error "API 服务健康检查失败"
        return 1
    fi
    
    # 检查数据库
    if docker-compose exec -T postgres pg_isready -U firecrawl -d firecrawl > /dev/null 2>&1; then
        log_success "数据库连接正常"
    else
        log_error "数据库连接失败"
        return 1
    fi
    
    # 检查 Redis
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis 连接正常"
    else
        log_error "Redis 连接失败"
        return 1
    fi
    
    log_success "所有服务健康检查通过"
}

# 显示部署信息
show_deployment_info() {
    log_success "部署完成！"
    echo
    echo "=== 服务访问信息 ==="
    echo "API 服务: http://localhost:8000"
    echo "API 文档: http://localhost:8000/docs"
    echo "Grafana 监控: http://localhost:3000"
    echo "Prometheus: http://localhost:9090"
    echo
    echo "=== 管理命令 ==="
    echo "查看日志: docker-compose logs -f [service_name]"
    echo "重启服务: docker-compose restart [service_name]"
    echo "停止服务: docker-compose down"
    echo "备份数据: docker-compose run --rm backup"
    echo
    echo "=== 重要提醒 ==="
    echo "1. 请确保已正确配置 .env 文件中的 API 密钥"
    echo "2. 建议定期备份数据库"
    echo "3. 监控服务运行状态和资源使用情况"
    echo "4. 查看 README.md 获取更多使用说明"
}

# 主函数
main() {
    echo "=== 火鸟门户系统 Firecrawl 集成部署脚本 ==="
    echo
    
    check_requirements
    create_env_file
    create_config_files
    deploy_services
    run_migrations
    health_check
    show_deployment_info
    
    log_success "部署脚本执行完成！"
}

# 处理命令行参数
case "${1:-}" in
    "install")
        main
        ;;
    "start")
        log_info "启动服务..."
        docker-compose up -d
        health_check
        ;;
    "stop")
        log_info "停止服务..."
        docker-compose down
        ;;
    "restart")
        log_info "重启服务..."
        docker-compose restart
        health_check
        ;;
    "status")
        log_info "服务状态:"
        docker-compose ps
        ;;
    "logs")
        docker-compose logs -f "${2:-}"
        ;;
    "backup")
        log_info "执行数据备份..."
        docker-compose run --rm backup
        ;;
    "update")
        log_info "更新服务..."
        docker-compose pull
        docker-compose build
        docker-compose up -d
        health_check
        ;;
    "clean")
        log_warning "清理所有数据和容器..."
        read -p "确认删除所有数据？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            docker system prune -f
            log_success "清理完成"
        fi
        ;;
    *)
        echo "用法: $0 {install|start|stop|restart|status|logs|backup|update|clean}"
        echo
        echo "命令说明:"
        echo "  install  - 完整安装和部署"
        echo "  start    - 启动服务"
        echo "  stop     - 停止服务"
        echo "  restart  - 重启服务"
        echo "  status   - 查看服务状态"
        echo "  logs     - 查看日志 (可指定服务名)"
        echo "  backup   - 备份数据库"
        echo "  update   - 更新服务"
        echo "  clean    - 清理所有数据"
        exit 1
        ;;
esac