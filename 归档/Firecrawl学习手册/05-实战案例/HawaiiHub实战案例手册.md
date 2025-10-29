# HawaiiHub 实战案例手册

> **创建时间**: 2025-10-27
> **项目**: HawaiiHub - 夏威夷华人社区平台
> **目标**: 使用 Firecrawl 构建完整的数据采集和分析系统
> **难度**: 初级 → 高级（循序渐进）

---

## 📖 手册简介

本手册以 **HawaiiHub** 项目为例，通过 **15 个实战案例**展示如何使用 Firecrawl 构建生产级数据采集系统。

### 🎯 学习目标

通过本手册，你将学会：

- ✅ 爬取夏威夷本地新闻网站
- ✅ 采集华人商家信息（餐厅、超市、服务）
- ✅ 监控租房价格变化
- ✅ 分析用户评论和反馈
- ✅ 提取招聘信息
- ✅ 构建 AI 驱动的智能推荐系统

### 📊 案例统计

| 类别               | 案例数 | 技术栈                    |
| ------------------ | ------ | ------------------------- |
| 数据采集           | 5      | Scrape、Crawl、Map        |
| 数据分析           | 3      | Extract、Pandas、Charts   |
| 实时监控           | 2      | Change Tracking、定时任务 |
| AI 应用            | 3      | LLM、RAG、推荐系统        |
| 完整系统           | 2      | 端到端解决方案            |
| **总计**           | **15** | **Python + Next.js**      |

### 🗂️ 案例组织

```
HawaiiHub实战案例手册.md        ← 本文档（总览）
│
├── 案例 01-05: 数据采集基础    ← 爬取各类数据
├── 案例 06-08: 数据分析        ← 提取和分析
├── 案例 09-10: 实时监控        ← 变更监控
├── 案例 11-13: AI 应用         ← 智能推荐
└── 案例 14-15: 完整系统        ← 生产级系统
```

---

## 🚀 快速开始

### 前置条件

```bash
# 1. Python 环境
Python 3.11+

# 2. 安装依赖
pip3 install firecrawl-py python-dotenv requests pandas pydantic

# 3. 配置 API 密钥
cp env.template .env
# 编辑 .env，添加 FIRECRAWL_API_KEY=fc-xxx

# 4. 验证环境
python3 -c "from firecrawl import FirecrawlApp; print('✅ 环境就绪')"
```

### 目录结构

```bash
hawaiihub-firecrawl-cases/
├── case-01-news-scraper/           # 案例 01
├── case-02-restaurant-collector/   # 案例 02
├── case-03-housing-monitor/        # 案例 03
├── ...
├── data/                           # 数据存储
├── utils/                          # 工具函数
└── README.md
```

---

## 📚 案例目录

### 第一部分：数据采集基础（案例 01-05）

#### 案例 01: 夏威夷新闻采集器 ⭐⭐⭐

**业务需求**: 自动采集夏威夷本地新闻，为社区提供最新资讯

**涉及网站**:
- Hawaii News Now: https://www.hawaiinewsnow.com/
- Honolulu Star-Advertiser: https://www.staradvertiser.com/
- Civil Beat: https://www.civilbeat.org/

**核心功能**:
- 使用 Scrape API 采集单篇新闻
- 使用 Crawl API 爬取完整新闻列表
- 提取标题、作者、时间、内容
- 保存为 JSON 和 Markdown

**技术栈**: Python + Firecrawl Scrape/Crawl API

**难度**: ⭐⭐⭐（初级）

**学习时间**: 2 小时

**参考项目**:
- `blog-articles` (examples/blog-articles)
- `hacker_news_scraper` (examples/hacker_news_scraper)

---

#### 案例 02: 华人商家信息采集 ⭐⭐⭐⭐

**业务需求**: 建立完整的夏威夷华人商家数据库

**目标商家类型**:
- 中餐厅
- 华人超市
- 中文学校
- 移民服务
- 房地产中介

