# 🚀 GitHub 仓库配置指南

> **项目**: FireShot - Firecrawl 云 API 实践项目
> **仓库**: https://github.com/Poghappy/firecrawlagent
> **更新时间**: 2025-10-28

---

## 📋 目录

- [仓库基本设置](#仓库基本设置)
- [分支保护规则](#分支保护规则)
- [Secrets 配置](#secrets-配置)
- [GitHub Actions 权限](#github-actions-权限)
- [标签管理](#标签管理)
- [Topics 设置](#topics-设置)
- [其他推荐配置](#其他推荐配置)

---

## 仓库基本设置

### 1. General 设置

访问：`Settings` → `General`

#### Features（功能）

- ✅ **Issues**: 启用问题追踪
- ✅ **Discussions**: 启用社区讨论
- ✅ **Projects**: 启用项目管理
- ✅ **Wiki**: 启用 Wiki（可选）
- ✅ **Sponsorships**: 启用赞助（如果需要）

#### Pull Requests（拉取请求）

- ✅ **Allow squash merging**: 允许压缩合并
  - 默认标题：`PR title`
  - 默认消息：`PR body`
- ✅ **Allow merge commits**: 允许合并提交
- ✅ **Allow rebase merging**: 允许变基合并
- ✅ **Always suggest updating pull request branches**: 总是建议更新分支
- ✅ **Automatically delete head branches**: 自动删除已合并的分支

#### Archives（存档）

- ✅ **Include Git LFS objects in archives**: 包含 Git LFS 对象

---

## 分支保护规则

### 1. 保护 main 分支

访问：`Settings` → `Branches` → `Add branch protection rule`

#### Branch name pattern（分支名称模式）

```
main
```

#### Protect matching branches（保护匹配的分支）

##### ✅ Require a pull request before merging（合并前需要 PR）

- **Required approvals**: 1
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners

##### ✅ Require status checks to pass before merging（合并前需要状态检查通过）

- ✅ Require branches to be up to date before merging

**Required status checks**（必需的状态检查）:
- `Python 3.11 测试`
- `Python 3.12 测试`
- `Python 3.13 测试`
- `Node.js 测试`
- `安全审计`
- `文档完整性检查`
- `根目录文档数量检查`

##### ✅ Require conversation resolution before merging（合并前需要解决所有讨论）

##### ✅ Require signed commits（需要签名提交）（推荐）

##### ✅ Require linear history（需要线性历史）

##### ✅ Include administrators（包括管理员）

##### ✅ Restrict who can push to matching branches（限制谁可以推送到匹配的分支）

- 添加允许推送的团队或用户

##### ✅ Allow force pushes（允许强制推送）- 仅对管理员

- Specify who can force push: 仅管理员

##### ❌ Allow deletions（允许删除）- 禁止删除

### 2. 保护 develop 分支（如果使用 Git Flow）

使用与 main 分支相同的设置，但可以降低审查要求：

- **Required approvals**: 1
- 其他设置保持一致

### 3. 保护 release/* 分支模式

Branch name pattern:
```
release/*
```

设置与 main 分支类似，确保发布分支的稳定性。

---

## Secrets 配置

### 1. Repository Secrets

访问：`Settings` → `Secrets and variables` → `Actions`

#### 添加以下 Secrets

点击 `New repository secret` 添加：

1. **FIRECRAWL_API_KEY**
   - Description: Firecrawl 主 API 密钥
   - Value: `fc-your-api-key-here`

2. **FIRECRAWL_API_KEY_BACKUP_1**
   - Description: Firecrawl 备用 API 密钥 1
   - Value: `fc-your-backup-key-1-here`

3. **FIRECRAWL_API_KEY_BACKUP_2**
   - Description: Firecrawl 备用 API 密钥 2
   - Value: `fc-your-backup-key-2-here`

4. **FIRECRAWL_API_KEY_BACKUP_3**
   - Description: Firecrawl 备用 API 密钥 3
   - Value: `fc-your-backup-key-3-here`

5. **CODECOV_TOKEN**（可选）
   - Description: Codecov 代码覆盖率上传令牌
   - Value: 从 https://codecov.io/ 获取

6. **PYPI_API_TOKEN**（如果发布到 PyPI）
   - Description: PyPI 发布令牌
   - Value: 从 https://pypi.org/ 账户设置获取

### 2. Environment Secrets（可选）

如果需要区分不同环境（开发/生产），可以创建 Environments：

`Settings` → `Environments` → `New environment`

- **Development**
  - Protection rules: 无需审批
  - Secrets: 开发环境 API 密钥

- **Production**
  - Protection rules: 需要审批
  - Required reviewers: 添加审批人
  - Secrets: 生产环境 API 密钥

---

## GitHub Actions 权限

### 1. Workflow 权限

访问：`Settings` → `Actions` → `General`

#### Actions permissions（Actions 权限）

- ✅ **Allow all actions and reusable workflows**: 允许所有 Actions

或者选择：
- ⭕ **Allow [organization] and select non-[organization], actions and reusable workflows**

#### Workflow permissions（工作流权限）

- ⭕ **Read and write permissions**: 读写权限
  - ✅ Allow GitHub Actions to create and approve pull requests

或者（更安全）：
- ⭕ **Read repository contents and packages permissions**: 只读权限
  - 需要时使用 `GITHUB_TOKEN` 明确授权

#### Fork pull request workflows（Fork PR 工作流）

- ✅ **Run workflows from fork pull requests**: 运行来自 fork PR 的工作流
  - ⭕ **Require approval for first-time contributors**: 首次贡献者需要批准

---

## 标签管理

### 1. 创建标签

访问：`Issues` → `Labels`

#### 默认标签保留

- `bug` - 🐛 Bug/问题
- `documentation` - 📝 文档改进
- `duplicate` - 重复的 Issue
- `enhancement` - ✨ 新功能或请求
- `good first issue` - 👋 适合新贡献者
- `help wanted` - 🙋 需要帮助

#### 推荐添加的标签

点击 `New label` 添加：

1. **priority: P0**
   - Color: `#d73a4a` (红色)
   - Description: 关键，必须立即处理

2. **priority: P1**
   - Color: `#fbca04` (黄色)
   - Description: 重要，尽快处理

3. **priority: P2**
   - Color: `#0e8a16` (绿色)
   - Description: 正常，按计划处理

4. **priority: P3**
   - Color: `#bfd4f2` (浅蓝)
   - Description: 低优先级，未来考虑

5. **type: feature**
   - Color: `#84b6eb` (蓝色)
   - Description: 新功能

6. **type: fix**
   - Color: `#d93f0b` (橙红)
   - Description: Bug 修复

7. **type: refactor**
   - Color: `#fbca04` (黄色)
   - Description: 代码重构

8. **type: perf**
   - Color: `#1d76db` (深蓝)
   - Description: 性能优化

9. **status: in progress**
   - Color: `#fbca04` (黄色)
   - Description: 正在进行中

10. **status: blocked**
    - Color: `#d73a4a` (红色)
    - Description: 被阻塞

11. **area: firecrawl**
    - Color: `#e99695` (粉红)
    - Description: Firecrawl 相关

12. **area: hawaiihub**
    - Color: `#c2e0c6` (浅绿)
    - Description: HawaiiHub 相关

13. **dependencies**
    - Color: `#0366d6` (蓝色)
    - Description: 依赖更新

14. **security**
    - Color: `#d73a4a` (红色)
    - Description: 安全相关

---

## Topics 设置

### 1. 添加 Topics

访问仓库首页 → `About` 设置（右侧齿轮图标）→ `Topics`

#### 推荐 Topics

```
firecrawl
web-scraping
data-collection
hawaiihub
python
typescript
mcp
cursor-ai
web-crawler
api-client
automation
data-extraction
markdown
llm
ai-tools
```

#### 仓库描述

```
🔥 FireShot - Firecrawl 云 API 最佳实践和 HawaiiHub 数据采集工具。支持 Scrape、Crawl、Batch、Search 等强大功能。
```

#### Website

```
https://firecrawl.dev
```

---

## 其他推荐配置

### 1. Code Security and Analysis

访问：`Settings` → `Code security and analysis`

#### Dependency graph（依赖关系图）
- ✅ **Enable**: 启用依赖关系图

#### Dependabot alerts（Dependabot 警报）
- ✅ **Enable**: 启用 Dependabot 安全警报

#### Dependabot security updates（Dependabot 安全更新）
- ✅ **Enable**: 启用 Dependabot 安全更新

#### Dependabot version updates（Dependabot 版本更新）
- ✅ **Enable**: 已通过 `.github/dependabot.yml` 配置

#### Code scanning（代码扫描）
- ✅ **Set up**: 设置 CodeQL 分析（推荐）

点击 `Set up` → `Default`，GitHub 将自动配置 CodeQL。

#### Secret scanning（密钥扫描）
- ✅ **Enable**: 启用密钥扫描（GitHub Advanced Security 功能，私有仓库需要付费）

### 2. Webhooks（可选）

访问：`Settings` → `Webhooks`

如果需要集成外部服务（如 Slack、Discord），可以添加 Webhook：

1. **Slack 通知**
   - Payload URL: Slack Webhook URL
   - Content type: `application/json`
   - Events: `Issues`, `Pull requests`, `Pushes`

2. **Discord 通知**
   - Payload URL: Discord Webhook URL + `/github`
   - Content type: `application/json`
   - Events: `Issues`, `Pull requests`, `Pushes`

### 3. Pages（GitHub Pages）（可选）

访问：`Settings` → `Pages`

如果要发布文档到 GitHub Pages：

1. **Source**: Deploy from a branch
2. **Branch**: `gh-pages` 或 `main`
3. **Folder**: `/docs` 或 `/ (root)`
4. **Custom domain**（可选）: 输入自定义域名

### 4. Discussions 类别

访问：`Discussions` → `Categories` → 设置图标

#### 推荐类别

1. **Announcements** 📣
   - Description: 项目公告和重要更新
   - Format: Announcement

2. **General** 💬
   - Description: 一般讨论
   - Format: Discussion

3. **Ideas** 💡
   - Description: 功能想法和建议
   - Format: Discussion

4. **Q&A** ❓
   - Description: 问题和解答
   - Format: Question/Answer

5. **Show and tell** 🎉
   - Description: 分享您的项目和成果
   - Format: Discussion

### 5. Project 模板（可选）

访问：`Projects` → `New project`

#### 推荐模板

1. **Team backlog** - 团队待办事项
2. **Bug tracking** - Bug 追踪
3. **Feature planning** - 功能规划

---

## ✅ 配置完成检查清单

### 基本设置
- [ ] 启用 Issues、Discussions、Projects
- [ ] 配置 PR 设置（自动删除已合并分支）
- [ ] 设置仓库描述和 Topics

### 安全配置
- [ ] 配置 main 分支保护规则
- [ ] 添加所有必需的 Secrets
- [ ] 启用 Dependabot alerts 和 updates
- [ ] 启用 Secret scanning（如果可用）
- [ ] 设置 CodeQL 代码扫描

### Actions 配置
- [ ] 配置 Workflow 权限
- [ ] 设置 Fork PR 工作流策略
- [ ] 验证 CI/CD 工作流正常运行

### 社区配置
- [ ] 创建标签系统
- [ ] 设置 Discussions 类别
- [ ] 配置 Webhooks（如果需要）

### 高级配置
- [ ] 设置 Environments（如果需要）
- [ ] 配置 GitHub Pages（如果需要）
- [ ] 创建 Project 看板

---

## 🔍 验证配置

### 1. 测试 CI/CD

创建一个测试分支并提交 PR：

```bash
git checkout -b test/ci-validation
echo "# Test CI" >> test_ci.md
git add test_ci.md
git commit -m "test(ci): 验证 CI/CD 工作流"
git push origin test/ci-validation
```

在 GitHub 上创建 PR，检查：
- ✅ 所有 CI 检查都运行
- ✅ 状态检查显示在 PR 中
- ✅ 分支保护规则生效

### 2. 测试 Dependabot

等待 Dependabot 自动创建 PR（通常在配置后几分钟内），检查：
- ✅ Dependabot PR 自动创建
- ✅ PR 描述清晰
- ✅ 标签正确应用

### 3. 测试安全扫描

推送一个包含潜在密钥的提交（测试用）：

```bash
# 注意：这只是测试，不要提交真实密钥
echo "API_KEY=test-fake-key-12345" > test_secret.txt
git add test_secret.txt
git commit -m "test: 测试密钥扫描"
git push
```

检查：
- ✅ Secret scanning 检测到潜在密钥
- ✅ 收到安全警报

**记得删除测试文件**：
```bash
git rm test_secret.txt
git commit -m "chore: 删除测试文件"
git push
```

---

## 📊 仓库健康度评分

完成上述配置后，您的仓库应该达到：

| 指标 | 目标 | 说明 |
|------|------|------|
| **Community Standards** | 100% | LICENSE、README、CONTRIBUTING、CODE_OF_CONDUCT、SECURITY 全部存在 |
| **Branch Protection** | ✅ | main 分支已保护 |
| **CI/CD** | ✅ | GitHub Actions 配置完整 |
| **Security** | ✅ | Dependabot、Secret scanning、CodeQL 已启用 |
| **Documentation** | ✅ | 文档完整且最新 |

检查仓库健康度：
- 访问：`Insights` → `Community Standards`

---

## 🎯 最佳实践总结

### 1. 分支策略
- **main**: 生产分支，只接受 PR 合并
- **develop**: 开发分支（可选）
- **feature/***: 功能分支
- **fix/***: 修复分支
- **hotfix/***: 紧急修复分支

### 2. PR 工作流
1. 创建功能分支
2. 开发和测试
3. 创建 PR
4. 通过 CI 检查
5. 代码审查
6. 合并到 main
7. 自动删除分支

### 3. 发布流程
1. 更新 CHANGELOG.md
2. 创建版本标签（`v1.0.0`）
3. 推送标签：`git push --tags`
4. GitHub Actions 自动创建 Release

### 4. 安全规范
- ✅ 所有密钥存储在 Secrets
- ✅ 启用分支保护
- ✅ 启用 2FA（两因素认证）
- ✅ 定期审查权限
- ✅ 及时更新依赖

---

## 📞 获取帮助

### 官方文档
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [分支保护规则](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Secrets 管理](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql)

### 项目文档
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [SECURITY.md](../SECURITY.md)
- [CI/CD 工作流](../.github/workflows/)

---

**维护者**: HawaiiHub AI Team
**最后更新**: 2025-10-28
**仓库**: https://github.com/Poghappy/firecrawlagent

🎉 恭喜！您的 GitHub 仓库已按照业界最佳实践完成配置！
