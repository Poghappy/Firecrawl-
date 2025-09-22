# 贡献指南

欢迎为Firecrawl数据采集器项目做出贡献！本指南将帮助您了解如何参与项目开发。

## 📋 目录
- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交流程](#提交流程)
- [测试要求](#测试要求)
- [文档要求](#文档要求)
- [发布流程](#发布流程)

## 🚀 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd Firecrawl数据采集器
```

### 2. 设置虚拟环境
```bash
# 使用Makefile快速设置
make setup
source firecrawl_env/bin/activate

# 或手动设置
python3 -m venv firecrawl_env
source firecrawl_env/bin/activate
pip install -r requirements.txt
```

### 3. 安装开发依赖
```bash
make dev
# 或
pip install -r requirements-dev.txt
pre-commit install
```

### 4. 验证环境
```bash
make check-all
```

## 💻 代码规范

### Python代码规范
- 遵循PEP 8标准
- 使用Black进行代码格式化
- 使用Ruff进行代码检查
- 使用MyPy进行类型检查

### 代码格式化
```bash
make format
```

### 代码检查
```bash
make lint
```

### 类型检查
```bash
mypy src/
```

## 📝 提交流程

### 1. 创建分支
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 提交规范
使用Conventional Commits规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 提交类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 提交示例
```bash
feat(api): add user authentication endpoint
fix(collector): handle timeout errors gracefully
docs(readme): update installation instructions
test(unit): add tests for data processor
```

### 3. 提交前检查
```bash
make check-all
```

### 4. 推送和创建PR
```bash
git push origin feature/your-feature-name
```

## 🧪 测试要求

### 测试覆盖率
- 单元测试覆盖率 ≥ 80%
- 集成测试覆盖率 ≥ 60%
- 关键业务逻辑覆盖率 ≥ 95%

### 运行测试
```bash
# 运行所有测试
make test

# 运行单元测试
make test-unit

# 运行集成测试
make test-integration

# 运行端到端测试
make test-e2e

# 生成覆盖率报告
make cov
```

### 测试编写规范
```python
import pytest
from unittest.mock import Mock, patch

class TestDataProcessor:
    """数据处理器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.processor = DataProcessor()
    
    def test_process_valid_data(self):
        """测试处理有效数据"""
        # Given
        input_data = {"title": "Test", "content": "Test content"}
        
        # When
        result = self.processor.process(input_data)
        
        # Then
        assert result["title"] == "Test"
        assert result["content"] == "Test content"
    
    @pytest.mark.asyncio
    async def test_process_async_data(self):
        """测试异步数据处理"""
        # Given
        input_data = {"title": "Async Test"}
        
        # When
        result = await self.processor.process_async(input_data)
        
        # Then
        assert result is not None
    
    def test_process_invalid_data(self):
        """测试处理无效数据"""
        # Given
        invalid_data = None
        
        # When & Then
        with pytest.raises(ValueError):
            self.processor.process(invalid_data)
```

## 📚 文档要求

### 代码文档
- 所有公共函数和类必须有docstring
- 使用Google风格的docstring
- 包含参数、返回值和异常说明

```python
def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理采集的原始数据
    
    Args:
        data: 原始数据字典
        
    Returns:
        处理后的结构化数据
        
    Raises:
        ValueError: 当数据格式不正确时
        ProcessingError: 当处理过程中发生错误时
        
    Example:
        >>> processor = DataProcessor()
        >>> result = processor.process_data({"title": "Test"})
        >>> print(result["title"])
        Test
    """
    pass
```

### API文档
- 使用FastAPI自动生成API文档
- 为每个端点提供详细描述
- 包含请求和响应示例

### 项目文档
- 更新README.md
- 维护CHANGELOG.md
- 编写部署指南

## 🔄 发布流程

### 1. 版本管理
使用语义化版本控制：
- MAJOR: 不兼容的API修改
- MINOR: 向下兼容的功能性新增
- PATCH: 向下兼容的问题修正

### 2. 发布检查清单
- [ ] 所有测试通过
- [ ] 代码覆盖率达标
- [ ] 文档已更新
- [ ] CHANGELOG.md已更新
- [ ] 版本号已更新

### 3. 发布命令
```bash
# 发布准备
make release-prep

# 构建Docker镜像
make build-prod

# 部署到生产环境
make deploy
```

## 🐛 问题报告

### Bug报告模板
```markdown
## Bug描述
简要描述bug

## 重现步骤
1. 执行步骤1
2. 执行步骤2
3. 执行步骤3

## 预期行为
描述预期行为

## 实际行为
描述实际行为

## 环境信息
- Python版本: 3.13.7
- 操作系统: macOS
- 项目版本: v1.0.0

## 附加信息
添加任何其他相关信息
```

### 功能请求模板
```markdown
## 功能描述
简要描述请求的功能

## 使用场景
描述功能的使用场景

## 预期行为
描述功能的预期行为

## 替代方案
描述考虑过的替代方案

## 附加信息
添加任何其他相关信息
```

## 🤝 代码审查

### 审查检查清单
- [ ] 代码符合项目规范
- [ ] 测试覆盖率达标
- [ ] 文档已更新
- [ ] 性能影响已评估
- [ ] 安全问题已检查

### 审查流程
1. 创建Pull Request
2. 等待代码审查
3. 根据反馈修改代码
4. 审查通过后合并

## 📞 获取帮助

- 查看项目文档
- 提交Issue
- 参与讨论
- 联系维护者

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！
