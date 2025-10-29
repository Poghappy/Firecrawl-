# 🔥 Firecrawl 官方模板完整目录

> **最后更新**: 2025-10-28
> **来源**: Firecrawl 官方文档 + GitHub 主仓库
> **总计**: 55+ 模板（代码片段 + 全栈项目）

---

## 📋 目录概览

### 📦 代码片段分类（按功能）

- **Scrape（单页爬取）**: 15+ 模板
- **Crawl（网站爬取）**: 10+ 模板
- **Map（网站地图）**: 5+ 模板
- **Search（搜索）**: 5+ 模板
- **Batch Scrape（批量爬取）**: 8+ 模板
- **Extract（数据提取）**: 8+ 模板
- **Webhook（事件通知）**: 6+ 模板
- **异步操作**: 4+ 模板

### 🏗️ 全栈项目模板（9个）

- Open Lovable - RAG 聊天机器人
- Open Agent Builder - AI 代理构建器
- Fireplexity - AI 搜索引擎
- FireGEO - SaaS 品牌监控
- Fire Enrich - 数据丰富化工具
- Firesearch - 深度研究工具
- Firestarter - 网站聊天机器人
- AI Ready Website - 网站结构化转换
- Open Researcher - AI 研究助手

---

## 🎯 核心功能模板详解

### 1️⃣ Scrape（单页爬取）

#### 基础爬取

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# 基础爬取 - 返回 Markdown 和 HTML
doc = firecrawl.scrape(
    "https://firecrawl.dev",
    formats=["markdown", "html"]
)
print(doc.markdown)
```

**适用场景**:

- 单个网页内容提取
- 新闻文章爬取
- 产品详情页采集
- 博客文章获取

#### JSON 结构化提取

```python
# 定义数据结构
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "price": {"type": "number"},
        "rating": {"type": "number"}
    },
    "required": ["title", "author"]
}

# 爬取并提取结构化数据
doc = firecrawl.scrape(
    "https://example.com/product",
    formats=[{
        "type": "json",
        "schema": schema
    }]
)

print(doc.extract)  # 结构化的 JSON 数据
```

**适用场景**:

- 电商产品信息提取
- 餐厅信息采集（Yelp、Google Maps）
- 招聘信息结构化
- 房屋租赁信息

#### 截图模式

```python
# 爬取页面并生成截图
doc = firecrawl.scrape(
    "https://example.com",
    formats=[{
        "type": "screenshot",
        "fullPage": True,
        "quality": 90
    }]
)

# 保存截图
with open("screenshot.png", "wb") as f:
    f.write(doc.screenshot)
```

**适用场景**:

- 页面快照存档
- UI/UX 监控
- 视觉回归测试
- 合规性证据

#### 代理模式

```python
# 使用代理爬取（绕过地理限制）
doc = firecrawl.scrape(
    "https://example.com",
    formats=["markdown"],
    location={"country": "US"}
)
```

**适用场景**:

- 地理限制内容
- IP 封禁规避
- 本地化内容测试
- 多地区数据采集

#### 快速模式

```python
# 快速爬取（跳过 JavaScript 渲染）
doc = firecrawl.scrape(
    "https://example.com",
    formats=["markdown"],
    max_age=172800000  # 使用2天内缓存
)
```

**适用场景**:

- 静态网站
- 降低成本
- 批量快速采集
- 定期更新内容

---

### 2️⃣ Crawl（网站爬取）

#### 基础爬取

```python
# 爬取整个网站（自动发现链接）
docs = firecrawl.crawl(
    url="https://docs.firecrawl.dev",
    limit=10,  # 最多爬取10个页面
    max_depth=2  # 最大深度2层
)

for doc in docs:
    print(f"{doc.url}: {len(doc.markdown)} 字符")
```

**适用场景**:

- 文档站点完整采集
- 博客归档
- 产品目录爬取
- 知识库建设

#### Webhook 异步爬取

```python
# 异步爬取（大型网站）
job_id = firecrawl.async_crawl(
    url="https://example.com",
    limit=1000,
    webhook="https://your-server.com/webhook"
)

# Webhook 接收器（FastAPI 示例）
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if data["status"] == "completed":
        # 处理完成的数据
        docs = data["data"]
        print(f"爬取完成: {len(docs)} 个页面")

    return {"received": True}
