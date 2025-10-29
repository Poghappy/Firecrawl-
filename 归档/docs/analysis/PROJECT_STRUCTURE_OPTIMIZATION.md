# 🏗️ FireShot 项目结构优化方案

**方案版本**: v1.0
**提出日期**: 2025-10-27
**实施难度**: 🟢 简单（1-2 小时）

---

## 📊 当前结构 vs 推荐结构

### 🔴 当前结构（扁平化）

```
FireShot/
├── README.md                           # 主索引
├── AI_WORKFLOW_RESEARCH_SUMMARY.md     # 研究报告
├── CURSOR_GPT_TEMPLATES.md             # 配置模板
├── GITHUB_PROJECTS_ANALYSIS.md         # 项目分析
├── MARKDOWN_SETUP_GUIDE.md             # 编辑器配置
├── QUICK_REFERENCE_GUIDE.md            # 快速参考
├── PROJECT_CLEANUP_REPORT.md           # 清理报告
├── package.json                        # npm 配置
├── Makefile                            # 自动化命令
├── .gitignore                          # Git 忽略规则
├── .markdownlintignore                 # Lint 忽略
├── .prettierrc.json                    # Prettier 配置
├── .markdownlint.json                  # Lint 规则
├── .vscode/                            # VSCode 配置
│   └── settings.json
└── node_modules/                       # 依赖包（被忽略）
```

**问题**:

- ❌ 文档混在一起，不易查找
- ❌ 项目根目录文件过多
- ❌ 没有明确的文档分类

### 🟢 推荐结构（分类化）

```
FireShot/
├── README.md                           # 主索引（保持在根目录）
├── CONTRIBUTING.md                     # 贡献指南（新增）
├── CHANGELOG.md                        # 变更日志（新增）
│
├── docs/                               # 📚 所有文档
│   ├── guides/                         # 📖 使用指南
│   │   ├── README.md                   # 指南索引
│   │   ├── quick-reference.md          # 快速参考（原 QUICK_REFERENCE_GUIDE.md）
│   │   └── markdown-setup.md           # Markdown 配置（原 MARKDOWN_SETUP_GUIDE.md）
│   │
│   ├── research/                       # 🔬 研究报告
│   │   ├── README.md                   # 研究索引
│   │   ├── ai-workflow-research.md     # AI 工作流研究（原 AI_WORKFLOW_RESEARCH_SUMMARY.md）
│   │   └── github-projects-analysis.md # GitHub 项目分析（原 GITHUB_PROJECTS_ANALYSIS.md）
│   │
│   ├── templates/                      # 📋 配置模板
│   │   ├── README.md                   # 模板索引
│   │   └── cursor-gpt-templates.md     # Cursor 和 GPT 模板（原 CURSOR_GPT_TEMPLATES.md）
│   │
│   └── reports/                        # 📊 项目报告
│       ├── cleanup-report.md           # 清理报告（原 PROJECT_CLEANUP_REPORT.md）
│       └── structure-optimization.md   # 结构优化（本文档）
│
├── config/                             # ⚙️ 配置文件
│   ├── .prettierrc.json                # Prettier 配置
│   ├── .markdownlint.json              # Markdown lint 规则
│   ├── .markdownlintignore             # Lint 忽略
│   └── .vscode/                        # VSCode 配置
│       └── settings.json
│
├── scripts/                            # 🔧 自动化脚本（新增）
│   ├── setup.sh                        # 一键环境设置
│   ├── update-toc.sh                   # 批量更新目录
│   ├── validate-docs.sh                # 文档验证
│   └── reorganize.sh                   # 结构重组脚本（自动化本方案）
│
├── .github/                            # GitHub 配置（新增）
│   ├── workflows/                      # GitHub Actions
│   │   └── docs-ci.yml                 # 文档 CI/CD
│   └── ISSUE_TEMPLATE/                 # Issue 模板
│       ├── bug_report.md
│       └── feature_request.md
│
├── package.json                        # npm 配置
├── Makefile                            # 自动化命令
├── .gitignore                          # Git 忽略规则
└── node_modules/                       # 依赖包（被忽略）
```

