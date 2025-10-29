# .cursor 配置目录

## 📁 目录结构

```text
.cursor/
├── README.md                    # 本文件
├── project-config.json          # 项目自定义配置
├── QUICK_START.md               # 快速开始指南
├── MIGRATION_REPORT.md          # 迁移报告
├── SETUP_COMPLETE.md            # 设置完成指南
│
├── prompts/                     # Prompts 系统
│   ├── README.md
│   ├── INDEX.md
│   ├── roles/                   # 角色定义（9个）
│   ├── stages/                  # 阶段定义
│   └── workflows/               # 工作流（7个）
│
├── scripts/                     # 工具脚本
│   ├── verify-prompts.sh
│   └── check-roles.sh
│
└── hooks/                       # Git Hooks
    ├── pre-commit
    └── pre-push
```

## 📋 文件说明

### 核心配置

- **project-config.json** - 项目自定义配置（环境、工具、限制等）
  - 注意：这不是 Cursor 的 environment.json，而是项目特定配置

### 快速指南

- **QUICK_START.md** - 3 分钟快速上手指南
- **SETUP_COMPLETE.md** - 设置完成检查清单
- **MIGRATION_REPORT.md** - 详细迁移记录

### Prompts 系统

- **prompts/** - 完整的多角色 Agent 提示词库
  - 10 个专业角色
  - 7 个工作流阶段
  - 统一交接格式

### 自动化工具

- **scripts/** - 验证和检查脚本
- **hooks/** - Git 提交和推送检查

## 🚀 使用方式

### 1. 主规则文件

Cursor 自动加载项目根目录的 `.cursorrules` 文件（非本目录）。

### 2. Prompts 系统

通过 `.cursorrules` 引用本目录下的 prompts 文件。

### 3. 工具和脚本

运行 `make cursor-setup` 激活所有工具和 Git Hooks。

## 📚 相关文档

- [快速开始](./QUICK_START.md)
- [Prompts 使用手册](./prompts/README.md)
- [迁移完成报告](./MIGRATION_REPORT.md)
- [设置完成指南](./SETUP_COMPLETE.md)

## ⚙️ 配置说明

### project-config.json

这是项目的自定义配置文件，包含：

- 项目信息和路径
- 命令快捷方式
- 质量标准
- API 配额
- 环境配置
- 工具集成

**注意**: 这不是 Cursor IDE 的标准配置文件，而是供项目团队参考的配置清单。

## 🔧 维护

### 更新配置

1. 修改 `project-config.json`
2. 运行 `make verify-cursor-config`
3. 重启 Cursor

### 更新 Prompts

1. 修改 `prompts/` 目录下的相应文件
2. 运行 `make check-roles`
3. 重启 Cursor

### 验证配置

```bash
make verify-cursor-config
make check-roles
```

---

**版本**: v2.0.0
**更新**: 2025-10-29
**维护**: AI 全栈工程师团队
