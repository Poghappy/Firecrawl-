#!/bin/bash

# GitHub仓库初始化脚本
# 用于将本地项目推送到GitHub仓库

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_NAME="Firecrawl数据采集器"
GITHUB_REPO="Poghappy/Firecrawl-"
GITHUB_URL="https://github.com/${GITHUB_REPO}.git"

echo -e "${BLUE}🚀 开始初始化GitHub仓库...${NC}"

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📦 初始化Git仓库...${NC}"
    git init
    git branch -M main
else
    echo -e "${GREEN}✅ Git仓库已存在${NC}"
fi

# 检查远程仓库
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}🔄 更新远程仓库URL...${NC}"
    git remote set-url origin $GITHUB_URL
else
    echo -e "${YELLOW}➕ 添加远程仓库...${NC}"
    git remote add origin $GITHUB_URL
fi

# 添加所有文件
echo -e "${YELLOW}📁 添加文件到Git...${NC}"
git add .

# 检查是否有变更
if git diff --staged --quiet; then
    echo -e "${GREEN}✅ 没有新的变更需要提交${NC}"
else
    # 提交变更
    echo -e "${YELLOW}💾 提交变更...${NC}"
    git commit -m "feat: 初始化Firecrawl数据采集器项目

- 添加核心采集器模块
- 配置Docker部署环境
- 设置CI/CD工作流
- 完善项目文档和配置

项目特性:
- 基于Firecrawl API的智能数据采集
- 支持多种网站内容监控
- 集成火鸟门户系统
- 提供Web Dashboard和API接口
- 支持Docker容器化部署"

    # 推送到GitHub
    echo -e "${YELLOW}🚀 推送到GitHub仓库...${NC}"
    git push -u origin main
    
    echo -e "${GREEN}🎉 GitHub仓库初始化完成！${NC}"
    echo -e "${BLUE}📋 仓库地址: https://github.com/${GITHUB_REPO}${NC}"
    echo -e "${BLUE}📋 Actions: https://github.com/${GITHUB_REPO}/actions${NC}"
    echo -e "${BLUE}📋 Issues: https://github.com/${GITHUB_REPO}/issues${NC}"
fi

echo -e "${GREEN}✅ 脚本执行完成${NC}"