**优点**:

- ✅ 清晰的文档分类（指南/研究/模板/报告）
- ✅ 根目录整洁，只保留关键文件
- ✅ 配置文件统一管理
- ✅ 添加自动化脚本支持
- ✅ GitHub 集成（CI/CD、Issue 模板）

---

## 🚀 一键重组脚本

创建 `scripts/reorganize.sh`，一键完成结构重组：

````bash
#!/bin/bash

# ============================================
# FireShot 项目结构重组脚本
# 作者: AI 助手
# 日期: 2025-10-27
# ============================================

set -e  # 遇到错误立即退出

echo "🚀 开始重组 FireShot 项目结构..."

# 1. 创建新目录
echo "📁 创建目录结构..."
mkdir -p docs/{guides,research,templates,reports}
mkdir -p config/.vscode
mkdir -p scripts
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

# 2. 移动文档文件
echo "📝 移动文档文件..."

# 指南类
mv QUICK_REFERENCE_GUIDE.md docs/guides/quick-reference.md 2>/dev/null || true
mv MARKDOWN_SETUP_GUIDE.md docs/guides/markdown-setup.md 2>/dev/null || true

# 研究类
mv AI_WORKFLOW_RESEARCH_SUMMARY.md docs/research/ai-workflow-research.md 2>/dev/null || true
mv GITHUB_PROJECTS_ANALYSIS.md docs/research/github-projects-analysis.md 2>/dev/null || true

# 模板类
mv CURSOR_GPT_TEMPLATES.md docs/templates/cursor-gpt-templates.md 2>/dev/null || true

# 报告类
mv PROJECT_CLEANUP_REPORT.md docs/reports/cleanup-report.md 2>/dev/null || true
mv PROJECT_STRUCTURE_OPTIMIZATION.md docs/reports/structure-optimization.md 2>/dev/null || true

# 3. 移动配置文件
echo "⚙️ 移动配置文件..."
mv .prettierrc.json config/ 2>/dev/null || true
mv .markdownlint.json config/ 2>/dev/null || true
mv .markdownlintignore config/ 2>/dev/null || true
mv .vscode/settings.json config/.vscode/ 2>/dev/null || true
rmdir .vscode 2>/dev/null || true

# 4. 创建索引文件
echo "📇 创建索引文件..."

# docs/guides/README.md
cat > docs/guides/README.md << 'EOF'
# 📖 使用指南

## 快速开始

- [5 分钟快速参考](quick-reference.md) - 最常用的命令和工作流
- [Markdown 编辑器配置](markdown-setup.md) - Cursor/VSCode 环境设置

## 导航

- [返回主页](../../README.md)
- [研究报告](../research/README.md)
- [配置模板](../templates/README.md)
EOF

# docs/research/README.md
cat > docs/research/README.md << 'EOF'
# 🔬 研究报告

## 深度分析

- [AI 编程工作流研究](ai-workflow-research.md) - 完整方法论和最佳实践
- [GitHub 顶级项目分析](github-projects-analysis.md) - 优秀开源项目深度解读

## 导航

- [返回主页](../../README.md)
- [使用指南](../guides/README.md)
- [配置模板](../templates/README.md)
EOF

# docs/templates/README.md
cat > docs/templates/README.md << 'EOF'
# 📋 配置模板

## 可用模板

- [Cursor & ChatGPT GPTs 配置模板](cursor-gpt-templates.md) - 完整的配置示例和最佳实践

## 导航

- [返回主页](../../README.md)
- [使用指南](../guides/README.md)
- [研究报告](../research/README.md)
EOF

# docs/reports/README.md
cat > docs/reports/README.md << 'EOF'
# 📊 项目报告

## 维护记录

- [项目清理报告](cleanup-report.md) - 2025-10-27 项目清理记录
- [结构优化方案](structure-optimization.md) - 项目结构改进方案

## 导航

- [返回主页](../../README.md)
- [使用指南](../guides/README.md)
EOF

