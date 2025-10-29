# 📚 文档索引

> Firecrawl 数据采集器 - 完整文档导航

**最后更新**: 2024-10-29

---

## 📂 目录结构

### 🤖 Cursor AI 集成 🆕

#### Cursor 配置

- [.cursorrules](../.cursorrules) - **Cursor 主规则文件**（自动加载）
- [.cursor/project-config.json](../.cursor/project-config.json) - 项目自定义配置
- [.cursor/README.md](../.cursor/README.md) - .cursor 目录说明
- [.cursor/QUICK_START.md](../.cursor/QUICK_START.md) - **3 分钟快速上手**（⭐ 推荐）
- [.cursor/MIGRATION_REPORT.md](../.cursor/MIGRATION_REPORT.md) - 迁移完成报告
- [.cursor/SETUP_COMPLETE.md](../.cursor/SETUP_COMPLETE.md) - 设置完成指南

#### Prompts 系统

- [.cursor/prompts/](../.cursor/prompts/) - 多角色 Agent 提示词库
  - [README.md](../.cursor/prompts/README.md) - **Prompts 使用指南**（⭐ 必读）
  - [INDEX.md](../.cursor/prompts/INDEX.md) - Prompts 索引
  - [system_prompt.md](../.cursor/prompts/system_prompt.md) - 系统级提示词
  - [orchestrator.md](../.cursor/prompts/orchestrator.md) - 编排器配置
  - [project_config.md](../.cursor/prompts/project_config.md) - 项目配置常量
  - [handoff_format.md](../.cursor/prompts/handoff_format.md) - 统一交接格式
  - [guardrails.md](../.cursor/prompts/guardrails.md) - 质量闸口与失败自愈

#### 角色系统（10 个）

- [.cursor/prompts/roles/](../.cursor/prompts/roles/) - 角色提示词
  - PO (产品负责人), PM (产品经理), BA (需求分析师)
  - PjM (项目经理), Arch (架构师), LLME (LLM 工程师)
  - DEV (开发工程师), QA (测试工程师), Ops (DevOps)
  - TW (技术写手)

#### 工作流（7 个阶段）

- 用户故事 → PRD → 任务分解 → 技术设计 → 实现 → 测试 → 迭代

#### 工具和脚本

- [.cursor/scripts/](../.cursor/scripts/) - 自动化脚本
  - `verify-prompts.sh` - 配置验证脚本
  - `check-roles.sh` - 角色完整性检查
- [.cursor/hooks/](../.cursor/hooks/) - Git Hooks
  - `pre-commit` - 提交前检查
  - `pre-push` - 推送前质量检查

#### Makefile 命令

```bash
make cursor-setup           # 一键设置 Cursor
make verify-cursor-config   # 验证配置
make check-roles           # 检查角色
make cursor-info           # 显示信息
```

---

### 🔧 开发文档

#### API 文档

- [API.md](./API.md) - 完整的 API 接口文档

#### 代码示例

- [examples/](./examples/) - 代码示例目录
  - [basic_usage.py](./examples/basic_usage.py) - 基础使用示例
  - [advanced_usage.py](./examples/advanced_usage.py) - 高级功能示例

#### 官方文档

- [official-docs/](./official-docs/) - Firecrawl 官方文档（约 892 个文件）
  - 完整的 Firecrawl API 使用指南
  - 最佳实践和使用案例
  - **NEW!** [官方示例项目](./official-docs/05-应用案例/examples/) - 3 个官方示例项目
    - [fire-enrich](./official-docs/05-应用案例/examples/fire-enrich/) - AI 数据丰富工具
    - [open-agent-builder](./official-docs/05-应用案例/examples/open-agent-builder/) - 可视化工作流构建器
    - [open-lovable](./official-docs/05-应用案例/examples/open-lovable/) - AI 网站克隆工具

#### 学习资源 🆕

- [learning/](./learning/) - Firecrawl 学习笔记和分析
  - [README.md](./learning/README.md) - **学习指南总览**（⭐ 必读）
  - [fire-enrich-analysis.md](./learning/fire-enrich-analysis.md) - Fire Enrich 深度分析
  - [agent-builder-patterns.md](./learning/agent-builder-patterns.md) - Agent Builder 模式分析
  - [open-lovable-insights.md](./learning/open-lovable-insights.md) - Open Lovable 核心逻辑
  - [firecrawl-best-practices.md](./learning/firecrawl-best-practices.md) - 最佳实践总结

---

### 📊 项目管理

#### 项目信息

- [PROJECT_INDEX.md](./PROJECT_INDEX.md) - 项目索引
- [PROJECT_METADATA.json](./PROJECT_METADATA.json) - 项目元数据

#### 博客案例

