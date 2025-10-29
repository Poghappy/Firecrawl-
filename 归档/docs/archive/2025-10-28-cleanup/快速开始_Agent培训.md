# Agent 团队 OpenSpec 培训 - 快速开始

**更新时间**: 2025-10-28
**培训时长**: 3 天（总计约 4 小时）

---

## 🚀 一键启动培训

### 方法 1: 使用交互式培训脚本（推荐）

```bash
cd /Users/zhiledeng/Downloads/FireShot
./openspec/start-training.sh
```

**脚本功能**:
- ✅ 自动检查环境配置
- ✅ 交互式培训引导
- ✅ 按天分步学习
- ✅ 实战练习指导
- ✅ 角色选择助手

### 方法 2: 手动按文档学习

按照以下顺序阅读文档：

#### 第 1 天（60 分钟）
```bash
# 1. 文档导航（10 分钟）
cat openspec/README.md

# 2. 快速上手（30 分钟）
cat openspec/AGENT_TEAM_QUICKSTART.md

# 3. 实战练习（20 分钟）
# 练习1: 查找成本控制要求
cat openspec/specs/firecrawl-scraper/spec.md | grep -A 10 "成本控制"

# 练习2: 创建变更提案（在 Cursor 中）
# 对 AI 说：/openspec:proposal 添加结构化日志记录

# 练习3: 查看规范差异
cat openspec/changes/*/specs/*/spec.md
```

#### 第 2 天（35 分钟）
```bash
# 1. 项目全局规范（15 分钟）
cat openspec/project.md

# 2. Firecrawl 爬虫规范（10 分钟）
cat openspec/specs/firecrawl-scraper/spec.md

# 3. HawaiiHub 数据规范（10 分钟）
cat openspec/specs/hawaiihub-data/spec.md
```

#### 第 3 天（2.5 小时）
```bash
# 1. 团队角色分工（20 分钟）
cat openspec/AGENT_ROLES_GUIDE.md

# 2. 明确角色职责（10 分钟）
# 选择你的角色：Product/Development/Quality/Documentation/DevOps

# 3. 创建真实变更（2 小时）
# 根据角色实施一个完整变更
```

---

## 📋 培训前检查清单

### 环境要求

```bash
# 检查 OpenSpec CLI
openspec --version

# 检查项目结构
ls openspec/

# 检查培训文档
ls openspec/*.md
```

**预期输出**:
```
openspec/
├── README.md
├── AGENT_TEAM_QUICKSTART.md
├── AGENT_ROLES_GUIDE.md
├── project.md
├── specs/
├── changes/
└── archive/
```

### 软件要求

- ✅ Node.js (OpenSpec CLI)
- ✅ Cursor AI 或其他支持的编辑器
- ✅ Git
- ✅ Python 3.14（如果是开发角色）

---

## 🎯 培训目标

完成 3 天培训后，你将能够：

### 技能掌握
- ✅ 理解 OpenSpec 的核心概念（Spec、Change、Delta）
- ✅ 熟练使用 OpenSpec CLI 命令
- ✅ 独立创建和实施变更提案
- ✅ 遵循项目编码规范和流程
- ✅ 与其他 Agent 协作开发

### 角色明确
- ✅ 明确自己在团队中的角色
- ✅ 了解角色的职责和工作流
- ✅ 掌握角色专属的工具和命令

### 实战能力
- ✅ 完成至少 1 个真实变更
- ✅ 能够审查和验证规范
- ✅ 能够归档完成的变更

---

## 📚 培训内容概览

### 第 1 天：环境熟悉

| 步骤 | 内容 | 时长 | 输出 |
|------|------|------|------|
| 1 | 阅读文档索引 | 10 分钟 | 了解文档结构 |
| 2 | 快速上手培训 | 30 分钟 | 掌握基本流程 |
| 3 | 实战练习（3个） | 20 分钟 | 实践操作 |

**学习重点**:
- specs/、changes/、archive/ 目录的区别
- Requirement 和 Scenario 的格式
- 创建变更的完整流程

### 第 2 天：规范学习

| 步骤 | 内容 | 时长 | 输出 |
|------|------|------|------|
| 1 | 项目全局规范 | 15 分钟 | 掌握编码标准 |
| 2 | Firecrawl 爬虫规范 | 10 分钟 | 了解工具使用 |
| 3 | HawaiiHub 数据规范 | 10 分钟 | 理解数据模型 |

**学习重点**:
- Python 代码规范（类型注解、docstring）
- Firecrawl 工具选择策略
- 数据清洗和验证标准

### 第 3 天：角色定位

| 步骤 | 内容 | 时长 | 输出 |
|------|------|------|------|
| 1 | 团队角色分工 | 20 分钟 | 明确角色职责 |
| 2 | 角色选择 | 10 分钟 | 确定工作方向 |
| 3 | 实战变更 | 2 小时 | 完成真实任务 |

**学习重点**:
- 5 个角色的职责和工作流
- 团队协作最佳实践
- 完整的变更生命周期

---

## 🎭 角色快速参考

### 📋 Product Agent（产品规划）
**职责**: 创建变更提案、定义需求
**核心命令**: `/openspec:proposal <功能描述>`
**时间占比**: 20%

### 💻 Development Agent（核心开发）
**职责**: 实施变更、编写代码
**核心命令**: `/openspec:apply <变更名>`
**时间占比**: 50%

