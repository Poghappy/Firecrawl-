# Cursor Markdown 编辑配置指南

## 📋 配置清单

### ✅ 已完成配置

- [x] `.prettierrc.json` - Prettier 格式化配置
- [x] `.markdownlint.json` - Markdown 规则配置
- [x] `.markdownlintignore` - 排除不需要检查的文件
- [x] `.vscode/settings.json` - Cursor/VSCode 工作区设置
- [x] `package.json` - 依赖和脚本配置
- [x] `Makefile` - 自动化命令
- [x] `.gitignore` - Git 忽略配置

## 🚀 快速开始

### 1. 推荐安装的 Cursor 扩展

打开命令面板 (`Cmd+Shift+P`)，输入 `Extensions: Install Extensions`，搜索并安装：

```bash
1. Prettier - Code formatter (esbenp.prettier-vscode)        # 代码格式化
2. markdownlint (DavidAnson.vscode-markdownlint)            # Markdown 规则检查
3. Markdown All in One (yzhang.markdown-all-in-one)         # 快捷键和工具
4. Markdown Preview Enhanced (shd101wyy.markdown-preview-enhanced)  # 增强预览
```

### 2. 核心功能

#### 🎨 自动格式化

- **保存时自动格式化**：每次 `Cmd+S` 保存时自动美化
- **手动格式化**：`Cmd+Shift+P` → Format Document
- **格式化所有文件**：`make format` 或 `npm run format`

#### 🔍 实时检查

- **保存时检查**：自动运行 markdownlint
- **手动检查**：`make lint` 或 `npm run lint`
- **自动修复**：`npm run lint:fix`

#### 📚 目录生成

- **自动生成目录**：`make toc`
- 为所有 `.md` 文件添加/更新目录

#### 🖼️ 实时预览

- **并排预览**：`Cmd+Shift+V`
- **新标签预览**：`Cmd+K V`
- **预览与编辑同步滚动**：已自动启用

## 📝 常用命令

### Makefile 命令

```bash
make format    # 格式化所有 .md 文件
make lint      # 检查 Markdown 错误
make toc       # 自动生成目录
make check     # 一键执行所有任务（format + lint + toc）
make clean     # 清理临时文件
make help      # 显示帮助信息
```

### NPM 命令

```bash
npm run format     # 格式化所有 .md 文件
npm run lint       # 检查 Markdown 错误
npm run lint:fix   # 自动修复 lint 问题
npm run check      # 执行所有检查
```

## ⚙️ 配置详解

### Prettier 配置 (`.prettierrc.json`)

```json
{
  "proseWrap": "preserve", // 保持原有换行
  "printWidth": 100, // 最大行宽 100 字符
  "tabWidth": 2, // 缩进 2 空格
  "useTabs": false // 使用空格而非制表符
}
```

### Markdownlint 配置 (`.markdownlint.json`)

已禁用的规则：

- `MD013`: 行长度限制（允许长行）
- `MD033`: HTML 标签（允许 HTML）
- `MD041`: 首行必须是标题（更灵活）
- `MD024`: 重复标题（允许重复）
- 其他 10+ 规则已优化

### 编辑器配置 (`.vscode/settings.json`)

核心设置：

- 保存时自动格式化
- 保存时自动修复 lint 问题
- 智能代码补全
- 实时预览同步滚动
- 100 字符标尺提示

## 🎯 实用技巧

### 1. 快捷键（Markdown All in One）

```bash
Cmd+B           # 加粗文本
Cmd+I           # 斜体文本
Cmd+Shift+]     # 增加标题层级
Cmd+Shift+[     # 减少标题层级
Cmd+K Cmd+M     # 切换列表样式
Opt+Shift+F     # 格式化表格
```

### 2. 代码块快捷输入

输入 ` ```js ` 然后按 `Tab`，自动创建：

````markdown
```javascript
// 代码
```
````

### 3. 表格快速创建

输入 `| Header |` 然后按 `Enter`，自动生成：

```markdown
| Header |
| ------ |
|        |
```

### 4. 粘贴图片

- 安装 `Paste Image` 扩展
- 截图后直接 `Cmd+Opt+V` 粘贴
- 自动保存图片到项目目录

## 🐛 故障排除

### 问题 1：格式化不生效

**解决方案**：

1. 确认已安装 Prettier 扩展
2. 检查 `.prettierrc.json` 是否存在
3. 重启 Cursor

### 问题 2：Markdownlint 检查 node_modules

**解决方案**：

- 已创建 `.markdownlintignore` 排除 `node_modules/`
- 如果仍有问题，运行 `npm run lint`（不检查 node_modules）

### 问题 3：保存时不自动格式化

**解决方案**：

1. 确认 `.vscode/settings.json` 中 `editor.formatOnSave` 为 `true`
2. 确认 Markdown 文件的默认格式化器为 Prettier
3. 手动格式化测试：`Cmd+Shift+P` → Format Document

## 📚 相关文档

- [Prettier 官方文档](https://prettier.io/docs/en/)
- [Markdownlint 规则](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)
- [Cursor 官方文档](https://cursor.sh/docs)

## 🎉 项目文件统计

```bash
配置文件：      7 个
安装扩展：      4 个（推荐）
npm 包：        120 个（自动安装）
Makefile 命令： 6 个
npm 脚本：      4 个
```

## 📞 支持

如有问题，请检查：

1. 所有扩展是否已安装
2. `npm install` 是否成功执行
3. `.vscode/settings.json` 是否正确加载
4. Cursor 是否需要重启

---

**最后更新**: 2025-10-27
**作者**: 乐哥
**项目**: FireShot Markdown 工作流
