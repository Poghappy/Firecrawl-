# 🚀 OpenSpec Agent 培训 - 立即开始

**FireShot 项目**
**更新时间**: 2025-10-28
**培训时长**: 3 天（总计 4 小时）

---

## ⚡ 一键启动（最快方式）

```bash
cd /Users/zhiledeng/Downloads/FireShot
./openspec/start-training.sh
```

**就这么简单！** 脚本会自动引导你完成整个培训流程。

---

## 📚 培训资源导航

### 🎯 新手必读（按顺序）

| 序号 | 文档 | 用途 | 时间 |
|------|------|------|------|
| **1** | `快速开始_Agent培训.md` | 培训概览 | 5 分钟 |
| **2** | `openspec/start-training.sh` | 交互式培训 ⭐ | 按需 |
| **3** | `openspec/README.md` | 文档导航 | 10 分钟 |

### 📖 核心培训文档

| 文档 | 内容 | 适合人群 |
|------|------|---------|
| `AGENT_TEAM_QUICKSTART.md` | 30分钟快速上手 | 所有 Agent |
| `AGENT_ROLES_GUIDE.md` | 5 个角色详解 | 所有 Agent |
| `openspec/project.md` | 项目全局规范 | Development Agent |

### 📚 参考文档（需要时查阅）

| 文档 | 内容 | 大小 |
|------|------|------|
| `OPENSPEC_GUIDE.md` | 完整使用指南 | 25 KB |
| `OPENSPEC_SETUP_COMPLETE.md` | 环境配置报告 | - |
| `AGENTS.md` | AI 助手规范 | 20 KB |
| `AGENT_TEAM_OPENSPEC_COMPLETE.md` | 培训总结报告 | - |

---

## 🎓 3 天学习计划

### 第 1 天：环境熟悉（60 分钟）

```bash
# 启动培训脚本，选择 "1"
./openspec/start-training.sh

# 或手动学习
cat openspec/README.md                      # 10 分钟
cat openspec/AGENT_TEAM_QUICKSTART.md       # 30 分钟
# 完成 3 个实战练习                          # 20 分钟
```

**学到什么**:
- ✅ OpenSpec 基本概念
- ✅ specs/、changes/、archive/ 的区别
- ✅ 如何创建变更提案
- ✅ 完整工作流程

### 第 2 天：规范学习（35 分钟）

```bash
# 启动培训脚本，选择 "2"
./openspec/start-training.sh

# 或手动学习
cat openspec/project.md                           # 15 分钟
cat openspec/specs/firecrawl-scraper/spec.md      # 10 分钟
cat openspec/specs/hawaiihub-data/spec.md         # 10 分钟
```

**学到什么**:
- ✅ Python 代码规范
- ✅ Firecrawl 使用标准
- ✅ 数据模型定义
- ✅ 质量要求

### 第 3 天：角色定位（2.5 小时）

```bash
# 启动培训脚本，选择 "3"
./openspec/start-training.sh

# 或手动学习
cat openspec/AGENT_ROLES_GUIDE.md        # 20 分钟
# 选择角色                               # 10 分钟
# 创建第一个真实变更                     # 2 小时
```

**学到什么**:
- ✅ 5 个专业角色职责
- ✅ 团队协作流程
- ✅ 实战操作能力

---

## 🎭 选择你的角色

### 📋 Product Agent（产品规划）
**适合**: 喜欢需求分析和产品设计
**核心工作**: 创建变更提案、定义规范
**常用命令**: `/openspec:proposal <功能>`
**时间占比**: 20%

### 💻 Development Agent（核心开发）
**适合**: 喜欢编写代码和实现功能
**核心工作**: 实施变更、编写代码、测试
**常用命令**: `/openspec:apply <变更名>`
**时间占比**: 50%

### 🧪 Quality Agent（质量保证）
**适合**: 注重细节和质量标准
**核心工作**: 测试验证、代码审查
**常用命令**: `pytest tests/ --cov`
**时间占比**: 15%

### 📚 Documentation Agent（文档维护）
**适合**: 善于技术写作和知识管理
**核心工作**: 编写文档、维护知识库
**常用命令**: 编写 Markdown 文档
**时间占比**: 10%

### 🚀 DevOps Agent（运维部署）
**适合**: 关注系统稳定性和性能
**核心工作**: 部署监控、成本优化
**常用命令**: 监控工具
**时间占比**: 5%

---

## ⚡ 常用命令速查卡

### OpenSpec 命令

```bash
openspec list              # 查看所有变更
openspec view              # 交互式仪表板
openspec show <变更>       # 查看变更详情
openspec validate <变更>   # 验证规范格式
openspec archive <变更> -y # 归档变更
```

### Cursor Slash 命令

```bash
/openspec:proposal <描述>  # 创建变更提案
/openspec:apply <变更名>   # 实施变更
/openspec:archive <变更名> # 归档变更
```

### Git 提交规范

```bash
git commit -m "feat(scraper): 添加租房信息爬虫"
git commit -m "fix(parser): 修复日期解析错误"
git commit -m "docs(api): 更新 API 文档"
```

