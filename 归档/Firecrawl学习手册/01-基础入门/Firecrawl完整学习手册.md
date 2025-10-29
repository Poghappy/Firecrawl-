# Firecrawl 完整学习手册

> **创建时间**: 2025-10-27
> **文档来源**: 官方中文文档 + 实战经验
> **适用版本**: v2.4.0
> **目标读者**: HawaiiHub 项目团队

---

## 📖 目录

- [第一章：Firecrawl 基础](#chapter-1)
- [第二章：核心功能详解](#chapter-2)
- [第三章：Python SDK 完全指南](#chapter-3)
- [第四章：高级特性](#chapter-4)
- [第五章：HawaiiHub 实战应用](#chapter-5)
- [第六章：最佳实践与优化](#chapter-6)
- [附录](#appendix)

---

<div id="chapter-1">

## 第一章：Firecrawl 基础

</div>

### 1.1 什么是 Firecrawl？

**Firecrawl** 是一个将网站转换为 LLM-ready（适配大语言模型）数据的开源 API 服务。

**核心价值**:

- ✅ **零配置**: 无需 sitemap，自动发现所有页面
- ✅ **LLM-ready**: 输出干净的 Markdown、结构化 JSON
- ✅ **解决棘手问题**: 代理、反爬、JS 渲染、速率限制
- ✅ **极速**: 数秒内返回结果，支持高吞吐场景
- ✅ **高度可定制**: 排除标签、自定义 headers、设置深度

### 1.2 开源 vs 云端

| 功能                        | 开源版 | 云端版         |
| --------------------------- | ------ | -------------- |
| 基础爬取                    | ✅     | ✅             |
| 高级反爬绕过                | ❌     | ✅             |
| 全球代理池                  | ❌     | ✅             |
| Actions（页面交互）         | ❌     | ✅             |
| Change Tracking（变更监控） | ❌     | ✅             |
| 99.9% 可用性                | ❌     | ✅             |
| 并发优化                    | 有限   | ✅ 高性能      |
| 免费额度                    | -      | 500 credits/月 |

**HawaiiHub 选择**: ✅ 云端版（高级功能 + 稳定性保证）

### 1.3 5 大核心功能

#### 1. **Scrape（单页爬取）**

- 输入：单个 URL
- 输出：Markdown、HTML、JSON、截图、摘要
- 适用：单篇文章、产品页面

#### 2. **Crawl（整站爬取）**

- 输入：起始 URL
- 输出：所有子页面的内容
- 适用：整站数据采集、文档爬取

#### 3. **Map（站点地图）**

- 输入：网站 URL
- 输出：所有 URL 列表
- 适用：快速发现网站结构

#### 4. **Search（智能搜索）**

- 输入：搜索关键词
- 输出：搜索结果 + 完整内容
- 适用：内容发现、竞品监控

#### 5. **Extract（数据提取）**

- 输入：URL + Schema/Prompt
- 输出：结构化数据
- 适用：表单数据、产品信息

### 1.4 快速上手（5 分钟）

#### 步骤 1: 安装 SDK

```bash
pip install firecrawl-py python-dotenv
```

#### 步骤 2: 配置 API Key

```bash
# .env
FIRECRAWL_API_KEY=fc-your-key-here
```

#### 步骤 3: 第一个爬取

```python
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# 爬取单页
result = app.scrape(
    url="https://www.hawaiinewsnow.com/",
    formats=["markdown"],
    only_main_content=True
)

print(result.markdown[:500])  # 前 500 字符
```

**预期输出**:

```
✅ 成功返回干净的 Markdown
📄 标题: Hawaii News Now - Breaking News...
📝 内容长度: ~36,000 字符
⏱️ 耗时: ~1 秒
```

---

<div id="chapter-2">

## 第二章：核心功能详解

</div>

### 2.1 Scrape（单页爬取）

#### 基本用法

```python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key="fc-your-key")

result = app.scrape(
    url="https://example.com",
    formats=["markdown"],         # 输出格式
    only_main_content=True       # 只要主要内容
)

# 访问结果（SDK v2）
content = result.markdown        # ✅ 属性访问
title = result.metadata.title
url = result.url
```

#### 支持的输出格式

| 格式         | 用途          | 示例           |
| ------------ | ------------- | -------------- |
| `markdown`   | LLM 训练、RAG | 博客文章、新闻 |
| `html`       | 保留结构      | 复杂布局       |
| `rawHtml`    | 原始 HTML     | 调试、分析     |
| `screenshot` | 可视化        | 页面快照       |
| `links`      | 链接提取      | SEO 分析       |
| `json`       | 结构化数据    | 产品信息       |
| `summary`    | 摘要          | 快速预览       |
| `images`     | 图片 URL      | 图像采集       |

#### 多格式同时获取

```python
result = app.scrape(
    url="https://example.com",
    formats=["markdown", "html", "links", "screenshot"]
)

# 访问不同格式
print(result.markdown)     # Markdown 内容
print(result.html)         # HTML 内容
print(result.links)        # 链接列表
print(result.screenshot)   # Base64 编码的截图
```

#### JSON 模式（结构化提取）

##### 方式 1: 使用 Schema

```python
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    author: str
    date: str
    summary: str

result = app.scrape(
    url="https://news.example.com/article",
    formats=[{
        "type": "json",
        "schema": Article.model_json_schema()
    }]
)

print(result.json)  # 结构化数据
```

##### 方式 2: 使用 Prompt（无 Schema）

```python
result = app.scrape(
    url="https://restaurant.com",
    formats=[{
        "type": "json",
        "prompt": "提取餐厅名称、地址、电话、营业时间"
    }]
)

print(result.json)  # LLM 自动决定结构
```

#### Actions（页面交互）

```python
result = app.scrape(
    url="https://google.com",
    formats=["markdown", "screenshot"],
    actions=[
        {"type": "wait", "milliseconds": 2000},
        {"type": "write", "text": "Firecrawl", "selector": "textarea[name='q']"},
        {"type": "press", "key": "Enter"},
        {"type": "wait", "milliseconds": 3000},
        {"type": "screenshot", "fullPage": False}
    ]
)
```

**支持的 Actions**:

- `wait` - 等待指定时间
- `click` - 点击元素
- `write` - 输入文本
- `press` - 按键
- `scroll` - 滚动页面
- `screenshot` - 截图

### 2.2 Crawl（整站爬取）

#### 基本用法

```python
# 阻塞式（等待完成）
crawl_result = app.crawl(
    url="https://example.com/blog/",
    limit=100,                    # 最多爬取 100 页
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

print(f"爬取了 {len(crawl_result.data)} 个页面")
for page in crawl_result.data:
    print(f"- {page.url}: {len(page.markdown)} 字符")
```

#### 非阻塞式（启动后轮询）

```python
# 启动爬取任务
crawl_job = app.start_crawl(
    url="https://example.com",
    limit=100
)

print(f"任务 ID: {crawl_job.id}")

# 检查状态
status = app.get_crawl_status(crawl_job.id)
print(f"状态: {status.status}")
print(f"已完成: {status.completed}/{status.total}")
```

#### 高级配置

```python
crawl_result = app.crawl(
    url="https://example.com",
    limit=200,
    max_depth=3,                  # 最大爬取深度
    allow_subdomains=False,        # 是否包含子域名
    crawl_entire_domain=False,     # 是否爬取整个域名
    scrape_options={
        "formats": ["markdown", {"type": "json", "prompt": "提取标题和日期"}],
        "only_main_content": True,
        "exclude_tags": ["nav", "footer", "aside"],
        "max_age": 3600000,        # 缓存 1 小时
    }
)
```

#### Crawl 参数详解

| 参数                  | 类型   | 默认值 | 说明             |
| --------------------- | ------ | ------ | ---------------- |
| `url`                 | string | -      | 起始 URL（必需） |
| `limit`               | int    | 10000  | 最大爬取页面数   |
| `max_depth`           | int    | -      | 最大爬取深度     |
| `allow_subdomains`    | bool   | False  | 是否包含子域名   |
| `crawl_entire_domain` | bool   | False  | 是否爬取整个域名 |
| `scrape_options`      | object | {}     | Scrape 选项      |
| `webhook`             | string | -      | Webhook URL      |

#### WebSocket 实时监控

```python
from firecrawl.utils import create_watcher

# 启动爬取任务
crawl_job = app.start_crawl(
    url="https://example.com",
    limit=50
)

# 创建监控器
watcher = create_watcher(crawl_job.id, app)

# 注册事件处理器
@watcher.on("page")
def on_page(page):
    print(f"✅ 爬取: {page.url} ({len(page.markdown)} 字符)")

@watcher.on("completed")
def on_completed(data):
    print(f"🎉 完成! 共 {len(data)} 页")

@watcher.on("failed")
def on_failed(error):
    print(f"❌ 失败: {error}")

# 开始监控
watcher.start()
```

### 2.3 Map（站点地图）

#### 基本用法

```python
map_result = app.map(
    url="https://example.com"
)

print(f"发现 {len(map_result.links)} 个 URL")
for url in map_result.links[:10]:
    print(f"- {url}")
```

#### 高级用法

```python
map_result = app.map(
    url="https://example.com",
    search="blog",              # 只包含 "blog" 的 URL
    ignore_sitemap=False,       # 使用 sitemap
    include_subdomains=False,   # 不包含子域名
    limit=5000                  # 最多返回 5000 个 URL
)
```

**应用场景**:

1. **先 Map 后 Crawl**: 先发现所有 URL，再批量爬取
2. **选择性爬取**: 只爬取特定路径
3. **站点分析**: 了解网站结构

### 2.4 Search（智能搜索）

#### 基本用法

```python
search_result = app.search(
    query="夏威夷 华人 餐厅",
    sources=[{"type": "web"}],  # 搜索来源：web、news、images
    limit=10
)

for item in search_result:
    print(f"标题: {item.title}")
    print(f"URL: {item.url}")
```

#### 搜索 + 爬取

```python
search_result = app.search(
    query="Firecrawl Python tutorial",
    sources=[{"type": "web"}],
    limit=5,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

# 直接获取搜索结果的完整内容
for item in search_result:
    print(f"\n{item.title}")
    print(f"{item.markdown[:200]}...")
```

#### 搜索分类（v2.1.0+）

```python
# GitHub 搜索
github_results = app.search(
    query="firecrawl python",
    categories=["github"]  # GitHub 仓库、代码、Issues、文档
)

# 学术搜索
research_results = app.search(
    query="AI machine learning",
    categories=["research"]  # arXiv、Nature、IEEE、PubMed
)

# PDF 搜索（v2.4.0+）
pdf_results = app.search(
    query="研究报告",
    categories=["pdf"]
)
```

### 2.5 Batch Scrape（批量爬取）

#### 基本用法

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

# 阻塞式（等待完成）
batch_result = app.batch_scrape(
    urls=urls,
    formats=["markdown"],
    only_main_content=True
)

for page in batch_result:
    print(f"{page.url}: {len(page.markdown)} 字符")
```

#### 非阻塞式

```python
# 启动批量任务
batch_job = app.start_batch_scrape(
    urls=urls,
    formats=["markdown"]
)

# 检查状态
status = app.get_batch_scrape_status(batch_job.id)
print(f"进度: {status.completed}/{status.total}")
```

---

<div id="chapter-3">

## 第三章：Python SDK 完全指南

</div>

### 3.1 安装与初始化

#### 安装

```bash
pip install firecrawl-py python-dotenv
```

#### 初始化

```python
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

# 方式 1: 环境变量
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# 方式 2: 直接传参
app = FirecrawlApp(api_key="fc-your-key-here")
```

### 3.2 SDK v2 重要变化

#### 命名约定变化

```python
# ✅ v2 正确（下划线）
result = app.scrape(
    url="...",
    only_main_content=True,    # ✅ 下划线
    max_age=172800000,          # ✅ 下划线
    block_ads=True,             # ✅ 下划线
    skip_tls_verification=True  # ✅ 下划线
)

# ❌ v1 错误（驼峰式）
result = app.scrape(
    url="...",
    onlyMainContent=True,       # ❌ 会报错
    maxAge=172800000            # ❌ 会报错
)
```

#### 返回值类型变化

```python
# ✅ v2 正确（Document 对象）
result = app.scrape(url="...", formats=["markdown"])

content = result.markdown       # ✅ 属性访问
title = result.metadata.title   # ✅ 元数据访问
url = result.url                # ✅ URL 访问

# ❌ v1 错误（字典访问）
content = result.get("markdown")      # ❌ 报错
content = result["markdown"]          # ❌ 报错
```

### 3.3 完整 API 参考

#### Scrape 参数

```python
result = app.scrape(
    url="https://example.com",              # 必需：URL
    formats=["markdown", "html", "links"],  # 输出格式
    only_main_content=True,                 # 只要主要内容
    include_tags=["article", "main"],       # 包含的标签
    exclude_tags=["nav", "footer"],         # 排除的标签
    wait_for=5000,                          # 等待时间（毫秒）
    timeout=30000,                          # 超时时间
    max_age=3600000,                        # 缓存时间（1小时）
    actions=[...],                          # 页面交互
    location={                              # 地理位置
        "country": "US",
        "languages": ["en-US"]
    },
    mobile=False,                           # 移动端模式
    skip_tls_verification=False,            # 跳过 TLS 验证
    remove_base64_images=True,              # 移除 Base64 图片
    block_ads=True                          # 屏蔽广告
)
```

#### Crawl 参数

```python
crawl_result = app.crawl(
    url="https://example.com",
    limit=100,                    # 最大页面数
    max_depth=3,                  # 最大深度
    allow_subdomains=False,       # 子域名
    crawl_entire_domain=False,    # 整个域名
    ignore_sitemap=False,         # 忽略 sitemap
    include_paths=["/blog/"],     # 包含路径
    exclude_paths=["/admin/"],    # 排除路径
    scrape_options={...}          # Scrape 选项
)
```

### 3.4 异步支持

```python
from firecrawl import AsyncFirecrawlApp
import asyncio

async def main():
    app = AsyncFirecrawlApp(api_key="fc-your-key")

    # 异步爬取
    result = await app.scrape(
        url="https://example.com",
        formats=["markdown"]
    )

    print(result.markdown)

asyncio.run(main())
```

### 3.5 错误处理

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import (
    FirecrawlError,
    RequestTimeoutError,
    RateLimitError
)

app = FirecrawlApp(api_key="fc-your-key")

try:
    result = app.scrape(url="https://example.com")
except RequestTimeoutError as e:
    print(f"超时: {e}")
except RateLimitError as e:
    print(f"速率限制: {e}")
except FirecrawlError as e:
    print(f"Firecrawl 错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

<div id="chapter-4">

## 第四章：高级特性

</div>

### 4.1 缓存策略

#### 默认缓存（2 天）

```python
# 默认 maxAge = 172800000 毫秒（2 天）
result = app.scrape(
    url="https://example.com",
    formats=["markdown"]
)
# 如果 2 天内有缓存，直接返回
```

#### 自定义缓存时间

```python
# 10 分钟缓存
result = app.scrape(
    url="https://example.com",
    max_age=600000,  # 10 分钟
    formats=["markdown"]
)

# 始终获取最新
result = app.scrape(
    url="https://example.com",
    max_age=0,  # 不使用缓存
    formats=["markdown"]
)

# 不存储到缓存
result = app.scrape(
    url="https://example.com",
    store_in_cache=False,
    formats=["markdown"]
)
```

**成本优化**:

- 默认 2 天缓存可节省 **50%+ 成本**
- 新闻网站：1 小时缓存
- 静态文档：7 天缓存
- 实时数据：`max_age=0`

### 4.2 地理位置与语言

```python
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    location={
        "country": "JP",              # 日本
        "languages": ["ja-JP", "en"]  # 日语优先，英语次之
    }
)
```

**支持的国家代码**（部分）:

- `US` - 美国
- `GB` - 英国
- `AU` - 澳大利亚
- `JP` - 日本
- `CN` - 中国
- `DE` - 德国
- `FR` - 法国

### 4.3 Stealth Mode（隐身模式）

针对高级反爬网站：

```python
result = app.scrape(
    url="https://protected-site.com",
    formats=["markdown"],
    proxy="stealth"  # 使用隐身代理
)
```

**适用场景**:

- 大型电商网站（Amazon、eBay）
- 社交媒体（LinkedIn）
- 受保护的新闻站点

### 4.4 Change Tracking（变更监控）

```python
# 首次爬取
result1 = app.scrape(
    url="https://example.com/product",
    formats=["markdown"]
)

# 定期检查变更
import time
time.sleep(3600)  # 1 小时后

result2 = app.scrape(
    url="https://example.com/product",
    formats=["markdown", "changeTracking"]
)

# 检查是否有变更
if result2.change_tracking.changed:
    print("页面已更新！")
    print(f"变更内容: {result2.change_tracking.diff}")
```

### 4.5 Extract（智能数据提取）

#### 单页提取

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str
    rating: float

result = app.scrape(
    url="https://shop.example.com/product",
    formats=[{
        "type": "json",
        "schema": Product.model_json_schema()
    }]
)

product = result.json
print(f"{product['name']}: ${product['price']}")
```

#### 整站提取（FIRE-1 Beta）

```python
extract_result = app.extract(
    urls=["https://shop.com/category1", "https://shop.com/category2"],
    prompt="提取所有产品的名称、价格、库存状态",
    schema={
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "in_stock": {"type": "boolean"}
                    }
                }
            }
        }
    }
)
```

---

<div id="chapter-5">

## 第五章：HawaiiHub 实战应用

</div>

### 5.1 夏威夷新闻爬取系统

#### 目标网站

1. **Hawaii News Now** - `https://www.hawaiinewsnow.com/`
2. **Star Advertiser** - `https://www.staradvertiser.com/`
3. **Civil Beat** - `https://www.civilbeat.org/`

#### 实现代码

```python
from firecrawl import FirecrawlApp
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class HawaiiNewsScrap:
    """夏威夷新闻爬虫"""

    def __init__(self):
        self.sources = [
            "https://www.hawaiinewsnow.com/",
            "https://www.staradvertiser.com/",
            "https://www.civilbeat.org/"
        ]

    def scrape_homepage(self, url: str) -> dict:
        """爬取新闻首页"""
        try:
            result = app.scrape(
                url=url,
                formats=["markdown", "links"],
                only_main_content=True,
                max_age=3600000  # 1 小时缓存
            )

            return {
                "url": url,
                "success": True,
                "content": result.markdown,
                "links": result.links,
                "scraped_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "url": url,
                "success": False,
                "error": str(e)
            }

    def extract_article_links(self, links: list) -> list:
        """提取文章链接"""
        article_links = []
        for link in links:
            # 过滤条件
            if any(keyword in link.lower() for keyword in ['article', 'news', 'story']):
                if not any(exclude in link.lower() for exclude in ['video', 'weather', 'sports']):
                    article_links.append(link)
        return article_links[:10]  # 限制 10 篇

    def scrape_articles(self, article_links: list) -> list:
        """批量爬取文章"""
        try:
            batch_result = app.batch_scrape(
                urls=article_links,
                formats=["markdown", {"type": "json", "prompt": "提取标题、作者、日期、摘要"}],
                only_main_content=True
            )

            articles = []
            for page in batch_result:
                articles.append({
                    "url": page.url,
                    "markdown": page.markdown,
                    "metadata": page.json if hasattr(page, 'json') else {}
                })

            return articles
        except Exception as e:
            print(f"批量爬取失败: {e}")
            return []

    def run(self):
        """执行完整爬取流程"""
        all_articles = []

        for source in self.sources:
            print(f"\n📰 爬取: {source}")

            # 1. 爬取首页
            homepage = self.scrape_homepage(source)
            if not homepage["success"]:
                print(f"❌ 失败: {homepage['error']}")
                continue

            # 2. 提取文章链接
            article_links = self.extract_article_links(homepage["links"])
            print(f"📊 发现 {len(article_links)} 篇文章")

            # 3. 批量爬取文章
            articles = self.scrape_articles(article_links)
            all_articles.extend(articles)

            print(f"✅ 成功爬取 {len(articles)} 篇文章")

        # 保存结果
        self.save_results(all_articles)
        return all_articles

    def save_results(self, articles: list):
        """保存爬取结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON 格式
        with open(f"data/hawaii_news_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        # Markdown 格式
        with open(f"data/hawaii_news_{timestamp}.md", "w", encoding="utf-8") as f:
            f.write(f"# 夏威夷新闻汇总\n\n")
            f.write(f"> 爬取时间: {datetime.now()}\n\n")
            for i, article in enumerate(articles, 1):
                f.write(f"## {i}. {article.get('url', 'N/A')}\n\n")
                f.write(f"{article['markdown'][:500]}...\n\n")
                f.write("---\n\n")

# 使用
scraper = HawaiiNewsScrap()
articles = scraper.run()
print(f"\n🎉 完成！共采集 {len(articles)} 篇文章")
```

### 5.2 与 NewsAPI 集成

```python
from firecrawl import FirecrawlApp
from newsapi import NewsApiClient
import os

# 初始化
firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

def fetch_hawaii_news():
    """NewsAPI 发现 + Firecrawl 采集"""

    # 1. 使用 NewsAPI 搜索
    articles = newsapi.get_everything(
        q="Hawaii Chinese community",
        language="en",
        sort_by="publishedAt",
        page_size=20
    )

    # 2. 提取 URL
    urls = [article["url"] for article in articles["articles"]]

    # 3. 使用 Firecrawl 批量爬取完整内容
    full_articles = firecrawl.batch_scrape(
        urls=urls,
        formats=["markdown"],
        only_main_content=True
    )

    # 4. 合并数据
    results = []
    for i, full_article in enumerate(full_articles):
        results.append({
            **articles["articles"][i],  # NewsAPI 元数据
            "full_content": full_article.markdown  # Firecrawl 完整内容
        })

    return results
```

### 5.3 成本监控与优化

```python
class CostMonitor:
    """成本监控器"""

    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.request_count = 0
        self.total_cost = 0.0

    def track_request(self, cost: float = 0.01):
        """记录请求成本"""
        self.request_count += 1
        self.total_cost += cost

        if self.total_cost >= self.daily_budget:
            raise Exception(f"超出每日预算: ${self.daily_budget}")

        print(f"请求 #{self.request_count} | 成本: ${cost:.4f} | 累计: ${self.total_cost:.2f}/{self.daily_budget}")

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_requests": self.request_count,
            "total_cost": self.total_cost,
            "average_cost": self.total_cost / self.request_count if self.request_count > 0 else 0,
            "budget_remaining": self.daily_budget - self.total_cost
        }

# 使用
monitor = CostMonitor(daily_budget=10.0)

def scrape_with_monitoring(url: str) -> dict:
    """带成本监控的爬取"""
    monitor.track_request(cost=0.01)
    result = app.scrape(url=url, formats=["markdown"])
    return result

# 统计信息
stats = monitor.get_stats()
print(f"📊 今日统计: {stats}")
```

---

<div id="chapter-6">

## 第六章：最佳实践与优化

</div>

### 6.1 性能优化

#### 1. 使用缓存

```python
# ❌ 错误：每次都重新爬取
for i in range(10):
    result = app.scrape(url="https://example.com", max_age=0)

# ✅ 正确：使用缓存
for i in range(10):
    result = app.scrape(url="https://example.com", max_age=3600000)  # 1 小时
```

#### 2. 批量优于单个

```python
# ❌ 错误：逐个爬取
urls = ["url1", "url2", "url3"]
for url in urls:
    result = app.scrape(url)

# ✅ 正确：批量爬取
results = app.batch_scrape(urls)
```

#### 3. 只要主要内容

```python
# ✅ 正确：移除导航、广告、页脚
result = app.scrape(
    url="...",
    only_main_content=True,
    exclude_tags=["nav", "footer", "aside", "script"],
    block_ads=True
)
```

### 6.2 错误处理与重试

```python
import time

def safe_scrape(url: str, max_retries: int = 3) -> dict | None:
    """安全爬取，带重试"""
    for attempt in range(max_retries):
        try:
            result = app.scrape(
                url=url,
                formats=["markdown"],
                only_main_content=True
            )

            if not result or not hasattr(result, "markdown"):
                raise ValueError("无效结果")

            print(f"✅ 成功爬取: {url}")
            return result

        except RequestTimeoutError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"⏳ 超时，{wait_time}秒后重试... ({attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"❌ 失败（{max_retries}次重试后）: {url}")
                return None

        except Exception as e:
            print(f"❌ 错误: {url} - {e}")
            return None
```

### 6.3 数据验证

```python
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class Article(BaseModel):
    """文章数据模型"""
    title: str = Field(..., min_length=1, max_length=200)
    url: HttpUrl
    author: str
    date: str
    content: Optional[str] = None

# 验证
try:
    article = Article(
        title="测试文章",
        url="https://example.com",
        author="张三",
        date="2025-10-27",
        content="..."
    )
except ValidationError as e:
    print(f"验证失败: {e}")
```

### 6.4 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/firecrawl.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("HawaiiNews")

# 使用日志
def scrape_with_logging(url: str):
    logger.info(f"开始爬取: {url}")
    try:
        result = app.scrape(url=url)
        logger.info(f"成功: {len(result.markdown)} 字符")
        return result
    except Exception as e:
        logger.error(f"失败: {url} - {e}")
        return None
```

### 6.5 数据清洗

```python
import re

def clean_markdown(content: str) -> str:
    """清洗 Markdown 内容"""
    # 移除多余空行
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 移除特定模式
    patterns = [
        r"Subscribe to.*newsletter",
        r"Advertisement",
        r"Related Articles",
        r"Share on.*"
    ]

    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    return content.strip()
```

---

<div id="appendix">

## 附录

</div>

### A. 术语表

| 术语         | 中文      | 说明                     |
| ------------ | --------- | ------------------------ |
| Scrape       | 爬取/抓取 | 单页内容采集             |
| Crawl        | 整站爬取  | 递归爬取所有子页面       |
| Map          | 站点地图  | 快速发现所有 URL         |
| Extract      | 提取      | 结构化数据提取           |
| LLM-ready    | 适配 LLM  | 适合大语言模型使用的格式 |
| Schema       | 架构      | 数据结构定义             |
| Actions      | 操作/动作 | 页面交互（点击、输入等） |
| Stealth Mode | 隐身模式  | 绕过高级反爬机制         |

### B. 错误码对照

| 错误码 | 说明         | 解决方案               |
| ------ | ------------ | ---------------------- |
| 401    | API Key 无效 | 检查环境变量           |
| 429    | 速率限制     | 降低请求频率或升级计划 |
| 500    | 服务器错误   | 稍后重试               |
| 504    | 超时         | 增加 timeout 参数      |

### C. 速查表

#### 常用参数

```python
# Scrape
result = app.scrape(
    url="...",
    formats=["markdown"],        # 输出格式
    only_main_content=True,      # 主要内容
    max_age=3600000,             # 缓存 1 小时
    exclude_tags=["nav"]         # 排除标签
)

# Crawl
crawl_result = app.crawl(
    url="...",
    limit=100,                   # 最多 100 页
    max_depth=3,                 # 深度 3 层
    scrape_options={...}         # Scrape 选项
)

# Map
map_result = app.map(
    url="...",
    limit=5000                   # 最多 5000 URL
)

# Search
search_result = app.search(
    query="...",
    sources=[{"type": "web"}],
    limit=10
)
```

### D. 资源链接

#### 官方资源

- 📖 在线文档: https://docs.firecrawl.dev/
- 🐙 GitHub: https://github.com/firecrawl/firecrawl
- 💬 Discord: https://discord.gg/firecrawl
- 📝 Changelog: https://www.firecrawl.dev/changelog
- 🎮 Playground: https://firecrawl.dev/playground

#### 本地资源

- 📂 官方中文文档: `firecrawl-docs/zh/`
- 📋 项目规则: `.cursorrules`
- 📊 更新日志: `Firecrawl更新日志汇总.md`
- ⚙️ SDK 配置: `SDK_CONFIGURATION_COMPLETE.md`

---

**最后更新**: 2025-10-27
**文档版本**: v1.0
**作者**: HawaiiHub AI Team
**总字数**: 约 15,000 字

🎉 **恭喜完成学习！现在你已经掌握 Firecrawl 的所有核心功能！**
