# 🧪 测试索引

> 测试脚本和测试工具

**最后更新**: 2024-10-29

---

## 📂 测试文件

### 🔬 基础测试

- [test_basic.py](./test_basic.py) - 基础功能测试
  - 核心功能验证
  - 基本 API 测试
  - 配置加载测试

---

### 🚀 快速测试

- [quick_test.py](./quick_test.py) - 快速测试脚本

  - 快速功能验证
  - 开发环境测试

- [quick_test_fixed.py](./quick_test_fixed.py) - 修复版快速测试
  - 修复已知问题
  - 改进的测试用例

---

### 🔌 集成测试

- [integration_test.py](./integration_test.py) - 集成测试套件

  - 端到端测试
  - 多模块协同测试
  - 外部服务集成测试

- [test_enhanced_api.py](./test_enhanced_api.py) - 增强 API 测试
  - 高级 API 功能测试
  - 性能测试
  - 边界条件测试

---

### 🏠 本地测试

- [local_test.py](./local_test.py) - 本地环境测试
  - 本地数据库测试
  - 本地配置验证
  - 开发环境专用测试

---

### ✅ 验证测试

- [verify_fixes.py](./verify_fixes.py) - 修复验证测试
  - Bug 修复验证
  - 回归测试
  - 问题复现和验证

---

## 🗂️ 归档文件

- `archive.zip` - 历史测试文件归档
  - 包含过时的测试脚本
  - 已弃用的测试用例

---

## 🔍 测试类型分类

### 按测试级别

| 测试类型   | 文件                   | 用途             |
| ---------- | ---------------------- | ---------------- |
| 单元测试   | `test_basic.py`        | 基础功能验证     |
| 集成测试   | `integration_test.py`  | 模块协同测试     |
| 端到端测试 | `test_enhanced_api.py` | 完整流程测试     |
| 快速测试   | `quick_test*.py`       | 开发阶段快速验证 |

### 按测试环境

| 环境     | 文件                  | 说明                 |
| -------- | --------------------- | -------------------- |
| 本地环境 | `local_test.py`       | 本地开发测试         |
| 集成环境 | `integration_test.py` | 集成环境测试         |
| 生产环境 | -                     | 使用生产专用测试套件 |

---

## 🚀 快速开始

### 运行测试

#### 1. 基础测试

```bash
pytest tests/test_basic.py -v
```

#### 2. 快速测试

```bash
python tests/quick_test_fixed.py
```

#### 3. 集成测试

```bash
pytest tests/integration_test.py -v
```

#### 4. 所有测试

```bash
pytest tests/ -v
```

---

## 📊 测试覆盖率

### 当前状态

- **单元测试**: ✅ 已覆盖核心功能
- **集成测试**: ✅ 已覆盖主要流程
- **API 测试**: ✅ 已覆盖关键接口
- **性能测试**: ⚠️ 部分覆盖

### 改进目标

- [ ] 提升单元测试覆盖率至 >80%
- [ ] 完善边界条件测试
- [ ] 增加性能基准测试
- [ ] 添加压力测试

---

## 🛠️ 测试工具

### 使用的测试框架

- **pytest** - 主测试框架
- **pytest-asyncio** - 异步测试支持
- **pytest-cov** - 覆盖率报告

### 安装依赖

```bash
pip install -r requirements-dev.txt
```

---

## 📝 测试最佳实践

### 编写测试

1. **命名清晰** - 使用描述性的测试函数名
2. **独立性** - 每个测试独立运行
3. **可重复** - 测试结果应该可重复
4. **快速执行** - 保持测试运行快速

### 测试结构

```python
def test_feature_name():
    # Arrange - 准备测试数据
    # Act - 执行被测试的功能
    # Assert - 验证结果
```

### Mock 外部依赖

```python
@pytest.fixture
def mock_api():
    # Mock 外部 API 调用
    pass
```

---

## 🔧 CI/CD 集成

### GitHub Actions

测试自动化已集成到 CI/CD 流程：

- 每次 Push 自动运行测试
- PR 合并前必须通过测试
- 生成测试覆盖率报告

---

## 🐛 调试技巧

### 运行单个测试

```bash
pytest tests/test_basic.py::test_specific_function -v
```

### 显示打印输出

```bash
pytest tests/ -v -s
```

### 调试失败的测试

```bash
pytest tests/ --pdb
```

---

**维护者**: AI 全栈工程师团队
**测试覆盖率目标**: >80%
