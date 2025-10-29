#!/bin/bash

# Firecrawl 学习手册 GitHub 同步检查脚本
# 创建时间: 2025-10-27
# 用途: 检查 GitHub 仓库是否有新的示例项目

echo "🔍 Firecrawl 学习手册 - GitHub 更新检查"
echo "=========================================="
echo ""

# 定义路径
HANDBOOK_DIR="/Users/zhiledeng/Downloads/FireShot/Firecrawl学习手册"
EXAMPLES_DIR="$HANDBOOK_DIR/05-实战案例/示例应用/firecrawl-app-examples"
GITHUB_URL="https://github.com/firecrawl/firecrawl-app-examples.git"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查目录是否存在
if [ ! -d "$EXAMPLES_DIR" ]; then
    echo -e "${RED}❌ 错误: 示例项目目录不存在${NC}"
    echo -e "${YELLOW}📂 期望路径: $EXAMPLES_DIR${NC}"
    echo ""
    echo -e "${BLUE}💡 建议: 运行以下命令重新克隆${NC}"
    echo "    cd \"$HANDBOOK_DIR/05-实战案例/示例应用/\""
    echo "    git clone $GITHUB_URL"
    exit 1
fi

# 进入目录
cd "$EXAMPLES_DIR" || exit 1

echo "📂 当前目录: $EXAMPLES_DIR"
echo ""

# 1. 统计本地项目数量
echo -e "${BLUE}📊 Step 1: 统计本地项目${NC}"
echo "----------------------------------------"
LOCAL_COUNT=$(find . -maxdepth 1 -type d ! -name ".*" ! -name "." | wc -l)
LOCAL_COUNT=$((LOCAL_COUNT)) # 去除空格
echo -e "${GREEN}✅ 本地项目数量: $LOCAL_COUNT 个${NC}"
echo ""

# 列出前 10 个项目
echo "本地项目列表（前 10 个）:"
find . -maxdepth 1 -type d ! -name ".*" ! -name "." | sort | head -10 | sed 's|./|  - |'
echo "  ..."
echo ""

# 2. 检查 Git 状态
echo -e "${BLUE}📊 Step 2: 检查 Git 状态${NC}"
echo "----------------------------------------"

# 检查是否是 Git 仓库
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 不是 Git 仓库${NC}"
    echo -e "${YELLOW}💡 建议: 重新克隆仓库${NC}"
    exit 1
fi

# 显示远程仓库信息
echo "远程仓库:"
git remote -v | head -2
echo ""

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo -e "当前分支: ${GREEN}$CURRENT_BRANCH${NC}"
echo ""

# 3. 拉取最新更新
echo -e "${BLUE}📊 Step 3: 拉取最新更新${NC}"
echo "----------------------------------------"
echo "正在从远程仓库拉取更新..."

# 执行 fetch
git fetch origin 2>&1

# 检查是否有更新
UPDATES=$(git log HEAD..origin/$CURRENT_BRANCH --oneline)

if [ -z "$UPDATES" ]; then
    echo -e "${GREEN}✅ 本地代码已是最新版本${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  发现 GitHub 有新的更新:${NC}"
    echo ""
    echo "$UPDATES" | head -10
    echo ""
    echo -e "${BLUE}💡 建议: 运行以下命令更新${NC}"
    echo "    git pull origin $CURRENT_BRANCH"
    echo ""
fi

# 4. 对比远程项目数量
echo -e "${BLUE}📊 Step 4: 对比远程项目数量${NC}"
echo "----------------------------------------"
echo "正在获取远程仓库信息..."

