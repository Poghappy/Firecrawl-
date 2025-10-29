#!/bin/bash
# Firecrawl v2 统一新闻采集器 - 生产环境部署脚本

set -e

echo "🚀 Firecrawl v2 统一新闻采集器 - 生产环境部署"
echo "=================================================="

# 检查环境变量
if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo "❌ 错误: 请设置FIRECRAWL_API_KEY环境变量"
    echo "例如: export FIRECRAWL_API_KEY='your-api-key'"
    exit 1
fi

echo "✅ 环境变量检查通过"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p data logs results config/prometheus config/grafana

# 创建环境变量文件
echo "🔧 创建环境变量文件..."
cat > .env << EOF
FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
LOG_LEVEL=INFO
TZ=Asia/Shanghai
EOF

# 创建Prometheus配置
echo "📊 创建Prometheus配置..."
cat > config/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'firecrawl-scraper'
    static_configs:
      - targets: ['firecrawl-scraper:8000']
    scrape_interval: 30s
    metrics_path: /metrics

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

# 创建Grafana配置
echo "📈 创建Grafana配置..."
mkdir -p config/grafana/datasources
cat > config/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
docker build -f Dockerfile.production -t firecrawl-v2-scraper:latest .

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose -f docker-compose.production.yml down || true

# 启动服务
echo "🚀 启动生产环境服务..."
docker-compose -f docker-compose.production.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.production.yml ps

# 运行测试
echo "🧪 运行功能测试..."
docker-compose -f docker-compose.production.yml exec firecrawl-scraper python -c "
import sys
sys.path.append('/app')
from firecrawl_v2_unified_scraper import FirecrawlV2UnifiedScraper
import os

# 测试API连接
scraper = FirecrawlV2UnifiedScraper()
results = scraper.search_news_v2('人工智能 新闻', limit=2)
print(f'✅ API连接测试成功: 找到 {len(results)} 条结果')
"

# 显示访问信息
echo ""
echo "🎉 部署完成!"
echo "=================================================="
echo "📊 监控面板:"
echo "  - Grafana: http://localhost:3000 (admin/admin123)"
echo "  - Prometheus: http://localhost:9090"
echo ""
echo "📝 日志查看:"
echo "  docker-compose -f docker-compose.production.yml logs -f firecrawl-scraper"
echo ""
echo "🔄 重启服务:"
echo "  docker-compose -f docker-compose.production.yml restart"
echo ""
echo "🛑 停止服务:"
echo "  docker-compose -f docker-compose.production.yml down"
echo ""
echo "📁 数据目录:"
echo "  - 采集结果: ./results/"
echo "  - 日志文件: ./logs/"
echo "  - 数据文件: ./data/"
echo "=================================================="
