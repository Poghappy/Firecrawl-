# 🔥 GitHub Python + Firecrawl 优秀项目推荐

**更新时间**: 2025-10-29
**筛选标准**: ⭐ Stars > 10, 活跃维护, 完整示例

---

## 🎯 推荐项目列表

### 1. 📰 新闻聚合系统

**适用场景**: 火鸟门户新闻资讯
**技术栈**: Python + Firecrawl + FastAPI + SQLite

**GitHub 搜索关键词**:

```
firecrawl python news scraper
firecrawl fastapi news aggregator
python web scraping news firecrawl
```

**参考实现**:

```python
# 基于官方示例改进
from firecrawl import AsyncFirecrawl
from datetime import datetime

class NewsAggregator:
    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)

    async def collect_news(self, sources: list[str]) -> list[dict]:
        """从多个新闻源并发采集"""
        tasks = [
            self.client.search(
                query=f"latest news site:{source}",
                limit=20,
                sources=[{"type": "news"}],
                tbs="qdr:d"  # 24小时内
            )
            for source in sources
        ]

        results = await asyncio.gather(*tasks)

        articles = []
        for result in results:
            for item in result.get("data", {}).get("web", []):
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description"),
                    "scraped_at": datetime.now().isoformat()
                })

        return articles

# 使用
aggregator = NewsAggregator(api_key="fc-xxx")
news = await aggregator.collect_news([
    "techcrunch.com",
    "theverge.com",
    "arstechnica.com"
])
```

---

### 2. 🛒 电商价格监控

**适用场景**: 省钱团购网
**技术栈**: Python + Firecrawl + Pandas + SQLite

**GitHub 搜索关键词**:

```
firecrawl python price monitoring
python ecommerce scraper firecrawl
price tracker firecrawl
```

**参考实现**:

```python
from firecrawl import AsyncFirecrawl
from pydantic import BaseModel
import pandas as pd

class Product(BaseModel):
    name: str
    price: float
    url: str

class PriceMonitor:
    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)

    async def track_prices(self, product_urls: list[str]) -> pd.DataFrame:
        """批量监控商品价格"""
        tasks = [
            self.client.scrape(
                url,
                formats=[{
                    "type": "json",
                    "schema": Product.model_json_schema()
                }],
                maxAge=0  # 实时价格
            )
            for url in product_urls
        ]

        results = await asyncio.gather(*tasks)

        # 转换为 DataFrame
        data = [
            {
                "name": r.json["name"],
                "price": r.json["price"],
                "url": r.json["url"],
                "timestamp": datetime.now()
            }
            for r in results
        ]

        return pd.DataFrame(data)

# 使用
monitor = PriceMonitor(api_key="fc-xxx")
df = await monitor.track_prices([
    "https://amazon.com/product/1",
    "https://amazon.com/product/2"
])

# 价格趋势分析
df.groupby('name')['price'].plot(kind='line')
```

---

### 3. 💼 招聘信息采集

**适用场景**: Aloha 招聘网
**技术栈**: Python + Firecrawl + Pydantic + PostgreSQL

**GitHub 搜索关键词**:

```
firecrawl python job scraper
indeed scraper firecrawl
python recruitment data extraction
```

**参考实现**:

```python
from firecrawl import AsyncFirecrawl
from pydantic import BaseModel
from typing import List

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    salary_range: str | None
    requirements: List[str]
    description: str

class JobScraper:
    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)

    async def search_jobs(self, keyword: str, location: str) -> list[JobPosting]:
        """搜索并提取招聘信息"""
        # 1. 搜索职位列表
        search_result = await self.client.search(
            query=f"{keyword} jobs {location}",
            limit=50,
            sources=[{"type": "web"}]
        )

        # 2. 提取职位 URL
        job_urls = [
            item["url"]
            for item in search_result.get("data", {}).get("web", [])
            if "job" in item["url"].lower()
        ]

        # 3. 批量抓取详情
        tasks = [
            self.client.scrape(
                url,
                formats=[{
                    "type": "json",
                    "schema": JobPosting.model_json_schema()
                }]
            )
            for url in job_urls[:20]  # 限制 20 个
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 4. 解析为 Pydantic 模型
        jobs = []
        for result in results:
            if not isinstance(result, Exception):
                try:
                    jobs.append(JobPosting(**result.json))
                except:
                    continue

        return jobs

# 使用
scraper = JobScraper(api_key="fc-xxx")
jobs = await scraper.search_jobs("Python Developer", "Remote")

for job in jobs:
    print(f"{job.title} @ {job.company}")
    print(f"Location: {job.location}")
    print(f"Salary: {job.salary_range}")
    print("---")
```