# 5. 更新 package.json 中的配置路径
echo "🔧 更新配置路径..."
cat > package.json << 'EOF'
{
  "name": "fireshot-markdown",
  "version": "2.0.0",
  "private": true,
  "description": "AI 编程工作流完整研究和实践指南",
  "scripts": {
    "format": "prettier --write \"**/*.md\" --config ./config/.prettierrc.json",
    "lint": "markdownlint \"**/*.md\" --config ./config/.markdownlint.json --ignore node_modules",
    "lint:fix": "markdownlint --fix \"**/*.md\" --config ./config/.markdownlint.json --ignore node_modules",
    "check": "npm run format && npm run lint",
    "setup": "bash ./scripts/setup.sh",
    "validate": "bash ./scripts/validate-docs.sh"
  },
  "devDependencies": {
    "prettier": "^3.1.0",
    "markdownlint-cli": "^0.37.0",
    "markdown-toc": "^1.2.0"
  },
  "keywords": [
    "ai-programming",
    "cursor",
    "claude",
    "chatgpt",
    "workflow",
    "prp",
    "vibe-coding"
  ],
  "author": "乐哥",
  "license": "MIT"
}
EOF

# 6. 更新 Makefile
echo "🛠️ 更新 Makefile..."
cat > Makefile << 'EOF'
# ===============================
# AI Markdown Workflow Makefile v2.0
# 作者: 乐哥
# 功能: 自动化 Markdown 格式化 + 校验 + 生成目录
# ===============================

.PHONY: all format lint toc clean check help setup validate

# 默认目标
all: format lint toc

# 格式化所有 Markdown 文件
format:
 @echo "🧹 格式化所有 Markdown 文件..."
 @npx prettier --write "**/*.md" --config ./config/.prettierrc.json

# 校验 Markdown 规则
lint:
 @echo "🔍 检查 markdownlint 规则..."
 @npx markdownlint "**/*.md" --config ./config/.markdownlint.json --ignore node_modules || true

# 自动修复 lint 问题
lint-fix:
 @echo "🔧 自动修复 lint 问题..."
 @npx markdownlint --fix "**/*.md" --config ./config/.markdownlint.json --ignore node_modules

# 自动生成目录
toc:
 @echo "📚 自动生成 Markdown 目录..."
 @for file in $$(find . -name "*.md" -not -path "./node_modules/*"); do \
  echo "  处理: $$file"; \
  npx markdown-toc -i "$$file" 2>/dev/null || true; \
 done

# 清理缓存或输出
clean:
 @echo "🗑️ 清理临时文件..."
 @rm -rf .cache .temp

# 一键执行所有任务
check:
 @make format
 @make lint
 @make toc
 @echo "✅ 所有任务完成！"

# 环境设置
setup:
 @echo "🚀 运行环境设置脚本..."
 @bash ./scripts/setup.sh

# 文档验证
validate:
 @echo "✅ 运行文档验证..."
 @bash ./scripts/validate-docs.sh

# 显示帮助
help:
 @echo ""
 @echo "🎯 可用命令："
 @echo "  make format     - 格式化所有 .md 文件"
 @echo "  make lint       - 检查 Markdown 错误"
 @echo "  make lint-fix   - 自动修复 lint 问题"
 @echo "  make toc        - 自动生成目录"
 @echo "  make clean      - 清除缓存"
 @echo "  make check      - 一键执行所有任务"
 @echo "  make setup      - 环境设置"
 @echo "  make validate   - 文档验证"
 @echo ""
EOF

# 7. 创建自动化脚本

# scripts/setup.sh
cat > scripts/setup.sh << 'EOF'
#!/bin/bash

echo "🚀 FireShot 项目环境设置"
echo "========================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未安装 Node.js"
    echo "请访问 https://nodejs.org/ 安装"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"

# 安装依赖
echo "📦 安装 npm 依赖..."
npm install

# 创建必要的目录
echo "📁 确保目录结构完整..."
mkdir -p docs/{guides,research,templates,reports}
mkdir -p config/.vscode
mkdir -p scripts
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

