#!/bin/bash
# 重建虚拟环境脚本

set -e

echo "🐍 创建虚拟环境..."
python3 -m venv venv

echo "📦 安装依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 虚拟环境创建完成"
echo ""
echo "激活虚拟环境:"
echo "  source venv/bin/activate"
