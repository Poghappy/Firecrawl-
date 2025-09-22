# 🤝 贡献指南

感谢您对Firecrawl数据采集器项目的关注！我们欢迎各种形式的贡献，包括但不限于代码、文档、测试、问题报告等。

## 📋 贡献方式

### 🐛 报告问题
- 使用 [Bug报告模板](.github/ISSUE_TEMPLATE/bug_report.md)
- 提供详细的复现步骤和环境信息
- 检查是否已有类似问题

### 💡 功能请求
- 使用 [功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)
- 描述使用场景和预期效果
- 考虑向后兼容性

### 🔧 代码贡献
- Fork仓库并创建功能分支
- 遵循代码规范和提交规范
- 添加必要的测试和文档
- 提交Pull Request

## 🛠️ 开发环境设置

### 1. 环境要求
- Python 3.9+
- Git
- Docker (可选)

### 2. 本地开发设置
```bash
# 1. Fork并克隆仓库
git clone https://github.com/your-username/Firecrawl-.git
cd Firecrawl-

# 2. 创建虚拟环境
python -m venv firecrawl_env
source firecrawl_env/bin/activate  # Linux/Mac
# 或
firecrawl_env\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入必要的API密钥

# 5. 运行测试
pytest tests/ -v
```

### 3. 代码质量工具
```bash
# 代码格式化
black src/ tests/
isort src/ tests/

# 代码检查
flake8 src/ tests/
mypy src/

# 运行测试
pytest tests/ --cov=src --cov-report=html
```

## 📝 代码规范

### 1. Python代码规范
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 使用 [isort](https://pycqa.github.io/isort/) 进行导入排序
- 使用 [mypy](http://mypy-lang.org/) 进行类型检查

### 2. 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 示例
```
feat(api): add user authentication endpoint

- Add JWT token validation
- Implement user login/logout
- Add password hashing

Closes #123
```

### 3. 分支命名规范
- `feature/功能名称`: 新功能开发
- `fix/问题描述`: Bug修复
- `docs/文档更新`: 文档相关
- `refactor/重构内容`: 代码重构

## 🧪 测试指南

### 1. 测试类型
- **单元测试**: 测试单个函数或方法
- **集成测试**: 测试模块间交互
- **端到端测试**: 测试完整工作流

### 2. 测试覆盖率
- 目标覆盖率: 80%+
- 核心模块覆盖率: 90%+

### 3. 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api.py

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行测试并查看覆盖率
pytest --cov=src --cov-report=term-missing
```

## 📚 文档规范

### 1. 代码文档
- 使用 [Google风格](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) 的docstring
- 为所有公共函数和类添加文档
- 包含参数、返回值和异常说明

### 2. 示例
```python
def crawl_url(url: str, options: dict = None) -> dict:
    """爬取指定URL的内容。
    
    Args:
        url: 要爬取的URL
        options: 爬取选项，包含headers、timeout等
        
    Returns:
        包含爬取结果的字典，格式为:
        {
            'success': bool,
            'data': dict,
            'error': str
        }
        
    Raises:
        ValueError: 当URL格式不正确时
        ConnectionError: 当网络连接失败时
    """
    pass
```

### 3. README更新
- 新功能需要更新README.md
- 添加使用示例和配置说明
- 更新依赖和安装说明

## 🔄 Pull Request流程

### 1. 创建PR前
- [ ] 确保代码通过所有测试
- [ ] 更新相关文档
- [ ] 添加必要的测试用例
- [ ] 遵循代码规范

### 2. PR描述
使用 [PR模板](.github/pull_request_template.md) 填写：
- 变更描述
- 相关Issue
- 测试说明
- 检查清单

### 3. 代码审查
- 至少需要1个审查者批准
- 解决所有审查意见
- 保持PR简洁，避免过大的变更

### 4. 合并后
- 删除功能分支
- 更新本地main分支
- 检查CI/CD状态

## 🏷️ 版本发布

### 1. 版本号规范
使用 [语义化版本](https://semver.org/lang/zh-CN/)：
- `MAJOR.MINOR.PATCH`
- `1.0.0` - 初始版本
- `1.1.0` - 新功能
- `1.1.1` - Bug修复

### 2. 发布流程
1. 更新 `CHANGELOG.md`
2. 更新版本号
3. 创建Git标签
4. 触发自动发布

## 🎯 贡献优先级

### 高优先级
- 修复关键bug
- 性能优化
- 安全加固
- 核心功能完善

### 中优先级
- 新功能开发
- 文档完善
- 测试覆盖率提升
- 用户体验改进

### 低优先级
- 代码重构
- 工具链优化
- 示例代码
- 社区建设

## 🚫 不接受的贡献

- 包含恶意代码的PR
- 违反项目许可证的代码
- 没有测试覆盖的新功能
- 破坏向后兼容性的变更（除非有充分理由）

## 📞 获取帮助

### 联系方式
- **GitHub Issues**: [问题跟踪](https://github.com/Poghappy/Firecrawl-/issues)
- **讨论区**: [GitHub Discussions](https://github.com/Poghappy/Firecrawl-/discussions)
- **邮件**: 通过GitHub联系维护者

### 常见问题
- 查看 [FAQ文档](docs/FAQ.md)
- 搜索现有Issues
- 查看 [故障排除指南](docs/TROUBLESHOOTING.md)

## 📄 许可证

本项目采用 [MIT许可证](LICENSE)。贡献代码即表示您同意将代码在MIT许可证下发布。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！您的贡献让项目变得更好。

---

**注意**: 请确保在贡献前仔细阅读本指南，如有疑问请随时联系维护者。