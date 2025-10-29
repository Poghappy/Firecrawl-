# ✅ 项目清理检查清单

**生成日期**: 2025-10-29
**项目**: Firecrawl 数据采集器
**分析工具**: AI 自动分析

---

## 📝 使用说明

- [ ] 阅读完整建议：`docs/maintenance/PROJECT_CLEANUP_RECOMMENDATIONS_2025-10-29.md`
- [ ] 执行清理前创建备份
- [ ] 使用自动化脚本：`./scripts/cleanup-project.sh`
- [ ] 手动勾选已完成的项目

---

## 🔴 高优先级清理（立即执行）

### 虚拟环境
- [ ] 删除 `firecrawl_env/` 目录（150-200 MB）
  - 说明：Python 虚拟环境，不应提交到版本控制

### 空目录
- [ ] 删除 `components/` 目录（空）
  - 说明：空目录，可能是误创建

### 压缩包文件
- [ ] 删除 `docs/archive.zip`
- [ ] 删除 `docs/官方文档.zip`（已解压）
- [ ] 删除 `scripts/archive.zip`
- [ ] 删除 `tests/archive.zip`
- [ ] 删除 `prompts/archive.zip`

### 数据库文件（排除）
- [ ] 从 Git 移除 `data/firecrawl.db`
- [ ] 从 Git 移除 `data/feedback.db`
- [ ] 从 Git 移除 `results/firecrawl_jobs.db`
- [ ] 从 Git 移除 `results/archive/test_firecrawl.db`
  - 说明：本地保留，但不提交到版本控制

---

## 🟡 中优先级清理（建议执行）

### AI 提示词系统
- [ ] 删除 `prompts/` 目录及所有内容（20+ 文件）
  - [ ] `prompts/README.md`
  - [ ] `prompts/system_prompt.md`
  - [ ] `prompts/orchestrator.md`
  - [ ] `prompts/guardrails.md`
  - [ ] `prompts/handoff_format.md`
  - [ ] `prompts/project_config.md`
  - [ ] `prompts/00_guidelines.md`
  - [ ] `prompts/10_user_story.md`
  - [ ] `prompts/20_prd.md`
  - [ ] `prompts/30_task_breakdown.md`
  - [ ] `prompts/40_tech_design.md`
  - [ ] `prompts/50_impl.md`
  - [ ] `prompts/60_test.md`
  - [ ] `prompts/70_iteration.md`
  - [ ] `prompts/roles/` 目录（10 个文件）
  - [ ] `prompts/stages/` 目录（2 个文件）
  - 说明：已配置在 `.cursorrules`，无需保留副本

### 官方示例代码
- [ ] 删除 `docs/official-docs/05-应用案例/firecrawl-app-examples-main/` 目录（800+ 文件，50-100 MB）
  - 说明：第三方示例代码，应通过官方仓库查看

### 博客教程文档
- [ ] 移动 `docs/official-docs/02_Kimi_K2旅行应用构建教程.md` → `docs/blog/`
- [ ] 移动 `docs/official-docs/03_2025年最佳AI代理开源框架.md` → `docs/blog/`
- [ ] 移动 `docs/official-docs/04_Engage_Together反人口贩卖资源映射案例.md` → `docs/blog/`
- [ ] 移动 `docs/official-docs/05_Grok4医疗AI应用构建教程.md` → `docs/blog/`
- [ ] 移动 `docs/official-docs/06_网络爬虫工具Top10指南.md` → `docs/blog/`
  - 说明：营销教程，非技术文档

### GitHub Actions 脚本
- [ ] 归档 `scripts/github-actions/` 目录（7 个文件）
  - [ ] `scripts/github-actions/check-github-actions.sh`
  - [ ] `scripts/github-actions/fix-github-actions-complete.sh`
  - [ ] `scripts/github-actions/fix-github-actions.py`
  - [ ] `scripts/github-actions/fix-github-actions.sh`
  - [ ] `scripts/github-actions/github-init.sh`
  - [ ] `scripts/github-actions/verify-github-config.py`
  - [ ] `scripts/github-actions/verify-github-secrets.py`
  - 目标：`scripts/archive/github-actions/`
  - 说明：一次性设置脚本，已完成

### 文档整理元文档
- [ ] 移动 `docs/official-docs/APPROVE_Firecrawl文档整理.md` → `docs/maintenance/`
- [ ] 移动 `docs/official-docs/DESIGN_Firecrawl文档整理.md` → `docs/maintenance/`
- [ ] 移动 `docs/official-docs/REQUIREMENTS_Firecrawl文档整理.md` → `docs/maintenance/`
- [ ] 移动 `docs/official-docs/TASK_Firecrawl文档整理.md` → `docs/maintenance/`
  - 说明：项目管理文档，不属于 API 文档