---

## 🎯 快速验证环境

```bash
# 检查 OpenSpec CLI
openspec --version

# 检查培训文档
ls openspec/*.md

# 运行验证测试
./openspec/start-training.sh  # 选择 "5"
```

**预期结果**:
```
✓ OpenSpec CLI 已安装
✓ README.md
✓ AGENT_TEAM_QUICKSTART.md
✓ AGENT_ROLES_GUIDE.md
✓ project.md
```

---

## 📊 培训进度自检

### ✅ 第 1 天完成标志
- [ ] 能运行 `openspec list`
- [ ] 理解 specs/、changes/、archive/
- [ ] 能创建变更提案
- [ ] 完成 3 个实战练习

### ✅ 第 2 天完成标志
- [ ] 理解 Python 代码规范
- [ ] 知道 Firecrawl 工具选择
- [ ] 了解数据模型定义
- [ ] 能阅读规范文档

### ✅ 第 3 天完成标志
- [ ] 明确自己的角色
- [ ] 完成 1 个真实变更
- [ ] 能独立工作
- [ ] 知道如何协作

---

## 💡 实战练习提示

### 练习 1: 查找成本控制（5 分钟）
```bash
cat openspec/specs/firecrawl-scraper/spec.md | grep -A 10 "成本控制"
```

**回答问题**:
1. 每次爬取前检查什么？→ 每日预算
2. 缓存参数是什么？→ `max_age=172800000`
3. 成本记录到哪里？→ 日志文件

### 练习 2: 创建变更提案（10 分钟）
```
在 Cursor 中对 AI 说：
/openspec:proposal 添加结构化日志记录
```

**检查点**:
- [ ] proposal.md 有背景和目标
- [ ] tasks.md 至少 3 个任务
- [ ] specs/ 有规范差异

### 练习 3: 审查规范（5 分钟）
```bash
cat openspec/changes/*/specs/*/spec.md
```

**检查**:
- Delta 标记：ADDED/MODIFIED/REMOVED
- Scenario 覆盖完整
- 格式正确（当...则...并且...）

---

## 🆘 遇到问题？

### 常见问题快速解决

| 问题 | 解决方法 |
|------|---------|
| 脚本无法运行 | `chmod +x openspec/start-training.sh` |
| 找不到文档 | `ls openspec/*.md` |
| 不知道怎么做 | 阅读 `AGENT_TEAM_QUICKSTART.md` |
| 命令不生效 | 确认在项目根目录 `/Users/zhiledeng/Downloads/FireShot` |

### 获取帮助

```bash
# 查看文档导航
cat openspec/README.md

# 查看快速指南
cat 快速开始_Agent培训.md

# 查看完整指南
cat OPENSPEC_GUIDE.md
```

---

## 🎉 培训完成后

### 你将能够

✅ 独立创建和实施 OpenSpec 变更
✅ 遵循项目编码规范和流程
✅ 与团队协作开发
✅ 维护和优化规范库
✅ 成为 FireShot 核心成员

### 下一步行动

1. **完成 2-3 个真实变更** - 巩固所学
2. **与团队建立协作** - 参与代码审查
3. **优化规范文档** - 提出改进建议
4. **分享经验** - 帮助新成员

---

## 📞 联系方式

- **项目**: FireShot
- **团队**: HawaiiHub AI Team
- **版本**: v1.0.0
- **更新**: 2025-10-28

---

## 🚀 现在就开始！

### 推荐路径（最快）

```bash
# 1. 运行培训脚本
cd /Users/zhiledeng/Downloads/FireShot
./openspec/start-training.sh

# 2. 选择 "1" 开始第 1 天

# 3. 跟随提示完成培训
```

### 或查看快速指南

```bash
cat 快速开始_Agent培训.md
```

---

**🎯 目标**: 3 天成为 OpenSpec 高手！
**🚀 开始**: 运行 `./openspec/start-training.sh`
**💪 信心**: 你一定可以做到！

---

## 📋 完整资源清单

```
FireShot/
├── 🚀立即开始_OpenSpec培训.md          ← 你在这里
├── 快速开始_Agent培训.md               ← 详细指南
├── AGENT_TEAM_OPENSPEC_COMPLETE.md     ← 培训总结
│
├── openspec/
│   ├── start-training.sh               ← 交互式培训 ⭐
│   ├── README.md                       ← 文档导航
│   ├── AGENT_TEAM_QUICKSTART.md       ← 30分钟上手
│   ├── AGENT_ROLES_GUIDE.md           ← 角色分工
│   ├── project.md                      ← 全局规范
│   │
│   └── specs/                          ← 规范文档
│       ├── firecrawl-scraper/spec.md
│       └── hawaiihub-data/spec.md
│
├── OPENSPEC_GUIDE.md                   ← 完整指南
├── OPENSPEC_SETUP_COMPLETE.md          ← 配置报告
└── AGENTS.md                           ← AI 规范
```

---

**准备好了吗？让我们开始吧！** 🎉

```bash
./openspec/start-training.sh
```