**采集来源**:
- Yelp: https://www.yelp.com/search?find_desc=Chinese&find_loc=Honolulu
- Google Maps
- 本地分类信息网站

**核心功能**:
- 使用 Extract API 结构化提取
- 提取：名称、地址、电话、营业时间、评分
- 验证数据完整性
- 去重和数据清洗

**技术栈**: Python + Firecrawl Extract API + Pydantic

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 4 小时

**参考项目**:
- `company-data-scraper` (firecrawl-app-examples)
- `crm_lead_enrichment` (examples/crm_lead_enrichment)
- `gpt-4.1-company-researcher` (examples/gpt-4.1-company-researcher)

---

#### 案例 03: 租房信息监控系统 ⭐⭐⭐⭐

**业务需求**: 实时监控夏威夷租房市场，提供价格预警

**采集来源**:
- Craigslist Honolulu: https://honolulu.craigslist.org/search/apa
- Zillow
- Apartments.com

**核心功能**:
- 使用 Crawl API 爬取房源列表
- 提取价格、面积、位置、设施
- 使用 Change Tracking 监控价格变化
- 价格低于预期时发送通知

**技术栈**: Python + Firecrawl Crawl + Change Tracking + Email

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 4 小时

**参考项目**:
- `automated_price_tracking` (firecrawl-app-examples)
- `deep-research-apartment-finder` (examples/deep-research-apartment-finder)
- `o3-mini-deal-finder` (examples/o3-mini-deal-finder)

---

#### 案例 04: 招聘信息聚合 ⭐⭐⭐

**业务需求**: 为华人社区提供本地招聘信息

**采集来源**:
- Indeed Honolulu
- LinkedIn Jobs
- 本地华人论坛招聘板块

**核心功能**:
- 使用 Search API 搜索相关职位
- 提取职位名称、公司、薪资、要求
- 按类别分类（餐饮、零售、技术等）
- 生成每日招聘简报

**技术栈**: Python + Firecrawl Search + Extract API

**难度**: ⭐⭐⭐（初级）

**学习时间**: 3 小时

**参考项目**:
- `ai-resume-job-matching` (firecrawl-app-examples)
- `job-resource-analyzer` (examples/job-resource-analyzer)
- `o1_job_recommender` (examples/o1_job_recommender)

---

#### 案例 05: 活动信息爬取 ⭐⭐⭐

**业务需求**: 汇总夏威夷本地活动，方便华人参与

**采集来源**:
- Eventbrite Honolulu
- Facebook Events
- 本地社区网站

**核心功能**:
- 使用 Map API 发现所有活动页面
- 批量爬取活动详情
- 提取时间、地点、价格、主办方
- 按类型分类（文化、运动、音乐等）

**技术栈**: Python + Firecrawl Map + Batch Scrape

**难度**: ⭐⭐⭐（初级）

**学习时间**: 2 小时

**参考项目**:
- `blog-articles` (examples/blog-articles)

---

### 第二部分：数据分析（案例 06-08）

#### 案例 06: 商家评论情感分析 ⭐⭐⭐⭐

**业务需求**: 分析华人商家的用户评论，提取关键问题

**分析维度**:
- 情感分析（正面、负面、中立）
- 关键词提取（服务、价格、环境等）
- 评分趋势分析
- 改进建议生成

**核心功能**:
- 爬取 Yelp 评论
- 使用 LLM 进行情感分析
- 生成可视化报告
- 提供改进建议

**技术栈**: Python + Firecrawl + Claude/GPT + Pandas

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 5 小时

**参考项目**:
- `review-analyzer` (firecrawl-app-examples)
- `claude-3.7-stock-analyzer` (examples/claude-3.7-stock-analyzer)

---

#### 案例 07: 租房市场数据分析 ⭐⭐⭐⭐

**业务需求**: 分析租房市场趋势，提供定价建议

