# Firecrawl SDK 配置完成总结

> **配置时间**: 2025-10-27
> **项目**: FireShot - Firecrawl 专项
> **状态**: ✅ 配置成功

---

## 📦 已完成的配置

### 1. 环境文件

#### ✅ `.env` - 环境变量配置

- **位置**: `/Users/zhiledeng/Downloads/FireShot/.env`
- **内容**:
  - 主 API 密钥 + 3 个备用密钥
  - API 端点配置
  - 超时和重试设置
  - 缓存配置
  - 成本限制
- **安全**: 已添加到 `.gitignore`，不会提交到 Git

#### ✅ `requirements.txt` - Python 依赖包

- **核心依赖**:
  ```txt
  firecrawl-py>=1.0.0
  python-dotenv>=1.0.0
  pandas>=2.0.0
  pydantic>=2.0.0
  requests>=2.31.0
  loguru>=0.7.0
  ```
- **安装命令**: `pip3 install -r requirements.txt`

#### ✅ `.gitignore` - Git 忽略文件

- **保护敏感文件**:
  - `.env` 和所有环境变量文件
  - Python 缓存文件
  - 数据和日志文件
  - IDE 配置

### 2. 配置脚本

#### ✅ `setup_sdk.py` - 自动配置脚本

- **功能**:
  1. ✅ 检查 Python 版本（需要 3.8+）
  2. ✅ 检查 pip 可用性
  3. ✅ 自动安装依赖包
  4. ✅ 创建 `.env` 文件（从模板）
  5. ✅ 更新 `.gitignore`
  6. ✅ 测试 API 密钥连接

- **使用方法**:
  ```bash
  python3 setup_sdk.py
  ```

---

## 🎯 验证结果

### ✅ Python 环境

- **版本**: Python 3.14.0
- **pip**: v25.2
- **状态**: ✅ 符合要求

### ✅ 依赖包安装

- **firecrawl-py**: ✅ 已安装
- **python-dotenv**: ✅ 已安装
- **其他依赖**: ✅ 已安装

### ✅ API 密钥测试

- **密钥**: `fc-0a2c801...9f2742edf4`
- **测试 URL**: https://firecrawl.dev/
- **测试结果**: ✅ 连接成功
- **返回数据**: 21,404 字符

---

## 🚀 快速开始

### 1. 基础爬取示例

```python
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化客户端
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# 爬取网页
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    only_main_content=True
)

print(result.markdown)
```

### 2. 批量爬取示例

```python
# 批量爬取多个 URL
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]

results = app.batch_scrape(
    urls=urls,
    formats=["markdown"],
    only_main_content=True
)

for result in results:
    print(f"URL: {result.url}")
    print(f"标题: {result.metadata.get('title')}")
    print(f"内容: {len(result.markdown)} 字符\n")
```

### 3. 搜索 + 爬取示例

```python
# 搜索并获取完整内容
results = app.search(
    query="夏威夷华人社区",
    sources=[{"type": "web"}],
    limit=5,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

for result in results:
    print(f"标题: {result['title']}")
    print(f"URL: {result['url']}")
    if 'markdown' in result:
        print(f"内容: {result['markdown'][:200]}...\n")
```

---

## 📚 项目脚本

### 可用脚本

| 脚本文件                    | 功能描述            | 使用方法                            |
| --------------------------- | ------------------- | ----------------------------------- |
| `setup_sdk.py`              | SDK 配置脚本        | `python3 setup_sdk.py`              |
| `quick_start.py`            | 快速开始示例        | `python3 quick_start.py`            |
| `test_api_keys.py`          | API 密钥测试        | `python3 test_api_keys.py`          |
| `scrape_firecrawl_blog.py`  | 爬取 Firecrawl 博客 | `python3 scrape_firecrawl_blog.py`  |
| `analyze_firecrawl_blog.py` | 分析博客数据        | `python3 analyze_firecrawl_blog.py` |

### 运行顺序建议

1. ✅ **配置环境**: `python3 setup_sdk.py`
2. **测试 API**: `python3 test_api_keys.py`
3. **快速示例**: `python3 quick_start.py`
4. **实战爬取**: `python3 scrape_firecrawl_blog.py`

---

## 🔑 SDK v2 重要变化

### 命名约定

- ✅ **使用下划线**: `only_main_content=True`
- ❌ **不使用驼峰**: ~~`onlyMainContent=True`~~

### 返回值类型

- ✅ **Document 对象**: `result.markdown`
- ❌ **不是字典**: ~~`result.get("markdown")`~~

### 推荐参数

```python
app.scrape(
    url="...",
    formats=["markdown"],           # 输出格式
    only_main_content=True,         # 只要主内容
    max_age=172800000,              # 缓存 2 天（毫秒）
    block_ads=True,                 # 阻止广告
    skip_tls_verification=True,     # 跳过 TLS 验证
    remove_base64_images=True       # 移除 Base64 图片
)
```

---

## 📖 文档资源

### 本地文档

