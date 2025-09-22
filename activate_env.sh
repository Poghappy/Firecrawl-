#!/bin/bash
# Firecrawl数据采集器环境激活脚本

echo "🚀 激活Firecrawl数据采集器开发环境..."
cd "/Users/zhiledeng/Documents/augment-projects/01-active-projects/Firecrawl数据采集器"
source firecrawl_env/bin/activate

echo "✅ 环境已激活"
echo "📍 当前目录: $(pwd)"
echo "🐍 Python版本: $(python --version)"
echo "📦 虚拟环境: $VIRTUAL_ENV"

echo ""
echo "🔧 可用命令:"
echo "  python scripts/ai-agent-validator.py  # 验证AI Agent配置"
echo "  python scripts/feedback-collector.py  # 运行反馈收集器"
echo "  pytest tests/ -v                     # 运行测试"
echo "  python src/api_server.py             # 启动API服务器"
echo ""

export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
echo "📁 PYTHONPATH已设置: $PYTHONPATH"