**分析内容**:
- 不同区域价格对比
- 房型价格分布
- 价格随时间变化趋势
- 性价比分析

**核心功能**:
- 爬取历史租房数据
- 数据清洗和标准化
- 统计分析和可视化
- 生成市场报告

**技术栈**: Python + Firecrawl + Pandas + Matplotlib

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 4 小时

**参考项目**:
- `scrape_and_analyze_airbnb_data_e2b` (examples/scrape_and_analyze_airbnb_data_e2b)
- `visualize_website_topics_e2b` (examples/visualize_website_topics_e2b)

---

#### 案例 08: 竞品分析系统 ⭐⭐⭐⭐

**业务需求**: 监控竞品动态，生成分析报告

**分析对象**:
- 其他华人社区平台
- 本地分类信息网站
- 社交媒体群组

**核心功能**:
- 定期爬取竞品网站
- 对比功能和内容
- 分析用户反馈
- 生成竞品分析报告

**技术栈**: Python + Firecrawl + LLM

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 5 小时

**参考项目**:
- `search-competitor-analysis` (firecrawl-app-examples)
- `gemini-github-analyzer` (examples/gemini-github-analyzer)

---

### 第三部分：实时监控（案例 09-10）

#### 案例 09: 价格变动监控 ⭐⭐⭐⭐

**业务需求**: 实时监控关键商品和服务价格

**监控对象**:
- 租房价格
- 二手车价格
- 商家促销信息

**核心功能**:
- 使用 Change Tracking 监控变化
- 设置价格阈值
- 自动发送通知（Email/SMS/微信）
- 保存历史价格数据

**技术栈**: Python + Firecrawl Change Tracking + 通知服务

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 3 小时

**参考项目**:
- `automated_price_tracking` (firecrawl-app-examples)
- `change-detection-tutorial` (firecrawl-app-examples)

---

#### 案例 10: 内容更新监控 ⭐⭐⭐

**业务需求**: 监控重要网站内容更新

**监控对象**:
- 政府公告
- 签证政策
- 本地新闻
- 社区活动

**核心功能**:
- 定时检查网站变化
- 提取新增内容
- 生成更新摘要
- 推送到社区

**技术栈**: Python + Firecrawl + 定时任务

**难度**: ⭐⭐⭐（初级）

**学习时间**: 2 小时

**参考项目**:
- `change-detection-tutorial` (firecrawl-app-examples)

---

### 第四部分：AI 应用（案例 11-13）

#### 案例 11: 智能问答系统 ⭐⭐⭐⭐⭐

**业务需求**: 构建 HawaiiHub 知识库问答系统

**知识来源**:
- 网站所有文章
- 用户常见问题
- 本地服务指南

**核心功能**:
- 爬取所有内容构建知识库
- 使用 RAG 技术实现智能问答
- 支持中英文问答
- 持续更新知识库

**技术栈**: Python + Firecrawl + LangChain + Vector DB

**难度**: ⭐⭐⭐⭐⭐（高级）

**学习时间**: 8 小时

**参考项目**:
- `local-website-chatbot` (firecrawl-app-examples)
- `deepseek-rag` (firecrawl-app-examples)
- `web_data_rag_with_llama3` (examples/web_data_rag_with_llama3)
- `website_qa_with_gemini_caching` (examples/website_qa_with_gemini_caching)

---

#### 案例 12: 个性化推荐系统 ⭐⭐⭐⭐⭐

**业务需求**: 为用户推荐合适的商家和服务

**推荐内容**:
- 餐厅推荐
- 租房推荐
- 活动推荐
- 服务推荐

**核心功能**:
- 爬取用户浏览历史
- 分析用户偏好
- 使用协同过滤推荐
- 实时更新推荐结果

**技术栈**: Python + Firecrawl + ML 推荐算法

**难度**: ⭐⭐⭐⭐⭐（高级）

**学习时间**: 10 小时

