#!/bin/bash
# GitHub配置快速设置脚本
# 自动完成GitHub Secrets和Actions配置

set -e

echo "🚀 Firecrawl数据采集器 - GitHub配置快速设置"
echo "=============================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置信息
REPO_URL="https://github.com/Poghappy/Firecrawl-"
FIRECRAWL_API_KEY="fc-0a2c801f433d4718bcd8189f2742edf4"
DOCKER_USERNAME="denzhile"
DOCKER_PASSWORD="dckr_pat_9zHDbXagx0b60xvwbqRKNIVo_J0"

echo -e "${BLUE}📋 配置信息:${NC}"
echo "仓库地址: $REPO_URL"
echo "Firecrawl API密钥: ${FIRECRAWL_API_KEY:0:10}...${FIRECRAWL_API_KEY: -4}"
echo "Docker用户名: $DOCKER_USERNAME"
echo "Docker密码: ${DOCKER_PASSWORD:0:10}...${DOCKER_PASSWORD: -4}"
echo ""

# 检查必要的工具
echo -e "${BLUE}🔍 检查必要工具...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git未安装，请先安装Git${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装，请先安装Python3${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 必要工具检查通过${NC}"

# 检查Git仓库状态
echo -e "${BLUE}🔍 检查Git仓库状态...${NC}"

if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 当前目录不是Git仓库${NC}"
    exit 1
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  检测到未提交的更改${NC}"
    echo "是否要提交这些更改？(y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "feat: complete GitHub configuration setup"
        echo -e "${GREEN}✅ 更改已提交${NC}"
    else
        echo -e "${YELLOW}⚠️  跳过提交，继续配置${NC}"
    fi
fi

# 运行验证脚本
echo -e "${BLUE}🧪 运行配置验证...${NC}"
python3 scripts/verify-github-config.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 配置验证通过${NC}"
else
    echo -e "${RED}❌ 配置验证失败${NC}"
    exit 1
fi

# 测试Firecrawl API
echo -e "${BLUE}🔍 测试Firecrawl API...${NC}"
python3 scripts/test-firecrawl-api.py "$FIRECRAWL_API_KEY"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Firecrawl API测试通过${NC}"
else
    echo -e "${RED}❌ Firecrawl API测试失败${NC}"
    exit 1
fi

# 显示配置指南
echo ""
echo -e "${GREEN}🎉 本地配置完成！${NC}"
echo ""
echo -e "${YELLOW}📋 接下来需要手动完成的配置:${NC}"
echo ""
echo -e "${BLUE}1. 配置GitHub Secrets:${NC}"
echo "   访问: $REPO_URL/settings/secrets/actions"
echo "   添加以下Secrets:"
echo "   - FIRECRAWL_API_KEY: $FIRECRAWL_API_KEY"
echo "   - DOCKER_USERNAME: $DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD: $DOCKER_PASSWORD"
echo ""
echo -e "${BLUE}2. 启用GitHub Actions:${NC}"
echo "   访问: $REPO_URL/settings/actions"
echo "   在'Workflow permissions'部分:"
echo "   - 选择 'Read and write permissions'"
echo "   - 勾选 'Allow GitHub Actions to create and approve pull requests'"
echo ""
echo -e "${BLUE}3. 推送代码触发工作流:${NC}"
echo "   git push origin main"
echo ""

# 询问是否推送代码
echo -e "${YELLOW}是否要推送代码到GitHub？(y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📤 推送代码到GitHub...${NC}"
    git push origin main
    echo -e "${GREEN}✅ 代码已推送${NC}"
    echo ""
    echo -e "${BLUE}🔍 检查工作流状态:${NC}"
    echo "访问: $REPO_URL/actions"
else
    echo -e "${YELLOW}⚠️  跳过推送，请稍后手动推送${NC}"
fi

echo ""
echo -e "${GREEN}🎉 配置完成！${NC}"
echo ""
echo -e "${BLUE}📚 相关文档:${NC}"
echo "- 配置指南: docs/GITHUB_SECRETS_SETUP.md"
echo "- 完整报告: GITHUB_SETUP_COMPLETE.md"
echo "- 项目状态: project_status.md"
echo ""
echo -e "${BLUE}🔗 重要链接:${NC}"
echo "- 仓库地址: $REPO_URL"
echo "- Actions状态: $REPO_URL/actions"
echo "- Issues: $REPO_URL/issues"
echo "- Docker Hub: https://hub.docker.com/r/denzhile/firecrawl"
echo ""
echo -e "${GREEN}感谢使用Firecrawl数据采集器！🚀${NC}"