- 📘 **快速指南**: `FIRECRAWL_CLOUD_SETUP_GUIDE.md`
- 📕 **API 规则**: `FIRECRAWL_CLOUD_API_RULES.md`
- 📗 **生态系统**: `FIRECRAWL_ECOSYSTEM_GUIDE.md`
- 📙 **更新日志**: `firecrawl_changelog.md` ⭐️ 新增
- 📓 **研究总结**: `FIRECRAWL_RESEARCH_SUMMARY.md`

### 在线文档

- 🌐 **官方文档**: https://docs.firecrawl.dev/
- 🐙 **GitHub**: https://github.com/firecrawl/firecrawl
- 💬 **Discord**: https://discord.gg/firecrawl

---

## ⚠️ 重要提醒

### 安全最佳实践

1. ✅ **使用环境变量**: 从 `.env` 读取 API 密钥
2. ❌ **不要硬编码**: 永远不要在代码中写死密钥
3. ✅ **Git 保护**: 确保 `.env` 在 `.gitignore` 中
4. ✅ **密钥轮换**: 使用备用密钥实现高可用

### 成本控制

- 💰 **每日预算**: $10.00（在 `.env` 中配置）
- 💰 **每月预算**: $200.00
- 📊 **使用缓存**: `max_age=172800000`（2天）可节省 50%+ 成本
- 📈 **监控用量**: 定期检查 https://firecrawl.dev/app/usage

### 性能优化

- ⚡ **批量爬取**: 使用 `batch_scrape()` 而非循环 `scrape()`
- ⚡ **合理缓存**: 设置适当的 `max_age` 参数
- ⚡ **限制并发**: 避免触发速率限制
- ⚡ **错误重试**: 设置 `max_retries=3`

---

## 🎓 学习路径

### 初级（第 1 周）

1. ✅ **完成 SDK 配置**（本文档）
2. 运行 `quick_start.py` 学习基础用法
3. 阅读 `FIRECRAWL_CLOUD_SETUP_GUIDE.md`
4. 实现一个简单的新闻爬虫

### 中级（第 2-4 周）

1. 学习 Actions 功能（页面交互）
2. 实现 Batch Scrape（批量爬取）
3. 集成 Search API（搜索 + 爬取）
4. 实现错误处理和重试机制

### 高级（第 1-3 月）

1. 实现成本监控和预算控制
2. 集成 Redis 缓存系统
3. 实现密钥轮换和负载均衡
4. 部署到生产环境

---

## 🛠️ 故障排查

### 常见问题

#### 1. 导入错误

```python
ImportError: No module named 'firecrawl'
```

**解决方案**:

```bash
pip3 install --break-system-packages firecrawl-py
```

#### 2. API 密钥错误

```python
FirecrawlError: Invalid API key
```

**解决方案**:

1. 检查 `.env` 文件是否存在
2. 确认 API 密钥格式正确（`fc-xxx`）
3. 运行 `python3 test_api_keys.py` 验证

#### 3. 参数名称错误

```python
TypeError: got an unexpected keyword argument 'onlyMainContent'
```

**解决方案**: 使用下划线命名 `only_main_content=True`

#### 4. 返回值访问错误

```python
AttributeError: 'Document' object has no attribute 'get'
```

**解决方案**: 使用属性访问 `result.markdown` 而非 `result.get("markdown")`

---

## 📊 配置统计

| 项目        | 数值            |
| ----------- | --------------- |
| Python 版本 | 3.14.0          |
| 已安装包    | 15+             |
| 配置文件    | 4 个            |
| API 密钥    | 4 个（1主+3备） |
| 测试数据    | 21,404 字符     |
| 配置耗时    | ~5 分钟         |

---

## ✅ 配置清单

- [x] Python 环境检查
- [x] pip 工具验证
- [x] 依赖包安装
- [x] 环境变量配置
- [x] Git 忽略文件
- [x] API 密钥测试
- [x] 示例脚本准备
- [x] 文档资源整理

---

## 🎉 下一步行动

### 立即可做

1. 运行 `python3 quick_start.py` 查看示例
2. 运行 `python3 test_api_keys.py` 测试所有密钥
3. 阅读 `firecrawl_changelog.md` 了解最新功能

### 本周任务

1. 实现 HawaiiHub 新闻爬虫
2. 集成 NewsAPI（已配置）+ Firecrawl（已配置）
3. 建立数据清洗和存储流程

### 本月目标

1. 完成夏威夷本地新闻采集系统
2. 实现自动化定时任务
3. 部署到生产环境

---

**配置完成时间**: 2025-10-27
**配置人员**: HawaiiHub AI Team
**项目状态**: ✅ 就绪，可以开始开发

---

## 📮 获取帮助

- **项目文档**: `/Users/zhiledeng/Downloads/FireShot/`
- **官方文档**: https://docs.firecrawl.dev/
- **Discord 社区**: https://discord.gg/firecrawl
- **GitHub Issues**: https://github.com/firecrawl/firecrawl/issues
