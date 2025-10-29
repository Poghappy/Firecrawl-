#!/bin/bash
# GitHub Actions状态检查脚本

echo "🔍 检查GitHub Actions工作流状态..."

# 获取最新的工作流运行状态
echo "📊 获取工作流运行信息..."

# 检查CI/CD工作流
echo "🔧 CI/CD Pipeline工作流状态:"
gh run list --workflow="ci-cd.yml" --limit=3

echo ""
echo "🐳 Docker Build工作流状态:"
gh run list --workflow="docker-build.yml" --limit=3

echo ""
echo "📈 工作流运行统计:"
gh run list --limit=10

echo ""
echo "🌐 查看详细状态: https://github.com/Poghappy/Firecrawl-/actions"
