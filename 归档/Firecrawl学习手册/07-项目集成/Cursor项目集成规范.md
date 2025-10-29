# Firecrawl 专项规则

> **最后更新**: 2025-10-27
> **SDK 版本**: v2.x
> **适用场景**: Firecrawl 云 API 使用

---

## 🔥 核心原则

### 1. 工具选择优先级

```
P0: MCP 工具（最简单、最可靠）
├─ 复杂页面（大量 JS、动态加载）
├─ 快速原型验证
└─ 单次爬取需求

P1: Python SDK v2（需要更多控制）
├─ 批量爬取（batch_scrape）
├─ 整站爬取（crawl）
├─ 搜索+爬取（search）
└─ 需要高级配置

P2: 手动实现（不推荐）
└─ 仅在 Firecrawl 不可用时考虑
```

---

## 🆕 SDK v2 重要变化

### 命名约定（重要！）

| 场景           | v1 (旧)           | v2 (新)             | 说明        |
| -------------- | ----------------- | ------------------- | ----------- |
| **MCP 工具**   | `onlyMainContent` | `onlyMainContent`   | ✅ 驼峰式   |
| **Python SDK** | `onlyMainContent` | `only_main_content` | ✅ 下划线   |
| **返回值**     | `dict`            | `Document` 对象     | ⚠️ 类型变化 |

### 正确用法示例

```python
# ✅ MCP 工具（驼峰式）
result = mcp_firecrawl_scrape(
    url="https://example.com",
    formats=["markdown"],
    onlyMainContent=True  # 驼峰式
)

# ✅ Python SDK v2（下划线）
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    only_main_content=True  # 下划线
)

# ✅ 访问结果（属性，不是字典）
content = result.markdown  # 正确
title = result.metadata.title  # 正确

# ❌ 错误写法
content = result.get("markdown")  # 会报错
content = result["markdown"]  # 会报错
```

---

## 📊 常用 API 方法

### 1. scrape() - 单页爬取

```python
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],           # 可选: markdown, html, rawHtml, links
    only_main_content=True,         # 只提取主要内容
    max_age=172800000,              # 缓存 2 天（毫秒）
    block_ads=True,                 # 屏蔽广告
    skip_tls_verification=False,    # TLS 验证
    remove_base64_images=True       # 移除 base64 图片
)

# 访问结果
markdown = result.markdown
html = result.html
url = result.url
title = result.metadata.title if result.metadata else None
```

### 2. batch_scrape() - 批量爬取

```python
urls = ["url1", "url2", "url3"]
results = app.batch_scrape(
    urls=urls,
    formats=["markdown"],
    only_main_content=True
)

# 处理结果
for item in results:
    if isinstance(item, tuple):
        success, result = item
        if success:
            print(result.markdown)
    else:
        print(item.markdown)
```

### 3. crawl() - 整站爬取

```python
# 启动爬取
crawl_result = app.crawl(
    url="https://example.com",
    max_depth=3,                # 最大深度
    limit=100,                  # 最大页面数
    allow_backward_links=False, # 允许向后链接
    allow_external_links=False, # 允许外部链接
    formats=["markdown"]
)

# 获取 ID
crawl_id = crawl_result.id

# 检查状态
status = app.check_crawl_status(crawl_id)
```

### 4. search() - 搜索+爬取

```python
results = app.search(
    query="夏威夷 华人 餐厅",
    sources=[{"type": "web"}],
    limit=10,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)
```

### 5. map() - 获取站点地图

```python
site_map = app.map(
    url="https://example.com",
    search="news",  # 可选：搜索特定内容
    limit=1000
)

# 获取所有链接
urls = site_map.links
```

---

## ⚡ 性能优化

### 1. 使用缓存（节省 50%+ 成本）

```python
# ✅ 推荐：使用缓存
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    max_age=172800000  # 2 天缓存（毫秒）
)

# 缓存策略
CACHE_TTL = {
    "news": 3600000,      # 1 小时（新闻更新快）
    "products": 43200000, # 12 小时（商品中等）
    "company": 86400000   # 24 小时（公司信息慢）
}
```

### 2. 批量处理

```python
# ✅ 推荐：批量爬取
urls = ["url1", "url2", "url3", "url4", "url5"]
results = app.batch_scrape(urls, formats=["markdown"])

# ❌ 避免：逐个爬取
for url in urls:
    result = app.scrape(url)  # 慢且贵
```

