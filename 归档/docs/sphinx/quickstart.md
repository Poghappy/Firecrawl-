# 快速开始

本指南将帮助你在 10 分钟内开始使用 FireShot。

## 环境准备

### 系统要求

- Python 3.11+ (推荐 3.14+)
- Node.js 18+ (用于 TypeScript 工具)
- Git 2.0+

### 检查环境

```bash
# 检查 Python 版本
python --version

# 检查 Node.js 版本
node --version

# 检查 Git 版本
git --version
```

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/FireShot.git
cd FireShot
```

### 2. 安装 Python 依赖

```bash
# 方式1：使用 pip
pip install -r requirements.txt

# 方式2：使用 uv (更快)
uv pip install -r requirements.txt

# 方式3：使用 poetry
poetry install
```

### 3. 安装 Node.js 依赖（可选）

```bash
npm install
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp env.template .env

# 编辑 .env 文件，填入你的 Firecrawl API 密钥
# FIRECRAWL_API_KEY=fc-your-key-here
```

### 5. 测试安装

```bash
# 测试 API 密钥
python test_api_keys.py

# 运行快速开始示例
python quick_start.py

# 运行测试套件
pytest tests/ -v
```

## 第一个爬虫

### 示例：爬取网页内容

```python
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 Firecrawl 客户端
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# 爬取网页
result = app.scrape(
    url="https://www.hawaiinewsnow.com/",
    formats=["markdown"],
    only_main_content=True,
    max_age=172800000  # 2天缓存
)

# 打印结果
print(f"标题: {result.metadata.title}")
print(f"URL: {result.url}")
print(f"内容:\n{result.markdown}")
```

### 运行示例

```bash
python my_first_scraper.py
```

## 常见问题

### API 密钥无效

**问题**: `Invalid API key`

**解决方案**:
1. 检查 `.env` 文件中的密钥是否正确
2. 确保密钥以 `fc-` 开头
3. 前往 [Firecrawl Dashboard](https://firecrawl.dev) 验证密钥

### 导入错误

**问题**: `ModuleNotFoundError: No module named 'firecrawl'`

**解决方案**:
```bash
pip install firecrawl-py
```

### 权限错误

**问题**: `Permission denied`

**解决方案**:
```bash
chmod -R 755 .
```

## 下一步

- 阅读 [完整使用指南](usage.md)
- 查看 [API 参考](api/config.md)
- 了解 [开发流程](development/contributing.md)