```

**适用场景**:

- 大型网站爬取（100+ 页面）
- 长时间运行任务
- 后台数据采集
- 定时爬取任务

#### 路径过滤

```python
# 只爬取特定路径
docs = firecrawl.crawl(
    url="https://example.com",
    include_paths=["/blog/*", "/docs/*"],  # 只包含这些路径
    exclude_paths=["/admin/*", "/api/*"],  # 排除这些路径
    limit=50
)
```

**适用场景**:

- 特定栏目采集
- 排除无用页面
- 降低爬取成本
- 精准内容获取

#### 实时进度监控

```python
# 监控爬取进度
job = firecrawl.crawl(
    url="https://example.com",
    limit=100,
    poll_interval=5  # 每5秒检查一次
)

# 实时打印进度
for status in job:
    print(f"进度: {status.completed}/{status.total}")
    print(f"当前页面: {status.current_url}")
```

**适用场景**:

- 用户界面进度显示
- 任务监控
- 调试和测试
- 成本预估

---

### 3️⃣ Map（网站地图）

#### 快速生成网站地图

```python
# 快速发现网站所有链接
urls = firecrawl.map(
    url="https://firecrawl.dev",
    limit=100,  # 最多发现100个链接
    sitemap="include"  # 包含 sitemap.xml
)

print(f"发现 {len(urls.links)} 个链接:")
for link in urls.links:
    print(f"- {link}")
```

**适用场景**:

- 网站结构分析
- SEO 审计
- 内容清单
- 爬取前规划

#### 搜索特定内容

```python
# 搜索包含特定关键词的页面
urls = firecrawl.map(
    url="https://example.com",
    search="pricing",  # 搜索包含 "pricing" 的页面
    limit=50
)

print(f"找到 {len(urls.links)} 个相关页面")
```

**适用场景**:

- 特定页面发现
- 内容审计
- 竞品分析
- 数据采集准备

---

### 4️⃣ Search（智能搜索）

#### 基础搜索

```python
# 搜索互联网内容
results = firecrawl.search(
    query="firecrawl python examples",
    limit=10
)

for result in results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print(f"摘要: {result.snippet}\n")
```

**适用场景**:

- 竞品监控
- 市场调研
- 内容发现
- 数据采集源查找

#### 搜索 + 爬取

```python
# 搜索并立即爬取结果页面
results = firecrawl.search(
    query="best restaurants in hawaii",
    limit=5,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

for result in results:
    print(f"{result.title}")
    print(result.markdown[:200])  # 前200字符
```

**适用场景**:

- 一键数据采集
- 内容聚合
- 研究自动化
- RAG 数据源

#### 时间范围过滤

```python
# 搜索最近一周的内容
results = firecrawl.search(
    query="AI news",
    limit=10,
    time="week"  # day, week, month, year
)
```

**适用场景**:

- 新闻采集
- 趋势分析
- 时效性内容
- 定期更新

---

### 5️⃣ Batch Scrape（批量爬取）

#### 基础批量爬取

```python
# 批量爬取多个 URL
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

job = firecrawl.batch_scrape(
    urls=urls,
    formats=["markdown"],
    poll_interval=2,
    wait_timeout=120
)

print(f"状态: {job.status}")
print(f"完成: {job.completed}/{job.total}")

# 访问结果
for doc in job.data:
    print(f"{doc.url}: {len(doc.markdown)} 字符")
```

**适用场景**:

- 已知 URL 列表采集
- 产品详情批量获取
- 新闻文章批量爬取
- 数据批量更新

#### 异步批量爬取

```python
# 异步启动批量任务
job_id = firecrawl.start_batch_scrape(
    urls=[f"https://example.com/page{i}" for i in range(100)],
    formats=["markdown"],
    webhook="https://your-server.com/webhook"
)

print(f"任务ID: {job_id}")

# 稍后检查状态
job = firecrawl.check_batch_status(job_id)
print(f"进度: {job.completed}/{job.total}")
```

**适用场景**:

- 大批量 URL（100+）
- 后台数据采集
- 定时任务
- 长时间运行

#### 错误处理

```python
# 批量爬取并处理错误
job = firecrawl.batch_scrape(urls=urls, formats=["markdown"])

for doc in job.data:
    if doc.error:
        print(f"失败: {doc.url} - {doc.error}")
    else:
        print(f"成功: {doc.url}")
```

**适用场景**:

- 可靠性要求高
- 错误日志记录
- 重试机制
- 质量监控

---

### 6️⃣ Extract（数据提取）

#### 基础提取

```python
# 从网页提取结构化数据
schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"}
    },
    "required": ["description"]
}

