# ⚡ FireShot 项目优化快速指南

**最后更新**: 2025-10-28
**版本**: v2.0.0
**阅读时间**: 3 分钟

---

## 🚀 立即开始（30 秒）

### 1. 检查项目健康度

```bash
# 方式 1: 使用脚本
./scripts/project_health_check.sh

# 方式 2: 使用 Makefile（推荐）
make health

# 方式 3: 使用 npm
npm run health
```

**预期输出**: 项目健康度评分（90%+ 为优秀）

---

### 2. 优化项目配置

```bash
# 方式 1: 使用脚本
./scripts/optimize_project.sh

# 方式 2: 使用 Makefile（推荐）
make optimize

# 方式 3: 使用 npm
npm run optimize
```

**功能**: 自动清理、优化、格式化代码

---

### 3. 一键完整维护

```bash
make maintenance
```

**包含**: 健康检查 + 项目优化

---

## 📋 常用命令速查

### 开发命令

```bash
# 代码质量
make lint              # Python Linter（Ruff）
make format            # 代码格式化
make type-check        # 类型检查（MyPy）
make check             # 快速检查（Lint + 类型）

# 测试
make test              # 运行测试
make test-cov          # 测试 + 覆盖率报告

# 清理
make clean             # 清理缓存
make clean-all         # 深度清理（包括虚拟环境）
```

### Node.js 命令

```bash
# 安装依赖
npm install            # 安装所有依赖

# 代码质量
npm run lint           # ESLint 检查
npm run format         # Prettier 格式化
npm run type-check     # TypeScript 类型检查
npm run check          # 完整检查

# 构建
npm run build          # 编译 TypeScript
npm run dev            # 开发模式（监听）
```

### Python 命令

```bash
# 环境配置
make setup             # 一键配置环境
make install           # 安装生产依赖
make dev               # 安装开发依赖

# 运行示例
make quick-start       # 快速开始示例
make scrape-blog       # 爬取 Firecrawl 博客
```

---

## 🎯 最佳实践

### 提交代码前

```bash
# 1. 检查代码质量
make check

# 2. 运行测试
make test

# 3. 提交代码（自动运行 lint-staged）
git add .
git commit -m "feat: 添加新功能"
```

### 每周维护（5 分钟）

```bash
# 1. 运行健康检查
make health

# 2. 查看警告项，逐个改进
# 3. 运行优化脚本
make optimize

# 4. 提交优化结果
git add .
git commit -m "chore: 每周维护优化"
```

### 每月审查（15 分钟）

```bash
# 1. 检查依赖更新
npm outdated

# 2. 更新依赖
npm update

# 3. 运行完整测试
make all

# 4. 生成测试报告
make test-cov
```

---

## 🔧 解决警告项

根据健康检查结果，这里是常见警告的解决方案：

### ⚠️ ESLint / Prettier 未安装

```bash
# 安装 Node.js 依赖
npm install

# 验证安装
npm run lint
npm run format
```

### ⚠️ 发现大型文件

```bash
# 查找大型文件
find . -type f -size +10M ! -path "./.git/*" ! -path "./node_modules/*"

# 添加到 .gitignore 或 .cursorignore
echo "path/to/large/file" >> .gitignore
```

### ⚠️ 未配置远程仓库

```bash
# 添加 GitHub 远程仓库
git remote add origin https://github.com/username/FireShot.git

# 验证
git remote -v
```

### ⚠️ 有未提交的更改

```bash
# 查看更改
git status

# 提交更改
git add .
git commit -m "chore: 提交项目优化"

# 推送到远程
git push origin main
```

---

## 📊 健康度评级

| 评分        | 等级      | 建议               |
| ----------- | --------- | ------------------ |
| **90-100%** | 🎉 优秀   | 保持现状，定期维护 |
| **75-89%**  | 👍 良好   | 改进警告项         |
| **60-74%**  | ⚠️ 一般   | 尽快解决失败项     |
| **< 60%**   | ❌ 需改进 | 立即处理失败项     |

---

## 🆘 快速故障排查

### 问题：脚本权限错误

```bash
# 添加执行权限
chmod +x scripts/project_health_check.sh
chmod +x scripts/optimize_project.sh
```

### 问题：npm install 失败

```bash
# 清理并重新安装
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 问题：Python 依赖问题

```bash
# macOS
pip3 install --break-system-packages -r requirements.txt

# Linux/Windows
pip3 install -r requirements.txt
```

### 问题：Git hooks 不工作

```bash
# 重新配置 Husky
rm -rf .husky
npm run prepare
```

---

## 📚 更多信息

### 完整文档

- [优化完成报告](./PROJECT_OPTIMIZATION_COMPLETE.md) - 500+ 行详细报告
- [README.md](./README.md) - 项目概览
- [AGENTS.md](./AGENTS.md) - AI 助手规范

### 脚本源码

- [project_health_check.sh](./scripts/project_health_check.sh) - 456 行健康检查
- [optimize_project.sh](./scripts/optimize_project.sh) - 520 行优化脚本

### 配置文件

- [pyproject.toml](./pyproject.toml) - Python 配置
- [package.json](./package.json) - Node.js 配置
- [Makefile](./Makefile) - Make 命令

---

## 💡 小贴士

### 提升开发效率

1. **使用 Makefile**：`make` 命令比 `npm run` 更简洁
2. **配置别名**：在 `~/.zshrc` 或 `~/.bashrc` 添加：
   ```bash
   alias fh='make health'
   alias fo='make optimize'
   alias fm='make maintenance'
   ```
3. **定时任务**：使用 cron 每周自动运行健康检查

### Git Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```bash
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式
refactor: 重构
perf: 性能优化
test: 测试相关
chore: 构建/工具链
```

### 代码审查清单

- [ ] 通过 `make check`
- [ ] 通过 `make test`
- [ ] 通过 `make health` (90%+)
- [ ] Git commit 遵循规范
- [ ] 更新 CHANGELOG.md

---

## 🎓 学习资源

### 官方文档

- [Ruff 文档](https://docs.astral.sh/ruff/) - Python Linter
- [MyPy 文档](https://mypy.readthedocs.io/) - 类型检查
- [ESLint 文档](https://eslint.org/) - JavaScript Linter
- [Prettier 文档](https://prettier.io/) - 代码格式化

### 最佳实践

- [Python 代码规范](https://peps.python.org/pep-0008/)
- [TypeScript 规范](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines)
- [Git 提交规范](https://www.conventionalcommits.org/)

---

## 🆘 需要帮助？

### 问题反馈

1. 查看 [故障排查](#-快速故障排查) 章节
2. 运行 `make health` 获取诊断信息
3. 查看脚本源码了解详细逻辑

### 联系方式

- **团队**: HawaiiHub AI Team
- **文档**: 见项目 `docs/` 目录
- **脚本**: 见项目 `scripts/` 目录

---

<div align="center">

## ⚡ 开始使用优化工具

**一行命令，提升项目质量**

```bash
make maintenance
```

---

**更新时间**: 2025-10-28
**版本**: v2.0.0
**维护**: HawaiiHub AI Team

</div>
