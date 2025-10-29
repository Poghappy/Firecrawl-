# Firecrawl 数据采集器 - Cursor AI Prompts 系统

## 📋 系统概述

完整的多角色 Agent 系统提示词包，专为 Firecrawl 数据采集器项目设计。

**版本**: v2.0.0
**最后更新**: 2025-10-29

## 🎯 核心特性

- ✅ **10 个专业角色**: PO/PM/BA/PjM/Arch/LLME/DEV/QA/Ops/TW
- ✅ **完整工作流**: 用户故事 → PRD → 任务分解 → 技术方案 → 实现 → 测试 → 迭代/发布
- ✅ **统一交接格式**: JSON 格式确保信息传递完整性
- ✅ **质量闸口**: 严格的质量控制和失败自愈流程
- ✅ **项目特定优化**: 针对 Firecrawl 数据采集器定制

## 📁 文件结构

```
.cursor/prompts/
├── README.md                    # 本文件
├── INDEX.md                     # 提示词索引
├── system_prompt.md             # 系统级提示词
├── orchestrator.md              # 编排器配置
├── project_config.md            # 项目配置常量
├── handoff_format.md            # 统一交接格式
├── guardrails.md                # 质量闸口与失败自愈
│
├── roles/                       # 角色系统提示词
│   ├── 01_product_owner.md
│   ├── 02_product_manager.md
│   ├── 03_business_analyst.md
│   ├── 05_architect.md
│   ├── 06_llm_engineer.md
│   ├── 07_developer.md
│   ├── 08_qa_engineer.md
│   ├── 09_devops.md
│   └── 10_technical_writer.md
│
├── stages/                      # 阶段提示词
│   ├── 01_user_stories.md
│   └── 02_prd.md
│
└── workflows/                   # 工作流定义
    ├── 10_user_story.md
    ├── 20_prd.md
    ├── 30_task_breakdown.md
    ├── 40_tech_design.md
    ├── 50_impl.md
    ├── 60_test.md
    └── 70_iteration.md
```

## 🚀 快速开始

### 1. 系统已自动配置

Prompts 系统已通过以下方式激活：

- ✅ **主规则文件**: `/.cursorrules` （Cursor 自动加载）
- ✅ **环境配置**: `/.cursor/environment.json`
- ✅ **提示词库**: `/.cursor/prompts/*`
- ✅ **工具脚本**: `/.cursor/scripts/*`

### 2. 验证配置

运行验证脚本检查配置：

```bash
# 验证配置完整性
./.cursor/scripts/verify-prompts.sh

# 或使用 make 命令
make verify-cursor-config
```

### 3. 使用方式

#### 方式 A: 自动模式（推荐）

直接在 Cursor 中开始对话，系统会自动：

1. 检查项目状态
2. 按顺序触发各角色
3. 使用统一交接格式
4. 执行质量闸口检查

#### 方式 B: 手动指定角色

在对话中明确指定角色：

```
@PO 请帮我明确这个功能的业务目标
@Arch 请设计这个模块的技术架构
@DEV 请实现这个功能
```

#### 方式 C: 工作流模式

使用阶段命令：

```
/user-story    # 启动用户故事阶段
/prd          # 启动 PRD 阶段
/tech-design  # 启动技术设计阶段
/implement    # 启动实现阶段
/test         # 启动测试阶段
```

## 👥 角色说明

| 角色     | 职责          | 输出文档                |
| -------- | ------------- | ----------------------- |
| **PO**   | 产品负责人    | PROJECT_BRIEF.md        |
| **PM**   | 产品经理      | USER_STORIES.md, PRD.md |
| **BA**   | 需求分析师    | 详细需求文档、接口规范  |
| **PjM**  | 项目经理      | TASKS.md、项目计划      |
| **Arch** | 架构师        | TECH_DESIGN.md、架构图  |
| **LLME** | LLM 工程师    | 提示词模板、AI 系统设计 |
| **DEV**  | 开发工程师    | 源代码、测试用例        |
| **QA**   | 测试工程师    | 测试计划、测试报告      |
| **Ops**  | DevOps 工程师 | 部署脚本、监控配置      |
| **TW**   | 技术写手      | 用户手册、API 文档      |

## 🔄 标准工作流程

### 阶段 1: 需求分析

```
PO → PM → BA
```

