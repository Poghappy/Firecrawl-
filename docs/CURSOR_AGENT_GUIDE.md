# Cursor Agent 开发最佳实践指南

## 🎯 概述

本指南为Firecrawl数据采集器项目建立了完整的Cursor Agent开发最佳实践体系，实现了从用户故事到迭代优化的完整产品/研发链路。

## 📋 项目概览

### 核心价值
- **智能采集**: 基于AI的内容过滤和重要性分析
- **高效处理**: 异步并发处理，支持大规模数据采集
- **灵活集成**: 支持多种数据源和输出格式
- **自动化运维**: 完整的监控、告警和部署自动化

### 技术栈
- **后端**: Python 3.13+, FastAPI, SQLAlchemy, Redis
- **数据库**: PostgreSQL, Redis
- **监控**: Prometheus, Grafana
- **部署**: Docker, Docker Compose
- **AI集成**: OpenAI API, LangChain

## 🏗️ 工程化基座

### 1. 统一开发环境
```bash
# 一键环境设置
make setup          # 创建虚拟环境
make install        # 安装依赖
make dev           # 开发环境设置
```

### 2. 质量闸口（本地即可跑）
```bash
# 代码质量检查
make lint          # 代码风格&静态检查
make format        # 自动格式化
make test          # 运行所有测试
make cov           # 生成覆盖率报告
```

### 3. 结构化仓库
```
├─ docs/                    # 项目文档
│  ├─ PROJECT_BRIEF.md      # 项目概览
│  ├─ USER_STORIES.md       # 用户故事集合
│  ├─ PRD.md               # 需求文档
│  ├─ TECH_DESIGN.md       # 技术设计文档
│  ├─ TEST_PLAN.md         # 测试计划
│  └─ CHANGELOG.md         # 变更记录
├─ prompts/                 # 提示词模板
│  ├─ 00_guidelines.md      # 通用开发规范
│  ├─ 10_user_story.md      # 用户故事模板
│  ├─ 20_prd.md            # PRD模板
│  ├─ 30_task_breakdown.md  # 任务分解模板
│  ├─ 40_tech_design.md    # 技术设计模板
│  ├─ 50_impl.md           # 实现模板
│  ├─ 60_test.md           # 测试模板
│  └─ 70_iteration.md      # 迭代模板
├─ src/                     # 源代码
├─ tests/                   # 测试代码
├─ scripts/                 # 工具脚本
├─ config/                  # 配置文件
├─ Makefile                 # 一键命令
├─ .pre-commit-config.yaml  # 提交前检查
└─ CONTRIBUTING.md          # 贡献指南
```

## 🔄 提示词架构

### 七步工作流
1. **用户故事** → 2. **需求文档** → 3. **任务分解** → 4. **技术方案** → 5. **实现** → 6. **测试** → 7. **迭代**

### 模板使用方式
```markdown
# 在Cursor Chat中使用
请使用 <USER_STORY> 阶段模板，基于以下输入生成用户故事：
[输入内容]

# 或直接引用模板
请参考 prompts/10_user_story.md 模板生成用户故事
```

## 🛠️ 操作型工作流

### 1. "小步快跑，步步有据"循环
- **第一步**: Agent产出"计划与影响面" → 审看
- **第二步**: 限定"只改动X个文件，合计不超过N行" → 降低风险  
- **第三步**: "先测后并" → 先生成/更新测试，再实现

### 2. 文件写入规则
- **新文件**: 必须列在"变更清单"
- **每次回复**: 最前给出"文件树Diff"
- **变更验证**: 必须可通过 `make lint && make test` 验证
- **配置安全**: 涉及配置/密钥只写 `.env.example`

### 3. Commit规范
```
<type>[optional scope]: <description>

feat(api): add user authentication endpoint
fix(collector): handle timeout errors gracefully
docs(readme): update installation instructions
test(unit): add tests for data processor
```

## 🔧 工具与适配

### 1. 一键命令封装
```bash
# 开发流程
make dev-loop        # 格式化→检查→测试
make check-all       # 运行所有检查
make release-prep    # 发布准备

# 部署运维
make build          # 构建Docker镜像
make deploy         # 部署到生产环境
make logs           # 查看应用日志
```

### 2. 质量保证工具
- **代码格式化**: Black, Ruff, isort
- **静态检查**: MyPy, Flake8, Bandit
- **测试框架**: Pytest, pytest-cov, pytest-asyncio
- **安全扫描**: Safety, pip-audit

