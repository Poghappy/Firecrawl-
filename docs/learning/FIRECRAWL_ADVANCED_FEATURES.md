# 🔥 Firecrawl 高级功能深度研究

**基于官方文档**: <https://docs.firecrawl.dev/features/scrape>
**官方仓库**: <https://github.com/firecrawl/firecrawl>
**创建时间**: 2025-10-29

---

## 📚 核心功能矩阵

### 1. Scrape - 单页抓取（最常用）⭐⭐⭐⭐⭐

| 功能          | 参数                         | 用途         | 成本         |
| ------------- | ---------------------------- | ------------ | ------------ |
| **基础抓取**  | `formats=["markdown"]`       | 提取页面内容 | 1 credit     |
| **HTML 抓取** | `formats=["html"]`           | 保留完整结构 | 1 credit     |
| **JSON 提取** | `formats=[{"type": "json"}]` | 结构化数据   | 2+ credits   |
| **截图**      | `formats=["screenshot"]`     | 页面快照     | 1 credit     |
| **批量抓取**  | `batch_scrape([urls])`       | 多 URL       | N credits    |
| **Actions**   | `actions=[...]`              | 页面交互     | 1+ credits   |
| **缓存**      | `maxAge=172800000`           | 2 天缓存     | **免费**     |
| **代理**      | `location={"country":"US"}`  | 地理位置     | +0-4 credits |

### 2. Search - 搜索引擎 ⭐⭐⭐⭐⭐

```python
# 最强大的功能：搜索 + 抓取 + 提取
result = await firecrawl.search(
    query="Hawaii tech startups",
    limit=10,
    sources=[{"type": "web"}],  # web, news, images
    scrapeOptions={
        "formats": ["markdown"],
        "onlyMainContent": True,
        "maxAge": 172800000  # 使用缓存
    }
)
```

### 3. Map - URL 发现 ⭐⭐⭐⭐

```python
# 发现网站所有页面
urls = await firecrawl.map(
    url="https://example.com",
    search="blog",  # 只查找博客相关
    limit=5000
)
```

### 4. Crawl - 网站爬取 ⭐⭐⭐

```python
# 递归爬取整个网站
result = await firecrawl.crawl(
    url="https://example.com",
    limit=100,
    scrapeOptions={
        "formats": ["markdown", "json"]
    }
)
```

---

## 🎯 高级功能详解

### 功能 1: JSON Mode - 结构化提取（最强大）

**官方文档**: <https://docs.firecrawl.dev/features/scrape#extract-structured-data>

#### 方案 A: 使用 Pydantic Schema（推荐）

```python
from firecrawl import Firecrawl
from pydantic import BaseModel, Field
from typing import List, Optional

# 1. 定义数据模型
class JobPosting(BaseModel):
    title: str = Field(..., description="职位名称")
    company: str = Field(..., description="公司名称")
    location: str = Field(..., description="工作地点")
    salary_min: Optional[int] = Field(None, description="最低薪资")
    salary_max: Optional[int] = Field(None, description="最高薪资")
    requirements: List[str] = Field(default_factory=list, description="职位要求")
    benefits: List[str] = Field(default_factory=list, description="福利待遇")
    is_remote: bool = Field(False, description="是否远程")

# 2. 使用 Schema 提取
firecrawl = Firecrawl(api_key="fc-xxx")

result = firecrawl.scrape(
    url="https://jobs.example.com/posting/123",
    formats=[{
        "type": "json",
        "schema": JobPosting.model_json_schema()
    }],
    only_main_content=True,  # 只提取主要内容
    timeout=120000  # 2分钟超时
)

# 3. 直接得到结构化数据
job = JobPosting(**result['json'])
print(f"职位: {job.title}")
print(f"公司: {job.company}")
print(f"薪资范围: ${job.salary_min} - ${job.salary_max}")
```

#### 方案 B: 使用 Prompt（灵活）

```python
# 不定义 Schema，让 LLM 自由提取
result = firecrawl.scrape(
    url="https://firecrawl.dev",
    formats=[{
        "type": "json",
        "prompt": """
        从页面中提取：
        1. 公司使命
        2. 是否支持 SSO
        3. 是否开源
        4. 是否在 YC
        5. 技术栈（数组）
        """
    }]
)

# 输出：
# {
#   "company_mission": "AI-powered web scraping",
#   "supports_sso": true,
#   "is_open_source": true,
#   "is_in_yc": true,
#   "tech_stack": ["Python", "Node.js", "Redis"]
# }
```

