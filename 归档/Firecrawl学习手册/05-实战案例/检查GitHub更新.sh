#!/bin/bash

echo "🔍 检查 Firecrawl GitHub 仓库更新"
echo "=================================="
echo ""

# 检查仓库 1: firecrawl-app-examples
echo "📦 仓库 1: firecrawl-app-examples"
echo "----------------------------------"
cd "示例应用/firecrawl-app-examples" || exit

echo "当前项目数："
find . -maxdepth 1 -type d ! -name ".*" ! -name "." | wc -l

echo ""
echo "正在获取最新信息..."
git fetch origin

echo ""
echo "本地与远程差异："
git log HEAD..origin/main --oneline

if [ $? -eq 0 ]; then
    echo "✅ 检查完成"
    echo ""
    echo "如需更新，运行:"
    echo "  git pull origin main"
else
    echo "❌ 检查失败"
fi

echo ""
echo "=================================="
echo ""

# 检查仓库 2: firecrawl/firecrawl (main)
echo "📦 仓库 2: firecrawl/firecrawl (main)"
echo "------------------------------------"
cd "../../firecrawl-main-repo" || exit

echo "当前项目数："
find examples -maxdepth 1 -type d ! -name ".*" ! -name "examples" | wc -l

echo ""
echo "正在获取最新信息..."
git fetch origin

echo ""
echo "本地与远程差异："
git log HEAD..origin/main --oneline

if [ $? -eq 0 ]; then
    echo "✅ 检查完成"
    echo ""
    echo "如需更新，运行:"
    echo "  git pull origin main"
else
    echo "❌ 检查失败"
fi

echo ""
echo "=================================="
echo "🎉 所有仓库检查完成！"
echo ""
echo "建议："
echo "  1. 如果有更新，运行 git pull 获取最新代码"
echo "  2. 更新后运行 ls -la examples/ 查看新项目"
echo "  3. 更新项目索引文档"
echo ""
