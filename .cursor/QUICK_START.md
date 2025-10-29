# Cursor AI Prompts 快速开始

## 🚀 3 分钟快速上手

### 步骤 1: 激活配置（30 秒）

```bash
# 一键设置
make cursor-setup
```

输出示例：

```text
🚀 设置 Cursor Prompts 系统...
✅ Cursor Prompts 系统设置完成
请重启 Cursor 以加载新配置
```

### 步骤 2: 重启 Cursor（30 秒）

- **macOS**: `Cmd + Q` 退出，重新打开
- **Windows**: 关闭所有窗口，重新启动
- **Linux**: `Ctrl + Q` 退出，重新打开

### 步骤 3: 开始使用（2 分钟）

在 Cursor 中直接对话即可，系统会自动响应！

## 💡 快速命令

### 验证配置

```bash
make verify-cursor-config
```

### 查看信息

```bash
make cursor-info
```

### 检查角色

```bash
make check-roles
```

## 🎯 使用示例

### 示例 1: 创建新功能

在 Cursor 中输入：

```text
请帮我创建一个用户登录功能
```

系统会自动：

1. PO 明确业务目标
2. PM 创建用户故事
3. BA 分析技术需求
4. PjM 分解任务
5. Arch 设计架构
6. DEV 实现代码
7. QA 编写测试
8. Ops 配置部署
9. TW 编写文档

### 示例 2: 指定角色

```text
@Arch 请设计一个数据采集系统的架构
@DEV 请实现这个功能
@QA 请为这个模块编写测试
```

### 示例 3: 工作流命令

```text
/user-story    # 启动用户故事阶段
/prd          # 启动 PRD 阶段
/tech-design  # 启动技术设计阶段
/implement    # 启动实现阶段
/test         # 启动测试阶段
```

## 📊 质量保证

每次改动会自动包含：

### 输出四件套

1. ✅ **变更计划摘要** - 要做什么
2. ✅ **影响面分析** - 影响范围
3. ✅ **文件树 Diff** - 变更清单
4. ✅ **DoD 检查** - 完成标准

### 质量闸口

- ✅ 代码检查: `make lint`
- ✅ 测试验证: `make test`
- ✅ 覆盖率: >80%
- ✅ 性能: <500ms

## 🔧 常用命令

| 命令                        | 功能       |
| --------------------------- | ---------- |
| `make cursor-setup`         | 一键设置   |
| `make verify-cursor-config` | 验证配置   |
| `make check-roles`          | 检查角色   |
| `make cursor-info`          | 显示信息   |
| `make lint`                 | 代码检查   |
| `make test`                 | 运行测试   |
| `make cov`                  | 覆盖率报告 |

## 📚 完整文档

- [详细使用指南](.cursor/prompts/README.md)
- [迁移完成报告](.cursor/MIGRATION_REPORT.md)
- [角色系统](.cursor/prompts/roles/)
- [工作流定义](.cursor/prompts/)
- [项目配置](.cursor/prompts/project_config.md)

## ⚠️ 注意事项

### 首次使用必做

1. ✅ 运行 `make cursor-setup`
2. ✅ 重启 Cursor
3. ✅ 运行 `make verify-cursor-config`

### 常见问题

**Q: Cursor 没有识别规则？**

```bash
# 检查配置
make verify-cursor-config

# 重启 Cursor
```

**Q: 脚本无法执行？**

```bash
# 添加权限
chmod +x .cursor/scripts/*.sh
chmod +x .cursor/hooks/*
```

**Q: 角色不响应？**

```bash
# 确认已重启 Cursor
# 检查 .cursorrules 文件存在
ls -la .cursorrules
```

## 🎉 开始使用

现在就在 Cursor 中开始对话吧！系统会自动协调多个角色完成你的需求。

**示例：**

```text
创建一个数据采集API，要求：
1. 支持多种数据源
2. 实现速率限制
3. 提供REST API
4. 包含测试和文档
```

系统会自动完成完整的开发流程！

---

**版本**: v2.0.0
**更新**: 2025-10-29
**文档**: `.cursor/prompts/README.md`