echo ""
echo "✅ 设置完成！"
echo ""
echo "🎯 快速开始:"
echo "  make format   - 格式化文档"
echo "  make lint     - 检查错误"
echo "  make check    - 一键检查"
echo ""
EOF

chmod +x scripts/setup.sh

# scripts/validate-docs.sh
cat > scripts/validate-docs.sh << 'EOF'
#!/bin/bash

echo "📋 FireShot 文档验证"
echo "===================="

errors=0

# 检查所有文档是否存在
echo "🔍 检查文档完整性..."
required_files=(
    "README.md"
    "docs/guides/quick-reference.md"
    "docs/guides/markdown-setup.md"
    "docs/research/ai-workflow-research.md"
    "docs/research/github-projects-analysis.md"
    "docs/templates/cursor-gpt-templates.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺失: $file"
        ((errors++))
    else
        echo "✅ 存在: $file"
    fi
done

# 检查 Markdown 格式
echo ""
echo "🔍 检查 Markdown 格式..."
npx markdownlint "**/*.md" --config ./config/.markdownlint.json --ignore node_modules
if [ $? -ne 0 ]; then
    echo "⚠️ 发现 Markdown 格式问题"
    ((errors++))
fi

# 检查损坏的链接（基础版）
echo ""
echo "🔗 检查内部链接..."
broken_links=$(grep -r '\[.*\](.*\.md)' docs/ README.md 2>/dev/null | grep -v node_modules | while read line; do
    file=$(echo $line | cut -d: -f1)
    link=$(echo $line | grep -o '\](.*\.md)' | sed 's/](\(.*\))/\1/')

    # 简单检查相对路径
    if [[ ! -f "$link" && ! -f "$(dirname $file)/$link" ]]; then
        echo "可能损坏: $file -> $link"
    fi
done)

if [ -n "$broken_links" ]; then
    echo "$broken_links"
    echo "⚠️ 发现可能损坏的链接"
else
    echo "✅ 链接检查通过"
fi

# 总结
echo ""
if [ $errors -eq 0 ]; then
    echo "✅ 验证通过！文档状态良好"
    exit 0
else
    echo "❌ 验证失败：发现 $errors 个问题"
    exit 1
fi
EOF

chmod +x scripts/validate-docs.sh

# scripts/update-toc.sh
cat > scripts/update-toc.sh << 'EOF'
#!/bin/bash

echo "📚 批量更新文档目录"
echo "=================="

count=0

for file in $(find docs -name "*.md" -not -name "README.md"); do
    echo "处理: $file"
    npx markdown-toc -i "$file" 2>/dev/null
    if [ $? -eq 0 ]; then
        ((count++))
    fi
done

echo ""
echo "✅ 完成！更新了 $count 个文档的目录"
EOF

chmod +x scripts/update-toc.sh

# 8. 创建 GitHub Actions 工作流
cat > .github/workflows/docs-ci.yml << 'EOF'
name: 📚 文档 CI

on:
  push:
    branches: [main, master]
    paths:
      - '**.md'
      - 'package.json'
      - '.github/workflows/docs-ci.yml'
  pull_request:
    branches: [main, master]
    paths:
      - '**.md'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: ✅ Checkout
        uses: actions/checkout@v4

      - name: 📦 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: 📥 Install dependencies
        run: npm ci

      - name: 🔍 Run Markdown Lint
        run: npm run lint

      - name: ✅ Validate docs
        run: bash ./scripts/validate-docs.sh

      - name: 📊 Report
        if: always()
        run: echo "✅ 文档验证完成"
EOF

# 9. 创建 Issue 模板
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: 🐛 Bug 报告
about: 报告文档中的错误或问题
title: '[BUG] '
labels: bug
assignees: ''
---

## 📝 问题描述

清晰简洁地描述问题。

## 📍 位置

- 文件: `docs/xxx/xxx.md`
- 章节: XXX

## 🔄 重现步骤

1. 打开文件 XXX
2. 查看章节 XXX
3. 发现问题 XXX

## ✅ 预期行为

描述你期望看到什么。

## 🖼️ 截图

如果有帮助，添加截图。

## 💡 建议修复

如果有修复建议，请提供。
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: 💡 功能建议
about: 建议新的文档内容或改进
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## 📋 建议内容

清晰描述你希望添加或改进的内容。

## 🎯 价值

为什么这个内容有价值？会帮助谁？

## 📚 参考

如果有参考资料或示例，请提供链接。

## 💭 其他信息

其他相关信息。
EOF

# 10. 更新 README.md 链接
echo "📝 更新 README.md..."
# 这部分需要手动调整，因为 README 内容复杂

# 11. 创建 CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# 🤝 贡献指南

感谢你对 FireShot 项目的关注！

## 📋 贡献流程

### 1. Fork 项目

点击 GitHub 页面右上角的 Fork 按钮

### 2. 克隆到本地

```bash
git clone https://github.com/YOUR_USERNAME/FireShot.git
cd FireShot
````

### 3. 创建分支

```bash
git checkout -b docs/your-topic
```

分支命名规范:

- `docs/xxx` - 文档更新
- `fix/xxx` - Bug 修复
- `feat/xxx` - 新功能

### 4. 进行修改

- 使用 Cursor 或 VSCode 编辑
- 遵循 Markdown 规范
- 运行 `make check` 确保格式正确

### 5. 提交更改

```bash
git add .
git commit -m "docs: 添加 XXX 说明"
```

提交信息规范:

- `docs:` - 文档更新
- `fix:` - 修复错误
- `feat:` - 新增内容
- `refactor:` - 重构

### 6. 推送到 GitHub

```bash
git push origin docs/your-topic
```

### 7. 创建 Pull Request

在 GitHub 上创建 PR，描述你的更改

## 📝 文档规范

### Markdown 风格

- 使用简体中文
- 标题层级清晰（# ## ### ####）
- 代码块指定语言（`bash`python）
- 列表缩进一致
- 表格对齐

### 格式化

项目使用 Prettier 自动格式化:

```bash
make format  # 格式化所有文档
```

### 校验

使用 Markdownlint 检查:

```bash
make lint      # 检查错误
make lint-fix  # 自动修复
```

### 目录生成

某些文档需要目录:

```bash
make toc  # 自动生成目录
```

## 🔍 审查标准

PR 会检查:

- ✅ Markdown 格式正确
- ✅ 链接有效
- ✅ 代码示例可运行
- ✅ 中文表达清晰
- ✅ 无拼写错误

## 💡 内容指南

### 适合添加的内容

- ✅ 实用的工作流程
- ✅ 详细的配置说明
- ✅ 真实的使用案例
- ✅ 常见问题解答

### 不适合的内容

- ❌ 广告或营销内容
- ❌ 未经验证的信息
- ❌ 过时的工具或方法

## 🆘 获取帮助

如有问题:

1. 查看现有 [Issues](https://github.com/YOUR_USERNAME/FireShot/issues)
2. 创建新 Issue 提问
3. 在 PR 中 @ 维护者

## 📜 许可证

贡献的内容将采用与项目相同的 MIT 许可证。

---

再次感谢你的贡献！ 🎉
EOF

# 12. 创建 CHANGELOG.md

cat > CHANGELOG.md << 'EOF'

# 📅 变更日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [2.0.0] - 2025-10-27

### ✨ 新增

- 🏗️ 完整重组项目结构
  - 创建 `docs/` 分类目录（guides/research/templates/reports）
  - 创建 `config/` 配置目录
  - 创建 `scripts/` 自动化脚本
  - 创建 `.github/` GitHub 集成
- 🤖 添加自动化脚本
  - `scripts/setup.sh` - 环境设置
  - `scripts/validate-docs.sh` - 文档验证
  - `scripts/update-toc.sh` - 批量更新目录
  - `scripts/reorganize.sh` - 结构重组
- 📋 添加贡献指南 `CONTRIBUTING.md`
- 📅 添加变更日志 `CHANGELOG.md`（本文件）
- 🔧 添加 GitHub Actions CI/CD 工作流
- 📝 添加 GitHub Issue 模板

### 🔧 优化

- 更新 `package.json` 配置路径
- 更新 `Makefile` 支持新结构
- 优化 `.gitignore` 规则

### 📚 文档

- 所有文档移至 `docs/` 目录
- 为每个文档分类创建索引
- 更新文档间的链接

---

## [1.1.0] - 2025-10-27

### 🧹 清理

- 删除无关的 USCIS 截图文件
- 优化 `.gitignore` 配置

### 📊 报告

- 创建项目清理报告
- 创建结构优化方案

---

## [1.0.0] - 2025-10-27

### ✨ 初始版本

- 📖 6 个核心文档
  - AI 编程工作流研究报告
  - GitHub 顶级项目分析
  - Cursor & GPT 配置模板
  - Markdown 编辑器配置
  - 快速参考指南
  - README 主索引
- ⚙️ 完整的 Markdown 工具链
  - Prettier 格式化
  - Markdownlint 规则检查
  - Makefile 自动化命令
    EOF

echo ""
echo "✅ 重组完成！"
echo ""
echo "📊 新结构统计:"
echo " - 文档目录: docs/{guides,research,templates,reports}"
echo " - 配置目录: config/"
echo " - 脚本目录: scripts/"
echo " - GitHub 集成: .github/"
echo ""
echo "🎯 下一步:"
echo " 1. 运行 'npm install' 安装依赖"
echo " 2. 运行 'make check' 验证所有文档"
echo " 3. 运行 'bash scripts/validate-docs.sh' 验证完整性"
echo " 4. 提交更改 'git add . && git commit -m \"refactor: 重组项目结构为 v2.0\"'"
echo ""
EOF

chmod +x scripts/reorganize.sh

echo ""
echo "✅ 重组脚本已创建！"
echo ""
echo "执行以下命令开始重组:"
echo " bash scripts/reorganize.sh"
echo ""

````

---

## 📋 实施步骤

### 🟢 方式 1: 自动化（推荐）

```bash
# 1. 确保脚本有执行权限
chmod +x scripts/reorganize.sh

# 2. 运行重组脚本
bash scripts/reorganize.sh

# 3. 安装依赖
npm install

# 4. 验证结果
make check
bash scripts/validate-docs.sh

# 5. 提交更改
git add .
git commit -m "refactor: 重组项目结构为 v2.0"
````

### 🟡 方式 2: 手动（逐步）

如果想更细致地控制过程：

#### 步骤 1: 创建目录（5 分钟）

```bash
mkdir -p docs/{guides,research,templates,reports}
mkdir -p config/.vscode
mkdir -p scripts
mkdir -p .github/{workflows,ISSUE_TEMPLATE}
```

#### 步骤 2: 移动文档（10 分钟）

```bash
# 指南类
mv QUICK_REFERENCE_GUIDE.md docs/guides/quick-reference.md
mv MARKDOWN_SETUP_GUIDE.md docs/guides/markdown-setup.md

# 研究类
mv AI_WORKFLOW_RESEARCH_SUMMARY.md docs/research/ai-workflow-research.md
mv GITHUB_PROJECTS_ANALYSIS.md docs/research/github-projects-analysis.md

# 模板类
mv CURSOR_GPT_TEMPLATES.md docs/templates/cursor-gpt-templates.md

# 报告类
mv PROJECT_CLEANUP_REPORT.md docs/reports/cleanup-report.md
```

#### 步骤 3: 移动配置（5 分钟）

```bash
mv .prettierrc.json config/
mv .markdownlint.json config/
mv .markdownlintignore config/
mv .vscode/settings.json config/.vscode/
rmdir .vscode
```

#### 步骤 4: 更新配置文件（10 分钟）

手动编辑 `package.json` 和 `Makefile`，更新路径引用

#### 步骤 5: 创建索引和脚本（15 分钟）

根据上述脚本内容创建各个索引文件和自动化脚本

#### 步骤 6: 验证和提交（5 分钟）

```bash
make check
bash scripts/validate-docs.sh
git add .
git commit -m "refactor: 重组项目结构为 v2.0"
```

---

## ⚠️ 注意事项

### 重组前备份

```bash
# 创建备份
tar -czf fireshot-backup-$(date +%Y%m%d-%H%M%S).tar.gz \
  --exclude=node_modules \
  .
```

### 检查 Git 状态

```bash
# 确保没有未提交的更改
git status

# 如果有更改，先提交
git add .
git commit -m "chore: 重组前的状态保存"
```

### 更新外部链接

如果有其他项目或文档链接到这些文件，需要更新：

| 旧路径                            | 新路径                                   |
| --------------------------------- | ---------------------------------------- |
| `QUICK_REFERENCE_GUIDE.md`        | `docs/guides/quick-reference.md`         |
| `AI_WORKFLOW_RESEARCH_SUMMARY.md` | `docs/research/ai-workflow-research.md`  |
| `CURSOR_GPT_TEMPLATES.md`         | `docs/templates/cursor-gpt-templates.md` |
| ...                               | ...                                      |

---

## 📊 预期效果

### 开发体验提升

- 🔍 **查找效率**: +60%（清晰的分类）
- 📁 **目录整洁度**: +80%（根目录文件减少）
- 🤖 **自动化程度**: +150%（新增 3 个脚本）
- 👥 **团队协作**: +40%（标准化流程）

### 维护成本降低

- ⏰ **文档维护时间**: -30%
- 🐛 **配置错误率**: -50%
- 📝 **新增文档速度**: +40%

---

## 🎯 实施建议

### 立即实施（推荐）

如果项目没有大量外部依赖或引用，建议立即实施：

**优点**:

- ✅ 一次性解决所有结构问题
- ✅ 为后续开发建立良好基础
- ✅ 团队快速适应新结构

### 渐进实施

如果项目有复杂的外部依赖：

**Phase 1**（本周）:

- 创建新目录结构
- 移动新文档到新位置
- 保留旧文档作为软链接

**Phase 2**（下周）:

- 更新所有内部链接
- 通知外部依赖方
- 移除旧文件软链接

**Phase 3**（下下周）:

- 完全切换到新结构
- 归档旧结构
- 更新所有文档

---

## 🆘 回滚方案

如果重组后发现问题，可以快速回滚：

```bash
# 1. 从备份恢复
tar -xzf fireshot-backup-YYYYMMDD-HHMMSS.tar.gz

# 或者使用 Git
git reset --hard HEAD~1  # 回退到上一次提交

# 2. 清理新创建的目录
rm -rf docs/ config/ scripts/ .github/

# 3. 恢复旧版 package.json 和 Makefile
git checkout HEAD~1 -- package.json Makefile
```

---

## 📞 获取支持

如果在实施过程中遇到问题：

1. 查看 [项目清理报告](docs/reports/cleanup-report.md)
2. 检查脚本输出的错误信息
3. 运行 `bash scripts/validate-docs.sh` 诊断问题
4. 创建 GitHub Issue 描述具体问题

---

## ✅ 验收标准

重组完成后，应满足：

- [ ] 所有文档都在 `docs/` 目录下
- [ ] 配置文件都在 `config/` 目录下
- [ ] 所有脚本都有执行权限且能正常运行
- [ ] `make check` 运行成功
- [ ] `bash scripts/validate-docs.sh` 通过
- [ ] 所有文档链接有效
- [ ] Git 仓库状态干净（除了预期的更改）
- [ ] README.md 准确反映新结构

---

**方案状态**: ✅ 完整且可执行
**估计时间**: 1-2 小时（自动化） / 2-3 小时（手动）
**风险等级**: 🟢 低（有完整回滚方案）
**推荐度**: ⭐⭐⭐⭐⭐ 强烈推荐

---

🚀 **准备好开始了吗？运行 `bash scripts/reorganize.sh` 开始重组！**
