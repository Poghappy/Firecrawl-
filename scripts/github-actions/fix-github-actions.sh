#!/bin/bash
# GitHub Actions修复脚本

echo "🔧 修复GitHub Actions问题..."

# 1. 更新工作流文件中的actions版本
echo "📝 更新工作流文件..."
find .github/workflows -name "*.yml" -exec sed -i.bak \
  -e 's/actions\/download-artifact@v3/actions\/download-artifact@v5/g' \
  -e 's/actions\/upload-artifact@v3/actions\/upload-artifact@v4/g' \
  -e 's/actions\/cache@v3/actions\/cache@v4/g' \
  -e 's/actions\/setup-python@v4/actions\/setup-python@v5/g' \
  -e 's/actions\/checkout@v3/actions\/checkout@v4/g' \
  {} \;

# 2. 清理备份文件
find .github/workflows -name "*.bak" -delete

# 3. 提交更改
git add .github/workflows/
git commit -m "fix: update GitHub Actions versions

- Update actions/download-artifact to v5
- Update actions/upload-artifact to v4  
- Update actions/cache to v4
- Update actions/setup-python to v5
- Update actions/checkout to v4

Resolves dependabot PRs #1, #2, #3"

git push origin main

echo "✅ GitHub Actions修复完成"