# 使用 GitHub API 获取项目数量（需要 curl 和 jq）
if command -v curl &> /dev/null && command -v jq &> /dev/null; then
    # GitHub API 获取仓库文件列表
    API_URL="https://api.github.com/repos/firecrawl/firecrawl-app-examples/contents"

    # 获取根目录内容
    RESPONSE=$(curl -s "$API_URL")

    # 统计目录数量（排除文件）
    REMOTE_COUNT=$(echo "$RESPONSE" | jq '[.[] | select(.type == "dir")] | length')

    if [ "$REMOTE_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ GitHub 项目数量: $REMOTE_COUNT 个${NC}"
        echo ""

        # 对比数量
        if [ "$REMOTE_COUNT" -gt "$LOCAL_COUNT" ]; then
            DIFF=$((REMOTE_COUNT - LOCAL_COUNT))
            echo -e "${YELLOW}⚠️  GitHub 比本地多 $DIFF 个项目！${NC}"
            echo ""
            echo -e "${BLUE}💡 建议: 运行 git pull 更新${NC}"
        elif [ "$REMOTE_COUNT" -lt "$LOCAL_COUNT" ]; then
            DIFF=$((LOCAL_COUNT - REMOTE_COUNT))
            echo -e "${YELLOW}⚠️  本地比 GitHub 多 $DIFF 个项目（可能有本地修改）${NC}"
        else
            echo -e "${GREEN}✅ 项目数量一致${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  无法从 GitHub API 获取项目数量${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未安装 curl 或 jq，跳过远程对比${NC}"
    echo -e "${BLUE}💡 安装方法:${NC}"
    echo "    brew install curl jq"
fi

echo ""

# 5. 检查是否有 55 个项目
echo -e "${BLUE}📊 Step 5: 55 个项目检查${NC}"
echo "----------------------------------------"

if [ "$LOCAL_COUNT" -eq 40 ]; then
    echo -e "${YELLOW}⚠️  用户提到 GitHub 总仓有 55 个项目${NC}"
    echo -e "${YELLOW}⚠️  但本地只有 40 个项目${NC}"
    echo ""
    echo -e "${BLUE}可能的原因:${NC}"
    echo "  1. GitHub 仓库已更新，新增了 15 个项目"
    echo "  2. 用户指的是其他仓库（如 mendableai/firecrawl）"
    echo "  3. 用户记忆有误"
    echo ""
    echo -e "${BLUE}💡 建议操作:${NC}"
    echo "  1. 运行 git pull 更新到最新版本"
    echo "  2. 检查官方仓库: https://github.com/firecrawl/firecrawl-app-examples"
    echo "  3. 检查 mendableai 仓库: https://github.com/mendableai/firecrawl-app-examples"
elif [ "$LOCAL_COUNT" -eq 55 ]; then
    echo -e "${GREEN}✅ 本地已有 55 个项目，与用户描述一致！${NC}"
else
    echo -e "${YELLOW}⚠️  本地有 $LOCAL_COUNT 个项目，与 55 个不符${NC}"
    echo ""
    echo -e "${BLUE}💡 建议: 拉取最新更新${NC}"
fi

echo ""

# 6. 总结和建议
echo -e "${BLUE}📊 总结${NC}"
echo "=========================================="
echo -e "本地项目数量: ${GREEN}$LOCAL_COUNT${NC}"
echo -e "GitHub 更新状态: ${GREEN}已检查${NC}"
echo ""

echo -e "${BLUE}💡 下一步操作建议:${NC}"
echo ""
echo "1. 如果有更新，拉取最新代码:"
echo -e "   ${GREEN}cd \"$EXAMPLES_DIR\"${NC}"
echo -e "   ${GREEN}git pull origin main${NC}"
echo ""
echo "2. 查看更新的项目列表:"
echo -e "   ${GREEN}git log --oneline --name-status HEAD..origin/main${NC}"
echo ""
echo "3. 重新统计项目数量:"
echo -e "   ${GREEN}find . -maxdepth 1 -type d ! -name \".*\" ! -name \".\" | wc -l${NC}"
echo ""
echo "4. 查看完整项目索引:"
echo -e "   ${GREEN}open \"$HANDBOOK_DIR/05-实战案例/示例项目完整索引.md\"${NC}"
echo ""

# 7. 可选：自动更新
echo -e "${YELLOW}是否要立即更新到最新版本? (y/N)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}📥 正在更新...${NC}"
    git pull origin $CURRENT_BRANCH

    # 重新统计
    NEW_COUNT=$(find . -maxdepth 1 -type d ! -name ".*" ! -name "." | wc -l)
    NEW_COUNT=$((NEW_COUNT))

    echo ""
    echo -e "${GREEN}✅ 更新完成！${NC}"
    echo -e "更新后项目数量: ${GREEN}$NEW_COUNT${NC}"

    if [ "$NEW_COUNT" -gt "$LOCAL_COUNT" ]; then
        ADDED=$((NEW_COUNT - LOCAL_COUNT))
        echo -e "${GREEN}🎉 新增了 $ADDED 个项目！${NC}"
    fi
else
    echo ""
    echo -e "${YELLOW}跳过自动更新${NC}"
fi

echo ""
echo -e "${GREEN}✅ 检查完成！${NC}"
echo ""
