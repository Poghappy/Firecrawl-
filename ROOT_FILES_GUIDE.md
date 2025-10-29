# 📁 根目录文件说明

本文档说明项目根目录各文件的用途，帮助开发者快速了解项目结构。

## 📋 配置文件

### Python 依赖管理

| 文件                       | 用途         | 何时使用              |
| -------------------------- | ------------ | --------------------- |
| `requirements.txt`         | 生产环境依赖 | 生产部署、Docker 构建 |
| `requirements-dev.txt`     | 开发环境依赖 | 本地开发、测试        |
| `requirements-minimal.txt` | 最小化依赖   | CI/CD、快速测试       |

### Docker 配置

| 文件         | 用途         | 场景                     |
| ------------ | ------------ | ------------------------ |
| `Dockerfile` | 基础镜像构建 | GitHub Actions、开发环境 |

**注意**: 完整的生产环境 Docker 配置在 `config/deployment/` 目录，包括：

- `docker-compose.yml` - 开发环境配置
- `docker-compose.production.yml` - 生产环境配置

### 其他配置

| 文件                      | 用途                |
| ------------------------- | ------------------- |
| `.pre-commit-config.yaml` | Pre-commit 钩子配置 |
| `Makefile`                | 项目命令快捷方式    |
| `.gitignore`              | Git 忽略规则        |

## 📚 文档文件

### 核心文档

| 文件           | 用途               | 读者     |
| -------------- | ------------------ | -------- |
| `README.md`    | 项目说明和快速开始 | 所有人   |
| `CHANGELOG.md` | 版本变更记录       | 所有人   |
| `LICENSE`      | MIT 开源许可证     | 法律合规 |

### 贡献指南

| 文件                 | 用途     | 读者     |
| -------------------- | -------- | -------- |
| `CONTRIBUTING.md`    | 贡献指南 | 贡献者   |
| `CODE_OF_CONDUCT.md` | 行为准则 | 社区成员 |

### 运维文档

| 文件                | 用途         | 读者     |
| ------------------- | ------------ | -------- |
| `DEPLOYMENT.md`     | 部署指南     | 运维人员 |
| `project_status.md` | 项目当前状态 | 团队成员 |

## 🗂️ 目录结构

### 核心目录

| 目录       | 用途       | 说明                   |
| ---------- | ---------- | ---------------------- |
| `src/`     | 核心源代码 | 主要业务逻辑           |
| `tests/`   | 测试文件   | 单元测试、集成测试     |
| `docs/`    | 详细文档   | API 文档、指南、报告   |
| `config/`  | 配置文件   | 部署配置、服务配置     |
| `scripts/` | 管理脚本   | 部署、备份、初始化脚本 |

### 数据和日志

| 目录       | 用途     | Git 状态                |
| ---------- | -------- | ----------------------- |
| `data/`    | 数据存储 | ⚠️ 已忽略（.gitignore） |
| `logs/`    | 日志文件 | ⚠️ 已忽略（.gitignore） |
| `results/` | 测试结果 | 部分忽略                |

### 特殊目录

| 目录             | 用途            | 说明                    |
| ---------------- | --------------- | ----------------------- |
| `.cursor/`       | Cursor AI 配置  | AI 助手规则和模板       |
| `prompts/`       | AI 提示词库     | 团队协作提示词          |
| `templates/`     | 模板文件        | 邮件、文档模板          |
| `firecrawl_env/` | Python 虚拟环境 | ⚠️ 已忽略（.gitignore） |

## 🚀 快速开始

### 新开发者

1. 阅读 `README.md` - 了解项目
2. 查看 `CONTRIBUTING.md` - 贡献规范
3. 运行 `make setup` - 环境设置
4. 查看 `project_status.md` - 当前状态

### 部署人员

1. 阅读 `DEPLOYMENT.md` - 部署指南
2. 选择合适的 `docker-compose.*.yml` - 部署配置
3. 配置环境变量 - 参考 `.env.example`
4. 运行部署脚本 - `scripts/deployment/`

### 贡献者

1. Fork 项目并克隆
2. 创建功能分支
3. 遵循 `CONTRIBUTING.md` 规范
4. 运行 `make dev-loop` - 开发循环

## 🔍 常见问题

### 如何选择 Docker Compose 文件？

- **开发环境**: 使用 `config/deployment/docker-compose.yml`
- **生产环境**: 使用 `config/deployment/docker-compose.production.yml`

### 如何安装依赖？

```bash
# 生产环境
pip install -r requirements.txt

# 开发环境（推荐）
pip install -r requirements.txt -r requirements-dev.txt

# 快速测试
pip install -r requirements-minimal.txt
```

### 根目录为什么有多个 Dockerfile？

- **根目录 `Dockerfile`**: 简化版，用于 GitHub Actions 和快速构建
- **`config/deployment/Dockerfile`**: 完整版，用于生产环境
- **`config/deployment/Dockerfile.production`**: 生产优化版

每个文件有不同的优化策略和用途。

## 📊 文件统计

**根目录文件**: 约 17 个
**配置文件**: 6 个
**文档文件**: 7 个
**Docker 配置**: 1 个
**依赖文件**: 3 个

## 🔗 相关文档

- [项目状态](project_status.md) - 当前进度和计划
- [API 文档](docs/API.md) - 接口说明
- [官方文档](docs/official-docs/) - Firecrawl 官方文档
- [Cursor 配置](.cursor/README.md) - AI 助手配置说明
- [清理报告](docs/maintenance/CLEANUP_REPORT.md) - 项目整理记录

---

**最后更新**: 2024-10-29
**维护者**: AI 全栈工程师团队
**版本**: v2.0.0