res = firecrawl.extract(
    urls=["https://docs.firecrawl.dev"],
    prompt="Extract the page description",
    schema=schema
)

print(res.data["description"])
```

**适用场景**:

- 非结构化数据提取
- AI 辅助解析
- 复杂页面处理
- 智能字段识别

#### 无 Schema 提取

```python
# 使用 AI 自动推导结构
res = firecrawl.extract(
    urls=["https://example.com/product"],
    prompt="Extract product information including name, price, and reviews"
)

print(res.data)  # AI 自动生成的结构
```

**适用场景**:

- 探索性数据分析
- 结构不明确的页面
- 快速原型开发
- 灵活数据提取

#### Web Search + Extract

```python
# 搜索互联网并提取数据
res = firecrawl.extract(
    prompt="Find the top 3 AI tools launched in 2024",
    enable_web_search=True,
    schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "url": {"type": "string"}
            }
        }
    }
)

for tool in res.data:
    print(f"{tool['name']}: {tool['description']}")
```

**适用场景**:

- 市场调研
- 竞品分析
- 内容聚合
- 研究自动化

---

## 🏗️ 全栈项目模板详解

### 1. Open Lovable - RAG 聊天机器人

**技术栈**:

- Next.js 14 (App Router)
- Firecrawl API
- OpenAI API
- Pinecone (向量数据库)
- Tailwind CSS

**核心功能**:

- 爬取网站内容
- 向量化存储
- 语义搜索
- 流式对话

**使用场景**:

- 网站客服机器人
- 知识库问答
- 文档助手
- 学习辅导

**快速启动**:

```bash
git clone https://github.com/firecrawl/open-lovable
cd open-lovable
npm install
cp .env.example .env
# 配置 API 密钥
npm run dev
```

---

### 2. Open Agent Builder - AI 代理构建器

**技术栈**:

- Next.js 14
- Firecrawl API
- LangChain
- Supabase
- shadcn/ui

**核心功能**:

- 可视化代理构建
- 网页爬取集成
- 工作流编排
- 代理部署

**使用场景**:

- 自动化工作流
- 数据采集代理
- 研究助手
- 内容生成

---

### 3. Fireplexity - AI 搜索引擎

**技术栈**:

- Next.js 14
- Firecrawl Search
- OpenAI API
- Vercel AI SDK
- Groq API

**核心功能**:

- 实时搜索
- 流式响应
- 引用标注
- 多源聚合

**使用场景**:

- 研究工具
- 实时问答
- 新闻聚合
- 市场调研

---

### 4. FireGEO - SaaS 品牌监控

**技术栈**:

- Next.js 14
- Firecrawl API
- Supabase
- Stripe
- PostHog

**核心功能**:

- 品牌提及监控
- 自动化报告
- 用户认证
- 订阅计费

**使用场景**:

- 品牌监控
- 竞品分析
- 舆情监测
- SaaS 产品

---

### 5. Fire Enrich - 数据丰富化

**技术栈**:

- Next.js 14
- Firecrawl API
- OpenAI API
- CSV 处理

**核心功能**:

- 邮箱域名提取
- 网站爬取
- AI 数据提取
- CSV 导出

**使用场景**:

- 销售线索丰富化
- 客户数据补全
- 市场调研
- CRM 数据增强

---

### 6. Firesearch - 深度研究工具

**技术栈**:

- Next.js 14
- Firecrawl Search
- OpenAI API
- 引用验证

**核心功能**:

- 多步骤研究
- 事实验证
- 引用追踪
- 深度分析

**使用场景**:

- 学术研究
- 投资分析
- 新闻核查
- 专业报告

---

### 7. Firestarter - 网站聊天机器人

**技术栈**:

- Next.js 14
- Firecrawl Crawl
- OpenAI API
- Pinecone

**核心功能**:

- 一键网站爬取
- 自动向量化
- 嵌入式聊天
- 快速部署

**使用场景**:

- 网站客服
- 产品文档助手
- 在线支持
- 知识库问答

---

### 8. AI Ready Website - 网站结构化

**技术栈**:

- Python
- Firecrawl API
- JSON Schema
- LLM 集成

**核心功能**:

- 网站爬取
- 结构化转换
- Schema 生成
- AI-ready 输出

**使用场景**:

- AI 训练数据准备
- 网站归档
- 内容迁移
- 数据标准化

---

### 9. Open Researcher - AI 研究助手

**技术栈**:

- Next.js 14
- Firecrawl Search
- LangChain
- 多步骤推理

**核心功能**:

- 自动研究规划
- 多源数据采集
- 智能分析
- 报告生成

**使用场景**:

- 市场研究
- 学术调研
- 尽职调查
- 内容创作

---

## 🎯 HawaiiHub 专项应用场景

### 场景 1: 夏威夷新闻聚合

**推荐模板**:

- Crawl + Batch Scrape
- Webhook 异步处理

**实现方案**:

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# 新闻源列表
NEWS_SOURCES = [
    "https://www.hawaiinewsnow.com/",
    "https://www.staradvertiser.com/",
    "https://www.civilbeat.org/"
]

# 1. 使用 Map 发现文章链接
for source in NEWS_SOURCES:
    urls = firecrawl.map(
        url=source,
        search="news",  # 只查找新闻相关页面
        limit=50
    )

    # 2. 批量爬取文章
    articles = firecrawl.batch_scrape(
        urls=urls.links[:20],  # 每个源爬取20篇
        formats=["markdown"],
        poll_interval=5
    )

    # 3. 保存数据
    for article in articles.data:
        save_article(article)
```

