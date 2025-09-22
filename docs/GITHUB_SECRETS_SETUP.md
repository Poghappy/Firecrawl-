# 🔐 GitHub Secrets配置指南

## 📋 配置概览

本指南将帮助您完成GitHub Secrets和Actions的配置，确保CI/CD工作流能够正常运行。

## 🎯 配置目标

- ✅ 配置GitHub Secrets用于API认证
- ✅ 启用GitHub Actions的读写权限
- ✅ 验证Docker Hub集成
- ✅ 测试CI/CD工作流

## 🔑 第一步：配置GitHub Secrets

### 1.1 进入仓库设置

访问您的GitHub仓库设置页面：
```
https://github.com/Poghappy/Firecrawl-/settings/secrets/actions
```

### 1.2 添加必需的Secrets

点击 **"New repository secret"** 按钮，依次添加以下Secrets：

#### 🔑 FIRECRAWL_API_KEY
- **Name**: `FIRECRAWL_API_KEY`
- **Value**: 您的Firecrawl API密钥
- **用途**: 用于访问Firecrawl API服务
- **获取方式**: 访问 [Firecrawl.dev](https://firecrawl.dev/) 注册并获取API密钥

#### 🐳 DOCKER_USERNAME
- **Name**: `DOCKER_USERNAME`
- **Value**: `denzhile`
- **用途**: Docker Hub用户名，用于推送镜像
- **说明**: 这是您的Docker Hub账户用户名

#### 🔒 DOCKER_PASSWORD
- **Name**: `DOCKER_PASSWORD`
- **Value**: `dckr_pat_9zHDbXagx0b60xvwbqRKNIVo_J0`
- **用途**: Docker Hub访问令牌，用于推送镜像
- **说明**: 这是您的Docker Hub访问令牌（不是密码）

### 1.3 可选Secrets（根据需要添加）

#### 🗄️ DATABASE_URL
- **Name**: `DATABASE_URL`
- **Value**: `postgresql://username:password@host:port/database`
- **用途**: 生产环境数据库连接
- **示例**: `postgresql://user:pass@localhost:5432/firecrawl`

#### ⚡ REDIS_URL
- **Name**: `REDIS_URL`
- **Value**: `redis://username:password@host:port/database`
- **用途**: Redis缓存和任务队列
- **示例**: `redis://localhost:6379/0`

#### 📢 SLACK_WEBHOOK_URL
- **Name**: `SLACK_WEBHOOK_URL`
- **Value**: `https://hooks.slack.com/services/...`
- **用途**: Slack通知集成
- **获取方式**: 在Slack中创建Incoming Webhook

#### 💬 DISCORD_WEBHOOK_URL
- **Name**: `DISCORD_WEBHOOK_URL`
- **Value**: `https://discord.com/api/webhooks/...`
- **用途**: Discord通知集成
- **获取方式**: 在Discord服务器中创建Webhook

## 🚀 第二步：启用GitHub Actions

### 2.1 进入Actions设置

访问您的仓库Actions设置页面：
```
https://github.com/Poghappy/Firecrawl-/settings/actions
```

### 2.2 配置工作流权限

在 **"Workflow permissions"** 部分进行以下配置：

#### ✅ 选择 "Read and write permissions"
- 这将允许GitHub Actions读取和写入仓库内容
- 启用Docker镜像构建和推送功能
- 允许工作流修改仓库文件

#### ✅ 勾选 "Allow GitHub Actions to create and approve pull requests"
- 这将允许自动化工作流创建和批准PR
- 启用自动化的代码审查流程
- 支持自动化的依赖更新

### 2.3 保存设置

点击 **"Save"** 按钮保存所有更改。

## 🔍 第三步：验证配置

### 3.1 运行验证脚本

在项目根目录运行验证脚本：
```bash
python3 scripts/verify-github-config.py
```

### 3.2 检查工作流状态

访问GitHub Actions页面查看工作流状态：
```
https://github.com/Poghappy/Firecrawl-/actions
```

### 3.3 测试Docker构建

推送代码到main分支，观察Docker构建是否成功：
```bash
git add .
git commit -m "test: trigger GitHub Actions"
git push origin main
```

## 📊 配置检查清单

### ✅ GitHub Secrets配置
- [ ] FIRECRAWL_API_KEY 已添加
- [ ] DOCKER_USERNAME 已添加
- [ ] DOCKER_PASSWORD 已添加
- [ ] 可选Secrets根据需要添加

### ✅ GitHub Actions配置
- [ ] 已启用 "Read and write permissions"
- [ ] 已启用 "Allow GitHub Actions to create and approve pull requests"
- [ ] 设置已保存

### ✅ 验证测试
- [ ] 验证脚本运行成功
- [ ] GitHub Actions工作流正常运行
- [ ] Docker镜像构建成功
- [ ] 所有测试通过

## 🚨 常见问题解决

### 问题1：Docker推送失败
**错误**: `denied: requested access to the resource is denied`

**解决方案**:
1. 检查DOCKER_USERNAME是否正确
2. 检查DOCKER_PASSWORD是否为访问令牌（不是密码）
3. 确认Docker Hub仓库已创建

### 问题2：Firecrawl API调用失败
**错误**: `401 Unauthorized`

**解决方案**:
1. 检查FIRECRAWL_API_KEY是否正确
2. 确认API密钥未过期
3. 检查API使用配额

### 问题3：GitHub Actions权限不足
**错误**: `Resource not accessible by integration`

**解决方案**:
1. 确认已启用 "Read and write permissions"
2. 检查仓库权限设置
3. 重新保存Actions设置

## 🔗 相关链接

- **仓库设置**: [GitHub Settings](https://github.com/Poghappy/Firecrawl-/settings)
- **Secrets配置**: [Actions Secrets](https://github.com/Poghappy/Firecrawl-/settings/secrets/actions)
- **Actions设置**: [Actions General](https://github.com/Poghappy/Firecrawl-/settings/actions)
- **工作流状态**: [GitHub Actions](https://github.com/Poghappy/Firecrawl-/actions)
- **Docker Hub**: [Docker Hub Repository](https://hub.docker.com/r/denzhile/firecrawl)

## 📝 配置完成确认

完成所有配置后，您应该能够：

1. ✅ 在GitHub Actions中看到工作流运行
2. ✅ Docker镜像成功构建并推送到Docker Hub
3. ✅ 所有测试和代码质量检查通过
4. ✅ 收到构建状态通知（如果配置了通知）

## 🎉 恭喜！

您的Firecrawl数据采集器项目现在已经完全配置好了GitHub集成！

### 下一步建议：
1. 推送代码触发第一次CI/CD运行
2. 监控构建状态和日志
3. 根据需要调整工作流配置
4. 开始核心功能开发

---

**配置完成时间**: 2024年9月21日  
**配置状态**: ✅ 完成  
**维护者**: AI全栈工程师
