#!/bin/bash

echo "🔧 Phase 3: 代码去重"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

BACKUP_DIR="backups/code_dedup_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 备份重复文件..."

# 备份要删除的文件
if [ -f "src/enhanced_api_server.py" ]; then
    cp src/enhanced_api_server.py "$BACKUP_DIR/"
    echo "  ✅ 备份 enhanced_api_server.py"
fi

if [ -f "src/firecrawl_collector.py" ]; then
    cp src/firecrawl_collector.py "$BACKUP_DIR/"
    echo "  ✅ 备份 firecrawl_collector.py"
fi

# 备份重复的测试文件
for file in tests/quick_test*.py; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        echo "  ✅ 备份 $(basename $file)"
    fi
done

echo ""
echo "🗑️ 删除重复文件..."

# 删除 enhanced_api_server.py（功能被 api_server.py 覆盖）
if [ -f "src/enhanced_api_server.py" ]; then
    rm src/enhanced_api_server.py
    echo "  ✅ 删除 enhanced_api_server.py（330 行）"
fi

# 删除 firecrawl_collector.py（已被 firecrawl_v2_unified_scraper.py 取代）
if [ -f "src/firecrawl_collector.py" ]; then
    rm src/firecrawl_collector.py
    echo "  ✅ 删除 firecrawl_collector.py（旧版）"
fi

# 删除重复的快速测试
for file in tests/quick_test*.py; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  ✅ 删除 $(basename $file)"
    fi
done

echo ""
echo "📊 统计结果..."
echo "  备份位置: $BACKUP_DIR"
echo "  删除文件数: $(ls -1 $BACKUP_DIR | wc -l)"

echo ""
echo "✅ Phase 3 完成！"

