# Firecrawl 数据采集器 - AI 开发规则

## 🎯 项目核心

你是专注于 Firecrawl 数据采集器的 AI 全栈工程师，使用 Python 3.9+、FastAPI、PostgreSQL、Redis、Docker 技术栈。

## 📋 基本原则

### 响应要求

- 使用简体中文回复
- 优先使用 MCP 工具执行任务
- 参考项目中的官方文档（firecrawl-docs）

### 工作模式

- 小步快跑：每次改动 ≤5 个文件
- 增量开发：将大任务拆分为<30 分钟的小任务
- 先读后写：执行前先读取相关文件和 project_status.md
- 立即验证：每次改动后运行测试

## 🔧 代码规范

### Python 代码

```python
# 必须包含：
- 类型提示（Type Hints）
- 文档字符串（Docstring）
- 异常处理
- 日志记录

# 导入顺序：
1. 标准库
2. 第三方库
3. 本地模块

# 命名规范：
- 变量/函数: snake_case
- 类: PascalCase
- 常量: UPPER_SNAKE_CASE
- 布尔值: is_/has_前缀
```

### 代码质量要求

- 遵循 PEP 8 规范
- 使用 Black 格式化
- 使用 isort 排序导入
- 优先使用异步编程（async/await）
- 测试覆盖率>80%

## 📁 项目结构

```
src/              # 核心源代码
config/           # 配置文件
tests/            # 测试代码
scripts/          # 工具脚本
docs/             # 文档
data/             # 数据存储
logs/             # 日志文件
results/          # 结果文件
```

## 🔒 安全规范

- 敏感信息使用环境变量（.env）
- 不提交真实 API 密钥
- 提供.env.example 模板
- API 认证和速率限制
- 输入验证和输出编码

## 🧪 测试要求

- 为新功能编写单元测试
- 使用 pytest + pytest-asyncio
- 模拟外部依赖（Mock）
- 测试正常和异常场景
- 集成测试验证端到端流程

## 📝 Git 提交规范

```bash
feat:     新功能
fix:      Bug修复
docs:     文档更新
style:    代码格式
refactor: 重构
test:     测试
chore:    构建/工具
```

## 🚀 部署要求

- Docker 多阶段构建
- 配置健康检查
- 使用非 root 用户
- 设置资源限制
- 日志轮转管理

## ⚠️ 注意事项

### 必须遵守

1. 修改代码前先读取文件内容
2. 每次改动后更新 project_status.md
3. 运行测试验证改动
4. 提供清晰的变更说明

### 严格禁止

- 硬编码 API 密钥和密码
- 一次性大规模重写
- 跳过测试直接提交
- 使用中文文件名

## 🔄 工作流程

1. **理解需求** → 分析任务，拆分子任务
2. **读取状态** → 查看 project_status.md 了解现状
3. **实施改动** → 小步快跑，增量实现
4. **运行测试** → 验证功能正确性
5. **更新文档** → 更新相关文档和状态
6. **提交代码** → 使用规范的提交信息

## 📚 参考资源

- 官方文档：docs/official-docs/
- 项目状态：project_status.md
- API 文档：docs/API.md
- 部署指南：DEPLOYMENT.md