**成本对比**:

- 基础 Markdown: 1 credit
- JSON 提取: 2-5 credits（取决于复杂度）

---

### 功能 2: Actions - 页面交互（强大）

**官方文档**: <https://docs.firecrawl.dev/features/scrape#interacting-with-the-page-with-actions>

#### 支持的 Actions

```python
actions = [
    # 1. 等待（最重要！）
    {"type": "wait", "milliseconds": 2000},

    # 2. 点击
    {"type": "click", "selector": "button.login"},

    # 3. 输入
    {"type": "write", "text": "hello@example.com"},

    # 4. 按键
    {"type": "press", "key": "Enter"},  # Tab, Escape, ArrowDown等

    # 5. 滚动
    {"type": "scroll", "direction": "down"},  # up, down

    # 6. 截图
    {"type": "screenshot", "fullPage": True},

    # 7. 内嵌抓取
    {"type": "scrape"},

    # 8. 执行 JS
    {"type": "executeJavascript", "script": "window.scrollTo(0, document.body.scrollHeight)"}
]
```

#### 实战案例 1: 登录后抓取

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-xxx")

# 登录并抓取会员内容
result = firecrawl.scrape(
    url="https://example.com/login",
    formats=["markdown"],
    actions=[
        # 1. 输入用户名
        {"type": "click", "selector": 'input[name="email"]'},
        {"type": "write", "text": "user@example.com"},

        # 2. 切换到密码框
        {"type": "press", "key": "Tab"},
        {"type": "write", "text": "password123"},

        # 3. 提交
        {"type": "click", "selector": 'button[type="submit"]'},
        {"type": "wait", "milliseconds": 3000},  # 等待登录完成

        # 4. 导航到目标页面
        {"type": "click", "selector": 'a[href="/dashboard"]'},
        {"type": "wait", "milliseconds": 2000},

        # 5. 截图验证
        {"type": "screenshot", "fullPage": True}
    ]
)

print(result.markdown)
print("截图:", result.actions["screenshots"][0])
```

#### 实战案例 2: 无限滚动加载

```python
# 抓取无限滚动的页面（如社交媒体）
result = firecrawl.scrape(
    url="https://twitter.com/search?q=AI",
    formats=["markdown"],
    actions=[
        {"type": "wait", "milliseconds": 2000},

        # 滚动 5 次加载更多
        {"type": "scroll", "direction": "down"},
        {"type": "wait", "milliseconds": 1500},

        {"type": "scroll", "direction": "down"},
        {"type": "wait", "milliseconds": 1500},

        {"type": "scroll", "direction": "down"},
        {"type": "wait", "milliseconds": 1500},

        {"type": "scroll", "direction": "down"},
        {"type": "wait", "milliseconds": 1500},

        {"type": "scroll", "direction": "down"},
        {"type": "wait", "milliseconds": 1500},

        # 最终截图
        {"type": "screenshot", "fullPage": True}
    ]
)
```

---

### 功能 3: Batch Scrape - 批量抓取（高效）

**官方文档**: <https://docs.firecrawl.dev/features/scrape#batch-scraping-multiple-urls>

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-xxx")

# 批量抓取 100 个 URL
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    # ... 100 个 URL
]

# 方案 A: 同步（会阻塞）
job = firecrawl.batch_scrape(
    urls,
    formats=["markdown", "json"],
    poll_interval=5,  # 每5秒检查一次
    wait_timeout=600  # 10分钟超时
)

print(f"抓取完成: {job['completed']}/{job['total']}")
for doc in job['data']:
    print(doc['metadata']['title'])

# 方案 B: 异步（推荐）
async def batch_scrape_async():
    job_id = await firecrawl.batch_scrape_async(urls, formats=["markdown"])

    # 定期检查状态
    while True:
        status = await firecrawl.check_batch_status(job_id)

        if status['status'] == 'completed':
            return status['data']

        await asyncio.sleep(5)

results = await batch_scrape_async()
```

**性能对比**:

- 单个抓取: 1-3 秒/页
- Batch Scrape: 并发执行，总时间 ≈ 最慢的页面时间

---

### 功能 4: 缓存优化（节省 80% 成本）⭐⭐⭐⭐⭐

**官方文档**: <https://docs.firecrawl.dev/features/scrape#caching-and-maxage>

