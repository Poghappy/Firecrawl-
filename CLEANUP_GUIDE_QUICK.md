# 🧹 项目清理快速指南

**项目**: Firecrawl 数据采集器
**清理日期**: 2025-10-29
**清理目标**: 删除与项目主题无关的文件，优化项目结构

---

## 📊 清理摘要

本次清理将：
- ✅ 删除 **840+ 个无关文件**
- ✅ 节省 **226-362 MB** 磁盘空间
- ✅ 提升项目可维护性

---

## 🚀 快速开始

### 方法一：使用自动化脚本（推荐）

```bash
# 1. 执行清理脚本
./scripts/cleanup-project.sh

# 脚本会自动：
# - 创建备份
# - 按优先级清理文件
# - 生成清理报告
# - 询问用户确认

# 2. 验证项目
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/

# 3. 提交更改
git add .
git commit -m "chore: 清理项目无关文件"
```

### 方法二：手动清理

参考详细清理建议：`docs/maintenance/PROJECT_CLEANUP_RECOMMENDATIONS_2025-10-29.md`

---

## 📋 主要清理项目

### 🔴 高优先级（必须删除）

| 项目 | 大小 | 说明 |
|-----|-----|------|
| `firecrawl_env/` | 150-200 MB | Python 虚拟环境 |
| `components/` | 0 KB | 空目录 |
| 5个 `archive.zip` | 20-50 MB | 压缩包文件 |
| `firecrawl-app-examples-main/` | 50-100 MB | 官方示例代码（800+文件） |

### 🟡 中优先级（建议删除）

| 项目 | 大小 | 说明 |
|-----|-----|------|
| `prompts/` | 1-2 MB | AI 提示词系统（20+文件） |
| `scripts/github-actions/` | <1 MB | GitHub 初始化脚本 |
| 博客文章（5个） | <1 MB | 营销教程文档 |

### 🟢 低优先级（可选删除）

| 项目 | 大小 | 说明 |
|-----|-----|------|
| `results/config*.json` | <1 MB | 重复配置文件 |
| 旧报告文件 | <1 MB | 过期的测试报告 |

---

## ⚠️ 注意事项

### 清理前
1. ✅ 确保所有重要更改已提交到 Git
2. ✅ 运行测试确保项目功能正常
3. ✅ 备份数据库文件（如需要）

### 清理后
1. ✅ 重新创建虚拟环境
2. ✅ 运行测试验证功能
3. ✅ 更新项目文档
4. ✅ 提交 Git commit

---

## 📁 清理后的项目结构

```
Firecrawl数据采集器/
├── src/                    # 核心源代码
├── tests/                  # 测试文件
├── config/                 # 配置文件
├── docs/                   # 文档
│   ├── official-docs/     # Firecrawl API 文档
│   ├── blog/              # 博客文章（新增）
│   ├── maintenance/       # 维护文档
│   └── reports/           # 项目报告
├── scripts/               # 脚本文件
│   └── archive/           # 归档脚本
├── data/                  # 数据存储
├── logs/                  # 日志文件
├── results/               # 运行结果
└── templates/             # 模板文件
```

---

## 🔗 相关文档

- 📄 **详细清理建议**: `docs/maintenance/PROJECT_CLEANUP_RECOMMENDATIONS_2025-10-29.md`
- 📄 **自动化脚本**: `scripts/cleanup-project.sh`
- 📄 **项目状态**: `project_status.md`

---

## 🆘 帮助

### 如何恢复误删文件？

```bash
# 从备份恢复
tar -xzf firecrawl-backup-YYYYMMDD-HHMMSS.tar.gz

# 从 Git 恢复
git checkout HEAD -- path/to/file
```

### 如何查看清理报告？

清理完成后，查看 `docs/maintenance/CLEANUP_REPORT_YYYY-MM-DD.md`

---

**执行前请阅读**: `docs/maintenance/PROJECT_CLEANUP_RECOMMENDATIONS_2025-10-29.md`
**如有疑问**: 联系项目维护者