### 3. 只提取需要的格式

```python
# ✅ 推荐：只要 markdown
result = app.scrape(url, formats=["markdown"])

# ❌ 避免：要所有格式
result = app.scrape(url, formats=["markdown", "html", "rawHtml", "links"])
```

---

## 🛡️ 错误处理模板

### 标准错误处理

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import RequestTimeoutError, RateLimitError
import logging
import time

def safe_scrape(url: str, max_retries: int = 3) -> dict | None:
    """
    安全爬取，带重试和日志

    Args:
        url: 目标 URL
        max_retries: 最大重试次数

    Returns:
        爬取结果，失败返回 None
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    for attempt in range(max_retries):
        try:
            result = app.scrape(
                url=url,
                formats=["markdown"],
                only_main_content=True
            )

            # 验证结果
            if not result or not hasattr(result, "markdown"):
                raise ValueError("返回结果无效")

            logging.info(f"成功爬取: {url}")
            return result

        except RequestTimeoutError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logging.warning(
                    f"超时，{wait_time}秒后重试... "
                    f"({attempt+1}/{max_retries})"
                )
                time.sleep(wait_time)
            else:
                logging.error(
                    f"失败（{max_retries}次重试后）: {url} - {e}"
                )
                return None

        except RateLimitError as e:
            logging.error(f"速率限制: {url} - 考虑切换密钥")
            return None

        except Exception as e:
            logging.error(f"未知错误: {url} - {e}")
            return None

    return None
```

---

## 💰 成本控制

### 1. 请求计数

```python
class FirecrawlClient:
    """带成本控制的客户端"""

    def __init__(self, api_key: str, daily_budget: float = 10.0):
        self.app = FirecrawlApp(api_key=api_key)
        self.daily_budget = daily_budget
        self.request_count = 0
        self.total_cost = 0.0

    def scrape(self, url: str, **kwargs) -> dict:
        # 检查预算
        if self.total_cost >= self.daily_budget:
            raise BudgetExceededError(
                f"超出每日预算: ${self.daily_budget}"
            )

        # 执行爬取
        result = self.app.scrape(url, **kwargs)

        # 记录成本（假设 $0.01/请求）
        cost = 0.01
        self.request_count += 1
        self.total_cost += cost

        logging.info(
            f"请求 #{self.request_count} | "
            f"成本: ${cost:.4f} | "
            f"累计: ${self.total_cost:.2f}/{self.daily_budget}"
        )

        return result
```

### 2. 密钥轮换

```python
import itertools

class RotatingFirecrawlClient:
    """支持密钥轮换的客户端"""

    def __init__(self, api_keys: List[str]):
        self.api_keys = itertools.cycle(api_keys)
        self.current_key = next(self.api_keys)
        self.app = FirecrawlApp(api_key=self.current_key)

    def scrape(self, url: str, **kwargs) -> dict:
        try:
            return self.app.scrape(url, **kwargs)
        except RateLimitError:
            # 切换到下一个密钥
            self.current_key = next(self.api_keys)
            self.app = FirecrawlApp(api_key=self.current_key)
            logging.info(f"切换密钥: {self.current_key[:10]}...")
            return self.app.scrape(url, **kwargs)

# 使用
client = RotatingFirecrawlClient([
    os.getenv("FIRECRAWL_API_KEY"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_3"),
])
```

---

## 📋 最佳实践清单

### ✅ 必须做

- [ ] 使用环境变量存储 API 密钥
- [ ] 实现完整的错误处理（try-except）
- [ ] 设置合理的超时时间（60 秒）
- [ ] 启用缓存（max_age）
- [ ] 记录所有 API 调用日志
- [ ] 验证返回结果
- [ ] 使用 `only_main_content=True`

### ❌ 禁止做

- [ ] 硬编码 API 密钥
- [ ] 跳过错误处理
- [ ] 无限重试
- [ ] 不检查缓存直接爬取
- [ ] 串行处理大量 URL
- [ ] 不记录成本

---

## 🔗 参考资源

- 官方文档: https://docs.firecrawl.dev/
- SDK GitHub: https://github.com/mendableai/firecrawl-py
- MCP 服务器: https://github.com/firecrawl/mcp-server-firecrawl
- Discord 社区: https://discord.gg/firecrawl

---

_最后更新: 2025-10-27_
_SDK 版本: v2.x_
_维护者: HawaiiHub AI Team_
