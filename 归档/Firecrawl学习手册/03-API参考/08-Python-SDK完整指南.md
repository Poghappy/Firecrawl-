# Firecrawl Python SDK 完整学习指南

**版本**: SDK v4.5.0
**官方文档**: https://docs.firecrawl.dev/sdks/python
**更新时间**: 2025-10-28
**维护者**: HawaiiHub AI Team

---

## 📚 目录

1. [快速开始](#快速开始)
2. [核心功能](#核心功能)
3. [高级特性](#高级特性)
4. [最佳实践](#最佳实践)
5. [错误处理](#错误处理)
6. [性能优化](#性能优化)
7. [实战案例](#实战案例)

---

## 🚀 快速开始

### 安装

```bash
# 基础安装
pip install firecrawl-py

# 包含开发工具
pip install firecrawl-py python-dotenv pydantic
```

### 基本用法

```python
from firecrawl import FirecrawlApp

# 初始化（从环境变量读取 API 密钥）
app = FirecrawlApp()

# 或者显式传入 API 密钥
app = FirecrawlApp(api_key="fc-YOUR-API-KEY")

# Scrape 单个 URL
result = app.scrape(
    url="https://firecrawl.dev",
    formats=["markdown", "html"]
)

print(result.markdown)  # 访问 Markdown 内容
print(result.metadata.title)  # 访问元数据
```

### 环境配置

**推荐做法**：使用 `.env` 文件管理 API 密钥

```bash
# .env 文件
FIRECRAWL_API_KEY=fc-YOUR-API-KEY
```

```python
import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# 加载环境变量
load_dotenv()

# 自动读取 FIRECRAWL_API_KEY
app = FirecrawlApp()
```

---

## 🔧 核心功能

### 1. Scrape - 单页采集

**基础用法**：

```python
# 最简单的用法
result = app.scrape("https://example.com")
print(result.markdown)

# 指定返回格式
result = app.scrape(
    url="https://example.com",
    formats=["markdown", "html", "links", "screenshot"]
)

# 访问不同格式的内容
print(result.markdown)    # Markdown 内容
print(result.html)        # HTML 内容
print(result.links)       # 页面链接列表
print(result.screenshot)  # Base64 截图
```

**高级选项**：

```python
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],

    # 只提取主要内容（去除导航、广告等）
    only_main_content=True,

    # 包含的 HTML 标签
    include_tags=["article", "main", "p"],

    # 排除的 HTML 标签
    exclude_tags=["nav", "footer", "aside"],

    # 等待时间（毫秒）
    wait_for=2000,

    # 移除 Base64 图片（减少响应大小）
    remove_base64_images=True,

    # 缓存控制（2天）
    max_age=172800000
)
```

### 2. Crawl - 深度爬取

**阻塞式爬取**（等待完成）：

```python
# 简单爬取（自动分页，等待完成）
job = app.crawl(
    url="https://docs.firecrawl.dev",
    limit=5,              # 限制页面数
    poll_interval=1,      # 轮询间隔（秒）
    timeout=120           # 超时时间（秒）
)

# 访问结果
print(f"状态: {job.status}")
print(f"完成: {job.completed}/{job.total}")
for doc in job.data:
    print(f"- {doc.metadata.source_url}")
```

**非阻塞式爬取**（启动后检查）：

```python
# 启动爬取任务
job = app.start_crawl(
    url="https://docs.firecrawl.dev",
    limit=10,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

print(f"任务 ID: {job.id}")

# 稍后检查状态
status = app.get_crawl_status(job.id)
print(f"进度: {status.completed}/{status.total}")

# 取消任务
ok = app.cancel_crawl(job.id)
print(f"已取消: {ok}")
```

**高级爬取选项**：

```python
job = app.crawl(
    url="https://example.com",
    limit=100,

    # 允许的域名
    allow_subdomains=True,
    allow_external_links=False,

    # 路径过滤
    include_paths=["/blog/*", "/docs/*"],
    exclude_paths=["/admin/*", "/api/*"],

    # 去重
    deduplicate_similar_urls=True,

    # 延迟（毫秒，避免速率限制）
    delay=1000,

    # 最大发现深度
    max_discovery_depth=3,

    # 最大并发数
    max_concurrency=5,

    # 站点地图
    sitemap="include",  # "skip", "include", "only"

    # Scrape 选项
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True,
        "remove_base64_images": True
    }
)
```

### 3. Map - 站点地图

**发现所有 URL**：

```python
# 生成站点地图
result = app.map(
    url="https://firecrawl.dev",
    limit=100,

    # 包含子域名
    include_subdomains=False,

    # 忽略查询参数
    ignore_query_parameters=True,

    # 站点地图策略
    sitemap="include",  # "skip", "include", "only"

    # 搜索过滤
    search="docs"  # 只包含匹配的 URL
)

# 访问 URL 列表
print(f"发现 {len(result.links)} 个 URL")
for link in result.links:
    print(f"- {link}")
```

### 4. Batch Scrape - 批量采集

**阻塞式批量**（等待完成）：

```python
urls = [
    "https://firecrawl.dev",
    "https://docs.firecrawl.dev",
    "https://blog.firecrawl.dev"
]

job = app.batch_scrape(
    urls=urls,
    formats=["markdown"],
    poll_interval=1,
    timeout=60
)

# 访问结果
for doc in job.data:
    print(f"URL: {doc.metadata.source_url}")
    print(f"内容: {doc.markdown[:100]}...")
```

**非阻塞式批量**：

```python
# 启动批量任务
job = app.start_batch_scrape(urls)

# 检查状态
status = app.get_batch_scrape_status(job.id)
print(f"进度: {status.completed}/{status.total}")
```

### 5. Search - 智能搜索

```python
# 搜索 + 爬取一体化
results = app.search(
    query="夏威夷 华人 餐厅",
    limit=10,

    # 搜索来源
    sources=[{"type": "web"}],  # "web", "images", "news"

    # 地理位置
    location="us",

    # 过滤条件
    filter="site:yelp.com OR site:tripadvisor.com",

    # Scrape 选项（可选）
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

# 访问搜索结果
for item in results.get("web", []):
    print(f"标题: {item.get('title')}")
    print(f"URL: {item.get('url')}")
    if "markdown" in item:
        print(f"内容: {item['markdown'][:100]}...")
```

---

## 🚀 高级特性

### 1. WebSocket 实时监控

```python
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    app = AsyncFirecrawl()

    # 启动爬取
    job = await app.start_crawl("https://firecrawl.dev", limit=5)

    # 实时监控进度
    async for snapshot in app.watcher(
        job.id,
        kind="crawl",
        poll_interval=2,
        timeout=120
    ):
        if snapshot.status == "completed":
            print("✅ 完成")
            for doc in snapshot.data:
                print(f"- {doc.metadata.source_url}")
            break
        elif snapshot.status == "failed":
            print("❌ 失败")
            break
        else:
            print(f"⏳ 进度: {snapshot.completed}/{snapshot.total}")

asyncio.run(main())
```

### 2. 分页控制

**手动分页**（单页）：

```python
from firecrawl import PaginationConfig

# 启动任务
job = app.start_crawl("https://example.com", limit=100)

# 获取第一页（不自动分页）
status = app.get_crawl_status(
    job.id,
    pagination_config=PaginationConfig(auto_paginate=False)
)

print(f"本页文档数: {len(status.data)}")
print(f"下一页 URL: {status.next}")

# 如果需要，手动获取下一页
if status.next:
    next_status = app.get_crawl_status(
        job.id,
        pagination_config=PaginationConfig(auto_paginate=False, next=status.next)
    )
```

**限制自动分页**：

```python
# 自动分页，但提前停止
status = app.get_crawl_status(
    job.id,
    pagination_config=PaginationConfig(
        max_pages=2,        # 最多 2 页
        max_results=50,     # 最多 50 个结果
        max_wait_time=15    # 最多等待 15 秒
    )
)
```

### 3. 异步操作

```python
import asyncio
from firecrawl import AsyncFirecrawl

async def main():
    app = AsyncFirecrawl()

    # 异步 Scrape
    doc = await app.scrape("https://firecrawl.dev", formats=["markdown"])
    print(doc.markdown)

    # 异步 Search
    results = await app.search("firecrawl", limit=2)
    print(results.get("web", []))

    # 异步 Crawl
    job = await app.start_crawl("https://docs.firecrawl.dev", limit=3)
    status = await app.get_crawl_status(job.id)
    print(status.status)

    # 异步 Batch Scrape
    batch_job = await app.batch_scrape(
        ["https://firecrawl.dev", "https://docs.firecrawl.dev"],
        formats=["markdown"],
        poll_interval=1,
        timeout=60
    )
    print(f"完成: {batch_job.completed}/{batch_job.total}")

asyncio.run(main())
```

---

## 🎯 最佳实践

### 1. API 密钥管理

```python
import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# ✅ 正确：使用环境变量
load_dotenv()
app = FirecrawlApp()  # 自动读取 FIRECRAWL_API_KEY

# ❌ 错误：硬编码
app = FirecrawlApp(api_key="fc-hardcoded-key")  # 永远不要这样做！
```

### 2. 错误处理

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import (
    RequestTimeoutError,
    RateLimitError,
    AuthenticationError,
)
import time
import logging

def safe_scrape(url: str, max_retries: int = 3) -> dict | None:
    """安全爬取，带重试机制"""
    app = FirecrawlApp()

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

            logging.info(f"✅ 成功爬取: {url}")
            return result

        except AuthenticationError as e:
            logging.error(f"❌ 认证失败: {e}")
            return None  # 密钥问题，不重试

        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logging.warning(f"⏳ 速率限制，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                logging.error(f"❌ 达到速率限制: {url}")
                return None

        except RequestTimeoutError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logging.warning(f"⏳ 超时，{wait_time}秒后重试... ({attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                logging.error(f"❌ 超时失败: {url}")
                return None

        except Exception as e:
            logging.error(f"❌ 未知错误: {url} - {e}")
            return None

    return None
```

### 3. 缓存优化

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_scrape(url: str, max_age: int = 172800000) -> str:
    """带缓存的爬取（使用 Firecrawl 内置缓存 + Python LRU）"""
    app = FirecrawlApp()

    result = app.scrape(
        url=url,
        formats=["markdown"],
        only_main_content=True,
        max_age=max_age  # 2天缓存
    )

    return result.markdown

# 使用
content1 = cached_scrape("https://firecrawl.dev")
content2 = cached_scrape("https://firecrawl.dev")  # 命中 Python LRU 缓存
```

### 4. 批量处理模式

```python
def scrape_batch_smart(urls: list[str], batch_size: int = 10) -> list[dict]:
    """智能批量爬取（分批处理 + 错误处理）"""
    app = FirecrawlApp()
    all_results = []

    # 分批处理
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]

        try:
            job = app.batch_scrape(
                urls=batch,
                formats=["markdown"],
                poll_interval=2,
                timeout=120
            )

            all_results.extend(job.data)
            print(f"✅ 批次 {i//batch_size + 1}: {len(job.data)} 个页面")

        except Exception as e:
            print(f"❌ 批次 {i//batch_size + 1} 失败: {e}")
            # 逐个重试
            for url in batch:
                try:
                    result = app.scrape(url, formats=["markdown"])
                    all_results.append(result)
                except Exception as e2:
                    print(f"  ❌ {url}: {e2}")

        time.sleep(1)  # 避免速率限制

    return all_results
```

---

## 💰 成本控制

### 请求计数器

```python
class FirecrawlClient:
    """带成本控制的 Firecrawl 客户端"""

    def __init__(self, daily_budget: float = 10.0):
        self.app = FirecrawlApp()
        self.daily_budget = daily_budget
        self.request_count = 0
        self.total_cost = 0.0
        self.cost_per_request = 0.01  # 假设 $0.01/请求

    def scrape(self, url: str, **kwargs) -> dict:
        """爬取并记录成本"""
        # 检查预算
        if self.total_cost >= self.daily_budget:
            raise Exception(f"❌ 超出每日预算: ${self.daily_budget}")

        # 执行爬取
        result = self.app.scrape(url=url, **kwargs)

        # 记录成本
        self.request_count += 1
        self.total_cost += self.cost_per_request

        logging.info(
            f"📊 请求 #{self.request_count} | "
            f"成本: ${self.cost_per_request:.4f} | "
            f"累计: ${self.total_cost:.2f}/{self.daily_budget}"
        )

        return result

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "request_count": self.request_count,
            "total_cost": self.total_cost,
            "budget": self.daily_budget,
            "remaining": self.daily_budget - self.total_cost
        }

# 使用
client = FirecrawlClient(daily_budget=10.0)
result = client.scrape("https://example.com", formats=["markdown"])
print(client.get_stats())
```

---

## 📊 实战案例

### 案例 1：爬取 Firecrawl 博客

```python
from firecrawl import FirecrawlApp
import json
from datetime import datetime

def scrape_firecrawl_blog():
    """爬取 Firecrawl 博客所有文章"""
    app = FirecrawlApp()

    # 1. 发现所有 URL
    print("🔍 发现博客 URL...")
    map_result = app.map(
        url="https://firecrawl.dev/blog",
        limit=100,
        search="blog"
    )

    blog_urls = [
        link for link in map_result.links
        if "/blog/" in link and link != "https://firecrawl.dev/blog"
    ]

    print(f"✅ 发现 {len(blog_urls)} 篇文章")

    # 2. 批量爬取
    print("📥 批量爬取文章...")
    job = app.batch_scrape(
        urls=blog_urls,
        formats=["markdown"],
        poll_interval=2,
        timeout=180
    )

    # 3. 保存结果
    articles = []
    for doc in job.data:
        articles.append({
            "url": doc.metadata.source_url,
            "title": doc.metadata.title,
            "description": doc.metadata.description,
            "content": doc.markdown,
            "scraped_at": datetime.now().isoformat()
        })

    # 保存 JSON
    with open("firecrawl_blog.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    # 保存 Markdown
    with open("firecrawl_blog.md", "w", encoding="utf-8") as f:
        f.write(f"# Firecrawl 博客文章汇总\n\n")
        f.write(f"> 爬取时间: {datetime.now()}\n\n")
        f.write(f"> 文章数量: {len(articles)}\n\n")

        for article in articles:
            f.write(f"## {article['title']}\n\n")
            f.write(f"**URL**: {article['url']}\n\n")
            f.write(f"{article['content']}\n\n")
            f.write("---\n\n")

    print(f"✅ 完成！保存了 {len(articles)} 篇文章")

if __name__ == "__main__":
    scrape_firecrawl_blog()
```

### 案例 2：夏威夷新闻监控

```python
from firecrawl import FirecrawlApp
import json
from datetime import datetime
from typing import List, Dict

HAWAII_NEWS_SOURCES = [
    "https://www.hawaiinewsnow.com/",
    "https://www.staradvertiser.com/",
    "https://www.civilbeat.org/",
]

def scrape_hawaii_news() -> List[Dict]:
    """爬取夏威夷新闻"""
    app = FirecrawlApp()
    all_articles = []

    for source in HAWAII_NEWS_SOURCES:
        print(f"📰 爬取 {source}...")

        try:
            # 1. 爬取首页
            result = app.scrape(
                url=source,
                formats=["markdown", "links"],
                only_main_content=True
            )

            # 2. 提取文章链接
            article_links = [
                link for link in result.links
                if "article" in link or "news" in link
            ][:10]  # 限制 10 篇

            # 3. 批量爬取文章
            if article_links:
                job = app.batch_scrape(
                    urls=article_links,
                    formats=["markdown"],
                    poll_interval=1,
                    timeout=60
                )

                for doc in job.data:
                    all_articles.append({
                        "source": source,
                        "url": doc.metadata.source_url,
                        "title": doc.metadata.title,
                        "content": doc.markdown,
                        "scraped_at": datetime.now().isoformat()
                    })

            print(f"✅ {source}: {len(article_links)} 篇文章")

        except Exception as e:
            print(f"❌ {source} 失败: {e}")

    # 保存结果
    output_file = f"hawaii_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！共采集 {len(all_articles)} 篇新闻")
    print(f"📄 保存到: {output_file}")

    return all_articles

if __name__ == "__main__":
    scrape_hawaii_news()
```

### 案例 3：竞品监控

```python
from firecrawl import FirecrawlApp
import json
from datetime import datetime
from typing import Dict, List

def monitor_competitor_changes(url: str, previous_content: str = None) -> Dict:
    """监控竞品网站变更"""
    app = FirecrawlApp()

    # 爬取当前内容
    result = app.scrape(
        url=url,
        formats=["markdown", "html"],
        only_main_content=True
    )

    current_content = result.markdown

    # 检测变化
    has_changed = previous_content and current_content != previous_content

    return {
        "url": url,
        "title": result.metadata.title,
        "has_changed": has_changed,
        "content": current_content,
        "content_length": len(current_content),
        "checked_at": datetime.now().isoformat()
    }

def monitor_multiple_competitors(urls: List[str]) -> None:
    """批量监控多个竞品"""
    results = []

    for url in urls:
        try:
            result = monitor_competitor_changes(url)
            results.append(result)

            if result["has_changed"]:
                print(f"⚠️  变更检测: {url}")
            else:
                print(f"✅ 无变更: {url}")

        except Exception as e:
            print(f"❌ 失败: {url} - {e}")

    # 保存报告
    report_file = f"competitor_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 监控报告已保存: {report_file}")

# 使用
competitors = [
    "https://competitor1.com/pricing",
    "https://competitor2.com/features",
    "https://competitor3.com/products",
]

monitor_multiple_competitors(competitors)
```

---

## 📚 参考资源

### 官方文档
- **Python SDK**: https://docs.firecrawl.dev/sdks/python
- **API 参考**: https://docs.firecrawl.dev/api-reference/v2-introduction
- **更新日志**: https://firecrawl.dev/changelog

### 项目文档
- **快速参考**: `QUICK_REFERENCE.md`
- **配置总结**: `SDK_CONFIGURATION_COMPLETE.md`
- **最佳实践**: `FIRECRAWL_CLOUD_API_RULES.md`

### 社区资源
- **Discord**: https://discord.gg/gSmWdAkdwd
- **GitHub**: https://github.com/mendableai/firecrawl
- **博客**: https://firecrawl.dev/blog

---

## 🎓 下一步

1. **实践练习**: 运行上面的实战案例
2. **探索高级功能**: WebSocket、异步操作、分页控制
3. **性能优化**: 缓存、批量处理、成本控制
4. **集成应用**: 将 Firecrawl 集成到你的项目中

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28