**参考项目**:
- `ai-resume-job-matching` (firecrawl-app-examples)
- `o1_job_recommender` (examples/o1_job_recommender)

---

#### 案例 13: AI 内容生成 ⭐⭐⭐⭐

**业务需求**: 自动生成社区简报和内容

**生成内容**:
- 每周新闻简报
- 商家推荐文章
- 活动预告
- 生活指南

**核心功能**:
- 爬取相关内容
- 使用 LLM 生成文章
- 自动配图
- 定时发布

**技术栈**: Python + Firecrawl + GPT/Claude + CMS

**难度**: ⭐⭐⭐⭐（中级）

**学习时间**: 6 小时

**参考项目**:
- `aginews-ai-newsletter` (examples/aginews-ai-newsletter)
- `deepseek-v3-agi-newsletter` (firecrawl-app-examples)
- `ai-podcast-generator` (examples/ai-podcast-generator)

---

### 第五部分：完整系统（案例 14-15）

#### 案例 14: 端到端商家管理系统 ⭐⭐⭐⭐⭐

**业务需求**: 完整的商家信息管理系统

**系统功能**:
1. **数据采集**
   - 自动爬取商家信息
   - 更新营业时间、菜单、价格

2. **数据管理**
   - 商家信息存储
   - 评论管理
   - 图片管理

3. **数据展示**
   - 商家列表页面
   - 详情页面
   - 搜索和筛选

4. **监控告警**
   - 价格变动提醒
   - 新评论通知
   - 数据质量检查

**技术栈**:
- 后端: Python + Firecrawl + FastAPI + PostgreSQL
- 前端: Next.js + React + Tailwind CSS
- 部署: Docker + Vercel

**难度**: ⭐⭐⭐⭐⭐（高级）

**学习时间**: 2-3 天

**参考项目**:
- `company-data-scraper` (firecrawl-app-examples)
- `full_example_apps` (examples/full_example_apps)

---

#### 案例 15: HawaiiHub 完整数据平台 ⭐⭐⭐⭐⭐

**业务需求**: HawaiiHub 生产级数据采集和分析平台

**平台架构**:

```
┌─────────────────────────────────────────────┐
│           HawaiiHub 数据平台                │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ 数据采集层   │  │ 数据存储层   │        │
│  │              │  │              │        │
│  │ - Firecrawl  │──│ - PostgreSQL │        │
│  │ - 定时任务   │  │ - Redis      │        │
│  │ - 监控告警   │  │ - S3/OSS     │        │
│  └──────────────┘  └──────────────┘        │
│         │                  │                │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ 数据处理层   │  │ 应用服务层   │        │
│  │              │  │              │        │
│  │ - ETL        │──│ - API        │        │
│  │ - 清洗去重   │  │ - 搜索       │        │
│  │ - AI 分析    │  │ - 推荐       │        │
│  └──────────────┘  └──────────────┘        │
│         │                  │                │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ 前端展示层   │  │ 运营管理层   │        │
│  │              │  │              │        │
│  │ - Next.js    │  │ - Admin      │        │
│  │ - Mobile App │  │ - Dashboard  │        │
│  │ - 小程序     │  │ - Analytics  │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
```

**核心模块**:

1. **数据采集模块**
   - 新闻采集
   - 商家采集
   - 租房采集
   - 招聘采集
   - 活动采集

2. **数据处理模块**
   - 数据清洗
   - 去重验证
   - 格式标准化
   - AI 内容分析

3. **应用服务模块**
   - RESTful API
   - GraphQL API
   - WebSocket 实时推送
   - 搜索服务

4. **智能功能模块**
   - 智能推荐
   - 智能问答
   - 内容生成
   - 趋势分析

5. **运营管理模块**
   - 数据质量监控
   - 爬取任务管理
   - 用户行为分析
   - 成本控制

