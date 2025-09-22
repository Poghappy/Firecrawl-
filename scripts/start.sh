#!/bin/bash

# 火鸟门户系统 - Firecrawl Observer 启动脚本
# 版本: 2.0.0

echo "🔥 火鸟门户系统 - Firecrawl Observer 启动脚本"
echo "================================================"

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "❌ 错误: 未找到 config.json 配置文件"
    echo "请先配置 API 密钥和相关参数"
    exit 1
fi

# 创建必要目录
echo "📁 创建目录结构..."
mkdir -p logs
mkdir -p data/collected
mkdir -p data/backup
mkdir -p data/temp
mkdir -p templates/email

# 检查API密钥配置
echo "🔑 检查配置..."
if grep -q "your_firecrawl_api_key_here" config.json; then
    echo "⚠️  警告: 请先配置 Firecrawl API 密钥"
fi

if grep -q "your_huoniao_api_key_here" config.json; then
    echo "⚠️  警告: 请先配置火鸟门户 API 密钥"
fi

# 启动系统
echo "🚀 启动 Firecrawl Observer..."
echo "监控面板: http://localhost:8081"
echo "按 Ctrl+C 停止监控"
echo "================================================"

python3 firecrawl_observer.py