### 🧪 Quality Agent（质量保证）
**职责**: 测试验证、代码审查
**核心命令**: `pytest tests/ --cov`
**时间占比**: 15%

### 📚 Documentation Agent（文档维护）
**职责**: 编写文档、知识管理
**核心命令**: 编写 Markdown 文档
**时间占比**: 10%

### 🚀 DevOps Agent（运维部署）
**职责**: 部署监控、性能优化
**核心命令**: 监控工具
**时间占比**: 5%

---

## ⚡ 常用命令速查

### OpenSpec 命令

```bash
# 查看所有变更
openspec list

# 交互式仪表板
openspec view

# 查看变更详情
openspec show <change-name>

# 验证规范格式
openspec validate <change-name>

# 归档变更
openspec archive <change-name> --yes
```

### Cursor Slash 命令

```bash
# 创建变更提案
/openspec:proposal <功能描述>

# 实施变更
/openspec:apply <change-name>

# 归档变更
/openspec:archive <change-name>
```

### Git 命令

```bash
# 查看状态
git status

# 提交代码
git add .
git commit -m "feat(scraper): 添加功能"

# 推送代码
git push origin main
```

---

## 💡 实战练习参考答案

### 练习 1: 查找成本控制要求

**问题1**: 系统在执行每次爬取前应该检查什么？
**答案**: 检查是否超出每日预算

**问题2**: 缓存策略的参数是什么？
**答案**: `max_age=172800000`（2天，172800000 毫秒）

**问题3**: 成本记录应该输出到哪里？
**答案**: 输出到日志文件

### 练习 2: 创建变更提案

**步骤**:
1. 在 Cursor 中对 AI 说：`/openspec:proposal 添加结构化日志记录`
2. AI 自动生成提案文件
3. 运行 `openspec show add-logging` 查看
4. 运行 `openspec validate add-logging` 验证

**检查点**:
- [ ] proposal.md 包含背景和目标
- [ ] tasks.md 至少有 3 个任务
- [ ] specs/ 目录有规范差异

### 练习 3: 审查规范差异

**检查项**:
1. **规范差异标记**: 使用 `## ADDED Requirements`、`## MODIFIED Requirements`、`## REMOVED Requirements`
2. **Scenario 覆盖**: 每个 Requirement 必须有至少一个 Scenario
3. **格式规范**: 遵循"当...时 / 则... / 并且..."三段式

---

## 🆘 常见问题

### Q1: 培训脚本运行失败？

**检查**:
```bash
# 检查脚本权限
ls -l openspec/start-training.sh

# 设置可执行权限
chmod +x openspec/start-training.sh

# 检查 OpenSpec CLI
which openspec
```

### Q2: 找不到培训文档？

**解决**:
```bash
# 确认在项目根目录
pwd  # 应该是 /Users/zhiledeng/Downloads/FireShot

# 查看文档列表
ls openspec/*.md
```

### Q3: 实战练习不知道怎么做？

**建议**:
1. 先完整阅读 `AGENT_TEAM_QUICKSTART.md`
2. 查看相关规范示例
3. 参考上面的参考答案
4. 在团队会议中讨论

---

## 📈 学习进度追踪

### 第 1 天检查清单
- [ ] 运行 `openspec list` 验证环境
- [ ] 阅读 README.md（10 分钟）
- [ ] 阅读 AGENT_TEAM_QUICKSTART.md（30 分钟）
- [ ] 完成练习 1：查找成本控制
- [ ] 完成练习 2：创建变更提案
- [ ] 完成练习 3：审查规范差异

### 第 2 天检查清单
- [ ] 阅读 project.md（15 分钟）
- [ ] 阅读 firecrawl-scraper/spec.md（10 分钟）
- [ ] 阅读 hawaiihub-data/spec.md（10 分钟）
- [ ] 理解 Python 代码规范
- [ ] 理解数据模型定义

### 第 3 天检查清单
- [ ] 阅读 AGENT_ROLES_GUIDE.md（20 分钟）
- [ ] 选择自己的主要角色
- [ ] 创建第一个真实变更
- [ ] 实施并测试变更
- [ ] 归档完成的变更
- [ ] 与团队分享经验

---

## 🎉 培训完成标志

当你完成以下所有项目，就算正式完成培训：

- ✅ 能够独立运行 OpenSpec 命令
- ✅ 理解 specs/、changes/、archive/ 的作用
- ✅ 能够创建格式正确的变更提案
- ✅ 明确自己的角色和职责
- ✅ 完成至少 1 个真实变更的完整流程
- ✅ 知道在哪里查找帮助文档

---

## 📞 获取帮助

### 文档资源

```bash
# 快速参考
cat openspec/README.md

# 完整指南
cat OPENSPEC_GUIDE.md

# 配置报告
cat OPENSPEC_SETUP_COMPLETE.md
```

### 在线资源

- OpenSpec 官网: https://openspec.dev/
- FireShot 项目文档: `docs/` 目录
- Firecrawl 文档: https://docs.firecrawl.dev/

---

## 🚀 现在就开始！

### 推荐路径

```bash
# 1. 运行培训脚本
cd /Users/zhiledeng/Downloads/FireShot
./openspec/start-training.sh

# 2. 选择 "1" 开始第 1 天培训

# 3. 按照脚本提示完成每个步骤
```

### 或手动学习

```bash
# 从文档导航开始
cat openspec/README.md
```

---

**祝你培训顺利！成为 FireShot Agent 团队的优秀成员！** 🎉

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28