---

## 🟢 低优先级清理（可选执行）

### 重复配置文件
- [ ] 删除 `results/config_example.json`
- [ ] 删除 `results/config.json`
- [ ] 删除 `results/test_config.json`
  - 说明：配置文件应在 `config/` 目录

### 过时报告文件
- [ ] 归档 `docs/reports/feedback-report-20250921_162041.md` → `docs/reports/archive/`
- [ ] 归档 `docs/reports/test_report_toutiao.md` → `docs/reports/archive/`
  - 说明：过时的测试报告

### 过时项目文档
- [ ] 检查 `docs/PROJECT_BRIEF.md` 是否已合并到 `project_status.md`
- [ ] 检查 `docs/PROJECT_INDEX.md` 是否已合并到 `project_status.md`
- [ ] 检查 `docs/PROJECT_METADATA.json` 是否仍需要
  - 说明：可能存在信息重复

### JSON 报告文件
- [ ] 添加到 `.gitignore`: `results/*.json`
- [ ] 添加到 `.gitignore`: `docs/reports/*.json`
  - 说明：运行时生成，不需提交

### Archive 子目录
- [ ] 检查 `results/archive/` 是否仍需要
- [ ] 检查 `results/archive/backup/` 是否仍需要
  - 说明：如不需要可删除

---

## 📊 清理统计

### 预估效果
- **文件数量**: 删除约 840+ 个文件
- **磁盘空间**: 节省约 226-362 MB
- **目录清理**: 简化 5+ 个主要目录

### 分类统计
| 类别 | 文件数 | 大小 | 优先级 |
|-----|-------|------|--------|
| 虚拟环境 | 1 目录 | 150-200 MB | 🔴 |
| 示例代码 | 800+ | 50-100 MB | 🟡 |
| 压缩包 | 5 | 20-50 MB | 🔴 |
| 提示词 | 20+ | 1-2 MB | 🟡 |
| 其他 | 15+ | 5-10 MB | 🟢 |

---

## ⚙️ 执行方式

### 自动化清理（推荐）
```bash
# 使用清理脚本
./scripts/cleanup-project.sh

# 脚本会自动创建备份并执行清理
```

### 手动清理
```bash
# 1. 高优先级
rm -rf firecrawl_env/
rmdir components/
rm docs/archive.zip docs/官方文档.zip scripts/archive.zip tests/archive.zip prompts/archive.zip
git rm --cached data/*.db results/*.db results/archive/*.db

# 2. 中优先级
rm -rf prompts/
rm -rf docs/official-docs/05-应用案例/firecrawl-app-examples-main/
mkdir -p docs/blog
mv docs/official-docs/0[2-6]_*.md docs/blog/

# 3. 低优先级
rm results/config*.json results/test_config.json
mkdir -p docs/reports/archive
mv docs/reports/feedback-report-*.md docs/reports/test_report_toutiao.md docs/reports/archive/
```

---

## ✅ 验证清单

清理完成后，请验证：

### 功能验证
- [ ] 虚拟环境可重新创建: `python3 -m venv venv`
- [ ] 依赖可正常安装: `pip install -r requirements.txt`
- [ ] 测试可正常运行: `pytest tests/`
- [ ] API 服务可正常启动: `python src/api_server.py`
- [ ] Docker 镜像可正常构建: `docker build -t firecrawl .`

### 文档验证
- [ ] README.md 链接正常
- [ ] 文档结构清晰
- [ ] 无死链接
- [ ] 无重复内容

### Git 验证
- [ ] .gitignore 规则正确
- [ ] 无敏感文件提交
- [ ] 提交历史清晰
- [ ] 文件体积合理

---

## 📝 完成后操作

- [ ] 更新 `CHANGELOG.md`
- [ ] 更新 `project_status.md`
- [ ] 提交 Git commit
  ```bash
  git add .
  git commit -m "chore: 清理项目无关文件和冗余代码"
  ```
- [ ] 确认无误后删除备份文件

---

## 📞 相关文档

- 📄 **完整建议**: `docs/maintenance/PROJECT_CLEANUP_RECOMMENDATIONS_2025-10-29.md`
- 📄 **快速指南**: `CLEANUP_GUIDE_QUICK.md`
- 📄 **清理脚本**: `scripts/cleanup-project.sh`
- 📄 **项目状态**: `project_status.md`

---

**最后更新**: 2025-10-29
**维护者**: AI Assistant
**状态**: 待执行
