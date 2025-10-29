# Git Hooks 规范

**版本**: v1.0.0
**更新时间**: 2025-10-28
**适用项目**: FireShot + HawaiiHub
**维护者**: HawaiiHub AI Team

---

## 📋 目录

1. [概述](#概述)
2. [Hooks 架构](#hooks-架构)
3. [Pre-commit Hooks](#pre-commit-hooks)
4. [Commit-msg Hooks](#commit-msg-hooks)
5. [Pre-push Hooks](#pre-push-hooks)
6. [安装和配置](#安装和配置)
7. [最佳实践](#最佳实践)
8. [故障排查](#故障排查)

---

## 概述

### 什么是 Git Hooks？

Git Hooks 是在 Git 执行特定操作时自动触发的脚本，用于：
- **代码质量保证**：自动检查代码格式、类型、Linter 错误
- **提交规范**：强制 Conventional Commits 格式
- **安全防护**：防止敏感信息泄露（如 API 密钥、.env 文件）
- **自动化测试**：在推送前运行测试套件

### FireShot 项目的 Hooks 策略

```
客户端 Hooks（本地开发者机器）
├── pre-commit    # 代码质量检查（Ruff、类型检查、格式化）
├── commit-msg    # 提交消息验证（Conventional Commits）
└── pre-push      # 推送前测试（pytest、安全扫描）

服务端 Hooks（GitHub Actions，可选）
├── pre-receive   # 服务器端验证
└── update        # 分支保护
```

---

## Hooks 架构

### 技术栈选择

我们使用 **Husky** + **lint-staged** 作为 Hooks 管理工具：

| 工具 | 作用 | 优势 |
|------|------|------|
| **Husky** | Git Hooks 管理器 | 跨平台、易配置、团队共享 |
| **lint-staged** | 仅检查暂存文件 | 快速、高效、只检查变更代码 |
| **commitlint** | 提交消息验证 | 强制 Conventional Commits |

**替代方案**：
- **Pre-commit（Python）**：适合纯 Python 项目
- **自定义 Shell 脚本**：`.git/hooks/` 目录下的原生 Hooks

---

## Pre-commit Hooks

### 功能概述

在 `git commit` 之前自动执行：
1. **代码格式化**（Ruff/Black）
2. **Linter 检查**（Ruff）
3. **类型检查**（mypy --strict）
4. **敏感信息扫描**（检测 API 密钥、密码）
5. **文件大小检查**（防止大文件提交）

### 配置文件：`.husky/pre-commit`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${YELLOW}🔍 运行 Pre-commit 检查...${NC}"

# 1. 运行 lint-staged（仅检查暂存文件）
npx lint-staged

# 2. Python 类型检查（仅检查暂存的 .py 文件）
STAGED_PY_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$STAGED_PY_FILES" ]; then
    echo "${YELLOW}📝 运行类型检查...${NC}"

    # 使用 mypy 进行严格类型检查
    if ! python3 -m mypy --strict $STAGED_PY_FILES; then
        echo "${RED}❌ 类型检查失败！请修复类型错误。${NC}"
        exit 1
    fi

    echo "${GREEN}✅ 类型检查通过${NC}"
fi

# 3. 检测敏感信息
echo "${YELLOW}🔒 扫描敏感信息...${NC}"

if git diff --cached --name-only | grep -q '\.env$'; then
    echo "${RED}❌ 错误：尝试提交 .env 文件！${NC}"
    echo "${RED}   请将 .env 添加到 .gitignore${NC}"
    exit 1
fi

# 检查是否有硬编码的 API 密钥
if git diff --cached | grep -qiE '(api[_-]?key|secret|password|token)\s*=\s*["\x27][a-zA-Z0-9]{20,}'; then
    echo "${RED}❌ 警告：检测到可能的硬编码 API 密钥！${NC}"
    echo "${RED}   请使用环境变量：os.getenv('API_KEY')${NC}"
    exit 1
fi

echo "${GREEN}✅ 敏感信息检查通过${NC}"

# 4. 检查文件大小（>10MB）
echo "${YELLOW}📦 检查文件大小...${NC}"

MAX_SIZE=10485760 # 10MB in bytes
LARGE_FILES=$(git diff --cached --name-only --diff-filter=ACM | while read file; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        if [ "$size" -gt "$MAX_SIZE" ]; then
            echo "$file ($((size / 1048576))MB)"
        fi
    fi
done)

if [ -n "$LARGE_FILES" ]; then
    echo "${RED}❌ 错误：检测到大文件（>10MB）：${NC}"
    echo "$LARGE_FILES"
    echo "${YELLOW}   建议：使用 Git LFS 或外部存储${NC}"
    exit 1
fi

echo "${GREEN}✅ 文件大小检查通过${NC}"

echo "${GREEN}✨ Pre-commit 检查全部通过！${NC}"
```

### lint-staged 配置：`package.json`

```json
{
  "lint-staged": {
    "*.py": [
      "ruff format",
      "ruff check --fix",
      "git add"
    ],
    "*.{js,ts,tsx}": [
      "prettier --write",
      "eslint --fix",
      "git add"
    ],
    "*.md": [
      "prettier --write",
      "git add"
    ]
  }
}
```

---

## Commit-msg Hooks

### 功能概述

验证提交消息是否符合 **Conventional Commits** 规范：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 配置文件：`.husky/commit-msg`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${YELLOW}📝 验证提交消息格式...${NC}"

# 使用 commitlint 验证
npx --no -- commitlint --edit "$1"

if [ $? -ne 0 ]; then
    echo ""
    echo "${RED}❌ 提交消息格式错误！${NC}"
    echo ""
    echo "${YELLOW}正确格式示例：${NC}"
    echo "  feat(scraper): 添加夏威夷新闻爬虫"
    echo "  fix(parser): 修复日期解析错误"
    echo "  docs(readme): 更新安装指南"
    echo ""
    echo "${YELLOW}允许的类型：${NC}"
    echo "  feat, fix, docs, refactor, perf, test, chore, style"
    echo ""
    exit 1
fi

echo "${GREEN}✅ 提交消息格式正确${NC}"
```

### commitlint 配置：`commitlint.config.js`

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // 新功能
        'fix',      // Bug 修复
        'docs',     // 文档更新
        'refactor', // 代码重构
        'perf',     // 性能优化
        'test',     // 测试相关
        'chore',    // 构建/工具链
        'style',    // 代码格式
        'revert',   // 回退
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
  },
};
```

---

## Pre-push Hooks

### 功能概述

在 `git push` 之前自动执行：
1. **运行测试套件**（pytest）
2. **安全漏洞扫描**（bandit）
3. **依赖检查**（pip-audit）
4. **分支保护**（禁止直接推送到 main）

### 配置文件：`.husky/pre-push`

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${YELLOW}🚀 运行 Pre-push 检查...${NC}"

# 1. 获取当前分支
current_branch=$(git symbolic-ref --short HEAD)

# 2. 禁止直接推送到主分支
if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
    echo "${RED}❌ 错误：禁止直接推送到 $current_branch 分支！${NC}"
    echo "${YELLOW}   请创建 feature 分支并提交 Pull Request${NC}"
    exit 1
fi

# 3. 运行测试
echo "${YELLOW}🧪 运行测试套件...${NC}"

if ! python3 -m pytest tests/ -v --tb=short; then
    echo "${RED}❌ 测试失败！请修复测试后再推送。${NC}"
    exit 1
fi

echo "${GREEN}✅ 所有测试通过${NC}"

# 4. 安全漏洞扫描（可选，需要安装 bandit）
if command -v bandit &> /dev/null; then
    echo "${YELLOW}🔒 运行安全扫描...${NC}"

    if ! bandit -r src/ -ll -q; then
        echo "${RED}❌ 发现安全漏洞！请修复后再推送。${NC}"
        exit 1
    fi

    echo "${GREEN}✅ 安全扫描通过${NC}"
fi

# 5. 依赖漏洞检查（可选，需要安装 pip-audit）
if command -v pip-audit &> /dev/null; then
    echo "${YELLOW}📦 检查依赖安全性...${NC}"

    if ! pip-audit --require-hashes --disable-pip; then
        echo "${YELLOW}⚠️  警告：发现依赖漏洞，建议更新${NC}"
        # 不阻止推送，仅警告
    fi
fi

echo "${GREEN}✨ Pre-push 检查全部通过！${NC}"
```

---

## 安装和配置

### 方法 1：使用 Husky（推荐）

```bash
# 1. 安装依赖
npm install --save-dev husky lint-staged @commitlint/cli @commitlint/config-conventional

# 2. 初始化 Husky
npx husky install

# 3. 创建 Hooks
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
npx husky add .husky/pre-push "npm test"

# 4. 配置 package.json
npm pkg set scripts.prepare="husky install"
```

### 方法 2：使用 Pre-commit（Python）

```bash
# 1. 安装 pre-commit
pip install pre-commit

# 2. 创建配置文件 .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        args: [--strict]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=10240']
      - id: detect-private-key

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
EOF

# 3. 安装 Hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

### 方法 3：原生 Shell 脚本

```bash
# 1. 创建 .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "运行 Ruff 格式化..."
ruff format .

echo "运行 Ruff Linter..."
ruff check --fix .

echo "运行类型检查..."
mypy --strict src/

echo "✅ Pre-commit 检查通过"
EOF

# 2. 添加执行权限
chmod +x .git/hooks/pre-commit
```

---

## 最佳实践

### 1. 跳过 Hooks（仅紧急情况）

```bash
# 跳过 pre-commit hooks
git commit --no-verify -m "hotfix: 紧急修复生产环境错误"

# 跳过 pre-push hooks
git push --no-verify
```

**⚠️ 警告**：仅在紧急情况下使用，事后必须补充修复！

### 2. 团队共享 Hooks

```bash
# 将 Hooks 配置提交到 Git
git add .husky/ package.json commitlint.config.js
git commit -m "chore: 添加 Git Hooks 配置"
git push

# 团队成员安装
npm install    # 自动运行 husky install
```

### 3. CI/CD 集成

在 GitHub Actions 中复用相同的检查：

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: 安装依赖
        run: |
          pip install ruff mypy pytest
      - name: Ruff 检查
        run: ruff check .
      - name: 类型检查
        run: mypy --strict src/
      - name: 运行测试
        run: pytest tests/
```

### 4. 自定义 Hook 逻辑

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# 检查是否在 feature 分支
branch=$(git symbolic-ref --short HEAD)
if [[ ! "$branch" =~ ^(feature|fix|hotfix)/ ]]; then
    echo "❌ 请在 feature/fix/hotfix 分支上开发"
    exit 1
fi

# 检查是否有未解决的 TODO 注释
if git diff --cached | grep -i "TODO"; then
    echo "⚠️  警告：代码中存在 TODO 注释"
    read -p "是否继续提交？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

---

## 故障排查

### 问题 1：Hooks 未执行

**原因**：Hooks 文件没有执行权限

**解决**：
```bash
chmod +x .husky/*
chmod +x .git/hooks/*
```

### 问题 2：Husky 安装失败

**原因**：Node.js 版本过低或 npm 缓存问题

**解决**：
```bash
# 升级 Node.js
nvm install 18
nvm use 18

# 清理 npm 缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 问题 3：Pre-commit 检查太慢

**原因**：检查了所有文件而非仅暂存文件

**解决**：使用 `lint-staged` 仅检查变更文件
```json
{
  "lint-staged": {
    "*.py": ["ruff format", "ruff check --fix"]
  }
}
```

### 问题 4：Commit-msg 验证失败

**原因**：提交消息格式不符合 Conventional Commits

**解决**：
```bash
# 错误示例
git commit -m "更新代码"

# 正确示例
git commit -m "feat(scraper): 添加新闻爬虫"
git commit -m "fix(parser): 修复日期解析错误"
git commit -m "docs(readme): 更新安装指南"
```

### 问题 5：Pre-push 测试失败

**原因**：测试未通过或测试环境配置问题

**解决**：
```bash
# 本地运行测试
pytest tests/ -v

# 跳过测试（仅紧急情况）
git push --no-verify
```

---

## 参考资源

### 官方文档

- **Husky**: https://typicode.github.io/husky/
- **lint-staged**: https://github.com/okonet/lint-staged
- **commitlint**: https://commitlint.js.org/
- **Pre-commit（Python）**: https://pre-commit.com/

### 推荐配置

- **awesome-git-hooks**: https://github.com/CompSciLauren/awesome-git-hooks
- **Git Hooks Best Practices**: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks

### FireShot 项目相关

- **Conventional Commits**: 参考 `AGENTS.md` 第 368-395 行
- **Python 代码规范**: 参考 `.cursorrules` 第 143-239 行
- **Ruff 配置**: 参考 `pyproject.toml`

---

## 快速参考

### 常用命令

```bash
# 安装 Hooks
npm install              # Husky
pre-commit install       # Pre-commit

# 手动运行检查
npx lint-staged          # 仅检查暂存文件
pre-commit run --all-files  # 检查所有文件

# 更新 Hooks
npx husky add .husky/pre-commit "npx lint-staged"

# 跳过 Hooks（紧急情况）
git commit --no-verify
git push --no-verify

# 测试 Hooks
.husky/pre-commit        # 手动运行
```

### 提交类型速查

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(scraper): 添加夏威夷新闻爬虫` |
| `fix` | Bug 修复 | `fix(parser): 修复日期解析错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装指南` |
| `refactor` | 代码重构 | `refactor(storage): 优化数据存储` |
| `perf` | 性能优化 | `perf(cache): 实现 Redis 缓存` |
| `test` | 测试相关 | `test(scraper): 添加单元测试` |
| `chore` | 构建/工具链 | `chore(deps): 升级 Ruff 版本` |
| `style` | 代码格式 | `style: 统一使用双引号` |

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28
