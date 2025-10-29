#!/bin/bash
# 项目文件自动清理脚本
# 用途: 清理 Firecrawl 数据采集器项目中的无关文件
# 作者: AI Assistant
# 日期: 2025-10-29

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Firecrawl 数据采集器 - 项目清理工具${NC}"
echo "=================================================="
echo ""

# 检查是否在项目根目录
if [ ! -f "project_status.md" ]; then
    echo -e "${RED}❌ 错误: 请在项目根目录下运行此脚本${NC}"
    exit 1
fi

# 询问用户确认
echo -e "${YELLOW}⚠️  此脚本将执行以下操作:${NC}"
echo "  1. 删除虚拟环境目录 (firecrawl_env/)"
echo "  2. 删除空目录 (components/)"
echo "  3. 删除压缩包文件 (5 个 archive.zip)"
echo "  4. 删除官方示例代码 (800+ 个文件)"
echo "  5. 归档辅助脚本和旧报告"
echo ""
read -p "是否继续? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "清理已取消"
    exit 0
fi

# 创建备份
echo ""
echo -e "${GREEN}📦 创建备份...${NC}"
BACKUP_FILE="firecrawl-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$BACKUP_FILE" \
  --exclude='firecrawl_env' \
  --exclude='*.db' \
  --exclude='*.log' \
  --exclude='data/postgres' \
  --exclude='data/redis' \
  --exclude='data/grafana' \
  --exclude='data/prometheus' \
  --exclude='logs' \
  .
echo -e "${GREEN}✅ 备份已创建: $BACKUP_FILE${NC}"

# 高优先级清理
echo ""
echo -e "${RED}🔴 执行高优先级清理...${NC}"

if [ -d "firecrawl_env" ]; then
    echo "  - 删除虚拟环境..."
    rm -rf firecrawl_env/
    echo -e "    ${GREEN}✓${NC} firecrawl_env/ 已删除"
else
    echo "  - 虚拟环境目录不存在，跳过"
fi

if [ -d "components" ]; then
    echo "  - 删除空目录..."
    rmdir components/ 2>/dev/null && echo -e "    ${GREEN}✓${NC} components/ 已删除" || echo "    ⊘ components/ 不为空或不存在"
else
    echo "  - components/ 目录不存在，跳过"
fi

echo "  - 删除压缩包..."
deleted_archives=0
for archive in docs/archive.zip docs/官方文档.zip scripts/archive.zip tests/archive.zip prompts/archive.zip; do
    if [ -f "$archive" ]; then
        rm -f "$archive"
        echo -e "    ${GREEN}✓${NC} $archive 已删除"
        ((deleted_archives++))
    fi
done
if [ $deleted_archives -eq 0 ]; then
    echo "    ⊘ 未找到压缩包文件"
fi