**技术栈**:
- **后端**: Python + FastAPI + Celery + Redis
- **前端**: Next.js 14 + TypeScript + Tailwind CSS
- **数据库**: PostgreSQL + Redis + Elasticsearch
- **爬虫**: Firecrawl Cloud API
- **AI**: LangChain + OpenAI/Claude
- **部署**: Docker + Kubernetes + Vercel
- **监控**: Sentry + Grafana + Prometheus

**难度**: ⭐⭐⭐⭐⭐（专家级）

**学习时间**: 1-2 周

**参考项目**:
- 所有前面的案例
- `full_example_apps` (examples/full_example_apps)
- `kubernetes` (examples/kubernetes)

---

## 📖 案例详解

### 案例 01 详解：夏威夷新闻采集器

#### 步骤 1: 分析目标网站

```python
# 1.1 分析网站结构
# Hawaii News Now: https://www.hawaiinewsnow.com/

# 首页结构:
# - 头条新闻：class="lead-story"
# - 新闻列表：class="article-list"
# - 每篇新闻：<article>标签

# 新闻详情页结构:
# - 标题：<h1 class="headline">
# - 作者：<div class="byline">
# - 时间：<time datetime="">
# - 内容：<div class="article-body">
```

#### 步骤 2: 爬取单篇新闻

```python
from firecrawl import FirecrawlApp
import os
from datetime import datetime
import json

# 初始化客户端
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

def scrape_single_news(url: str) -> dict:
    """
    爬取单篇新闻

    Args:
        url: 新闻 URL

    Returns:
        新闻数据字典
    """
    try:
        # 使用 Scrape API
        result = app.scrape(
            url=url,
            formats=["markdown", "html"],
            only_main_content=True,  # 只提取主要内容
            remove_base64_images=True,  # 移除 base64 图片
        )

        # 提取数据
        news_data = {
            "url": url,
            "title": extract_title(result.markdown),
            "author": extract_author(result.markdown),
            "published_date": extract_date(result.markdown),
            "content": result.markdown,
            "html": result.html,
            "scraped_at": datetime.now().isoformat(),
        }

        return news_data

    except Exception as e:
        print(f"❌ 爬取失败: {url} - {e}")
        return None

def extract_title(markdown: str) -> str:
    """从 Markdown 中提取标题"""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "").strip()
    return "未知标题"

def extract_author(markdown: str) -> str:
    """从 Markdown 中提取作者"""
    # 实现提取逻辑
    # 通常在 "By " 或 "作者：" 之后
    import re
    match = re.search(r"By\s+([A-Za-z\s]+)", markdown)
    if match:
        return match.group(1).strip()
    return "未知作者"

def extract_date(markdown: str) -> str:
    """从 Markdown 中提取发布时间"""
    # 实现提取逻辑
    import re
    # 查找日期模式
    match = re.search(r"(\d{4}-\d{2}-\d{2}|\w+ \d{1,2}, \d{4})", markdown)
    if match:
        return match.group(1)
    return datetime.now().strftime("%Y-%m-%d")

# 测试
if __name__ == "__main__":
    test_url = "https://www.hawaiinewsnow.com/2025/01/27/some-news/"
    news = scrape_single_news(test_url)

    if news:
        print(f"✅ 成功爬取: {news['title']}")
        print(f"作者: {news['author']}")
        print(f"时间: {news['published_date']}")

        # 保存为 JSON
        with open(f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding="utf-8") as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
```

#### 步骤 3: 爬取新闻列表

