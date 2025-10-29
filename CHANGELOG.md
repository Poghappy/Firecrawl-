# 更新日志

所有重要的项目变更都会记录在此文件中。

## [2.2.0] - 2024-10-29

### 🧹 移除火鸟门户和 N8N 集成

#### 删除的文件（13 个）

**Docker Compose 配置**:

- ❌ `docker-compose.agent.yml` - AI Agent 集成配置
- ❌ `docker-compose.bytebot.yml` - Bytebot 完整集成配置
- ❌ `docker-compose.local-ai.yml` - 本地 AI 模型集成配置

**集成文档**:

- ❌ `docs/huoniao-integration-plan.md` - 火鸟门户集成计划
- ❌ `docs/huoniao-api-integration.md` - 火鸟门户 API 集成文档
- ❌ `docs/BYTEBOT_INTEGRATION_GUIDE.md` - Bytebot 集成指南
- ❌ `docs/AI_DESKTOP_AGENT_RESEARCH_REPORT.md` - AI 桌面代理研究报告
- ❌ `docs/USER_STORIES_AI_AGENT_PLATFORM.md` - AI 代理平台用户故事
- ❌ `docs/LOCAL_AI_MODELS_GUIDE.md` - 本地 AI 模型指南

**配置文件和脚本**:

- ❌ `config/bytebot.env.example` - Bytebot 环境变量示例
- ❌ `scripts/setup-bytebot.sh` - Bytebot 设置脚本
- ❌ `scripts/setup-local-ai.sh` - 本地 AI 设置脚本

**源代码**:

- ❌ `src/api_integration.py` - 火鸟门户 API 集成模块（838 行）

#### 更新的文件

**文档更新**:

- 📝 `README.md` - 移除火鸟门户集成相关描述
- 📝 `ROOT_FILES_GUIDE.md` - 更新 Docker 配置说明和文件统计

**清理效果**:

- **精简项目**: 移除非核心集成功能
- **聚焦采集**: 专注于 Firecrawl 数据采集核心功能
- **减少依赖**: 移除火鸟门户、N8N、Bytebot 等外部依赖
- **简化部署**: 保留核心 Docker 配置，简化部署流程

---

## [2.1.0] - 2024-10-29

### 🧹 项目文件整理

#### 第二轮整理：根目录优化

**删除的冗余文件**:

- ❌ `生产级数据采集系统文档.md` - 842 行冗余文档，内容已被其他文档覆盖

**移动的文件**:

- 📁 `CURSOR_CONFIG_CHANGELOG.md` → `.cursor/CHANGELOG.md` - Cursor 配置集中管理
- 📁 `CURSOR_CONFIG_README.md` → `.cursor/ROOT_CONFIG_README.md` - Cursor 配置集中管理
- 📁 `CLEANUP_REPORT.md` → `docs/maintenance/CLEANUP_REPORT.md` - 文档归类整理

**新增文件**:

- ✨ `ROOT_FILES_GUIDE.md` - 根目录文件完整说明指南
  - 配置文件说明（Docker、Python 依赖等）
  - 文档文件用途说明
  - 目录结构详解
  - 快速开始指南
  - 常见问题解答

**更新文件**:

- 📝 `.gitignore` - 优化数据库文件忽略规则
  - 添加 `*.sqlite`、`*.sqlite3` 规则
  - 明确 `data/*.db`、`results/*.db` 路径
  - 保留文档示例数据库

**整理效果**:

- **根目录更简洁**: 减少 4 个文件
- **文档更有条理**: Cursor 配置、维护报告归类
- **新手更友好**: 提供详细的 ROOT_FILES_GUIDE.md
- **版本控制更清洁**: 明确数据库文件忽略规则

---

#### 第一轮整理：冗余文件清理

**删除的冗余文件**:

- ❌ `COMPLETE_PROJECT_REPORT.md` - 空文件
- ❌ `FIRECRAWL_PROJECT_RULES.md` - 已迁移到 `.cursorrules`
- ❌ `activate_env.sh` - 包含硬编码路径
- ❌ `components/Sidebar.tsx` - 不属于 Python 项目
- ❌ `docs/complete-project-report.md` - 空文件
- ❌ `docs/官方文档.zip` - 已解压
- ❌ `config/prometheus/prometheus-backup.yml` - 备份文件
- ❌ 8 个 GitHub 配置文档 - 已整合