---

### 4. 🏠 房地产数据采集

**适用场景**: honolulu_rentals
**技术栈**: Python + Firecrawl + GeoPandas + Folium

**GitHub 搜索关键词**:

```
firecrawl python real estate scraper
zillow scraper python firecrawl
rental property data extraction
```

**参考实现**:

```python
from firecrawl import AsyncFirecrawl
from pydantic import BaseModel
import geopandas as gpd

class RentalListing(BaseModel):
    title: str
    price: float
    bedrooms: int
    bathrooms: float
    sqft: int
    address: str
    latitude: float | None
    longitude: float | None

class RealEstateScraper:
    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)

    async def crawl_rentals(self, base_url: str) -> gpd.GeoDataFrame:
        """爬取租房列表并生成地图"""
        # 1. 爬取列表页
        result = await self.client.crawl(
            url=base_url,
            limit=200,
            include_paths=["/rentals/*"],
            scrape_options={
                "formats": [{
                    "type": "json",
                    "schema": RentalListing.model_json_schema()
                }],
                "actions": [
                    {"type": "wait", "milliseconds": 2000},
                    {"type": "scroll", "direction": "down"}
                ]
            }
        )

        # 2. 转换为 GeoDataFrame
        listings = [RentalListing(**doc.json) for doc in result.data]

        gdf = gpd.GeoDataFrame(
            [l.dict() for l in listings],
            geometry=gpd.points_from_xy(
                [l.longitude for l in listings if l.longitude],
                [l.latitude for l in listings if l.latitude]
            )
        )

        return gdf

# 使用
scraper = RealEstateScraper(api_key="fc-xxx")
gdf = await scraper.crawl_rentals("https://rentals.example.com")

# 生成地图
import folium
m = folium.Map(location=[gdf.latitude.mean(), gdf.longitude.mean()])

for idx, row in gdf.iterrows():
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=f"{row.title} - ${row.price}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

m.save("rentals_map.html")
```

---

### 5. 📚 学术论文收集

**适用场景**: 学习网
**技术栈**: Python + Firecrawl + Scholarly + BibTeX

**GitHub 搜索关键词**:

```
firecrawl python research paper scraper
academic citation extraction firecrawl
arxiv scraper python
```

**参考实现**:

```python
from firecrawl import AsyncFirecrawl
from pydantic import BaseModel
from typing import List

class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    doi: str | None
    pdf_url: str | None
    keywords: List[str]

class AcademicScraper:
    def __init__(self, api_key: str):
        self.client = AsyncFirecrawl(api_key=api_key)

    async def search_papers(self, query: str, max_results: int = 50) -> list[ResearchPaper]:
        """搜索学术论文"""
        result = await self.client.search(
            query=query,
            limit=max_results,
            sources=[{"type": "web"}],
            categories=["research", "pdf"]  # 聚焦学术资源
        )

        # 提取论文 URL
        paper_urls = [
            item["url"]
            for item in result.get("data", {}).get("web", [])
            if any(domain in item["url"] for domain in ["arxiv.org", "ieee.org", "acm.org"])
        ]

        # 批量抓取论文信息
        tasks = [
            self.client.scrape(
                url,
                formats=[{
                    "type": "json",
                    "schema": ResearchPaper.model_json_schema()
                }],
                parsers=[{"type": "pdf", "maxPages": 5}]  # 只解析前5页
            )
            for url in paper_urls[:20]
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        papers = []
        for result in results:
            if not isinstance(result, Exception):
                try:
                    papers.append(ResearchPaper(**result.json))
                except:
                    continue

        return papers

# 使用
scraper = AcademicScraper(api_key="fc-xxx")
papers = await scraper.search_papers("machine learning web scraping")

# 导出为 BibTeX
for paper in papers:
    print(f"@article{{{paper.title.replace(' ', '_')},")
    print(f"  title={{{paper.title}}},")
    print(f"  author={{{', '.join(paper.authors)}}},")
    print(f"  doi={{{paper.doi}}},")
    print("}")
```

---

## 🛠️ 通用工具库推荐

### 1. 异步并发控制

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