```python
def scrape_news_list(homepage_url: str, limit: int = 20) -> list:
    """
    爬取新闻列表

    Args:
        homepage_url: 首页 URL
        limit: 爬取数量限制

    Returns:
        新闻列表
    """
    try:
        # 使用 Crawl API
        result = app.crawl(
            url=homepage_url,
            limit=limit,
            scrape_options={
                "formats": ["markdown"],
                "only_main_content": True,
            },
            include_paths=["/2025/", "/news/"],  # 只爬取新闻路径
            exclude_paths=["/weather/", "/sports/"],  # 排除不需要的路径
        )

        news_list = []
        for item in result:
            if isinstance(item, tuple):
                success, data = item
                if success:
                    news_list.append({
                        "url": data.url,
                        "title": extract_title(data.markdown),
                        "author": extract_author(data.markdown),
                        "published_date": extract_date(data.markdown),
                        "content": data.markdown,
                    })
            else:
                news_list.append({
                    "url": item.url,
                    "title": extract_title(item.markdown),
                    "author": extract_author(item.markdown),
                    "published_date": extract_date(item.markdown),
                    "content": item.markdown,
                })

        return news_list

    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    homepage = "https://www.hawaiinewsnow.com/"
    news_list = scrape_news_list(homepage, limit=10)

    print(f"✅ 成功爬取 {len(news_list)} 篇新闻")

    # 保存为 JSON
    with open(f"news_list_{datetime.now().strftime('%Y%m%d')}.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
```

#### 步骤 4: 使用 Extract API 结构化提取

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class NewsArticle(BaseModel):
    """新闻文章数据模型"""
    title: str = Field(..., description="新闻标题")
    author: str = Field(..., description="作者姓名")
    published_date: str = Field(..., description="发布日期")
    category: str = Field(..., description="新闻类别")
    summary: str = Field(..., description="新闻摘要")
    content: str = Field(..., description="新闻正文")
    tags: List[str] = Field(default_factory=list, description="标签列表")

def scrape_with_extract(url: str) -> Optional[NewsArticle]:
    """
    使用 Extract API 结构化提取新闻

    Args:
        url: 新闻 URL

    Returns:
        结构化新闻数据
    """
    try:
        result = app.scrape(
            url=url,
            formats=[{
                "type": "json",
                "schema": NewsArticle.model_json_schema(),
            }],
        )

        # 将 JSON 转换为 Pydantic 模型
        news = NewsArticle(**result.json)
        return news

    except Exception as e:
        print(f"❌ 提取失败: {url} - {e}")
        return None

# 测试
if __name__ == "__main__":
    test_url = "https://www.hawaiinewsnow.com/2025/01/27/some-news/"
    news = scrape_with_extract(test_url)

    if news:
        print(f"✅ 成功提取:")
        print(f"标题: {news.title}")
        print(f"作者: {news.author}")
        print(f"类别: {news.category}")
        print(f"摘要: {news.summary}")
        print(f"标签: {', '.join(news.tags)}")
```

#### 步骤 5: 定时任务

```python
import schedule
import time

def daily_news_scraper():
    """
    每日新闻爬取任务
    """
    print(f"🕐 {datetime.now()}: 开始爬取每日新闻...")

    # 爬取多个新闻源
    sources = [
        "https://www.hawaiinewsnow.com/",
        "https://www.staradvertiser.com/",
        "https://www.civilbeat.org/",
    ]

    all_news = []
    for source in sources:
        print(f"📰 爬取: {source}")
        news_list = scrape_news_list(source, limit=10)
        all_news.extend(news_list)

    # 保存数据
    filename = f"daily_news_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"✅ 完成！共爬取 {len(all_news)} 篇新闻，保存到 {filename}")

# 设置定时任务
schedule.every().day.at("08:00").do(daily_news_scraper)  # 每天早上 8 点执行

print("🚀 新闻爬取定时任务已启动...")
print("每天 08:00 自动爬取夏威夷新闻")

