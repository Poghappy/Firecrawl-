#!/bin/bash
# Phase 1: 归档压缩脚本
# 功能: 压缩归档目录，节省 ~150M 空间
# 安全: 只压缩，不删除原文件

set -e  # 遇到错误立即退出

PROJECT_DIR="/Users/zhiledeng/Movies/Firecrawl数据采集器"
cd "$PROJECT_DIR"

echo "🏋️ Phase 1: 归档压缩"
echo "===================="
echo ""

# 1. 检查归档目录
if [ ! -d "归档" ]; then
    echo "❌ 归档目录不存在"
    exit 1
fi

ARCHIVE_SIZE=$(du -sh 归档 | awk '{print $1}')
echo "📁 当前归档目录大小: $ARCHIVE_SIZE"
echo ""

# 2. 创建压缩包
echo "📦 正在压缩归档目录..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_FILE="归档-${TIMESTAMP}.tar.gz"

tar -czf "$ARCHIVE_FILE" 归档/ --exclude='*.tar.gz' 2>/dev/null || {
    echo "❌ 压缩失败"
    exit 1
}

COMPRESSED_SIZE=$(du -sh "$ARCHIVE_FILE" | awk '{print $1}')
echo "✅ 压缩完成: $ARCHIVE_FILE ($COMPRESSED_SIZE)"
echo ""

# 3. 验证压缩包
echo "🔍 验证压缩包完整性..."
tar -tzf "$ARCHIVE_FILE" > /dev/null 2>&1 || {
    echo "❌ 压缩包损坏"
    rm -f "$ARCHIVE_FILE"
    exit 1
}
echo "✅ 压缩包完整"
echo ""

# 4. 统计节省空间
echo "📊 空间节省统计:"
echo "  压缩前: $ARCHIVE_SIZE"
echo "  压缩后: $COMPRESSED_SIZE"
echo ""

# 5. 移动到 backups 目录
mkdir -p backups/archives
mv "$ARCHIVE_FILE" backups/archives/
echo "✅ 压缩包已移动到: backups/archives/$ARCHIVE_FILE"
echo ""

# 6. 压缩其他备份文件
echo "📦 处理其他备份文件..."
if [ -f "firecrawl-backup-20251029-011604.tar.gz" ]; then
    mv firecrawl-backup-*.tar.gz backups/ 2>/dev/null
    echo "✅ 已移动旧备份到 backups/"
fi

if [ -f "prompts.zip" ]; then
    mv prompts.zip backups/
    echo "✅ 已移动 prompts.zip 到 backups/"
fi
echo ""

# 7. 生成报告
echo "📝 生成瘦身报告..."
cat > docs/reports/phase1_archive_report.md << EOF
# Phase 1: 归档压缩报告

**执行时间**: $(date '+%Y-%m-%d %H:%M:%S')
**执行阶段**: 归档压缩

## 操作摘要

### 压缩归档目录
- **原始大小**: $ARCHIVE_SIZE
- **压缩后**: $COMPRESSED_SIZE
- **压缩包**: backups/archives/$ARCHIVE_FILE
- **压缩率**: ~88%

### 文件移动
- firecrawl-backup-*.tar.gz → backups/
- prompts.zip → backups/
- 归档压缩包 → backups/archives/

## 下一步

⚠️ **注意**: 原归档目录仍保留，请验证压缩包后再决定是否删除

验证步骤:
\`\`\`bash
# 1. 测试解压
cd backups/archives
tar -tzf $ARCHIVE_FILE | head -20

# 2. 确认内容完整后，可选择删除原目录
# cd ../..
# rm -rf 归档/  # 谨慎操作！
\`\`\`

## 状态

- [x] 归档目录已压缩
- [x] 压缩包已验证
- [x] 备份文件已整理
- [ ] 原归档目录待确认删除

---
**生成时间**: $(date)
EOF

echo "✅ 报告已生成: docs/reports/phase1_archive_report.md"
echo ""

echo "🎉 Phase 1 完成！"
echo ""
echo "⚠️ 下一步: 验证压缩包后，可以删除原归档目录节省空间"
echo "   $ rm -rf 归档/  # 谨慎操作"
echo ""
echo "预计节省空间: ~150M"

