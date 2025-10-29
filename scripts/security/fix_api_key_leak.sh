#!/bin/bash
# API Key 泄露紧急修复脚本
#
# 用途: 快速修复 honolulu_rentals/config.py 中的硬编码 API Key
# 优先级: P0 (最高)
# 预计时间: 30 分钟
#
# 作者: AI Assistant
# 创建时间: 2025-01-29

set -e

echo "🚨 API Key 泄露紧急修复脚本"
echo "=" * 60

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查环境
echo -e "${YELLOW}步骤 1: 检查环境...${NC}"
if [ ! -f "honolulu_rentals/config.py" ]; then
    echo -e "${RED}❌ 错误: honolulu_rentals/config.py 不存在${NC}"
    exit 1
fi

# 备份原文件
echo -e "${YELLOW}步骤 2: 备份原文件...${NC}"
cp honolulu_rentals/config.py honolulu_rentals/config.py.backup
echo -e "${GREEN}✅ 备份完成: honolulu_rentals/config.py.backup${NC}"

# 检查是否有硬编码的 Key
echo -e "${YELLOW}步骤 3: 检查硬编码的 API Key...${NC}"
if grep -q "fc-[a-z0-9]" honolulu_rentals/config.py; then
    echo -e "${RED}⚠️  发现硬编码的 API Key！${NC}"
    grep "fc-[a-z0-9]" honolulu_rentals/config.py
else
    echo -e "${GREEN}✅ 未发现硬编码的 API Key${NC}"
    exit 0
fi

# 创建 .env.example
echo -e "${YELLOW}步骤 4: 创建 .env.example...${NC}"
cat > honolulu_rentals/.env.example << 'EOF'
# Firecrawl API Keys
# 获取地址: https://firecrawl.dev/app/settings
FIRECRAWL_API_KEY_1=your-api-key-1
FIRECRAWL_API_KEY_2=your-api-key-2
FIRECRAWL_API_KEY_3=your-api-key-3
FIRECRAWL_API_KEY_4=your-api-key-4

# 日志级别
LOG_LEVEL=INFO

# 数据目录
DATA_DIR=./data
EOF
echo -e "${GREEN}✅ 创建 .env.example 完成${NC}"

# 修改 config.py
echo -e "${YELLOW}步骤 5: 修改 config.py...${NC}"
cat > honolulu_rentals/config.py.new << 'EOF'
"""
檀香山租房信息采集系统 - 配置文件

版本: v1.1 (安全修复)
修复日期: 2025-01-29
"""

import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================================
# Firecrawl API 配置
# ============================================================

# ✅ 从环境变量读取 API Keys（安全）
FIRECRAWL_API_KEYS = [
    os.getenv("FIRECRAWL_API_KEY_1"),
    os.getenv("FIRECRAWL_API_KEY_2"),
    os.getenv("FIRECRAWL_API_KEY_3"),
    os.getenv("FIRECRAWL_API_KEY_4"),
]

# 过滤掉 None 值
FIRECRAWL_API_KEYS = [key for key in FIRECRAWL_API_KEYS if key]

# 验证至少有一个 Key
if not FIRECRAWL_API_KEYS:
    raise ValueError(
        "未配置 Firecrawl API Key！\n"
        "请在 .env 文件中设置 FIRECRAWL_API_KEY_1 等变量。\n"
        "参考 .env.example 文件。"
    )

# 当前使用的 Key 索引（自动轮换）
CURRENT_KEY_INDEX = 0

def get_next_api_key() -> str:
    """获取下一个可用的 API Key（轮换策略）"""
    global CURRENT_KEY_INDEX
    if not FIRECRAWL_API_KEYS:
        raise ValueError("没有可用的 API Key")

    key = FIRECRAWL_API_KEYS[CURRENT_KEY_INDEX]
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(FIRECRAWL_API_KEYS)
    return key

# 下面是原有的其他配置...
EOF

# 从原文件复制其余配置（排除硬编码部分）
tail -n +40 honolulu_rentals/config.py >> honolulu_rentals/config.py.new

# 替换原文件
mv honolulu_rentals/config.py.new honolulu_rentals/config.py
echo -e "${GREEN}✅ config.py 修复完成${NC}"

# 提示用户操作
echo ""
echo -e "${YELLOW}=" * 60 "${NC}"
echo -e "${RED}⚠️  重要：请立即完成以下操作！${NC}"
echo -e "${YELLOW}=" * 60 "${NC}"
echo ""
echo "1. 撤销泄露的 API Key:"
echo "   访问: https://firecrawl.dev/app/settings"
echo "   撤销这 4 个 Key:"
echo "   - fc-31ebbe4647b84fdc975318d372eebea8"
echo "   - fc-00857d82ec534e8598df1bae9af9fb28"
echo "   - fc-9eb380b0dec74d6ebb6c756ee4de4c5a"
echo "   - fc-0a2c801f433d4718bcd8189f2742edf4"
echo ""
echo "2. 生成新的 API Key 并添加到 .env:"
echo "   cd honolulu_rentals"
echo "   cp .env.example .env"
echo "   # 编辑 .env，填入新生成的 Key"
echo ""
echo "3. 测试配置:"
echo "   python test_demo.py"
echo ""
echo "4. 从 Git 历史中删除敏感信息:"
echo "   git filter-repo --path honolulu_rentals/config.py --invert-paths --force"
echo ""
echo -e "${GREEN}✅ 本地代码已修复${NC}"
echo -e "${YELLOW}⚠️  请务必完成上述 4 步操作！${NC}"
echo ""
