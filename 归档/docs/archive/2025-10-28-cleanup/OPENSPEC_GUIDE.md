# OpenSpec 团队使用指南

**项目**: FireShot
**更新时间**: 2025-10-28
**版本**: v1.0.0

---

## 📚 目录

1. [什么是 OpenSpec](#什么是-openspec)
2. [快速开始](#快速开始)
3. [核心概念](#核心概念)
4. [完整工作流](#完整工作流)
5. [最佳实践](#最佳实践)
6. [常见问题](#常见问题)
7. [团队协作](#团队协作)

---

## 什么是 OpenSpec

OpenSpec 是一个**规范驱动开发框架**，专为 AI 编码助手设计。它通过以下方式提升开发效率：

### 核心价值

✅ **需求明确**: 在编码前用规范定义"要做什么"
✅ **避免返工**: AI 按照规范实施，减少误解和偏差
✅ **团队同步**: 所有 AI 助手共享相同的规范文档
✅ **可追溯**: 变更历史完整记录，随时回顾
✅ **渐进式**: 从小功能开始，逐步建立完整规范

### 与传统开发的区别

| 传统开发 | OpenSpec 开发 |
|---------|--------------|
| 直接写代码，边写边改 | 先写规范，再按规范实施 |
| 需求散落在脑中或文档 | 需求结构化存储在 `specs/` |
| 难以追踪变更历史 | 变更自动归档到 `archive/` |
| AI 容易误解需求 | AI 严格遵循规范文件 |

---

## 快速开始

### 1. 安装 OpenSpec CLI

```bash
npm install -g @fission-ai/openspec@latest
```

### 2. 验证安装

```bash
cd /Users/zhiledeng/Downloads/FireShot
openspec list  # 应该显示当前项目的变更列表
```

### 3. 查看项目规范

```bash
openspec view  # 打开交互式仪表板
```

### 4. 你的第一个变更提案

在 Cursor 中对 AI 说：

```
创建一个 OpenSpec 变更提案：添加夏威夷租房信息爬虫
```

或使用快捷命令（如果工具支持）：

```
/openspec:proposal 添加夏威夷租房信息爬虫
```

AI 会自动创建：
- `openspec/changes/add-rental-scraper/proposal.md`
- `openspec/changes/add-rental-scraper/tasks.md`
- `openspec/changes/add-rental-scraper/specs/...`

---

## 核心概念

### 目录结构

```
FireShot/
├── openspec/
│   ├── project.md           # 📋 项目总规范（全局约定）
│   ├── specs/               # ✅ 当前规范（系统现状）
│   │   ├── firecrawl-scraper/
│   │   │   └── spec.md
│   │   └── hawaiihub-data/
│   │       └── spec.md
│   ├── changes/             # 🚧 待实施变更（新功能/改进）
│   │   └── add-rental-scraper/
│   │       ├── proposal.md
│   │       ├── tasks.md
│   │       └── specs/
│   │           └── hawaiihub-data/
│   │               └── spec.md  # Delta（差异）
│   └── archive/             # 📦 已归档变更（历史记录）
│
└── AGENTS.md                # 🤖 AI 助手总规范
```

### 文件说明

#### `openspec/project.md`
- **用途**: 定义项目级别的全局约定
- **内容**: 技术栈、代码规范、Git 规范、禁止事项
- **更新频率**: 较低（项目初期确定后很少改动）

#### `openspec/specs/`
- **用途**: 存储系统当前的规范（真实状态）
- **内容**: 每个模块的需求、场景、实现约束
- **更新方式**: 通过归档变更自动更新

#### `openspec/changes/`
- **用途**: 存储待实施的变更提案
- **内容**: 提案说明、任务清单、规范差异（Delta）
- **生命周期**: 创建 → 实施 → 归档 → 删除

#### `openspec/archive/`
- **用途**: 存储已完成的变更历史
- **内容**: 完整的变更提案和实施记录
- **价值**: 可追溯、可回顾、可审计

---

## 完整工作流

### 阶段 1: 创建变更提案

**场景**: 产品经理说"我们需要添加租房信息爬虫"

**操作**:
```
你对 AI 说: 创建一个 OpenSpec 变更提案：添加夏威夷租房信息爬虫

AI 回复: 我会为您创建变更提案...
```

**生成文件**:
```
openspec/changes/add-rental-scraper/
├── proposal.md      # 功能说明、背景、目标
├── tasks.md         # 任务清单（可勾选）
└── specs/
    └── hawaiihub-data/
        └── spec.md  # 规范差异（ADDED/MODIFIED/REMOVED）
```

**示例 `proposal.md`**:

```markdown
# 变更提案: 添加夏威夷租房信息爬虫

## 背景
HawaiiHub 需要提供租房信息聚合服务，帮助华人用户快速找到合适的房源。

## 目标
- 从 Craigslist Hawaii 采集租房信息
- 数据包含：标题、价格、位置、卧室数、浴室数、描述
- 每天更新 4 次

## 价值
- 为用户节省 50% 找房时间
- 提升平台粘性
```

### 阶段 2: 审查和验证

**操作**:
```bash
# 查看所有活动变更
openspec list

# 验证规范格式
openspec validate add-rental-scraper

# 查看详细内容
openspec show add-rental-scraper
```

**输出示例**:
```
✓ Proposal found
✓ Tasks found (8 tasks)
✓ Spec deltas found (1 module)

Tasks:
  [ ] 1.1 创建 Rental 数据模型
  [ ] 1.2 添加 Pydantic 验证
  [ ] 2.1 实现 Craigslist 爬取逻辑
  ...
```

### 阶段 3: 迭代和完善

**场景**: 审查后发现需要补充需求

**操作**:
```
你对 AI 说: 在 add-rental-scraper 提案中，添加价格范围过滤功能

AI 回复: 我会更新提案和任务清单...
```

AI 会自动：
- 更新 `proposal.md`
- 在 `tasks.md` 中添加新任务
- 修改 `specs/hawaiihub-data/spec.md` 的差异部分

### 阶段 4: 实施变更

**操作**:
```
你对 AI 说: 提案看起来不错，开始实施 add-rental-scraper 变更

AI 回复: 我会按照任务清单实施...
```

**AI 的工作流程**:
1. 读取 `openspec/changes/add-rental-scraper/tasks.md`
2. 按顺序实施每个任务
3. 完成后在任务前打勾 `[x]`
4. 生成代码、测试、文档

**任务完成示例**:
```markdown
## 1. 数据模型
- [x] 1.1 创建 Rental 数据模型
- [x] 1.2 添加 Pydantic 验证

## 2. 爬虫实现
- [x] 2.1 实现 Craigslist 爬取逻辑
- [ ] 2.2 添加错误处理（进行中...）
```

### 阶段 5: 归档完成的变更

**操作**:
```bash
# 方式1: 命令行（推荐）
openspec archive add-rental-scraper --yes

# 方式2: 对 AI 说
你对 AI 说: 请归档 add-rental-scraper 变更
```

**归档过程**:
1. 将 `openspec/changes/add-rental-scraper/` 移动到 `archive/`
2. 将规范差异合并到 `openspec/specs/hawaiihub-data/spec.md`
3. 更新 `CHANGELOG.md`（如果存在）

**归档后的规范（自动合并）**:

```markdown
# HawaiiHub 数据采集规范

## 要求

### Requirement: 租房信息采集  # ← 新增的需求
系统必须从 Craigslist Hawaii 采集租房信息。

#### Scenario: 每日更新
- 当系统运行定时任务时
- 则每天采集 4 次（每 6 小时）
- 并且过滤价格范围 $500-$5000
```

---

## 最佳实践

### ✅ 推荐做法

#### 1. 小步快跑
```
❌ 不好: 创建一个"重构整个系统"的巨大变更
✅ 推荐: 创建多个小变更，如"优化爬虫性能"、"添加缓存机制"
```

#### 2. 明确的任务清单
```
❌ 不好:
- [ ] 实现功能

✅ 推荐:
- [ ] 1.1 创建数据模型（models/rental.py）
- [ ] 1.2 添加 Pydantic 验证
- [ ] 2.1 实现爬取逻辑（scrapers/craigslist.py）
- [ ] 2.2 添加单元测试（tests/test_rental.py）
```

#### 3. 使用 Scenario 描述行为
```
❌ 不好:
### Requirement: 价格过滤
系统应该过滤价格。

✅ 推荐:
### Requirement: 价格范围过滤
系统必须过滤价格范围在合理区间的租房信息。

#### Scenario: 过滤异常高价
- 当租房价格 > $10,000/月时
- 则系统应记录警告并跳过该条目
- 并且在日志中标记 "ABNORMAL_PRICE"
```

#### 4. 及时归档
```
❌ 不好: 积累 10+ 个已完成的变更不归档

✅ 推荐: 完成一个变更立即归档，保持 changes/ 目录整洁
```

### ⚠️ 避免的做法

#### 1. 直接修改 `openspec/specs/`
```
❌ 错误: 手动编辑 openspec/specs/hawaiihub-data/spec.md

✅ 正确: 创建变更提案 → 实施 → 归档（自动更新 specs/）
```

#### 2. 跳过验证步骤
```
❌ 错误: 创建提案后直接实施

✅ 正确: 创建 → 验证 → 审查 → 实施
```

#### 3. 规范太模糊
```
❌ 错误:
### Requirement: 数据质量
数据应该是好的。

✅ 正确:
### Requirement: 数据完整性验证
系统必须验证所有必填字段都存在且有效。

#### Scenario: 缺失必填字段
- 当 title 或 price 字段缺失时
- 则系统应记录 ERROR 日志
- 并且拒绝保存该条目
```

---

## 常见问题

### Q1: OpenSpec 和 .cursorrules 有什么区别？

**回答**:
- **`.cursorrules`**: 全局编码规范（如何写代码）
- **`openspec/project.md`**: 项目全局约定（技术栈、流程）
- **`openspec/specs/`**: 功能规范（要实现什么功能）
- **`AGENTS.md`**: AI 助手行为规范（AI 如何工作）

它们是互补关系，一起确保代码质量和功能正确性。

### Q2: 什么时候创建新的变更提案？

**回答**:
- ✅ 添加新功能
- ✅ 修改现有功能的行为
- ✅ 重构代码架构
- ✅ 性能优化（有明确目标）
- ❌ 修复拼写错误
- ❌ 格式化代码
- ❌ 简单的 Bug 修复

### Q3: 变更提案可以修改吗？

**回答**: 可以！在实施前可以随时修改：

```
你对 AI 说: 在 add-rental-scraper 提案中，添加图片采集功能

AI 会自动更新提案、任务清单和规范差异。
```

### Q4: 如果实施中发现问题怎么办？

**回答**: 有两种选择：

**方案 1: 更新当前变更**
```
你对 AI 说: add-rental-scraper 变更中，我发现需要添加去重逻辑，请更新提案
```

**方案 2: 创建新变更（推荐）**
```
你对 AI 说: 暂停 add-rental-scraper，创建一个新变更提案：添加租房信息去重
```

### Q5: 归档后还能找到历史变更吗？

**回答**: 可以！

```bash
# 查看归档的变更
ls openspec/archive/

# 查看具体变更内容
cat openspec/archive/add-rental-scraper/proposal.md
```

### Q6: 多人协作时如何避免冲突？

**回答**:
1. **分模块工作**: 不同人负责不同 `specs/` 模块
2. **小变更**: 减少重叠的可能性
3. **频繁同步**: 经常 `git pull` 获取最新规范
4. **使用分支**: 大变更在独立分支完成

---

## 团队协作

### 角色分工

#### 产品经理
- **职责**: 创建变更提案（通过 AI）
- **工具**: Cursor + `/openspec:proposal` 命令
- **示例**:
  ```
  /openspec:proposal 添加用户评论功能，支持文字和图片
  ```

#### 开发工程师
- **职责**: 审查提案、实施变更
- **工具**: Cursor + `/openspec:apply` 命令
- **工作流**:
  1. `openspec show <change>` 查看提案
  2. 提出修改建议
  3. `/openspec:apply <change>` 实施
  4. `openspec archive <change> --yes` 归档

#### 测试工程师
- **职责**: 验证实施结果符合规范
- **工具**: 对照 `specs/` 文件进行测试
- **检查清单**:
  - [ ] 所有 Scenario 都有对应测试用例
  - [ ] 测试覆盖所有边界条件
  - [ ] 错误处理符合规范要求

### 协作流程

```
产品经理: /openspec:proposal 添加租房信息爬虫
          ↓
开发工程师: openspec show add-rental-scraper
          ↓（审查）
开发工程师: /openspec:apply add-rental-scraper
          ↓（实施）
测试工程师: 验证规范符合度
          ↓（通过）
开发工程师: openspec archive add-rental-scraper --yes
```

---

## 快速命令参考

```bash
# 查看所有变更
openspec list

# 交互式仪表板
openspec view

# 查看变更详情
openspec show <change-name>

# 验证规范格式
openspec validate <change-name>

# 归档变更（自动更新 specs/）
openspec archive <change-name> --yes

# 更新 AI 助手配置
openspec update
```

---

## Slash 命令（Cursor/Claude Code）

```bash
# 创建变更提案
/openspec:proposal <功能描述>

# 实施变更
/openspec:apply <change-name>

# 归档变更
/openspec:archive <change-name>
```

---

## 下一步

1. **尝试创建第一个变更**: 选择一个小功能，创建提案并实施
2. **阅读现有规范**: 查看 `openspec/specs/` 了解现有系统
3. **参与团队讨论**: 在变更提案中提出改进建议
4. **查看归档历史**: 学习之前的变更是如何实施的

---

## 获取帮助

- **查看示例**: `openspec/specs/` 目录有完整的规范示例
- **阅读官方文档**: https://openspec.dev/
- **团队讨论**: 在项目会议中分享 OpenSpec 使用经验

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28

---

## 附录: 规范编写模板

### Requirement 模板

```markdown
### Requirement: <需求名称>

<一句话描述：系统必须/应该做什么>

#### Scenario: <场景名称>
- 当<触发条件>时
- 则<系统行为>
- 并且<额外约束>
```

### 变更提案模板

```markdown
# 变更提案: <变更名称>

## 背景
<为什么需要这个变更？>

## 目标
- <目标1>
- <目标2>

## 价值
<带来的业务价值或技术收益>

## 风险
<潜在风险和缓解措施>
```

### 任务清单模板

```markdown
## 1. <阶段名称>
- [ ] 1.1 <具体任务>（<文件路径>）
- [ ] 1.2 <具体任务>

## 2. <阶段名称>
- [ ] 2.1 <具体任务>
```
