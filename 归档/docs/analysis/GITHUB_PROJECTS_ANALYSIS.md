# 🔥 GitHub 优秀项目深度分析

## 目录

1. [顶级项目对比](#顶级项目对比)
2. [项目详细分析](#项目详细分析)
3. [快速启动指南](#快速启动指南)
4. [工具选择决策树](#工具选择决策树)

---

## 🏆 顶级项目对比

| 项目                        | 星标    | 核心价值          | 适用场景               | 学习曲线 |
| --------------------------- | ------- | ----------------- | ---------------------- | -------- |
| **PRPs-agentic-eng**        | 1.7k⭐  | 完整 PRP 方法论   | 生产级代码，一次性成功 | 中       |
| **vibe-coding-template**    | 78⭐    | 4 小时 MVP 工作流 | 快速原型验证           | 低       |
| **PRD-driven-context**      | 3⭐     | 企业级治理        | 大型团队协作           | 高       |
| **structured-ai-workflows** | Fork    | 跨工具兼容        | 多工具环境             | 低       |
| **awesome-cursorrules**     | 34.8k⭐ | 社区规则库        | Cursor 优化            | 低       |

---

## 📊 项目详细分析

### 1. PRPs-agentic-eng (Wirasm) ⭐⭐⭐⭐⭐

#### 核心优势

```
✅ 生产就绪 - 为"一次性成功"设计
✅ 完整工具链 - Claude命令、Python脚本、模板
✅ 验证循环 - 内置测试和linting
✅ 视频教程 - 实战演示
```

#### 文件结构

```
PRPs-agentic-eng/
├── .claude/
│   └── commands/           # 12个预配置命令
│       ├── create-base-prp.md
│       ├── execute-base-prp.md
│       ├── planning-create.md
│       ├── review-general.md
│       └── ...
├── PRPs/
│   ├── templates/          # PRP模板
│   │   ├── prp_base.md
│   │   ├── prp_spec.md
│   │   └── prp_planning_base.md
│   ├── scripts/            # 自动化脚本
│   │   └── prp_runner.py
│   └── ai_docs/           # AI文档
│       ├── cc_base.md
│       ├── cc_best_practices.md
│       └── ...
└── CLAUDE.md              # 项目指南
```

#### 12 个 Claude 命令详解

1. **/create-base-prp** - 生成综合 PRP（含研究）

   ```markdown
   用途：从零开始创建详细 PRD
   输入：功能描述
   输出：包含上下文和验证的完整 PRP
   ```

2. **/execute-base-prp** - 针对代码库执行 PRP

   ```markdown
   用途：实施 PRP 中定义的功能
   输入：PRP 文件路径
   输出：工作代码+测试
   ```

3. **/planning-create** - 创建带图表的规划文档

   ```markdown
   用途：架构设计和系统规划
   输入：系统需求
   输出：Mermaid 图表+详细计划
   ```

4. **/spec-create-adv** - 高级规范创建

   ```markdown
   用途：技术规范文档
   输入：功能描述
   输出：API 规范、数据模型等
   ```

5. **/review-general** - 通用代码审查

   ```markdown
   用途：质量检查
   输入：代码文件
   输出：改进建议+最佳实践
   ```

6. **/review-staged-unstaged** - Git 更改审查

   ```markdown
   用途：提交前检查
   输入：Git diff
   输出：审查报告
   ```

7. **/refactor-simple** - 简单重构任务

   ```markdown
   用途：代码优化
   输入：重构目标
   输出：改进的代码
   ```

8. **/create-pr** - 创建 Pull Request

   ```markdown
   用途：Git 工作流自动化
   输入：更改描述
   输出：格式化的 PR
   ```

9. **/prime-core** - 用项目上下文初始化 Claude

   ```markdown
   用途：会话开始时加载上下文
   输入：无
   输出：Claude 理解项目结构
   ```

10. **/onboarding** - 新团队成员入职

    ```markdown
    用途：快速上手项目
    输入：角色（开发/设计/PM）
    输出：定制化入职指南
    ```

11. **/debug** - 调试工作流

    ```markdown
    用途：问题诊断
    输入：错误描述
    输出：根因分析+解决方案
    ```

12. **/spec-execute** - 执行规范

    ```markdown
    用途：实现技术规范
    输入：规范文件
    输出：符合规范的代码
    ```

#### PRP Runner 脚本

```bash
# 交互模式（开发推荐）
uv run PRPs/scripts/prp_runner.py --prp my-feature --interactive

# Headless模式（CI/CD）
uv run PRPs/scripts/prp_runner.py --prp my-feature --output-format json

# 流式JSON（实时监控）
uv run PRPs/scripts/prp_runner.py --prp my-feature --output-format stream-json
```

#### 快速启动

```bash
# 1. 克隆仓库
git clone https://github.com/Wirasm/PRPs-agentic-eng.git
cd PRPs-agentic-eng

# 2. 复制到你的项目
cp -r .claude/commands /path/to/your-project/.claude/
cp -r PRPs /path/to/your-project/

# 3. 创建第一个PRP
# 在Claude Code中:
/create-base-prp 实现用户认证系统

# 4. 执行PRP
/execute-base-prp PRPs/user-auth.md
```

---

### 2. vibe-coding-prompt-template (KhazP) ⭐⭐⭐⭐

#### 核心优势

```
✅ 快速MVP - 4小时平均完成
✅ 工具灵活 - 支持10+种AI工具
✅ 初学者友好 - 详细教程
✅ 成功率高 - 87%达到部署
```

#### 四阶段提示模板

**Stage 1: Deep Research** (`part1-deepresearch.md`)

```markdown
# 用途：市场和技术验证

# 时间：20-30 分钟

# 输出：research-[AppName].txt

问题包括：

- 目标用户是谁？
- 现有竞品分析
- 技术可行性评估
- 成本预估
- MVP 范围建议
```

**Stage 2: PRD** (`part2-prd-mvp.md`)

```markdown
# 用途：产品定义

# 时间：15-20 分钟

# 输出：PRD-[AppName]-MVP.md

内容：

- 核心功能（3-5 个必须有的）
- 目标用户
- 成功指标
- UI/UX 愿景
```

**Stage 3: Technical Design** (`part3-tech-design-mvp.md`)

```markdown
# 用途：技术架构

# 时间：15-20 分钟

# 输出：TechDesign-[AppName]-MVP.md

决策：

- 平台（web/mobile/desktop）
- 技术栈选择
- No-code vs Low-code vs Full-code
- 部署策略
```

**Stage 4: AI Agent Instructions** (`part4-notes-for-agent.md`)

```markdown
# 用途：生成 AI 指令

# 时间：5-10 分钟

# 输出：NOTES.md + 工具特定配置

生成文件：

- NOTES.md（通用）
- CLAUDE.md（Claude Code）
- GEMINI.md（Gemini CLI）
- .cursorrules（Cursor）
- .windsurfrules（Windsurf）
```

#### 工具选择指南

| 你的情况     | 最佳工具             | 原因               |
| ------------ | -------------------- | ------------------ |
| 完全初学者   | Windsurf 或 Bolt.new | 最直观，即时结果   |
| 学习编码     | Cursor + Claude 4    | 最佳解释和控制     |
| 有经验开发者 | Claude Code          | 最强大和灵活       |
| 预算有限     | Cline + Gemini CLI   | 完全免费且强大     |
| 今天就需要   | Lovable 或 Bolt.new  | 即时部署，无需设置 |
| 构建移动应用 | Flutter + Cursor     | 最佳移动支持       |
| 复杂逻辑     | Claude Code + GPT-5  | 卓越推理           |

#### 实战示例

```bash
# 1. 使用AI Studio创建研究文档
# 粘贴 part1-deepresearch.md
# 回答问题
# 保存为 research-MyApp.txt

# 2. 创建PRD
# 新AI会话
# 粘贴 part2-prd-mvp.md
# 附加 research-MyApp.txt
# 保存为 PRD-MyApp-MVP.md

# 3. 技术设计
# 新AI会话
# 粘贴 part3-tech-design-mvp.md
# 附加 PRD-MyApp-MVP.md
# 保存为 TechDesign-MyApp-MVP.md

# 4. 生成AI指令
# 新AI会话
# 粘贴 part4-notes-for-agent.md
# 附加 PRD 和 TechDesign
# 保存所有生成的配置文件

# 5. 使用Cursor构建
# 打开Cursor
# 加载项目和.cursorrules
# 提示："读取NOTES.md并逐步构建MVP"
```

---

### 3. PRD-driven-context-engineering (mattgierhart) ⭐⭐⭐⭐

#### 核心优势

```
✅ 企业级 - 适合大型团队
✅ 治理框架 - 清晰的权限和流程
✅ 质量门控 - 多层验证
✅ 安全优先 - 秘密管理内置
```

#### Gear Heart Methodology (GHM)

**使命**:

- 让质量成为必然（而非事后审查）
- 单一真相源（SSOT）
- 人类和 AI 代理之间明确角色划分

**三文件纪律**:

```yaml
Command Center: # 操作真相
  位置: COMMAND_CENTER.md
  内容:
    - 项目概况
    - 当前状态
    - 关键决策
    - 提取文档索引
  更新: 持续

PRD: # 产品需求
  位置: PRD.md
  内容:
    - 目标和原因
    - 功能规范
    - 验收标准
  更新: 每个版本

Current EPIC: # 当前史诗
  位置: EPIC-[name].md
  内容:
    - 任务列表
    - 状态跟踪
    - 阻塞问题
  更新: 每日
```

**门控系统**:

```markdown
## Phase 1: 设计

验证门控：
✓ 架构评审通过
✓ 安全检查完成
✓ 性能目标定义
✓ 测试策略批准

## Phase 2: 实现

验证门控：
✓ 代码审查（2 位批准者）
✓ 单元测试覆盖率 > 80%
✓ Lint 零错误
✓ 类型检查通过

## Phase 3: 验证

验证门控：
✓ 集成测试通过
✓ E2E 测试成功
✓ 性能基准达标
✓ 安全扫描无高危

## Phase 4: 部署

验证门控：
✓ 暂存环境验证
✓ 回滚计划就绪
✓ 监控配置
✓ 文档更新
```

#### 文件结构

```
your-project/
├── gear-heart-methodology/
│   ├── docs/
│   │   ├── templates/
│   │   │   ├── COMMAND_CENTER_template.md
│   │   │   ├── PRD-template.md
│   │   │   └── EPIC-template.md
│   │   ├── workflow/
│   │   │   └── WORKFLOW-MASTER.md
│   │   ├── standards/
│   │   │   ├── coding-standards.md
│   │   │   └── documentation-standards.md
│   │   ├── security/
│   │   │   └── SECRETS-MANAGEMENT.md
│   │   └── mcp/  # Model Context Protocol（可选）
│   └── README.md
├── COMMAND_CENTER.md      # 你的Command Center
├── PRD.md                 # 你的PRD
├── epics/
│   ├── EPIC-auth.md
│   └── EPIC-payment.md
└── src/                   # 源代码
```

#### 快速启动

```bash
# 1. 克隆仓库
git clone https://github.com/mattgierhart/PRD-driven-context-engineering.git
cd PRD-driven-context-engineering

# 2. 复制模板到项目
cp gear-heart-methodology/docs/templates/COMMAND_CENTER_template.md ../your-project/COMMAND_CENTER.md
cp gear-heart-methodology/docs/templates/PRD-template.md ../your-project/PRD.md
cp gear-heart-methodology/docs/templates/EPIC-template.md ../your-project/epics/EPIC-feature1.md

# 3. 填写并提交
# 编辑文件
git add COMMAND_CENTER.md PRD.md epics/
git commit -m "feat: 初始化GHM文档结构"

# 4. 使用工作流
# 参考 gear-heart-methodology/docs/workflow/WORKFLOW-MASTER.md
```

---

### 4. structured-ai-workflows (jasonleinart) ⭐⭐⭐

#### 核心优势

```
✅ 跨工具 - Cursor + Claude Code统一
✅ 分步验证 - 每个任务独立审查
✅ 简单易用 - 3个文件搞定
✅ 视频教程 - 实战演示
```

#### 三个核心文件

**1. create-prd.md**

```markdown
功能：引导 AI 生成 PRD
使用：@create-prd.md
输入：功能描述 + 可选文件引用
输出：结构化 PRD 文档

模板包含：

- 问题陈述
- 目标用户
- 核心功能
- 成功指标
- 技术约束
- 非功能需求
```

**2. generate-tasks.md**

```markdown
功能：从 PRD 生成任务列表
使用：@generate-tasks.md @MyFeature-PRD.md
输入：PRD 文件
输出：分层任务列表

任务结构：
1.0 父任务 1
1.1 子任务 1.1
1.2 子任务 1.2
2.0 父任务 2
2.1 子任务 2.1
...
```

**3. process-task-list.md**

```markdown
功能：逐任务执行和验证
使用：@process-task-list.md（仅第一个任务）
输入：任务列表
输出：逐步实现的代码

流程：

1. AI 执行任务 1.1
2. AI 等待你审查
3. 你批准："yes"
4. AI 标记完成并移到 1.2
5. 重复...
```

#### Cursor 使用流程

```markdown
### 会话 1：创建 PRD

输入：
"""
使用 @create-prd.md
这是我想构建的功能：实现用户认证系统，支持邮箱/密码登录、
JWT 令牌、刷新令牌和会话管理。
参考这些文件：@src/auth/basic_auth.py @src/models/user.py
"""

输出：PRD-UserAuth.md

### 会话 2：生成任务

输入：
"""
现在取 @PRD-UserAuth.md 并使用 @generate-tasks.md 创建任务
"""

输出：Tasks-UserAuth.md（在 PRD 内或单独文件）

### 会话 3+：执行任务

输入（第一个任务）：
"""
请从任务 1.1 开始并使用 @process-task-list.md
"""

后续（每个任务）：

- AI：完成任务 1.1，等待审查
- 你："yes"（或提供反馈）
- AI：标记完成，移到 1.2
```

#### Claude Code 配置

```bash
# 1. 复制文件到项目
mkdir -p ai-dev-tasks
cp create-prd.md generate-tasks.md process-task-list.md ai-dev-tasks/

# 2. 更新CLAUDE.md
cat >> CLAUDE.md << 'EOF'

# AI Dev Tasks
使用这些文件进行结构化功能开发（使用PRD）：
/ai-dev-tasks/create-prd.md
/ai-dev-tasks/generate-tasks.md
/ai-dev-tasks/process-task-list.md
EOF

# 3. 创建自定义命令（可选）
mkdir -p .claude/commands

cat > .claude/commands/create-prd.md << 'EOF'
请使用 /ai-dev-tasks/create-prd.md 中的结构化工作流
帮我为新功能创建PRD。
EOF

cat > .claude/commands/generate-tasks.md << 'EOF'
请使用 /ai-dev-tasks/generate-tasks.md 从PRD生成任务。
如果没明确告诉使用哪个PRD，列出 /tasks 下的PRD并让我选择：
- 假设存储在 /tasks 下，文件名以 `prd-` 开头（如 `prd-[name].md`）
- 不应该已有对应的任务列表（如 `tasks-prd-[name].md`）
- **始终**在继续前让我确认PRD文件名
提供编号列表选项方便我回答。
EOF

cat > .claude/commands/process-task-list.md << 'EOF'
请使用 /ai-dev-tasks/process-task-list.md 处理任务列表
EOF

# 4. 重启Claude Code
/exit
# 然后重新启动

# 5. 使用命令
/create-prd
/generate-tasks
/process-task-list
```

---

## 🚀 快速启动指南

### 场景 1：新项目从零开始（推荐 Vibe Coding）

```bash
# Day 1: 研究和定义（1小时）
1. 打开AI Studio或Claude.ai
2. 粘贴 part1-deepresearch.md
3. 描述你的想法
4. 保存研究结果为 research-MyApp.txt

5. 新会话，粘贴 part2-prd-mvp.md
6. 附加研究结果
7. 保存PRD为 PRD-MyApp-MVP.md

8. 新会话，粘贴 part3-tech-design-mvp.md
9. 附加PRD
10. 保存设计为 TechDesign-MyApp-MVP.md

# Day 1-2: 实现（3-4小时）
11. 新会话，粘贴 part4-notes-for-agent.md
12. 生成NOTES.md和工具配置

13. 打开Cursor/Claude Code
14. 加载项目和配置
15. 提示："读取NOTES.md并逐步构建MVP"
16. 审查每个功能实现

# Day 2: 测试和部署（1小时）
17. 运行测试
18. 修复问题
19. 部署到Vercel/Railway
20. 🎉 完成！
```

### 场景 2：现有项目添加功能（推荐 PRPs）

```bash
# 准备（10分钟）
1. cd your-project
2. git clone https://github.com/Wirasm/PRPs-agentic-eng.git /tmp/prps
3. cp -r /tmp/prps/.claude/commands .claude/
4. cp -r /tmp/prps/PRPs .

# 创建PRP（30分钟）
5. 打开Claude Code
6. /create-base-prp 实现[你的功能]
7. 审查生成的PRP
8. 保存为 PRPs/feature-name.md

# 执行PRP（1-2小时）
9. /execute-base-prp PRPs/feature-name.md
10. 审查每个更改
11. 运行测试：Level 1 → Level 2 → Level 3
12. 提交代码

# 审查和合并（30分钟）
13. /create-pr
14. GitHub代码审查
15. 合并到main
```

### 场景 3：团队协作（推荐 GHM）

```bash
# 设置（1次，30分钟）
1. git clone https://github.com/mattgierhart/PRD-driven-context-engineering.git
2. cp -r gear-heart-methodology /your-project/
3. 复制模板：COMMAND_CENTER, PRD, EPIC
4. 设置CI门控（GitHub Actions）

# 每个EPIC（1-2周）
5. PM创建EPIC-[name].md
6. 团队填写COMMAND_CENTER.md
7. 开发者创建功能分支
8. AI辅助实现（使用任何工具）
9. 通过所有门控
10. 合并到main

# 持续维护
11. 每天更新COMMAND_CENTER
12. 每周EPIC回顾
13. 每月PRD更新
```

---

## 🌳 工具选择决策树

```
开始
 │
 ├─ 你是初学者？
 │   ├─ 是 → 使用 Bolt.new 或 Lovable
 │   └─ 否 → 继续
 │
 ├─ 需要今天上线？
 │   ├─ 是 → 使用 Bolt.new
 │   └─ 否 → 继续
 │
 ├─ 预算 < $10/月？
 │   ├─ 是 → 使用 Cline + Gemini CLI （免费）
 │   └─ 否 → 继续
 │
 ├─ 团队 > 5人？
 │   ├─ 是 → 使用 GHM + Cursor/Claude Code
 │   └─ 否 → 继续
 │
 ├─ 构建MVP验证想法？
 │   ├─ 是 → 使用 Vibe Coding工作流
 │   └─ 否 → 继续
 │
 ├─ 生产级应用？
 │   ├─ 是 → 使用 PRPs方法论
 │   └─ 否 → 继续
 │
 └─ 默认推荐
     └─ Cursor + Structured AI Workflows
```

---

## 💡 专家建议

### 来自 Wirasm（PRPs 作者）

> "上下文为王。不要给 AI 一个模糊的描述然后期待奇迹。
> 给它精确的文件路径、库文档、已知陷阱，以及可执行的验证循环。
> 这不仅仅是'提示工程'——这是上下文工程。"

### 来自 KhazP（Vibe Coding 作者）

> "最大的错误是跳过研究阶段。花 20 分钟让 AI 验证你的想法
> 可以节省 20 小时构建没人需要的东西。
> 结构化流程不是束缚——它是自由的基础。"

### 来自社区

> "使用正确的工具完成正确的工作：
>
> - Bolt.new 用于快速演示
> - Cursor 用于严肃开发
> - Claude Code 用于复杂重构
>
> 不要试图用一个工具做所有事情。"

---

## 📚 推荐学习路径

### 第 1 周：基础

- [ ] 阅读 Vibe Coding README
- [ ] 观看演示视频
- [ ] 使用免费工具构建简单 MVP
- [ ] 完成 1 个完整的 4 阶段工作流

### 第 2 周：结构化

- [ ] 学习 Structured AI Workflows
- [ ] 为 Cursor/Claude Code 配置命令
- [ ] 实践 PRD → 任务 → 实现流程
- [ ] 构建 1 个中等复杂度功能

### 第 3 周：生产级

- [ ] 深入 PRPs 方法论
- [ ] 设置验证循环
- [ ] 编写第一个完整 PRP
- [ ] 用 PRP 实现生产功能

### 第 4 周：企业级

- [ ] 学习 GHM
- [ ] 设置三文件纪律
- [ ] 实施门控系统
- [ ] 为团队文档化流程

---

## 🎯 成功案例

### 案例 1：SaaS 仪表板（4 小时）

```
工具：Vibe Coding + Bolt.new
结果：
- 用户认证 ✓
- 数据可视化 ✓
- CRUD操作 ✓
- 响应式设计 ✓
部署：Vercel（免费）
成本：$0
```

### 案例 2：API 微服务（1 天）

```
工具：PRPs + Claude Code
结果：
- RESTful API ✓
- PostgreSQL集成 ✓
- JWT认证 ✓
- 80%+测试覆盖率 ✓
部署：Railway
成本：$5/月
```

### 案例 3：企业应用（2 周）

```
工具：GHM + Cursor + 团队协作
结果：
- 多租户架构 ✓
- RBAC权限系统 ✓
- 审计日志 ✓
- 通过所有安全门控 ✓
部署：AWS ECS
成本：$200/月
```

---

## 🔗 有用链接

### 文档

- [Cursor Learn](https://cursor.com/learn)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### 社区

- [Reddit: r/cursor](https://reddit.com/r/cursor)
- [Reddit: r/ChatGPTPromptGenius](https://reddit.com/r/ChatGPTPromptGenius)
- [Discord: Cursor Community](https://discord.gg/cursor)

### 视频教程

- [PRPs 演示](https://www.youtube.com/watch?v=KVOZ9s1S9Gk)
- [Cursor VP 实时演示](https://www.youtube.com/watch?v=8QN23ZThdRY)
- [How I AI Podcast](https://www.youtube.com/watch?v=fD4ktSkNCw4)

---

## ⏭️ 下一步

1. **选择一个项目**从上面的对比表
2. **克隆和实验**用一个小功能
3. **测量结果**（时间、代码质量、成功率）
4. **迭代和改进**你的工作流
5. **与团队分享**经验和最佳实践

记住：**没有完美的工作流，只有最适合你的工作流**。
从简单开始，随着学习逐步增加复杂度。

🚀 祝你 AI 编码愉快！