---

### 场景 2: Yelp 餐厅信息采集

**推荐模板**:

- Scrape + JSON Extract
- 代理模式（绕过限制）

**实现方案**:

```python
# 定义餐厅数据结构
RESTAURANT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "rating": {"type": "number"},
        "price_range": {"type": "string"},
        "address": {"type": "string"},
        "phone": {"type": "string"},
        "cuisine": {"type": "array", "items": {"type": "string"}},
        "hours": {"type": "object"},
        "reviews_count": {"type": "number"}
    }
}

# 搜索檀香山中餐
search_url = "https://www.yelp.com/search?find_desc=Chinese&find_loc=Honolulu,+HI"

# 1. 爬取搜索结果页
search_page = firecrawl.scrape(
    url=search_url,
    formats=["markdown"],
    location={"country": "US"}  # 使用美国代理
)

# 2. 提取餐厅链接（需要自定义解析）
restaurant_urls = extract_restaurant_urls(search_page.markdown)

# 3. 批量爬取餐厅详情并提取结构化数据
restaurants = firecrawl.batch_scrape(
    urls=restaurant_urls,
    formats=[{
        "type": "json",
        "schema": RESTAURANT_SCHEMA
    }]
)

# 4. 保存到数据库
for restaurant in restaurants.data:
    save_restaurant(restaurant.extract)
```

---

### 场景 3: Craigslist 租房监控

**推荐模板**:

- Search + Crawl
- Webhook 实时通知

**实现方案**:

```python
# 租房信息结构
LISTING_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "bedrooms": {"type": "number"},
        "bathrooms": {"type": "number"},
        "sqft": {"type": "number"},
        "address": {"type": "string"},
        "posted_date": {"type": "string"},
        "description": {"type": "string"}
    }
}

# 搜索檀香山租房（价格 < $2000）
search_url = "https://honolulu.craigslist.org/search/apa?max_price=2000"

# 使用 Webhook 监控新房源
job_id = firecrawl.async_crawl(
    url=search_url,
    limit=100,
    webhook="https://hawaiihub.net/api/housing/webhook",
    formats=[{
        "type": "json",
        "schema": LISTING_SCHEMA
    }]
)

# Webhook 接收器（FastAPI）
@app.post("/api/housing/webhook")
async def housing_webhook(request: Request):
    data = await request.json()

    if data["type"] == "page":
        # 新房源发现
        listing = data["data"]["extract"]

        # 检查是否已存在
        if not listing_exists(listing):
            # 发送通知
            send_notification(listing)
            # 保存数据库
            save_listing(listing)

    return {"received": True}
```

---

### 场景 4: 华人社区活动采集

**推荐模板**:

- Map + Extract
- 定时任务

**实现方案**:

```python
# 活动信息结构
EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "date": {"type": "string"},
        "time": {"type": "string"},
        "location": {"type": "string"},
        "organizer": {"type": "string"},
        "description": {"type": "string"},
        "registration_url": {"type": "string"}
    }
}

# 华人社区网站列表
COMMUNITY_SITES = [
    "https://www.kauaichineseassociation.org/",
    "https://www.chinesechamber.com/",
    # 更多社区网站...
]

# 定时任务（每天运行）
def collect_community_events():
    for site in COMMUNITY_SITES:
        # 1. 发现活动页面
        urls = firecrawl.map(
            url=site,
            search="event",  # 查找活动相关页面
            limit=20
        )

        # 2. 提取活动信息
        events = firecrawl.extract(
            urls=urls.links,
            prompt="Extract event information including title, date, time, location, and description",
            schema=EVENT_SCHEMA
        )

        # 3. 保存到日历
        for event in events.data:
            save_event(event)

# 使用 schedule 库定时运行
import schedule
schedule.every().day.at("06:00").do(collect_community_events)
```

---

## 📊 模板选择决策树

```
需要采集什么？
├── 单个网页内容
│   ├── 简单文本 → Scrape (Markdown)
│   ├── 结构化数据 → Scrape (JSON)
│   └── 需要截图 → Scrape (Screenshot)
│
├── 多个已知 URL
│   ├── < 10 个 → Batch Scrape (同步)
│   └── > 10 个 → Batch Scrape (异步 + Webhook)
│
├── 整个网站
│   ├── 小型网站 (< 100 页) → Crawl (同步)
│   └── 大型网站 (> 100 页) → Crawl (异步 + Webhook)
│
├── 不知道具体 URL
│   ├── 先探索网站 → Map (发现所有链接)
│   └── 搜索互联网 → Search (查找相关内容)
│
└── 复杂数据提取
    ├── 有明确结构 → Extract (Schema)
    └── 结构不确定 → Extract (Prompt Only)
```

---

## 🛠️ 开发工具和配置

### 环境变量模板

```bash
# .env
# Firecrawl API 配置
FIRECRAWL_API_KEY=fc-YOUR-API-KEY
FIRECRAWL_API_KEY_BACKUP_1=fc-BACKUP-KEY-1
FIRECRAWL_API_KEY_BACKUP_2=fc-BACKUP-KEY-2
FIRECRAWL_API_KEY_BACKUP_3=fc-BACKUP-KEY-3

# API 配置
FIRECRAWL_API_URL=https://api.firecrawl.dev
FIRECRAWL_TIMEOUT=60
FIRECRAWL_MAX_RETRIES=3

# 成本控制
FIRECRAWL_DAILY_BUDGET=10.0
FIRECRAWL_MONTHLY_BUDGET=300.0

# Webhook 配置
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_SECRET=your-webhook-secret

# 数据库配置（可选）
DATABASE_URL=postgresql://user:password@localhost:5432/hawaiihub
REDIS_URL=redis://localhost:6379

# OpenAI API（用于 Extract）
OPENAI_API_KEY=sk-YOUR-OPENAI-KEY
```

---

### Python 配置文件模板

```python
# config/firecrawl_config.py
import os
from dotenv import load_dotenv
from firecrawl import Firecrawl

load_dotenv()

class FirecrawlConfig:
    """Firecrawl 配置类"""

    # API 密钥
    API_KEY = os.getenv("FIRECRAWL_API_KEY")
    BACKUP_KEYS = [
        os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
        os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
        os.getenv("FIRECRAWL_API_KEY_BACKUP_3"),
    ]

    # API 配置
    API_URL = os.getenv("FIRECRAWL_API_URL", "https://api.firecrawl.dev")
    TIMEOUT = int(os.getenv("FIRECRAWL_TIMEOUT", "60"))
    MAX_RETRIES = int(os.getenv("FIRECRAWL_MAX_RETRIES", "3"))

    # 成本控制
    DAILY_BUDGET = float(os.getenv("FIRECRAWL_DAILY_BUDGET", "10.0"))
    MONTHLY_BUDGET = float(os.getenv("FIRECRAWL_MONTHLY_BUDGET", "300.0"))

    # Webhook
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

    @classmethod
    def get_client(cls) -> Firecrawl:
        """获取 Firecrawl 客户端"""
        return Firecrawl(api_key=cls.API_KEY)

    @classmethod
    def get_backup_client(cls, index: int = 0) -> Firecrawl:
        """获取备用客户端"""
        if index < len(cls.BACKUP_KEYS):
            return Firecrawl(api_key=cls.BACKUP_KEYS[index])
        raise ValueError("备用密钥索引超出范围")

# 使用示例
firecrawl = FirecrawlConfig.get_client()
```

---

## 📝 最佳实践总结

### 性能优化

1. **使用缓存**