- [blog-cases-github-mapping.md](./blog-cases-github-mapping.md) - 博客案例与 GitHub 映射

---

### 🔧 集成指南

#### Vercel 集成

- [integration/vercel-integration.md](./integration/vercel-integration.md) - Vercel 模板集成完整指南

---

### 📈 项目报告

#### 测试报告

- [reports/test_report_toutiao.md](./reports/test_report_toutiao.md) - 今日头条测试报告
- [reports/ai-agent-validation-report.md](./reports/ai-agent-validation-report.md) - AI Agent 验证报告

#### 项目状态

- [reports/FINAL_PROJECT_STATUS.md](./reports/FINAL_PROJECT_STATUS.md) - 最终项目状态
- [reports/project_health_report.json](./reports/project_health_report.json) - 项目健康报告
- [reports/feedback-report-20250921_162041.md](./reports/feedback-report-20250921_162041.md) - 用户反馈报告

#### 代码审查

- [reports/code-review-and-fixes.md](./reports/code-review-and-fixes.md) - 代码审查与修复报告

---

### 🛠️ 维护文档

#### 清理报告

- [maintenance/CLEANUP_REPORT.md](./maintenance/CLEANUP_REPORT.md) - 项目清理报告
- [maintenance/CLEANUP_SUMMARY.md](./maintenance/CLEANUP_SUMMARY.md) - 清理汇总
- [maintenance/ROOT_DIRECTORY_CLEANUP_2024-10-29.md](./maintenance/ROOT_DIRECTORY_CLEANUP_2024-10-29.md) - 根目录清理详细报告
- [maintenance/REMOVE_HUONIAO_N8N_2024-10-29.md](./maintenance/REMOVE_HUONIAO_N8N_2024-10-29.md) - 火鸟门户和 N8N 移除报告

#### 优化计划

- [optimization/continuous-optimization-plan.md](./optimization/continuous-optimization-plan.md) - 持续优化计划

---

### 👥 团队文档

#### 新成员入职

- [team/onboarding/](./team/onboarding/) - 入职指南

#### 团队培训

- [team/training/](./team/training/) - 培训资料

---

## 🗂️ 归档文件

以下目录已压缩为 `.zip` 文件：

- `archive.zip` - 历史归档文档
- `../prompts/archive.zip` - Prompt 归档
- `../tests/archive.zip` - 测试归档
- `../scripts/archive.zip` - 脚本归档

---

## 🔍 快速查找

### 我想

#### 开始使用

1. 阅读 [API.md](./API.md) 了解 API 接口
2. 查看 [examples/basic_usage.py](./examples/basic_usage.py) 学习基础用法
3. **🆕 阅读 [learning/README.md](./learning/README.md) 学习官方示例项目**
4. 参考 [official-docs/](./official-docs/) 深入学习

#### 集成功能

- 前端集成 → [integration/vercel-integration.md](./integration/vercel-integration.md)

#### 查看报告

- 测试报告 → [reports/](./reports/)
- 项目状态 → [reports/FINAL_PROJECT_STATUS.md](./reports/FINAL_PROJECT_STATUS.md)
- 代码审查 → [reports/code-review-and-fixes.md](./reports/code-review-and-fixes.md)

#### 维护项目

- 清理历史 → [maintenance/CLEANUP_SUMMARY.md](./maintenance/CLEANUP_SUMMARY.md)
- 优化计划 → [optimization/continuous-optimization-plan.md](./optimization/continuous-optimization-plan.md)

#### 学习示例项目 🆕

1. **第一阶段（1-2 天）** - 理解 API 使用

   - 阅读 [learning/README.md](./learning/README.md) 总体了解
   - 研究 [fire-enrich](./official-docs/05-应用案例/examples/fire-enrich/) 数据丰富实现

2. **第二阶段（2-3 天）** - 学习 Agent 编排

   - 分析 [open-agent-builder](./official-docs/05-应用案例/examples/open-agent-builder/) 工作流架构
   - 学习 [agent-builder-patterns.md](./learning/agent-builder-patterns.md)

3. **第三阶段（3-5 天）** - 实战开发
   - 应用到我们的 8 个业务场景
   - 参考 [firecrawl-best-practices.md](./learning/firecrawl-best-practices.md)

---

## 📝 文档维护

### 文档更新原则

1. **及时更新** - 代码变更后立即更新相关文档
2. **版本标记** - 重大更新记录版本和日期
3. **清晰结构** - 保持文档层次清晰
4. **示例完整** - 提供可运行的代码示例

### 文档贡献

如需添加或修改文档，请：

1. 遵循现有文档结构
2. 使用清晰的标题和目录
3. 提供实际示例
4. 更新此索引文件

---

**维护者**: AI 全栈工程师团队
**反馈**: 请通过 Issue 提交文档问题