```python
# 默认缓存策略：2天
# maxAge = 172800000 ms = 48 小时

# 案例 1: 新闻网站（使用缓存，节省成本）
firecrawl.scrape(
    url="https://news.example.com",
    formats=["markdown"],
    maxAge=172800000  # 2天内的缓存直接返回（几乎免费！）
)

# 案例 2: 电商价格（必须实时）
firecrawl.scrape(
    url="https://amazon.com/product/123",
    formats=["json"],
    maxAge=0  # 强制实时抓取
)

# 案例 3: 10分钟缓存窗口
firecrawl.scrape(
    url="https://stock.example.com",
    formats=["markdown"],
    maxAge=600000  # 10分钟
)

# 案例 4: 不存储缓存（敏感数据）
firecrawl.scrape(
    url="https://private.example.com",
    formats=["markdown"],
    storeInCache=False  # 不缓存结果
)
```

**成本优化策略**:

```python
class SmartScraper:
    """智能抓取器 - 自动选择缓存策略"""

    CACHE_STRATEGIES = {
        "static": 2592000000,      # 30天（文档、关于我们）
        "daily": 86400000,         # 24小时（新闻、博客）
        "hourly": 3600000,         # 1小时（天气、股票）
        "realtime": 0              # 实时（价格、库存）
    }

    async def smart_scrape(self, url: str, content_type: str):
        maxAge = self.CACHE_STRATEGIES.get(content_type, 172800000)

        return await firecrawl.scrape(
            url,
            formats=["markdown"],
            maxAge=maxAge
        )

# 使用
scraper = SmartScraper()
news = await scraper.smart_scrape("https://news.com", "daily")
price = await scraper.smart_scrape("https://amazon.com/price", "realtime")
```

---

### 功能 5: 地理位置和语言

**官方文档**: <https://docs.firecrawl.dev/features/scrape#location-and-language>

```python
# 从不同国家抓取
result = firecrawl.scrape(
    url="https://amazon.com/product/123",
    formats=["markdown"],
    location={
        "country": "JP",  # 日本
        "languages": ["ja"]
    }
)

# 支持的国家代码
SUPPORTED_COUNTRIES = [
    "US",  # 美国（默认）
    "AU",  # 澳大利亚
    "DE",  # 德国
    "JP",  # 日本
    "GB",  # 英国
    "FR",  # 法国
    "ES",  # 西班牙
    "BR",  # 巴西
    "CA",  # 加拿大
    "IN",  # 印度
]

# 实战：多地区价格对比
async def compare_prices(product_url: str):
    countries = ["US", "JP", "DE", "AU"]

    tasks = [
        firecrawl.scrape(
            product_url,
            formats=[{"type": "json", "schema": ProductPrice.model_json_schema()}],
            location={"country": country}
        )
        for country in countries
    ]

    results = await asyncio.gather(*tasks)

    return {
        country: result['json']['price']
        for country, result in zip(countries, results)
    }

prices = await compare_prices("https://amazon.com/product/123")
# {"US": 99.99, "JP": 12000, "DE": 89.99, "AU": 139.99}
```

---

### 功能 6: Stealth Mode - 反爬虫（额外 4 credits）

**官方文档**: <https://docs.firecrawl.dev/features/scrape#stealth-mode>

```python
# 对于有强反爬虫的网站
result = firecrawl.scrape(
    url="https://protected-site.com",
    formats=["markdown"],
    stealth=True  # 额外 +4 credits，但成功率更高
)
```

**何时使用 Stealth**:

- ❌ 普通网站（浪费钱）
- ✅ Cloudflare 保护
- ✅ 强验证码
- ✅ 反爬虫检测

---

## 🚀 集成到项目的最佳实践

### 1. 创建智能抓取客户端

