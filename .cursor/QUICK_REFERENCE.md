# Cursor 配置快速参考

## 🚀 快速开始

### 配置文件位置

**主配置文件**: `/.cursorrules`（项目根目录）

这是 Cursor 官方推荐的标准配置文件，AI 助手会自动读取。

### 一分钟了解规则

```
✅ 使用简体中文
✅ 优先使用 MCP 工具
✅ 小步快跑，每次 ≤5 个文件
✅ 先读后写，立即验证
✅ 遵循 PEP 8 + Black + async/await
✅ 测试覆盖率 >80%
✅ 敏感信息用环境变量

❌ 禁止硬编码密钥
❌ 禁止大规模重写
❌ 禁止跳过测试
❌ 禁止中文文件名
```

## 📋 常用命令

### 开发工作流

```bash
# 1. 激活虚拟环境
source activate_env.sh

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
pytest tests/

# 4. 代码格式化
black src/
isort src/

# 5. 启动服务
python src/api_server.py
```

### Git 提交

```bash
# 提交格式
feat: 添加新功能
fix: 修复 Bug
docs: 更新文档
style: 代码格式调整
refactor: 重构代码
test: 添加测试
chore: 构建/工具更新
```

## 📁 重要文件

| 文件                   | 用途               |
| ---------------------- | ------------------ |
| `/.cursorrules`        | AI 助手规则配置    |
| `/project_status.md`   | 项目当前状态       |
| `/docs/official-docs/` | Firecrawl 官方文档 |
| `/docs/API.md`         | API 接口文档       |
| `/DEPLOYMENT.md`       | 部署指南           |
| `/.env.example`        | 环境变量模板       |

## 🔧 配置管理

### 修改规则

1. 编辑 `/.cursorrules` 文件
2. 保存后 AI 自动应用新规则
3. 保持规则简洁（建议 <100 行）

### 查看详细说明

- **配置说明**: `.cursor/README.md`
- **升级指南**: `.cursor/CURSOR_RULES_UPGRADE.md`
- **优化报告**: `.cursor/OPTIMIZATION_REPORT.md`

## 💡 最佳实践

### 编写规则

1. **简洁明确**: 每条规则应该清晰、可执行
2. **项目相关**: 专注于本项目的特定约定
3. **避免冗余**: 不重复通用编程规范
4. **定期审查**: 每季度 review 一次

### 使用 AI 助手

1. **提供上下文**: 说明需求时包含相关背景
2. **引用文档**: 指向项目中的官方文档
3. **小步验证**: 每次改动后立即测试
4. **及时反馈**: 发现问题及时调整规则

## 🎯 技术栈速查

| 技术       | 版本   | 用途         |
| ---------- | ------ | ------------ |
| Python     | 3.9+   | 主要开发语言 |
| FastAPI    | Latest | Web 框架     |
| PostgreSQL | Latest | 主数据库     |
| Redis      | Latest | 缓存/队列    |
| Docker     | Latest | 容器化部署   |
| pytest     | Latest | 测试框架     |

## 📞 获取帮助

### 文档资源

- **Cursor 官方**: <https://cursor.com/cn/docs/context/rules>
- **项目文档**: `/docs/`
- **问题反馈**: 项目 GitHub Issues

### 常见问题

**Q: AI 助手没有遵循规则？**
A: 检查 `.cursorrules` 文件是否在项目根目录，规则是否清晰明确。

**Q: 如何添加新规则？**
A: 编辑 `/.cursorrules`，保持简洁，重启对话生效。

**Q: 规则太多怎么办？**
A: 精简规则，删除冗余，保持 <100 行为宜。

---

**版本**: v3.0
**更新**: 2024-10-29
