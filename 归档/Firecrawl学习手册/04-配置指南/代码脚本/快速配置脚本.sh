#!/bin/bash

# ============ Firecrawl 快速配置脚本 ============
# 用途：自动化安装和配置 Firecrawl 生态系统
# 版本：v1.0
# 更新时间：2025-10-27

set -e  # 遇到错误立即退出

echo "🔥 Firecrawl 生态系统快速配置"
echo "================================"
echo ""

# ============ 检查依赖 ============
echo "📋 步骤 1/6: 检查依赖..."

# 检查 Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
else
    echo "❌ Python3 未安装"
    echo "   安装方式: brew install python3"
    exit 1
fi

# 检查 Node.js（可选）
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
    HAS_NODE=true
else
    echo "⚠️  Node.js 未安装（可选）"
    echo "   安装方式: brew install node"
    HAS_NODE=false
fi

# 检查 npm
if command -v npm &> /dev/null; then
    echo "✅ npm: $(npm --version)"
    HAS_NPM=true
else
    echo "⚠️  npm 未安装（可选）"
    HAS_NPM=false
fi

echo ""

# ============ 安装 Python SDK ============
echo "📦 步骤 2/6: 安装 Firecrawl Python SDK..."

if pip3 list | grep -q firecrawl-py; then
    echo "✅ firecrawl-py 已安装"
else
    echo "⏳ 正在安装 firecrawl-py..."
    pip3 install --break-system-packages firecrawl-py python-dotenv requests pydantic
    echo "✅ firecrawl-py 安装完成"
fi

echo ""

# ============ 安装 Node.js SDK（可选）============
if [ "$HAS_NPM" = true ]; then
    echo "📦 步骤 3/6: 安装 Firecrawl Node.js SDK（可选）..."

    read -p "是否安装 Node.js SDK 和 Data Connectors? (y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 初始化 npm（如果还没有 package.json）
        if [ ! -f "package.json" ]; then
            echo "⏳ 初始化 npm 项目..."
            npm init -y
        fi

        echo "⏳ 正在安装 @mendable/firecrawl-js 和 @mendable/data-connectors..."
        npm install @mendable/firecrawl-js @mendable/data-connectors

        echo "⏳ 安装 TypeScript 开发依赖..."
        npm install --save-dev typescript @types/node tsx

        echo "✅ Node.js SDK 安装完成"
    else
        echo "⏭️  跳过 Node.js SDK 安装"
    fi
else
    echo "⏭️  步骤 3/6: 跳过（未安装 npm）"
fi

echo ""

# ============ 配置环境变量 ============
echo "⚙️  步骤 4/6: 配置环境变量..."

if [ -f ".env" ]; then
    echo "⚠️  .env 文件已存在"
    read -p "是否覆盖? (y/n) " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⏭️  跳过环境变量配置"
    else
        cp .env.template .env
        echo "✅ 已从模板创建 .env 文件"
        echo ""
        echo "⚠️  重要：请编辑 .env 文件，填入你的 API 密钥"
        echo "   获取 Firecrawl API Key: https://www.firecrawl.dev/signin"
    fi
else
    if [ -f ".env.template" ]; then
        cp .env.template .env
        echo "✅ 已从模板创建 .env 文件"
        echo ""
        echo "⚠️  重要：请编辑 .env 文件，填入你的 API 密钥"
        echo "   获取 Firecrawl API Key: https://www.firecrawl.dev/signin"
    else
        echo "❌ 未找到 .env.template 文件"
    fi
fi

echo ""

# ============ 创建目录结构 ============
echo "📁 步骤 5/6: 创建项目目录..."

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/cache
mkdir -p logs

echo "✅ 目录结构创建完成："
echo "   - data/raw/       (原始数据)"
echo "   - data/processed/ (处理后数据)"
echo "   - data/cache/     (缓存)"
echo "   - logs/           (日志)"

echo ""

# ============ 测试配置 ============
echo "🧪 步骤 6/6: 测试配置..."

# 检查是否有 API Key
if [ -f ".env" ]; then
    source .env
    if [ -z "$FIRECRAWL_API_KEY" ] || [ "$FIRECRAWL_API_KEY" = "fc-xxxxxxxxxxxxxxxxxxxxxxxx" ]; then
        echo "⚠️  FIRECRAWL_API_KEY 未配置"
        echo "   请编辑 .env 文件，填入你的 API 密钥"
        echo ""
        echo "❌ 跳过 API 测试"
    else
        echo "✅ FIRECRAWL_API_KEY 已配置"
        echo "⏳ 正在测试 API 连接..."

        # 创建测试脚本
        cat > /tmp/test_firecrawl.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from firecrawl import FirecrawlApp

    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("❌ FIRECRAWL_API_KEY 未设置")
        exit(1)

    app = FirecrawlApp(api_key=api_key)
    result = app.scrape(url="https://example.com", formats=["markdown"])

    if hasattr(result, "markdown") and result.markdown:
        print("✅ API 测试成功！")
        print(f"   爬取了 {len(result.markdown)} 字符")
    else:
        print("❌ API 测试失败")

except Exception as e:
    print(f"❌ API 测试失败: {e}")
    exit(1)
EOF

        python3 /tmp/test_firecrawl.py
        rm /tmp/test_firecrawl.py
    fi
else
    echo "⚠️  未找到 .env 文件"
fi

echo ""
echo "================================"
echo "🎉 配置完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入 Firecrawl API Key"
echo "   获取：https://www.firecrawl.dev/signin"
echo ""
echo "2. 测试 Python SDK："
echo "   python3 scripts/scrape_firecrawl_blog.py"
echo ""
echo "3. 阅读完整文档："
echo "   cat FIRECRAWL_ECOSYSTEM_SETUP.md"
echo ""
echo "4. 查看示例代码："
echo "   cat FIRECRAWL_ECOSYSTEM_SETUP.md | grep -A 50 'TypeScript 源代码'"
echo ""
echo "================================"