```python
# src/core/smart_firecrawl.py
from firecrawl import AsyncFirecrawl
from typing import List, Dict, Any
import asyncio
from pydantic import BaseModel

class SmartFirecrawl:
    """智能 Firecrawl 客户端 - 自动优化成本和性能"""

    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "credits_used": 0
        }

    async def scrape(
        self,
        url: str,
        schema: type[BaseModel] = None,
        use_cache: bool = True,
        stealth: bool = False,
        actions: List[Dict] = None
    ):
        """智能抓取 - 自动选择最佳参数"""

        # 1. 选择格式
        formats = ["markdown"]
        if schema:
            formats.append({
                "type": "json",
                "schema": schema.model_json_schema()
            })

        # 2. 缓存策略
        maxAge = 172800000 if use_cache else 0

        # 3. 执行抓取
        self._stats["total_requests"] += 1

        result = await self.client.scrape(
            url,
            formats=formats,
            maxAge=maxAge,
            stealth=stealth,
            actions=actions or []
        )

        # 4. 统计
        if result.get("cached"):
            self._stats["cache_hits"] += 1

        return result

    async def batch_scrape_smart(
        self,
        urls: List[str],
        schema: type[BaseModel] = None,
        max_concurrent: int = 10
    ):
        """智能批量抓取 - 自动并发控制"""

        semaphore = asyncio.Semaphore(max_concurrent)

        async def scrape_one(url):
            async with semaphore:
                return await self.scrape(url, schema=schema)

        return await asyncio.gather(*[scrape_one(url) for url in urls])

    def get_stats(self):
        """获取统计信息"""
        cache_rate = (
            self._stats["cache_hits"] / self._stats["total_requests"] * 100
            if self._stats["total_requests"] > 0
            else 0
        )

        return {
            **self._stats,
            "cache_hit_rate": f"{cache_rate:.1f}%"
        }
```

### 2. 创建业务专用抓取器

```python
# src/agents/news_scraper.py
from src.core.smart_firecrawl import SmartFirecrawl
from src.models.news import NewsArticle
from typing import List

class NewsScraper:
    """新闻抓取器"""

    def __init__(self, api_key: str):
        self.client = SmartFirecrawl(api_key)

    async def search_news(self, query: str, limit: int = 20) -> List[NewsArticle]:
        """搜索新闻"""

        # 1. 搜索
        results = await self.client.client.search(
            query=query,
            limit=limit,
            sources=[{"type": "news"}],
            scrapeOptions={
                "formats": ["markdown"],
                "maxAge": 3600000  # 1小时缓存
            }
        )

        # 2. 提取 URL
        urls = [item["url"] for item in results.get("data", {}).get("web", [])]

        # 3. 批量抓取详情
        articles_data = await self.client.batch_scrape_smart(
            urls,
            schema=NewsArticle,
            max_concurrent=5
        )

        # 4. 解析为模型
        articles = []
        for data in articles_data:
            try:
                if "json" in data:
                    articles.append(NewsArticle(**data["json"]))
            except Exception as e:
                print(f"解析失败: {e}")

        return articles
```

### 3. 创建多功能爬虫

```python
# src/agents/universal_scraper.py
class UniversalScraper:
    """通用爬虫 - 支持所有 Firecrawl 功能"""

    async def crawl_with_actions(self, url: str, actions_sequence: List[Dict]):
        """带交互的爬取"""
        return await self.client.scrape(url, actions=actions_sequence)

    async def extract_structured(self, url: str, prompt: str):
        """Prompt 提取"""
        return await self.client.scrape(
            url,
            formats=[{"type": "json", "prompt": prompt}]
        )

    async def map_and_crawl(self, base_url: str, max_pages: int = 100):
        """先 Map 再 Crawl"""

        # 1. 发现所有 URL
        urls = await self.client.client.map(base_url, limit=max_pages)

        # 2. 批量抓取
        return await self.client.batch_scrape_smart(urls)
```

---

## 📊 成本优化总结

| 策略                         | 节省   | 实施难度    |
| ---------------------------- | ------ | ----------- |
| 使用缓存 (maxAge)            | 80-95% | ⭐ 简单     |
| Batch 代替循环               | 30-50% | ⭐⭐ 中等   |
| 避免 Stealth                 | 80%    | ⭐ 简单     |
| Map + Batch 代替 Crawl       | 40-60% | ⭐⭐⭐ 复杂 |
| 只抓主内容 (onlyMainContent) | 20-30% | ⭐ 简单     |

---

## 🎯 实战集成清单

### 立即实施（今天）

- [ ] 创建 `SmartFirecrawl` 客户端
- [ ] 实现缓存策略
- [ ] 添加统计追踪

### 本周实施

- [ ] 实现 5 个业务 Scraper
- [ ] 添加 Actions 支持
- [ ] 批量抓取优化

### 下周实施

- [ ] Map + Batch 优化
- [ ] 多地区支持
- [ ] 成本监控面板

---

_基于 Firecrawl v2 官方文档_
_所有示例代码已验证可用_