```python
# 使用 max_age 参数启用缓存
doc = firecrawl.scrape(
    "https://example.com",
    formats=["markdown"],
    max_age=172800000  # 2天缓存
)
```

2. **批量操作**

```python
# 优先使用 batch_scrape 而非循环 scrape
# ❌ 错误
for url in urls:
    doc = firecrawl.scrape(url)

# ✅ 正确
docs = firecrawl.batch_scrape(urls)
```

3. **异步处理**

```python
# 大批量任务使用异步 + Webhook
job_id = firecrawl.async_crawl(
    url="https://large-site.com",
    webhook="https://your-server.com/webhook"
)
```

---

### 成本控制

1. **合理设置限制**

```python
# 使用 limit 控制爬取数量
docs = firecrawl.crawl(
    url="https://example.com",
    limit=50,  # 最多50页
    max_depth=2  # 最多2层深度
)
```

2. **使用路径过滤**

```python
# 只爬取需要的内容
docs = firecrawl.crawl(
    url="https://example.com",
    include_paths=["/blog/*"],  # 只爬博客
    exclude_paths=["/admin/*", "/api/*"]  # 排除管理和API
)
```

3. **监控使用量**

```python
# 记录每次 API 调用
import logging

def track_usage(operation, cost):
    logging.info(f"{operation}: ${cost:.4f}")
    # 保存到数据库或监控系统
```

---

### 错误处理

```python
from firecrawl import Firecrawl, FirecrawlError

firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

def safe_scrape(url: str, max_retries: int = 3):
    """安全爬取，带重试机制"""
    for attempt in range(max_retries):
        try:
            doc = firecrawl.scrape(
                url=url,
                formats=["markdown"]
            )
            return doc

        except FirecrawlError as e:
            if "rate limit" in str(e).lower():
                # 切换到备用密钥
                firecrawl = FirecrawlConfig.get_backup_client(attempt)
                continue

            elif attempt < max_retries - 1:
                # 等待后重试
                import time
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue

            else:
                logging.error(f"爬取失败 {url}: {e}")
                return None
```

---

## 🎓 学习路径

### 初学者（1-2 天）

1. ✅ 阅读 [快速开始指南](../quickstart.md)
2. ✅ 运行基础 Scrape 示例
3. ✅ 理解 Markdown vs JSON 格式
4. ✅ 尝试 Map 功能发现网站结构

### 中级（3-5 天）

1. ✅ 学习 Crawl 和 Batch Scrape
2. ✅ 配置 Webhook 异步处理
3. ✅ 使用 Extract 提取结构化数据
4. ✅ 实现错误处理和重试

### 高级（1-2 周）

1. ✅ 部署全栈项目（Open Lovable/Fireplexity）
2. ✅ 实现成本监控和优化
3. ✅ 构建生产级数据管道
4. ✅ 集成到现有系统

---

## 📚 参考资源

### 官方文档

- [Firecrawl 官方文档](https://docs.firecrawl.dev/)
- [API 参考](https://docs.firecrawl.dev/api-reference/introduction)
- [SDK 文档](https://docs.firecrawl.dev/sdks/python)

### GitHub 资源

- [Firecrawl 主仓库](https://github.com/mendableai/firecrawl)
- [官方示例集合](https://github.com/firecrawl)
- [社区贡献](https://github.com/topics/firecrawl)

### 社区

- [Discord 社区](https://discord.gg/firecrawl)
- [Twitter/X](https://twitter.com/mendableai)
- [Blog](https://firecrawl.dev/blog)

---

## ✅ 快速检查清单

在开始使用模板前，确保：

- [ ] 已安装 Firecrawl Python SDK (`pip install firecrawl-py`)
- [ ] 已配置 API 密钥环境变量
- [ ] 已阅读相关功能文档
- [ ] 了解成本和限制
- [ ] 准备好数据存储方案
- [ ] 配置错误处理和日志
- [ ] 测试小规模爬取（< 10 页）
- [ ] 监控 API 使用量

---

**维护者**: HawaiiHub AI Team
**最后更新**: 2025-10-28
**版本**: v1.0.0

---

<div align="center">

🔥 **开始使用 Firecrawl 模板，加速 HawaiiHub 数据采集！**

**[快速开始](#-核心功能模板详解)** | **[全栈项目](#-全栈项目模板详解)** | **[HawaiiHub 场景](#-hawaiihub-专项应用场景)**

</div>
