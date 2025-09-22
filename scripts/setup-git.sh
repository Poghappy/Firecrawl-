#!/bin/bash

# Git配置和初始化脚本
# 用于配置Git用户信息和初始化仓库

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 配置Git环境...${NC}"

# 检查Git是否已安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git未安装，请先安装Git${NC}"
    exit 1
fi

# 配置Git用户信息（如果未配置）
if [ -z "$(git config --global user.name)" ]; then
    echo -e "${YELLOW}📝 配置Git用户名...${NC}"
    read -p "请输入Git用户名: " git_username
    git config --global user.name "$git_username"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo -e "${YELLOW}📧 配置Git邮箱...${NC}"
    read -p "请输入Git邮箱: " git_email
    git config --global user.email "$git_email"
fi

# 显示当前Git配置
echo -e "${GREEN}✅ 当前Git配置:${NC}"
echo -e "${BLUE}用户名: $(git config --global user.name)${NC}"
echo -e "${BLUE}邮箱: $(git config --global user.email)${NC}"

# 初始化Git仓库（如果不存在）
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📦 初始化Git仓库...${NC}"
    git init
    git branch -M main
else
    echo -e "${GREEN}✅ Git仓库已存在${NC}"
fi

# 配置Git忽略文件
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}📄 创建.gitignore文件...${NC}"
    # .gitignore文件已存在，跳过
else
    echo -e "${GREEN}✅ .gitignore文件已存在${NC}"
fi

echo -e "${GREEN}🎉 Git配置完成！${NC}"
echo -e "${BLUE}💡 现在可以运行 ./scripts/github-init.sh 来初始化GitHub仓库${NC}"
