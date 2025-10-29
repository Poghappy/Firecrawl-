# 🚀 GitHub 完整配置指南

## 📋 文档说明

本文档整合了所有 GitHub 相关配置信息，包括仓库设置、Secrets 配置、Actions 启用等完整指南。

**整合自以下文档**:

- GITHUB_SETUP.md
- GITHUB_SECRETS_SETUP.md
- github/GITHUB_CONFIGURATION_SUMMARY.md
- github/GITHUB_ACTIONS_FIX_REPORT.md
- github/GITHUB_SETUP_COMPLETE.md
- 其他 GitHub 相关配置文档

---

## 🎯 快速导航

1. [GitHub Secrets 配置](#1-github-secrets配置)
2. [GitHub Actions 启用](#2-github-actions启用)
3. [Docker Hub 集成](#3-docker-hub集成)
4. [工作流验证](#4-工作流验证)
5. [故障排除](#5-故障排除)
6. [配置检查清单](#6-配置检查清单)

---

## 1. GitHub Secrets 配置

### 1.1 访问 Secrets 设置

1. 进入仓库：<https://github.com/Poghappy/Firecrawl->
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 添加新的密钥

### 1.2 必需的 Secrets

#### 核心 API 密钥

| Secret 名称         | 描述               | 获取方式                                    | 必需性  |
| ------------------- | ------------------ | ------------------------------------------- | ------- |
| `FIRECRAWL_API_KEY` | Firecrawl API 密钥 | [Firecrawl 控制台](https://firecrawl.dev/)  | ✅ 必需 |
| `OPENAI_API_KEY`    | OpenAI API 密钥    | [OpenAI 平台](https://platform.openai.com/) | ⚠️ 可选 |

#### Docker Hub 配置

| Secret 名称       | 描述                | 获取方式                              | 必需性  |
| ----------------- | ------------------- | ------------------------------------- | ------- |
| `DOCKER_USERNAME` | Docker Hub 用户名   | [Docker Hub](https://hub.docker.com/) | ✅ 必需 |
| `DOCKER_PASSWORD` | Docker Hub 访问令牌 | Docker Hub 设置                       | ✅ 必需 |

#### 数据库配置（生产环境）

| Secret 名称    | 描述                | 示例值                                | 必需性  |
| -------------- | ------------------- | ------------------------------------- | ------- |
| `DATABASE_URL` | PostgreSQL 连接 URL | `postgresql://user:pass@host:port/db` | ⚠️ 可选 |
| `REDIS_URL`    | Redis 连接 URL      | `redis://user:pass@host:port`         | ⚠️ 可选 |

#### 通知配置

| Secret 名称           | 描述                 | 必需性  |
| --------------------- | -------------------- | ------- |
| `SLACK_WEBHOOK_URL`   | Slack 通知 Webhook   | ⚠️ 可选 |
| `DISCORD_WEBHOOK_URL` | Discord 通知 Webhook | ⚠️ 可选 |

### 1.3 添加 Secrets 步骤

```bash
# 1. 获取API密钥
# - Firecrawl: https://firecrawl.dev/
# - Docker Hub: https://hub.docker.com/settings/security

# 2. 在GitHub仓库中添加
# Settings → Secrets and variables → Actions → New repository secret

# 3. 逐个添加以下Secrets:
FIRECRAWL_API_KEY=fc-xxxxxxxxxxxx
DOCKER_USERNAME=your_username
DOCKER_PASSWORD=your_access_token
```

---

## 2. GitHub Actions 启用

### 2.1 配置工作流权限

1. 进入 **Settings** → **Actions** → **General**
2. 在 **Workflow permissions** 部分：
   - ✅ 选择 **Read and write permissions**
   - ✅ 勾选 **Allow GitHub Actions to create and approve pull requests**
3. 点击 **Save**

### 2.2 已配置的工作流

#### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

- ✅ 多 Python 版本测试 (3.9, 3.10, 3.11, 3.12)
- ✅ 代码质量检查 (black, ruff, flake8, mypy)
- ✅ 自动化测试和覆盖率报告
- ✅ 代码安全扫描

#### Docker Build (`.github/workflows/docker-build.yml`)

- ✅ 自动构建 Docker 镜像
- ✅ 推送到 GitHub Container Registry
- ✅ 多架构支持 (amd64, arm64)
- ✅ 镜像标签管理

### 2.3 触发工作流

```bash
# 方法1: 推送代码
git add .
git commit -m "feat: trigger CI/CD"
git push origin main

# 方法2: 创建Pull Request
git checkout -b feature/test
git push origin feature/test
# 在GitHub上创建PR

# 方法3: 手动触发（如果配置了workflow_dispatch）
# 在Actions标签页点击工作流，然后点击"Run workflow"
```

---

## 3. Docker Hub 集成

### 3.1 创建 Docker Hub 仓库

1. 访问 [Docker Hub](https://hub.docker.com/)
2. 点击 **Repositories** → **Create Repository**
3. 填写仓库信息：
   - Repository Name: `firecrawl-collector`
   - Description: `Firecrawl数据采集器 - 智能网页内容监控和采集系统`
   - Visibility: Public 或 Private
4. 点击 **Create**

### 3.2 生成访问令牌

1. 进入 **Account Settings** → **Security**
2. 点击 **New Access Token**
3. 填写令牌信息：
   - Token Description: `GitHub Actions`
   - Access permissions: **Read, Write, Delete**
4. 点击 **Generate**
5. **立即复制令牌**（稍后无法再查看）

### 3.3 配置 GitHub Secrets

将生成的令牌添加到 GitHub 仓库的 Secrets 中：

- `DOCKER_USERNAME`: 你的 Docker Hub 用户名
- `DOCKER_PASSWORD`: 刚才生成的访问令牌

### 3.4 验证 Docker 构建

```bash
# 1. 推送代码触发构建
git push origin main

# 2. 在Actions标签查看构建状态
# https://github.com/Poghappy/Firecrawl-/actions

# 3. 构建成功后，在Docker Hub检查镜像
# https://hub.docker.com/r/your_username/firecrawl-collector
```

---

## 4. 工作流验证

### 4.1 验证 Secrets 配置

运行验证脚本：

```bash
python scripts/github-actions/verify-github-secrets.py
```

### 4.2 验证工作流配置

```bash
python scripts/github-actions/verify-github-config.py
```

### 4.3 手动测试工作流

```bash
# 创建测试提交
git commit --allow-empty -m "test: verify GitHub Actions"
git push origin main

# 查看工作流执行
# https://github.com/Poghappy/Firecrawl-/actions
```

### 4.4 检查构建状态

在 GitHub 仓库的 README.md 中可以看到构建状态徽章：

- [![CI/CD](badge_url)](actions_url)
- [![Docker](badge_url)](docker_url)

---

## 5. 故障排除

### 5.1 常见问题

#### Problem: Actions 工作流失败 - "Error: Docker login failed"

**原因**: Docker Hub 密钥配置错误

**解决方案**:

1. 检查`DOCKER_USERNAME`和`DOCKER_PASSWORD`是否正确
2. 确认使用的是访问令牌，不是密码
3. 验证令牌权限包含读写权限

#### Problem: 工作流失败 - "Permission denied"

**原因**: GitHub Actions 权限不足

**解决方案**:

1. 进入 Settings → Actions → General
2. 选择"Read and write permissions"
3. 勾选"Allow GitHub Actions to create and approve pull requests"

#### Problem: Docker 镜像推送失败

**原因**: 镜像标签格式或仓库名称错误

**解决方案**:

1. 检查 docker-build.yml 中的镜像标签格式
2. 确认 Docker Hub 仓库已创建
3. 验证仓库名称匹配

#### Problem: 测试失败 - 找不到模块

**原因**: 依赖安装问题

**解决方案**:

1. 检查 requirements.txt 是否完整
2. 验证 Python 版本兼容性
3. 查看工作流日志中的具体错误信息

### 5.2 调试技巧

```bash
# 1. 查看工作流日志
# 在Actions标签页点击失败的工作流，查看详细日志

# 2. 本地复现问题
docker build -t test-image .
docker run test-image pytest

# 3. 检查环境变量
echo $FIRECRAWL_API_KEY | wc -c  # 确认密钥长度

# 4. 验证Secrets可见性
# 在工作流中添加调试步骤（注意不要打印敏感信息）:
# - name: Debug
#   run: |
#     echo "Secrets configured: ${{ secrets.FIRECRAWL_API_KEY != '' }}"
```

### 5.3 获取帮助

- 📋 **GitHub Issues**: [报告问题](https://github.com/Poghappy/Firecrawl-/issues)
- 💬 **Discussions**: [参与讨论](https://github.com/Poghappy/Firecrawl-/discussions)
- 📖 **文档**: 查看项目文档目录

---

## 6. 配置检查清单

### 6.1 基础配置

- [ ] GitHub 仓库已创建
- [ ] README.md 已更新
- [ ] LICENSE 文件已添加
- [ ] .gitignore 已配置

### 6.2 Secrets 配置

- [ ] FIRECRAWL_API_KEY 已添加
- [ ] DOCKER_USERNAME 已添加
- [ ] DOCKER_PASSWORD 已添加
- [ ] 其他可选 Secrets 已根据需要添加

### 6.3 GitHub Actions

- [ ] 工作流权限已设置为"Read and write"
- [ ] 允许 Actions 创建 PR 已勾选
- [ ] CI/CD 工作流可以正常运行
- [ ] Docker 构建工作流可以正常运行

### 6.4 Docker Hub

- [ ] Docker Hub 仓库已创建
- [ ] 访问令牌已生成
- [ ] 令牌已添加到 GitHub Secrets
- [ ] 镜像可以成功推送

### 6.5 验证测试

- [ ] 运行验证脚本通过
- [ ] 推送代码触发工作流成功
- [ ] Docker 镜像构建成功
- [ ] 所有测试通过

---

## 📊 配置完成状态

### ✅ 已完成配置

1. **GitHub 仓库设置** ✅

   - 基础配置完成
   - 分支保护规则
   - 协作者权限

2. **Secrets 管理** ✅

   - API 密钥配置
   - Docker Hub 认证
   - 环境变量管理

3. **GitHub Actions** ✅

   - CI/CD 流水线
   - Docker 自动构建
   - 代码质量检查

4. **Docker 集成** ✅

   - Docker Hub 仓库
   - 自动构建推送
   - 多架构支持

5. **文档体系** ✅
   - API 文档
   - 部署指南
   - 贡献指南

### 🔄 可选增强

- [ ] 配置 GitHub Pages 文档站点
- [ ] 添加代码覆盖率报告
- [ ] 集成安全扫描工具
- [ ] 配置自动发布流程
- [ ] 添加性能基准测试

---

## 🎉 配置完成

恭喜！您的 Firecrawl 数据采集器项目 GitHub 配置已全部完成。

### 下一步建议

1. **开始开发**

   ```bash
   git checkout -b feature/your-feature
   # 开发你的功能
   git push origin feature/your-feature
   # 创建Pull Request
   ```

2. **监控工作流**

   - 定期检查 Actions 运行状态
   - 关注构建失败通知
   - 及时更新依赖和配置

3. **完善文档**

   - 添加使用示例
   - 更新 API 文档
   - 编写最佳实践

4. **社区建设**
   - 回应 Issues 和 PR
   - 维护贡献指南
   - 发布版本更新

---

**文档维护者**: AI 全栈工程师
**最后更新**: 2024-10-29
**版本**: v2.0
**状态**: ✅ 完整版