echo "  - 排除数据库文件（Git）..."
git rm --cached data/*.db results/*.db results/archive/*.db 2>/dev/null && echo -e "    ${GREEN}✓${NC} 数据库文件已从 Git 移除" || echo "    ⊘ 数据库文件已排除或不在 Git 中"

# 中优先级清理
echo ""
echo -e "${YELLOW}🟡 执行中优先级清理...${NC}"

if [ -d "docs/official-docs/05-应用案例/firecrawl-app-examples-main" ]; then
    echo "  - 删除官方示例代码..."
    file_count=$(find docs/official-docs/05-应用案例/firecrawl-app-examples-main -type f | wc -l)
    rm -rf docs/official-docs/05-应用案例/firecrawl-app-examples-main/
    echo -e "    ${GREEN}✓${NC} 已删除 $file_count 个示例文件"
else
    echo "  - 官方示例代码目录不存在，跳过"
fi

echo "  - 移动博客文章..."
mkdir -p docs/blog
moved_blogs=0
for blog in docs/official-docs/0[2-6]_*.md; do
    if [ -f "$blog" ]; then
        mv "$blog" docs/blog/
        echo -e "    ${GREEN}✓${NC} $(basename $blog) → docs/blog/"
        ((moved_blogs++))
    fi
done
if [ $moved_blogs -eq 0 ]; then
    echo "    ⊘ 未找到博客文章"
fi

if [ -d "scripts/github-actions" ]; then
    echo "  - 归档 GitHub Actions 脚本..."
    mkdir -p scripts/archive/github-actions
    mv scripts/github-actions/* scripts/archive/github-actions/ 2>/dev/null || true
    rmdir scripts/github-actions 2>/dev/null && echo -e "    ${GREEN}✓${NC} GitHub Actions 脚本已归档" || echo "    ⊘ 目录不为空或移动失败"
else
    echo "  - GitHub Actions 脚本目录不存在，跳过"
fi

echo "  - 移动文档整理元文档..."
moved_meta=0
for meta in docs/official-docs/*_Firecrawl文档整理.md; do
    if [ -f "$meta" ]; then
        mv "$meta" docs/maintenance/
        echo -e "    ${GREEN}✓${NC} $(basename $meta) → docs/maintenance/"
        ((moved_meta++))
    fi
done
if [ $moved_meta -eq 0 ]; then
    echo "    ⊘ 未找到元文档"
fi

if [ -d "prompts" ]; then
    echo "  - 归档 prompts/ 目录..."
    read -p "    是否删除 prompts/ 目录? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 创建单独备份
        tar -czf "prompts-backup-$(date +%Y%m%d).tar.gz" prompts/
        rm -rf prompts/
        echo -e "    ${GREEN}✓${NC} prompts/ 已删除（备份: prompts-backup-*.tar.gz）"
    else
        echo "    ⊘ 保留 prompts/ 目录"
    fi
fi

# 低优先级清理
echo ""
echo -e "${GREEN}🟢 执行低优先级清理...${NC}"

echo "  - 清理 results/ 配置文件..."
deleted_configs=0
for config in results/config*.json results/test_config.json; do
    if [ -f "$config" ]; then
        rm -f "$config"
        echo -e "    ${GREEN}✓${NC} $(basename $config) 已删除"
        ((deleted_configs++))
    fi
done
if [ $deleted_configs -eq 0 ]; then
    echo "    ⊘ 未找到配置文件"
fi

echo "  - 归档旧报告..."
mkdir -p docs/reports/archive
moved_reports=0
for report in docs/reports/feedback-report-*.md docs/reports/test_report_toutiao.md; do
    if [ -f "$report" ]; then
        mv "$report" docs/reports/archive/
        echo -e "    ${GREEN}✓${NC} $(basename $report) → docs/reports/archive/"
        ((moved_reports++))
    fi
done
if [ $moved_reports -eq 0 ]; then
    echo "    ⊘ 未找到旧报告"
fi

# 更新 .gitignore
echo ""
echo -e "${GREEN}📝 更新 .gitignore...${NC}"
if ! grep -q "# Test results (added by cleanup script)" .gitignore; then
    cat >> .gitignore <<EOL

# Test results (added by cleanup script)
results/*.json
docs/reports/*.json
EOL
    echo -e "  ${GREEN}✓${NC} .gitignore 已更新"
else
    echo "  ⊘ .gitignore 已包含相关规则"
fi

# 生成清理报告
echo ""
echo -e "${GREEN}📊 生成清理报告...${NC}"
REPORT_FILE="docs/maintenance/CLEANUP_REPORT_$(date +%Y-%m-%d).md"
cat > "$REPORT_FILE" <<EOL
# 项目清理报告

**执行时间**: $(date '+%Y-%m-%d %H:%M:%S')
**备份文件**: $BACKUP_FILE
**脚本版本**: 1.0

---

## 📋 清理摘要

### 已删除
- ✅ firecrawl_env/ (虚拟环境目录)
- ✅ components/ (空目录)
- ✅ $deleted_archives 个 archive.zip 压缩文件
- ✅ firecrawl-app-examples-main/ (官方示例代码，约 800+ 文件)
- ✅ results/ 中的 $deleted_configs 个配置文件

### 已移动/归档
- 📦 $moved_blogs 个博客文章 → docs/blog/
- 📦 GitHub Actions 脚本 → scripts/archive/github-actions/
- 📦 $moved_meta 个文档整理元文档 → docs/maintenance/
- 📦 $moved_reports 个旧报告 → docs/reports/archive/

### 已更新
- ✏️  .gitignore (添加 test results 规则)
- ✏️  Git 索引 (排除数据库文件)

---

## 💾 备份信息

备份文件位置: \`$BACKUP_FILE\`

### 恢复方法
\`\`\`bash
# 如需恢复，解压备份文件
tar -xzf $BACKUP_FILE
\`\`\`

---

## ✅ 后续操作

### 1. 验证项目功能
\`\`\`bash
# 重新创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v
\`\`\`

### 2. 检查 Git 状态
\`\`\`bash
git status
git diff
\`\`\`

### 3. 提交更改
\`\`\`bash
git add .
git commit -m "chore: 清理项目无关文件和冗余代码"
\`\`\`

### 4. 确认后删除备份
\`\`\`bash
# ⚠️ 确认一切正常后再执行
rm $BACKUP_FILE
rm prompts-backup-*.tar.gz  # 如果创建了 prompts 备份
\`\`\`

---

## 📊 清理统计

- **删除的压缩包**: $deleted_archives 个
- **移动的博客文章**: $moved_blogs 个
- **移动的元文档**: $moved_meta 个
- **移动的旧报告**: $moved_reports 个
- **删除的配置文件**: $deleted_configs 个

---

**清理状态**: ✅ 完成
**生成工具**: scripts/cleanup-project.sh
EOL

echo -e "${GREEN}✅ 清理完成！${NC}"
echo ""
echo "=================================================="
echo -e "${GREEN}📋 清理报告:${NC} $REPORT_FILE"
echo -e "${GREEN}📦 备份文件:${NC} $BACKUP_FILE"
echo ""
echo -e "${YELLOW}⚠️  请执行以下验证操作:${NC}"
echo "   1. 重新创建虚拟环境:"
echo "      python3 -m venv venv && source venv/bin/activate"
echo ""
echo "   2. 安装依赖:"
echo "      pip install -r requirements.txt"
echo ""
echo "   3. 运行测试:"
echo "      pytest tests/ -v"
echo ""
echo "   4. 检查 Git 状态:"
echo "      git status"
echo ""
echo "   5. 提交更改:"
echo "      git add ."
echo "      git commit -m 'chore: 清理项目无关文件'"
echo ""
echo "   6. 确认无误后删除备份:"
echo "      rm $BACKUP_FILE"
echo ""
echo -e "${GREEN}感谢使用项目清理工具！${NC}"
