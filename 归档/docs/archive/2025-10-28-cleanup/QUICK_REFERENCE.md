# 🚀 FireShot 快速参考卡片

## ⚡ 立即执行（必须）

```bash
# 🔄 再次重启 Cursor（重要！）
Cmd+Shift+P → "Reload Window"
```

**原因**：刚刚创建了虚拟环境，必须重启才能让 Cursor 识别

---

## ✅ 重启后检查（3 步验证）

### 1️⃣ 检查底部状态栏

```
✅ Python: .venv/bin/python (3.14.0)
✅ Ruff: Ruff (native)
```

### 2️⃣ 测试自动格式化

1. 打开 `tests/test_example.py`
2. 修改代码格式（添加空格、删除空行）
3. 按 `Cmd+S` 保存
4. ✅ 应该自动格式化

### 3️⃣ 终端验证

```bash
cd /Users/zhiledeng/Downloads/FireShot
source .venv/bin/activate
python verify_python_setup.py
# 应该显示: ✅ 所有检查通过！(11/11)
```

---

## 🛠️ 如果底部状态栏不正确

### 手动选择 Python 解释器

```
1. 点击底部状态栏的 Python 版本
   或
   Cmd+Shift+P → "Python: Select Interpreter"

2. 选择:
   ✅ Python 3.14.0 ('.venv': venv) ./venv/bin/python
```

---

## 📋 当前配置汇总

| 组件         | 版本/状态       | 用途                |
| ------------ | --------------- | ------------------- |
| Python       | 3.14.0 (.venv)  | ✅ 项目解释器       |
| Ruff         | 0.14.2 (native) | ✅ 格式化 + Linting |
| Pylance      | 启用            | ✅ 智能提示         |
| mypy         | 1.18.2          | ✅ 类型检查         |
| pytest       | 8.4.2           | ✅ 测试框架         |
| firecrawl-py | v4.5.0          | ✅ 核心库           |

---

## 🎯 常用命令

### 激活虚拟环境

```bash
cd /Users/zhiledeng/Downloads/FireShot
source .venv/bin/activate
```

### 代码质量检查

```bash
ruff check .          # 检查问题
ruff check . --fix    # 自动修复
ruff format .         # 格式化代码
```

### 运行测试

```bash
pytest tests/ -v                  # 所有测试
pytest tests/test_example.py -v  # 单个文件
```

### 类型检查

```bash
mypy scripts/ --strict
```

---

## ❌ 常见问题速查

| 问题                       | 解决方案                         |
| -------------------------- | -------------------------------- |
| 底部显示 `Python (global)` | 手动选择 `.venv` 解释器          |
| Ruff 不自动格式化          | 检查 Output → Ruff，重启 Cursor  |
| 类型提示不工作             | 确认 Pylance 已启用（不是 None） |
| 终端 Python 路径错误       | `source .venv/bin/activate`      |

---

## 📚 详细文档

| 文档                           | 查看内容              |
| ------------------------------ | --------------------- |
| `SETUP_COMPLETE_NEXT_STEPS.md` | 完整验证步骤          |
| `RUFF_VENV_SOLUTION.md`        | 官方文档+社区最佳实践 |
| `RESOURCES_SUMMARY.md`         | 所有参考资源          |

---

**状态**: ✅ 配置完成
**下一步**: 🔄 重启 Cursor → ✅ 验证 → 🚀 开始开发