async def bounded_gather(
    tasks: list[Callable],
    max_concurrent: int = 10
) -> list[T]:
    """限制并发数的 gather"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def run_with_limit(task):
        async with semaphore:
            return await task()

    return await asyncio.gather(*[run_with_limit(t) for t in tasks])

# 使用
async def scrape_url(url):
    return await client.scrape(url)

urls = ["https://example.com/1", "https://example.com/2", ...]
results = await bounded_gather(
    [lambda u=url: scrape_url(u) for url in urls],
    max_concurrent=5
)
```

### 2. 错误重试装饰器

```python
import asyncio
from functools import wraps

def retry_async(max_retries=3, backoff_factor=2):
    """异步重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    print(f"重试 {attempt + 1}/{max_retries}，等待 {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
        return wrapper
    return decorator

# 使用
@retry_async(max_retries=5)
async def scrape_with_retry(url: str):
    return await client.scrape(url)
```

### 3. 进度条集成

```python
from tqdm.asyncio import tqdm
import asyncio

async def scrape_with_progress(urls: list[str]):
    """带进度条的批量抓取"""
    async with AsyncFirecrawl() as client:
        results = []

        for url in tqdm(urls, desc="抓取进度"):
            try:
                result = await client.scrape(url)
                results.append(result)
            except Exception as e:
                tqdm.write(f"❌ {url}: {e}")

        return results

# 使用
urls = ["https://example.com/1", "https://example.com/2", ...]
results = await scrape_with_progress(urls)
```

---

## 📦 推荐的 Python 包组合

### 数据采集

```bash
pip install firecrawl-py
pip install httpx aiohttp  # HTTP 客户端
pip install beautifulsoup4 lxml  # HTML 解析（备用）
```

### 数据处理

```bash
pip install pandas  # 数据分析
pip install pydantic  # 数据验证
pip install python-dateutil  # 日期处理
```

### 存储

```bash
pip install sqlalchemy  # ORM
pip install alembic  # 数据库迁移
pip install redis  # 缓存
```

### 可视化

```bash
pip install matplotlib seaborn  # 图表
pip install folium  # 地图
pip install streamlit  # 快速 UI
```

### 调度

```bash
pip install apscheduler  # 定时任务
pip install celery  # 分布式任务队列
```

---

## 🎓 学习资源

### 官方文档

- ✅ Firecrawl Python SDK: https://docs.firecrawl.dev/sdks/python
- ✅ Firecrawl API 参考: https://docs.firecrawl.dev/api-reference/introduction

### 视频教程

- YouTube 搜索: "Firecrawl Python tutorial"
- Bilibili 搜索: "Firecrawl 教程"

### 博客文章

- Firecrawl 官方博客: https://firecrawl.dev/blog
- Python Web Scraping 2025

### 社区

- Discord: https://discord.gg/gSmWdAkdwd
- GitHub Discussions: https://github.com/mendableai/firecrawl/discussions

---

## 🚀 快速启动模板

### 最小可运行示例

```python
#!/usr/bin/env python3
"""
Firecrawl 快速启动模板
"""
import asyncio
from firecrawl import AsyncFirecrawl
from pydantic import BaseModel
from typing import List
import os

class Article(BaseModel):
    title: str
    content: str
    author: str | None = None

async def main():
    # 1. 初始化客户端
    api_key = os.getenv("FIRECRAWL_API_KEY")

    async with AsyncFirecrawl(api_key=api_key) as client:
        # 2. 搜索内容
        results = await client.search(
            query="Python web scraping",
            limit=5
        )

        urls = [item["url"] for item in results.get("data", {}).get("web", [])]

        # 3. 批量抓取
        tasks = [
            client.scrape(
                url,
                formats=[{
                    "type": "json",
                    "schema": Article.model_json_schema()
                }]
            )
            for url in urls[:3]
        ]

        articles = await asyncio.gather(*tasks, return_exceptions=True)

        # 4. 处理结果
        for i, article in enumerate(articles):
            if not isinstance(article, Exception):
                print(f"\n{i+1}. {article.json['title']}")
                print(f"   内容: {article.json['content'][:100]}...")

if __name__ == "__main__":
    asyncio.run(main())
```

**运行**:

```bash
export FIRECRAWL_API_KEY="fc-your-key"
python quick_start.py
```

---

## 🎯 总结

### 核心要点

1. ✅ **异步优先**: 使用 `AsyncFirecrawl` 提升性能
2. ✅ **类型安全**: 用 Pydantic 定义数据模型
3. ✅ **并发控制**: Semaphore 限制并发数
4. ✅ **错误处理**: 实现重试和异常捕获
5. ✅ **成本优化**: 使用缓存（maxAge）

### 适合你的项目

- ✅ 新闻聚合 → NewsAggregator 模板
- ✅ 价格监控 → PriceMonitor 模板
- ✅ 招聘采集 → JobScraper 模板
- ✅ 房产数据 → RealEstateScraper 模板
- ✅ 学术论文 → AcademicScraper 模板

---

_更新时间: 2025-10-29_
_适用版本: Firecrawl v4.5.0 + Python 3.9+_
