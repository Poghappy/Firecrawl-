# 🚀 AI 编程工作流程最佳实践研究报告

## 📋 目录

1. [核心方法论](#核心方法论)
2. [推荐工具与平台](#推荐工具与平台)
3. [GitHub 优秀项目](#github-优秀项目)
4. [PRD 规范与模板](#prd-规范与模板)
5. [ChatGPT GPTs 创建指南](#chatgpt-gpts-创建指南)
6. [Cursor Agent 最佳实践](#cursor-agent-最佳实践)
7. [实施建议](#实施建议)

---

## 🎯 核心方法论

### 1. **PRP (Product Requirement Prompt) 方法论** ⭐⭐⭐⭐⭐

**来源**: [Wirasm/PRPs-agentic-eng](https://github.com/Wirasm/PRPs-agentic-eng) (1.7k⭐)

**核心理念**:

- **PRP = PRD + 代码库智能 + Agent 运行手册**
- 为 AI 提供"一次性实现成功"所需的最小可行信息包
- 结构化提示方法，2024 年夏季首次建立

**四大组成部分**:

```markdown
1. Goal（目标）
   - 明确要构建什么

2. Why（原因）
   - 商业价值和用户影响

3. Context（上下文）⭐ 关键差异点
   - 精确的文件路径和内容
   - 库版本和库上下文
   - 代码片段示例
   - 已知陷阱（Gotchas）

4. Implementation Blueprint（实施蓝图）
   - 任务和伪代码
   - 验证循环（Validation Loop）
```

**验证循环三层结构**:

```bash
# Level 1: 语法和风格
ruff check src/ --fix
mypy src/

# Level 2: 单元测试
uv run pytest tests/test_auth.py -v

# Level 3: 集成测试
curl -X POST http://localhost:8000/auth/login
```

**配置文件**:

- `.claude/commands/` - 12 个预配置命令
- `CLAUDE.md` - 项目特定指南
- `PRPs/templates/` - PRP 模板
- `PRPs/ai_docs/` - 库文档

**最佳实践**:

1. ✅ **上下文为王**: 包含所有必要的文档、示例和注意事项
2. ✅ **验证循环**: 提供可执行的测试/检查，AI 可以运行和修复
3. ✅ **信息密集**: 使用来自代码库的关键词和模式
4. ✅ **渐进式成功**: 从简单开始，验证，然后增强

---

### 2. **Vibe Coding 工作流** ⭐⭐⭐⭐

**来源**: [KhazP/vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template) (78⭐)

**四阶段流程**:

| 阶段           | 目标                 | 时间       | 输出              |
| -------------- | -------------------- | ---------- | ----------------- |
| 1️⃣ Research    | 验证市场和技术可行性 | 20-30 分钟 | `research-*.txt`  |
| 2️⃣ PRD         | 定义产品范围         | 15-20 分钟 | `PRD-*.md`        |
| 3️⃣ Tech Design | 决定技术栈           | 15-20 分钟 | `TechDesign-*.md` |
| 4️⃣ Build       | 生成和测试代码       | 1-3 小时   | 可工作的 MVP      |

**2025 年最新推荐工具**:

**免费选项**:

- [AI Studio](https://aistudio.google.com/) - Gemini 2.5 Pro (1M token 上下文)
- [Claude.ai](https://claude.ai/) - Claude 4 Sonnet
- [ChatGPT](https://chat.openai.com/) - GPT-5

**编码代理**:

- **Terminal**: Claude Code, Gemini CLI, OpenAI Codex CLI
- **Async/Cloud**: Jules by Google, GitHub Copilot Agent
- **IDE**: Cursor ($20/月), VS Code + Copilot ($10/月)
- **No-Code**: Bolt.new, Lovable, v0 by Vercel

**成功指标**:

- 使用此工作流构建的 MVP 超过**10,000 个**
- 平均 MVP 时间：**4 小时**（传统方式需 4 周）
- 成功率：**87%**达到部署

---

### 3. **Gear Heart Methodology (GHM)** ⭐⭐⭐⭐

**来源**: [mattgierhart/PRD-driven-context-engineering](https://github.com/mattgierhart/PRD-driven-context-engineering)

**核心原则**:

1. **三文件纪律**:
   - Command Center（指挥中心） - 单一操作真相
   - PRD - 产品需求文档
   - 当前 EPIC - 史诗任务

2. **3+3 模式**:
   - 当某部分增长时，提取专注文档（如技术架构）
   - 在 Command Center 保留简洁摘要

3. **门控执行** (Gate-Based Execution):
   - 质量门控
   - 安全门控
   - 性能门控
   - 业务规则门控

4. **上下文治理**:
   - 明确权限层级
   - 可预测路径
   - 归档历史
   - 零"神秘文件"

**测试方法**:

- **单元测试**: 逻辑边界快速检查
- **集成测试**: 系统接缝验证（auth、数据访问、工作流）
- **E2E 测试**: 最高价值流程的用户旅程验证
- **Golden Datasets**: AI 和确定性检查的策展真实数据
- **性能基准**: 与目标对齐，PR 时运行

---

### 4. **结构化 AI 工作流** ⭐⭐⭐

**来源**: [jasonleinart/structured-ai-workflows](https://github.com/jasonleinart/structured-ai-workflows)

**五步骤流程**:

```markdown
1. 创建 PRD
   使用 @create-prd.md

2. 生成任务列表
   使用 @generate-tasks.md

3. 检查任务列表
   审查生成的任务和子任务

4. 逐任务执行
   使用 @process-task-list.md
   每次只处理一个任务

5. 审查、批准、推进
   审查更改 → 批准 → 继续下一个
```

**Cursor 配置**:

- 使用 `@` 引用文件（如 `@create-prd.md`）
- MAX 模式推荐用于复杂 PRD
- 逐步验证确保质量

**Claude Code 配置**:

```bash
# 1. 复制文件到项目
/ai-dev-tasks/create-prd.md
/ai-dev-tasks/generate-tasks.md
/ai-dev-tasks/process-task-list.md

# 2. 在CLAUDE.md中引用
# 3. 创建自定义命令（可选）
.claude/commands/create-prd.md
.claude/commands/generate-tasks.md
.claude/commands/process-task-list.md
```

---

## 🛠️ 推荐工具与平台

### AI 模型（2025 更新）

| 模型                | 特点                | 最佳用途         |
| ------------------- | ------------------- | ---------------- |
| **Claude 4 Sonnet** | SWE-bench 72.7%评分 | 编码任务         |
| **Gemini 2.5 Pro**  | 1M token 上下文     | 研究和大型代码库 |
| **GPT-5**           | 速度和成本效率提升  | 通用任务         |
| **Claude 4.1 Opus** | 大型代码库处理更好  | 企业级项目       |

### 编码代理

**Terminal-Based** (高级用户):

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code
claude init

# Gemini CLI
npx https://github.com/google-gemini/gemini-cli
```

**IDE-Based** (友好界面):

- **Cursor** - 最强大 ($20/月)
- **Windsurf** - Cascade AI，深度代码库理解
- **VS Code + Copilot** - 初学者最佳 ($10/月)

**No-Code 平台** (最简单):

- **Bolt.new** - 即时 Web 应用 ($20/月 pro)
- **Lovable** - AI 全栈工程师 ($25/月)
- **v0 by Vercel** - UI 组件生成器

### 工作流工具

| 工具               | 用途         | 价格              |
| ------------------ | ------------ | ----------------- |
| **Linear**         | 问题追踪     | 免费起            |
| **Notion**         | 文档和知识库 | 免费起            |
| **GitHub Actions** | CI/CD        | 免费 2000 分钟/月 |
| **Vercel**         | 前端部署     | 免费层可用        |
| **Railway**        | 后端容器     | $5 起/月          |

---

## 📦 GitHub 优秀项目精选

### 1. **PRPs-agentic-eng** ⭐⭐⭐⭐⭐

- **链接**: <https://github.com/Wirasm/PRPs-agentic-eng>
- **星标**: 1.7k
- **特点**:
  - 完整的 PRP 方法论
  - 12 个预配置 Claude 命令
  - Python 脚本自动化
  - 视频教程：<https://www.youtube.com/watch?v=KVOZ9s1S9Gk>

### 2. **vibe-coding-prompt-template** ⭐⭐⭐⭐

- **链接**: <https://github.com/KhazP/vibe-coding-prompt-template>
- **星标**: 78
- **特点**:
  - 4 阶段 MVP 开发
  - 支持多种 AI 工具
  - 详细的工具选择指南
  - 平均 4 小时完成 MVP

### 3. **PRD-driven-context-engineering** ⭐⭐⭐⭐

- **链接**: <https://github.com/mattgierhart/PRD-driven-context-engineering>
- **星标**: 3（较新）
- **特点**:
  - Gear Heart Methodology
  - 完整模板库
  - 安全和秘密管理
  - MCP 集成（可选）

### 4. **structured-ai-workflows** ⭐⭐⭐

- **链接**: <https://github.com/jasonleinart/structured-ai-workflows>
- **星标**: Fork 自 snarktank/ai-dev-tasks
- **特点**:
  - 跨工具支持（Cursor/Claude Code）
  - 分步验证
  - 自定义命令支持
  - 视频演示

### 5. **cursor-vibe-coding-template** ⭐⭐⭐

- **链接**: <https://github.com/jpke/cursor-vibe-coding-template>
- **特点**:
  - 预配置 AI 工具
  - MCP 服务器
  - 智能开发工作流

---

## 📝 PRD 规范与模板

### Atlassian 敏捷 PRD 原则

**来源**: <https://www.atlassian.com/agile/product-management/requirements>

**精益敏捷 PRD 核心**:

1. **聚焦价值** - 不是功能列表
2. **协作创建** - 多方参与
3. **迭代更新** - 持续演进
4. **可测试标准** - 明确验收条件

### PRD 模板结构（推荐）

```markdown
# [功能名称] - 产品需求文档

## 1. 目标 (Goal)

- 一句话描述要构建什么

## 2. 原因 (Why)

- 商业价值
- 用户影响
- 成功指标

## 3. 内容 (What)

### 成功标准

- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

### 核心功能（3-5 个）

- 功能 1: 描述
- 功能 2: 描述

## 4. 上下文 (All Needed Context)

### 文档和参考

- url: [链接]
  why: 原因

- file: src/path/to/file.py
  why: 当前模式待替换

### 已知陷阱

# CRITICAL: 关键注意事项 1

# CRITICAL: 关键注意事项 2

## 5. 实施蓝图 (Implementation Blueprint)

[详细实施计划]

## 6. 验证循环 (Validation Loop)

### Level 1: 语法和风格

[命令]

### Level 2: 单元测试

[命令]

### Level 3: 集成测试

[命令]
```

### AI PRD 生成工具（2025）

| 工具              | 特点            | 价格        |
| ----------------- | --------------- | ----------- |
| **Craft.io**      | AI 驱动产品管理 | 付费        |
| **Aha!**          | 路线图和需求    | 付费        |
| **Notion AI**     | 内置 AI 助手    | $10/用户/月 |
| **Claude + 模板** | 完全可定制      | 模型费用    |

---

## 🤖 ChatGPT GPTs 创建指南

### 最佳实践（OpenAI 官方）

**来源**: <https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt>

**核心原则**:

1. **清晰具体**

   ```text
   ❌ 坏: "帮我写点代码"
   ✅ 好: "用Python写一个函数，接收用户列表，返回去重后按姓名排序的列表"
   ```

2. **提供上下文**

   ```markdown
   - 目标用户是谁
   - 预期输出格式
   - 约束条件
   - 示例输入/输出
   ```

3. **角色设定**

   ```markdown
   "Act as a senior Python developer specializing in FastAPI..."
   ```

4. **分步指导**

   ```markdown
   Step 1: 分析需求
   Step 2: 设计架构
   Step 3: 实现代码
   Step 4: 测试验证
   ```

### Custom GPT 构建指南（2025）

**Reddit 社区推荐**: <https://www.reddit.com/r/ChatGPTPromptGenius/>

**六步构建流程**:

1. **定义明确用例**
   - 不要构建"通用助手"
   - 聚焦特定问题

2. **编写智能指令**

   ```markdown
   # 角色

   You are an expert [role]

   # 任务

   Your job is to [specific task]

   # 约束

   - Always [constraint 1]
   - Never [constraint 2]

   # 输出格式

   [Specific format]
   ```

3. **知识文档**
   - 上传相关文档（最多 20 个文件）
   - 每个文件最大 512MB
   - 支持 PDF、TXT、MD

4. **Actions（可选）**
   - 连接外部 API
   - OpenAPI 规范
   - 身份验证

5. **测试迭代**
   - 用真实场景测试
   - 收集反馈
   - 持续改进

6. **发布和分享**
   - 私有/仅我
   - 链接分享
   - 公开发布（GPT Store）

### GPT 配置模板

```markdown
# Name

[简洁描述性名称]

# Description

[一句话说明 GPT 做什么]

# Instructions

You are [role]. Your purpose is to [main purpose].

## Core Capabilities

1. [Capability 1]
2. [Capability 2]
3. [Capability 3]

## Workflow

When a user asks you to [task]:

1. First, [step 1]
2. Then, [step 2]
3. Finally, [step 3]

## Output Format

Always structure your responses as:

- [Section 1]: [Content]
- [Section 2]: [Content]

## Constraints

- Always: [Do this]
- Never: [Don't do this]
- When [condition]: [Action]

# Conversation Starters

1. [Example question 1]
2. [Example question 2]
3. [Example question 3]
4. [Example question 4]

# Knowledge

[上传的文件将在这里列出]

# Capabilities

- [x] Web Browsing
- [x] DALL·E Image Generation
- [x] Code Interpreter

# Actions

[如果配置了 API 集成]
```

---

## 🖱️ Cursor Agent 最佳实践

### 官方学习资源

**Cursor Learn**: <https://cursor.com/learn/agents>

**核心模式**:

1. **结构化提示**

   ```markdown
   # 上下文

   @file1.ts @file2.py

   # 任务

   实现[具体功能]

   # 要求

   - 使用[技术栈]
   - 遵循[模式]
   - 测试覆盖率>80%
   ```

2. **长对话管理**
   - 定期总结上下文
   - 使用`.cursorrules`文件
   - 分割大任务为小任务

3. **有效委派**

   ```markdown
   Phase 1: 数据库模式
   Phase 2: API 端点
   Phase 3: 前端组件
   Phase 4: 集成测试
   ```

### Cursor 配置最佳实践

**`.cursorrules`文件示例**:

```markdown
# 项目：[项目名]

# 技术栈：[技术栈]

## 编码规范

- 使用 TypeScript strict 模式
- 所有函数必须有 JSDoc 注释
- 优先函数式编程
- 使用 Guard Clauses 错误处理

## 文件组织

- src/components/ - React 组件
- src/lib/ - 工具函数
- src/types/ - TypeScript 类型
- tests/ - 测试文件

## 测试要求

- 每个函数至少一个单元测试
- 关键流程需要集成测试
- 使用 Jest + React Testing Library

## Git 提交

- 遵循 Conventional Commits
- feat: 新功能
- fix: Bug 修复
- docs: 文档更新
- refactor: 重构

## AI 助手指导

- 始终参考现有代码模式
- 逐步实现，每步验证
- 解释重大架构决策
- 提供测试用例
```

### Cursor + Claude Code 集成

**工作流程**:
