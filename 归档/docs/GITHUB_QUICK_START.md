# ⚡ GitHub 仓库快速配置指南

> **5 分钟完成核心配置**
> **项目**: FireShot - Firecrawl 云 API 实践项目
> **仓库**: https://github.com/Poghappy/firecrawlagent

---

## 🎯 核心配置（必须完成）

### 1️⃣ 添加 API 密钥（2 分钟）

**路径**: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

```
FIRECRAWL_API_KEY=fc-your-api-key-here
```

### 2️⃣ 启用分支保护（2 分钟）

**路径**: `Settings` → `Branches` → `Add branch protection rule`

**Branch name pattern**: `main`

必选项：
- ✅ Require a pull request before merging
  - Required approvals: 1
- ✅ Require status checks to pass before merging
  - Python 3.11 测试
  - Python 3.12 测试
  - Python 3.13 测试
- ✅ Require conversation resolution before merging

### 3️⃣ 启用安全功能（1 分钟）

**路径**: `Settings` → `Code security and analysis`

- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates

---

## 📝 推荐配置（建议完成）

### 4️⃣ 添加 Topics

**路径**: 仓库首页 → `About` 设置（齿轮图标）

```
firecrawl web-scraping data-collection hawaiihub python typescript
```

### 5️⃣ 创建基本标签

**路径**: `Issues` → `Labels` → `New label`

快速创建：
- `priority: P0` (红色 `#d73a4a`)
- `priority: P1` (黄色 `#fbca04`)
- `type: feature` (蓝色 `#84b6eb`)
- `type: fix` (橙红 `#d93f0b`)

---

## ✅ 验证配置

### 测试 CI/CD

```bash
# 创建测试分支
git checkout -b test/ci
echo "# Test" >> test.md
git add test.md
git commit -m "test(ci): 验证 CI 工作流"
git push origin test/ci
```

然后在 GitHub 创建 PR，检查：
- ✅ CI 工作流自动运行
- ✅ 状态检查显示在 PR 中

---

## 🔗 完整配置指南

详细配置步骤请参考：[GITHUB_REPOSITORY_SETUP.md](./GITHUB_REPOSITORY_SETUP.md)

---

## 📞 需要帮助？

- 📖 [GitHub 官方文档](https://docs.github.com/en)
- 💬 [项目 Issues](https://github.com/Poghappy/firecrawlagent/issues)
- 📚 [贡献指南](../CONTRIBUTING.md)

---

**维护者**: HawaiiHub AI Team
**最后更新**: 2025-10-28

🚀 快速配置完成！开始使用 FireShot 吧！