1. PO 明确业务目标和边界
2. PM 创建用户故事和 PRD
3. BA 分析技术需求

### 阶段 2: 设计规划

```
PjM → Arch → LLME
```

4. PjM 分解任务和制定计划
5. Arch 设计系统架构
6. LLME 设计 AI 功能集成

### 阶段 3: 开发实现

```
DEV → QA → Ops
```

7. DEV 实现功能代码
8. QA 执行测试验证
9. Ops 部署和运维

### 阶段 4: 文档交付

```
TW → Orchestrator
```

10. TW 编写完整文档
11. Orchestrator 项目总结

## 📊 质量保证

### 输出四件套（每次改动必须包含）

1. **变更计划摘要**

   ```
   本次改动要做什么，为什么要做
   ```

2. **影响面分析**

   ```
   - 接口影响: 列出所有受影响的接口
   - 依赖影响: 列出依赖关系变化
   - 风险评估: 识别潜在风险
   ```

3. **文件树 Diff**

   ```
   新增:
     + src/new_module.py
     + tests/test_new_module.py

   修改:
     M src/existing.py
     M docs/API.md

   删除:
     - src/deprecated.py
   ```

4. **DoD 检查清单**

   ```
   - [ ] 代码通过 lint 检查
   - [ ] 单元测试通过
   - [ ] 集成测试通过
   - [ ] 文档已更新
   - [ ] 代码已审查
   ```

### 质量闸口

✅ **代码质量**: `make lint` 必须通过
✅ **测试覆盖**: `make test` 必须通过，覆盖率 ≥ 80%
✅ **API 性能**: 响应时间 < 500ms
✅ **安全检查**: 无高危漏洞
✅ **文档完整**: API 文档、用户文档齐全

## 🛠️ 自定义配置

### 修改项目常量

编辑 `project_config.md`:

```yaml
PROJECT_NAME: 你的项目名称
MAX_FILES: 单回合最大文件数
MAX_LINES: 单文件最大行数
# ... 其他配置
```

### 添加新角色

1. 在 `roles/` 创建新角色文件
2. 按现有格式编写角色提示词
3. 更新 `INDEX.md` 角色列表
4. 更新工作流程说明

### 调整质量闸口

编辑 `guardrails.md`:

- 添加新的质量要求
- 更新检查清单
- 定义新的失败处理流程

## 🔧 工具和脚本

### 验证脚本

```bash
# 验证 Prompts 配置
.cursor/scripts/verify-prompts.sh

# 验证角色完整性
.cursor/scripts/check-roles.sh

# 生成角色文档
.cursor/scripts/generate-docs.sh
```

### Git Hooks

```bash
# Pre-commit hook（自动验证）
.cursor/hooks/pre-commit

# Pre-push hook（质量检查）
.cursor/hooks/pre-push
```

### Make 命令

```bash
# 验证配置
make verify-cursor-config

# 运行质量检查
make quality-check

# 生成文档
make generate-docs
```

## 📈 最佳实践

### 1. 角色协作

- ✅ 确保每个角色有明确的输入输出
- ✅ 使用统一的交接格式
- ✅ 及时反馈和调整

### 2. 质量控制

- ✅ 严格执行质量闸口
- ✅ 及时处理失败情况
- ✅ 持续改进流程

### 3. 文档管理

- ✅ 保持文档同步更新
- ✅ 使用版本控制
- ✅ 定期审查和优化

## 🐛 故障排除

### 常见问题

**Q: 角色交接失败怎么办？**
A: 检查交接格式是否正确，确保所有必填字段完整。

**Q: 质量闸口不通过怎么办？**
A: 按照失败自愈流程：定位问题 → 最小化修复 → 复测验证。

**Q: 如何添加项目特定需求？**
A: 编辑 `project_config.md` 和相关角色提示词。

**Q: Cursor 没有识别规则怎么办？**
A: 重启 Cursor 或运行验证脚本检查配置。

## 📚 相关资源

- [Cursor 官方文档](https://cursor.com/docs)
- [项目配置说明](./project_config.md)
- [质量闸口规范](./guardrails.md)
- [角色系统文档](./roles/)
- [工作流定义](./workflows/)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 运行验证脚本
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE) 文件

---

**维护者**: AI 全栈工程师团队
**技术支持**: [GitHub Issues](https://github.com/firecrawl/firecrawl-agent/issues)
**文档更新**: 2025-10-29
