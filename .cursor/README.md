# .cursor 配置目录

## 📁 配置文件说明

### 项目根目录的 `.cursorrules`

这是 **Cursor 官方推荐的标准配置文件**，AI 助手会自动读取并遵循其中的规则。

**位置**: `/.cursorrules`（项目根目录）

**内容**: 包含项目的核心开发规范、代码风格、工作流程等

### .cursor 目录

用于存放额外的配置文件和模板：

```
.cursor/
├── README.md                  # 本说明文档
├── QUICK_REFERENCE.md        # 快速参考指南
├── CURSOR_RULES_UPGRADE.md   # 升级说明文档
├── CONFIGURATION_SUMMARY.md  # 完整配置总结
├── CURSOR_CONFIG_STATUS.md   # 配置状态跟踪
├── OPTIMIZATION_REPORT.md    # 优化历史报告
├── FILES_INDEX.md            # 文件索引
├── verify-config.sh          # 配置验证脚本
├── templates.py              # Python 代码模板库
└── archive/                  # 历史备份文件
```

## 🎯 配置最佳实践

### 根据 Cursor 官方文档建议

✅ **应该做的**:

- 使用简洁、具体、可执行的规则
- 专注于项目特定的约定和习惯
- 提供清晰的行为指导
- 保持规则文件精简（建议 <200 行）

❌ **不应该做的**:

- 包含过多理论性内容
- 添加大量代码示例
- 重复定义通用编码规范
- 规则过于冗长复杂

## 🔄 配置更新

修改 `.cursorrules` 后，AI 助手会在下次对话时自动应用新规则。

## 📚 参考资源

### Cursor 相关

- **Cursor 官方文档**: <https://cursor.com/cn/docs/context/rules>
- **配置状态**: `CURSOR_CONFIG_STATUS.md`
- **快速参考**: `QUICK_REFERENCE.md`
- **升级指南**: `CURSOR_RULES_UPGRADE.md`

### 项目相关

- **项目状态**: ../project_status.md
- **项目规则**: ../FIRECRAWL_PROJECT_RULES.md
- **官方文档**: ../docs/official-docs/
- **API 文档**: ../docs/API.md
- **部署指南**: ../DEPLOYMENT.md

## 📝 配置历史

### v2.0 (2024-10-28)

- 从 9 个规则文件（3000+行）精简到单个 rules.md（100 行）
- 旧文件已归档到 archive/

### v3.0 (2024-10-29)

- 迁移到标准的 `.cursorrules` 文件（根目录）
- 遵循 Cursor 官方最佳实践
- 进一步精简规则内容