# 运行定时任务
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次
```

---

## 🎓 学习建议

### 循序渐进学习路径

**第 1 周：基础案例**
- Day 1-2: 案例 01（新闻采集）
- Day 3-4: 案例 04（招聘信息）
- Day 5-6: 案例 05（活动信息）
- Day 7: 总结和复习

**第 2 周：进阶案例**
- Day 1-2: 案例 02（商家采集）
- Day 3-4: 案例 03（租房监控）
- Day 5-6: 案例 06（评论分析）
- Day 7: 实战项目

**第 3 周：高级案例**
- Day 1-2: 案例 11（智能问答）
- Day 3-4: 案例 13（内容生成）
- Day 5-7: 案例 14（完整系统）

**第 4 周：生产部署**
- Day 1-5: 案例 15（数据平台）
- Day 6-7: 优化和部署

### 实战技巧

1. **从简单开始** - 先掌握 Scrape API，再学习 Crawl
2. **多练习** - 每个案例至少运行 3 次
3. **修改参数** - 尝试不同的配置选项
4. **错误处理** - 添加完整的异常处理
5. **数据验证** - 使用 Pydantic 验证数据
6. **性能优化** - 使用缓存和批量处理
7. **成本控制** - 监控 API 使用量

---

## 📊 项目参考

### Firecrawl 官方示例（56 个）

位置: `/Users/zhiledeng/Downloads/FireShot/Firecrawl学习手册/05-实战案例/firecrawl-main-repo/examples/`

**推荐学习顺序**:

1. **爬虫基础** (学习 Crawl API)
   - `gpt-4.1-web-crawler`
   - `claude3.7-web-crawler`
   - `gemini-2.5-crawler`
   - `deepseek-v3-crawler`

2. **数据提取** (学习 Extract API)
   - `simple_web_data_extraction_with_claude`
   - `web_data_extraction`
   - `attributes-extraction-python-sdk.py`

3. **公司研究** (商家采集参考)
   - `gpt-4.1-company-researcher`
   - `deepseek-v3-company-researcher`
   - `R1_company_researcher`

4. **实战项目**
   - `hacker_news_scraper`
   - `blog-articles`
   - `scrape_and_analyze_airbnb_data_e2b`
   - `deep-research-apartment-finder`

5. **AI 集成**
   - `web_data_rag_with_llama3`
   - `website_qa_with_gemini_caching`
   - `openai_swarm_firecrawl`

### Firecrawl App Examples（40 个）

位置: `/Users/zhiledeng/Downloads/FireShot/Firecrawl学习手册/05-实战案例/示例应用/firecrawl-app-examples/`

**HawaiiHub 推荐**:

1. `company-data-scraper` - 商家数据采集
2. `automated_price_tracking` - 价格监控
3. `review-analyzer` - 评论分析
4. `local-website-chatbot` - 智能问答
5. `ai-resume-job-matching` - 招聘匹配

---

## 🔗 相关资源

### 文档

- 完整学习手册: `01-基础入门/Firecrawl完整学习手册.md`
- API 规范: `03-API参考/云端API规范.md`
- 配置指南: `04-配置指南/云端配置指南.md`
- 项目索引: `05-实战案例/示例项目完整索引.md`

### 官方资源

- 官方文档: https://docs.firecrawl.dev/
- GitHub 主仓库: https://github.com/firecrawl/firecrawl
- 示例仓库: https://github.com/firecrawl/firecrawl-app-examples
- Discord 社区: https://discord.gg/firecrawl

---

## 🎉 下一步

准备好开始了吗？

**推荐起点**:

```bash
# 1. 创建项目目录
mkdir -p hawaiihub-firecrawl-cases
cd hawaiihub-firecrawl-cases

# 2. 创建第一个案例
mkdir case-01-news-scraper
cd case-01-news-scraper

# 3. 复制上面的代码，开始实践！
```

**学习顺序**:

1. ✅ 从案例 01 开始
2. ✅ 每完成一个案例，记录笔记
3. ✅ 遇到问题查阅文档
4. ✅ 参考官方示例项目
5. ✅ 最终构建完整系统

---

**祝学习愉快，项目成功！** 🚀🌺

---

**创建时间**: 2025-10-27
**版本**: v1.0
**维护者**: HawaiiHub AI Team
**适用项目**: HawaiiHub - 夏威夷华人社区平台
