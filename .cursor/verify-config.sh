#!/bin/bash

# Cursor 配置验证脚本
# 用于验证配置文件是否正确设置

echo "======================================"
echo "  Cursor 配置验证"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查计数
PASS=0
FAIL=0

# 检查函数
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} 文件存在: $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} 文件缺失: $1"
        ((FAIL++))
        return 1
    fi
}

check_file_size() {
    if [ -f "$1" ]; then
        size=$(wc -l < "$1" | tr -d ' ')
        if [ "$size" -le "$2" ]; then
            echo -e "${GREEN}✓${NC} 文件大小合适: $1 (${size} 行 ≤ $2 行)"
            ((PASS++))
            return 0
        else
            echo -e "${YELLOW}⚠${NC} 文件可能过大: $1 (${size} 行 > $2 行)"
            ((PASS++))
            return 0
        fi
    else
        echo -e "${RED}✗${NC} 文件不存在: $1"
        ((FAIL++))
        return 1
    fi
}

check_content() {
    if [ -f "$1" ]; then
        if grep -q "$2" "$1"; then
            echo -e "${GREEN}✓${NC} 包含关键内容: $1"
            ((PASS++))
            return 0
        else
            echo -e "${YELLOW}⚠${NC} 缺少关键内容: $1"
            ((FAIL++))
            return 1
        fi
    else
        echo -e "${RED}✗${NC} 文件不存在: $1"
        ((FAIL++))
        return 1
    fi
}

echo "1. 检查主配置文件"
echo "------------------------------"
check_file ".cursorrules"
check_file_size ".cursorrules" 100
check_content ".cursorrules" "简体中文"
check_content ".cursorrules" "MCP"
echo ""

echo "2. 检查文档文件"
echo "------------------------------"
check_file ".cursor/README.md"
check_file ".cursor/CURSOR_RULES_UPGRADE.md"
check_file ".cursor/QUICK_REFERENCE.md"
check_file ".cursor/OPTIMIZATION_REPORT.md"
check_file ".cursor/CONFIGURATION_SUMMARY.md"
echo ""

echo "3. 检查归档文件"
echo "------------------------------"
check_file ".cursor/archive/rules-v2.0.md"
if [ -d ".cursor/archive/rules-backup-20251028" ]; then
    echo -e "${GREEN}✓${NC} 归档目录存在: .cursor/archive/rules-backup-20251028"
    ((PASS++))
else
    echo -e "${YELLOW}⚠${NC} 归档目录可能缺失: .cursor/archive/rules-backup-20251028"
    ((FAIL++))
fi
echo ""

echo "4. 检查状态文档"
echo "------------------------------"
check_file ".cursor/CURSOR_CONFIG_STATUS.md"
echo ""

echo "======================================"
echo "  验证结果"
echo "======================================"
echo -e "通过: ${GREEN}${PASS}${NC} 项"
echo -e "失败: ${RED}${FAIL}${NC} 项"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ 配置验证通过！${NC}"
    echo ""
    echo "下一步："
    echo "  1. 阅读 .cursorrules 了解规则"
    echo "  2. 查看 .cursor/QUICK_REFERENCE.md 快速参考"
    echo "  3. 开始使用 AI 助手进行开发"
    exit 0
else
    echo -e "${YELLOW}⚠ 发现一些问题，请检查上述失败项${NC}"
    echo ""
    echo "建议："
    echo "  1. 检查缺失的文件"
    echo "  2. 重新运行配置脚本"
    echo "  3. 查看 .cursor/README.md 了解详情"
    exit 1
fi
