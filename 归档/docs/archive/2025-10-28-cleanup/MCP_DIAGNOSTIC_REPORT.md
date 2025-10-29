# MCP 工具诊断报告

**生成时间**: 2025-10-27
**问题**: Cursor 显示功能减少（仅 2 个 MCP 资源）
**状态**: ✅ 配置文件完整，27 个服务器已配置

---

## 📊 配置文件状态

### 文件位置
```
~/.cursor/mcp.json
```

### 配置完整度
- ✅ 27 个 MCP 服务器已配置
- ✅ Firecrawl API Key 已设置
- ✅ GitHub Token 已设置
- ⚠️ 部分服务器缺少 API Key（Postman、Tinybird 等已禁用）

---

## 🔍 诊断结果

### 可能的故障原因

1. **Docker 服务未启动**（5 个服务器依赖 Docker）
   - fetch
   - docker
   - time
   - sequentialthinking
   - 需要检查：`docker ps` 是否正常

2. **npx 网络问题**（19 个服务器依赖 npx）
   - 首次运行需要下载包
   - 可能被网络防火墙阻止
   - 建议：检查 `npx --version`

3. **Cursor 内部加载失败**
   - MCP 服务器启动超时
   - Cursor 日志中可能有错误信息

---

## ✅ 修复步骤

### Step 1: 重启 Cursor MCP 服务

**方法 1: 通过 Cursor 命令面板**
1. 按 `Cmd+Shift+P` 打开命令面板
2. 输入 "Reload MCP Servers"
3. 回车执行

**方法 2: 完全重启 Cursor**
1. 退出 Cursor（`Cmd+Q`）
2. 打开 "活动监视器"，确保 Cursor 进程完全关闭
3. 重新启动 Cursor

### Step 2: 验证 Docker 状态

```bash
# 检查 Docker 是否运行
docker ps

# 如果失败，启动 Docker Desktop
open -a Docker

# 等待 Docker 完全启动（约 30 秒）
```

### Step 3: 预热 MCP 服务器（可选）

如果重启后仍有问题，手动测试关键服务器：

```bash
# 测试 Firecrawl
npx -y firecrawl-mcp --version

# 测试 Playwright
npx -y @playwright/mcp@latest --version

# 测试 GitHub
npx -y @modelcontextprotocol/server-github --version

# 测试 Context7
curl -I https://mcp.context7.com/mcp
```

### Step 4: 查看 Cursor 日志

如果问题持续：

1. 打开 Cursor 开发者工具：`Cmd+Option+I`
2. 切换到 "Console" 标签
3. 搜索关键词：`mcp`、`error`、`failed`
4. 复制错误信息进行进一步诊断

---

## 🚑 应急备份配置

如果需要重新配置，备份文件已保存：

```bash
# 备份当前配置
cp ~/.cursor/mcp.json ~/.cursor/mcp.backup.json

# 如果需要恢复
cp ~/.cursor/mcp.backup.json ~/.cursor/mcp.json
```

---

## 📞 进一步帮助

如果问题仍未解决，收集以下信息：

1. **Cursor 版本**
   - 菜单栏：Cursor → About Cursor

2. **系统环境**
   ```bash
   # Docker 版本
   docker --version

   # Node.js 版本
   node --version

   # npx 版本
   npx --version
   ```

3. **Cursor 日志片段**
   - 开发者工具（`Cmd+Option+I`）中的 MCP 相关错误

---

## 🎯 预期结果

修复后，在 Cursor 命令面板（`/`）中应该看到：

- ✅ Firecrawl 工具（scrape、crawl、map、search、extract）
- ✅ GitHub 工具（仓库、Issue、PR 管理）
- ✅ Playwright 工具（浏览器自动化）
- ✅ 文件系统工具（读写文件）
- ✅ Notion、Supabase 等其他工具

总计约 **100+ 个可用工具函数**。

---

**报告生成完毕** | 下一步：执行 Step 1（重启 MCP 服务）