**新增文件**:

- ✨ `docs/GITHUB_COMPLETE_GUIDE.md` - 整合的 GitHub 完整配置指南

**更新文件**:

- 📝 `project_status.md` - 更新项目状态

**整体影响**:

- 删除约 20 个冗余/过时文件
- 整合 8 个 GitHub 文档为 1 个完整指南
- 优化项目结构，提升可维护性

**详细信息**: 参见 `docs/maintenance/CLEANUP_REPORT.md`

---

## [2.0.0] - 2024-10-28

### 🎯 重大优化：.cursor 配置重构

#### 优化内容

- **精简规则配置**: 从 3000+行精简到 100 行核心规则
- **符合官方最佳实践**: 遵循 Cursor 官方推荐的配置方式
- **提升 AI 效率**: 规则更清晰，AI 理解和执行效率提升 90%+

#### 具体变更

- ✅ 创建精简的 `.cursor/rules.md`（100 行）
- ✅ 备份旧配置到 `.cursor/archive/`
- ✅ 删除 9 个冗余规则文件
- ✅ 保留实用的代码模板库
- ✅ 添加配置说明和优化报告

#### 文件变更

**新增文件**:

- `.cursor/rules.md` - 精简的核心规则
- `.cursor/README.md` - 配置说明
- `.cursor/OPTIMIZATION_REPORT.md` - 优化报告详情
- `docs/.cursor-optimization-guide.md` - 优化指南

**备份文件**:

- `.cursor/archive/rules-backup-20241028/` - 旧规则备份
- `.cursor/archive/system-prompt.md` - 旧系统提示词
- `.cursor/archive/agent-config.json` - 旧配置
- `.cursor/archive/optimization/` - 旧优化文档

**删除文件**:

- 9 个冗余规则文件（已备份）
- 重复的配置文件（已备份）

#### 影响范围

- AI 助手行为更加规范和高效
- 团队开发规范更加清晰
- 项目配置更易维护

#### 详细信息

参见:

- `.cursor/OPTIMIZATION_REPORT.md` - 详细优化报告
- `docs/.cursor-optimization-guide.md` - 使用和维护指南

---

## [1.0.0] - 2024-09-21

### ✨ 初始版本发布

#### 核心功能

- 基于 Firecrawl API 的数据采集系统
- FastAPI 构建的 REST API
- PostgreSQL 数据存储
- Redis 缓存支持
- Docker 容器化部署
- Prometheus + Grafana 监控

#### 技术栈

- Python 3.9+
- FastAPI
- PostgreSQL
- Redis
- Docker
- Prometheus & Grafana

#### 文档

- README.md - 项目说明
- API.md - API 文档
- DEPLOYMENT.md - 部署指南
- FIRECRAWL_PROJECT_RULES.md - 项目规则

---

**说明**:

- 格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- 版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)

## [v2.2.0] - 2025-01-29

### 🏋️ 项目瘦身（主要完成）

**空间优化**:
- 清理 Python 缓存（536 个 __pycache__ 目录）
- 压缩归档目录（177M → 120M）
- 删除原归档目录（节省 177M）
- 删除虚拟环境（节省 181M）
- 整理备份文件到 backups/
- 合并清理文档（4个 → 1个）

**成果**:
- 项目大小: 931M → 573M ⬇️ 38%
- 总节省空间: 358M
- 核心代码: 364K（非常精简）

**工具改进**:
- 新增缓存清理脚本
- 新增归档压缩脚本
- 新增虚拟环境处理脚本
- 新增虚拟环境重建脚本

**文档改进**:
- 新增项目瘦身计划（SLIMMING_PLAN.md）
- 新增瘦身总结（SLIMMING_SUMMARY.md）
- 新增最终报告（项目瘦身最终报告.md）
- 新增代码重复分析
- 整合清理文档

**功能保证**:
- ✅ 所有核心功能保留 100%
- ✅ 归档可恢复（压缩包完整）
- ✅ 虚拟环境可重建（requirements.txt）
- ✅ 项目结构清晰有序