### 3. CI/CD自动化
- **代码质量**: 自动lint检查
- **测试执行**: 单元测试、集成测试、端到端测试
- **性能测试**: 基准测试和性能回归检测
- **自动部署**: 测试环境、生产环境自动部署

## 📊 度量与验收

### 1. 过程指标
- **通过率**: 每次Agent回合的lint/test/格式通过率
- **修复回合数**: 平均需要几轮修复才能通过
- **响应时间**: Agent响应和代码生成时间

### 2. 结果指标
- **需求覆盖率**: 用户故事↔验收用例1:1映射
- **缺陷密度**: 每千行代码的缺陷数量
- **首次可运行时间**: Time-to-First-Green

### 3. 质量门槛
- **代码覆盖率**: ≥80%
- **测试覆盖率**: 单元测试≥80%，集成测试≥60%
- **性能指标**: API响应≤2秒，采集时间≤30秒
- **安全指标**: 无高危漏洞，敏感信息保护

## 🚀 多项目复用

### 1. 模板仓库
将以下文件抽成Template Repo：
- `docs/*` - 项目文档模板
- `prompts/*` - 提示词模板
- `Makefile` - 一键命令
- `.pre-commit-config.yaml` - 质量检查
- `CONTRIBUTING.md` - 开发规范

### 2. 新项目快速启动
```bash
# 1. 拷贝模板
git clone https://github.com/dengzhilehappy/01-active-projects.git new-project

# 2. 填写项目信息
# 编辑 docs/PROJECT_BRIEF.md
# 编辑 .env.example

# 3. 让Agent按阶段执行
# 使用系统提示词开始开发
```

### 3. GitHub仓库配置
当前项目已配置完整的GitHub功能：
- **CI/CD**: 自动化的构建、测试、部署流程
- **Issue模板**: Bug报告和功能请求模板
- **PR模板**: 标准化的代码审查流程
- **安全策略**: 安全漏洞报告和处理流程
- **依赖管理**: Dependabot自动依赖更新
- **代码所有者**: CODEOWNERS文件管理代码审查权限

### 3. 变量化配置
使用占位符便于批量替换：
- `{PROJECT_NAME}` - 项目名称
- `{BUSINESS_DOMAIN}` - 业务领域
- `{PERFORMANCE_TARGET}` - 性能目标

## 📝 使用指南

### 1. 环境设置
```bash
# 克隆项目
git clone <repository-url>
cd Firecrawl数据采集器

# 设置环境
make setup
source firecrawl_env/bin/activate
make install
make dev
```

### 2. 开发流程
```bash
# 日常开发循环
make dev-loop        # 格式化→检查→测试

# 功能开发
# 1. 使用对应阶段模板
# 2. 按提示词要求生成代码
# 3. 运行测试验证
# 4. 提交代码
```

### 3. 质量检查
```bash
# 提交前检查
make check-all

# 生成报告
make cov            # 覆盖率报告
make docs           # 生成文档
```

## 🎯 最佳实践总结

### 1. 工程化原则
- **一致性**: 统一的环境、工具、流程
- **自动化**: 尽可能自动化重复性工作
- **可观测**: 完整的日志、监控、告警
- **可复现**: 任何环境都能快速搭建

### 2. 开发原则
- **小步快跑**: 每次改动小而精
- **测试驱动**: 先写测试，再写实现
- **文档同步**: 代码和文档同步更新
- **持续集成**: 每次提交触发质量检查

### 3. 协作原则
- **规范统一**: 统一的代码规范和提交规范
- **透明可见**: 所有过程可追踪、可审计
- **知识共享**: 及时更新文档和最佳实践
- **持续改进**: 定期回顾和优化流程

## 🔗 相关资源

### 项目文档
- [项目概览](PROJECT_BRIEF.md)
- [开发规范](../prompts/00_guidelines.md)
- [API文档](API_DOCUMENTATION.md)
- [部署指南](DEPLOYMENT_GUIDE.md)

### 外部资源
- [Cursor官方文档](https://cursor.com/docs)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Python最佳实践](https://docs.python.org/3/tutorial/)
- [Docker文档](https://docs.docker.com/)

## 📞 支持与反馈

如有问题或建议，请：
1. 查看项目文档
2. 提交Issue
3. 参与讨论
4. 联系维护者

---

**🎉 恭喜！您现在拥有了一套完整的Cursor Agent开发最佳实践体系，可以快速产出高质量成果并在不同项目间复用。**
