#!/bin/bash
# 清理缓存和临时文件脚本
# 功能: 清理 Python 缓存、日志、临时文件
# 安全: 只删除可重建的文件

set -e

PROJECT_DIR="/Users/zhiledeng/Movies/Firecrawl数据采集器"
cd "$PROJECT_DIR"

echo "🧹 清理缓存和临时文件"
echo "======================"
echo ""

# 统计清理前大小
BEFORE_SIZE=$(du -sh . | awk '{print $1}')
echo "📊 清理前项目大小: $BEFORE_SIZE"
echo ""

# 1. 清理 Python 缓存
echo "🐍 清理 Python 缓存..."
PYCACHE_COUNT=$(find . -type d -name "__pycache__" | wc -l)
if [ "$PYCACHE_COUNT" -gt 0 ]; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type f -name "*.pyd" -delete 2>/dev/null || true
    echo "✅ 已清理 $PYCACHE_COUNT 个 __pycache__ 目录"
else
    echo "✅ 无需清理（已清理）"
fi
echo ""

# 2. 清理旧日志（保留最近 7 天）
echo "📝 清理旧日志文件..."
if [ -d "logs" ]; then
    OLD_LOGS=$(find logs/ -type f -mtime +7 2>/dev/null | wc -l)
    if [ "$OLD_LOGS" -gt 0 ]; then
        find logs/ -type f -mtime +7 -delete 2>/dev/null || true
        echo "✅ 已清理 $OLD_LOGS 个旧日志文件（>7天）"
    else
        echo "✅ 无旧日志文件需清理"
    fi
else
    echo "ℹ️ logs/ 目录不存在"
fi
echo ""

# 3. 清理临时目录
echo "🗑️ 清理临时目录..."
TEMP_DIRS=("temp" "output" ".pytest_cache" ".mypy_cache" ".tox" "htmlcov")
for dir in "${TEMP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "✅ 已删除: $dir/"
    fi
done
echo ""

# 4. 清理数据库备份（保留最近 3 个）
echo "💾 清理旧数据库备份..."
if [ -d "data" ]; then
    # 这里暂不自动删除，只统计
    OLD_DB=$(find data/ -type f -name "*.db-*" 2>/dev/null | wc -l)
    echo "ℹ️ 发现 $OLD_DB 个数据库备份文件"
    echo "   (手动清理: find data/ -name '*.db-*' -mtime +30 -delete)"
fi
echo ""

# 5. 清理 IDE 缓存
echo "💻 清理 IDE 缓存..."
IDE_DIRS=(".vscode/.ai" ".cursor/.ai" ".idea")
for dir in "${IDE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "✅ 已删除: $dir/"
    fi
done
echo ""

# 6. 清理 npm/node 缓存（如果有）
if [ -d "node_modules" ]; then
    echo "⚠️ 发现 node_modules/ 目录"
    echo "   如果不需要，可手动删除: rm -rf node_modules/"
fi
echo ""

# 统计清理后大小
AFTER_SIZE=$(du -sh . | awk '{print $1}')
echo "📊 清理后项目大小: $AFTER_SIZE"
echo ""

# 7. 生成报告
cat > docs/reports/cleanup_cache_report.md << EOF
# 缓存清理报告

**执行时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 清理摘要

### Python 缓存
- __pycache__ 目录: $PYCACHE_COUNT 个
- .pyc 文件: 已清理

### 日志文件
- 旧日志 (>7天): $OLD_LOGS 个

### 临时目录
$(for dir in "${TEMP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "- $dir/: 已删除"
    fi
done)

### 项目大小
- 清理前: $BEFORE_SIZE
- 清理后: $AFTER_SIZE

## 建议

### 定期清理
建议添加到 cron 任务:
\`\`\`bash
# 每周日凌晨 2 点执行
0 2 * * 0 cd /path/to/project && bash scripts/slimming/cleanup_cache.sh
\`\`\`

### 手动清理项
- 数据库备份: \`find data/ -name '*.db-*' -mtime +30 -delete\`
- Node modules: \`rm -rf node_modules/\`（如不需要）

---
**生成时间**: $(date)
EOF

echo "✅ 报告已生成: docs/reports/cleanup_cache_report.md"
echo ""
echo "🎉 清理完成！"

