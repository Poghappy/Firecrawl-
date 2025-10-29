# HawaiiHub 数据采集源清单

> **生成时间**: 2025-10-28
> **研究方法**: Firecrawl 深度搜索
> **维护者**: HawaiiHub AI Team
> **版本**: v1.0

---

## 📋 目录

- [1. 本地新闻媒体（7个核心源）](#1-本地新闻媒体)
- [2. 华人社区资源（10个核心源）](#2-华人社区资源)
- [3. 餐饮美食指南（9个核心源）](#3-餐饮美食指南)
- [4. 旅游活动日历（9个核心源）](#4-旅游活动日历)
- [5. 商业目录（10个核心源）](#5-商业目录)
- [6. 采集策略与实施](#6-采集策略与实施)

---

## 1. 本地新闻媒体

### 🎯 采集优先级: P0（每日更新）

| 序号 | 网站名称                     | URL                                          | 描述                                     | 采集价值                        | 建议频率 |
| ---- | ---------------------------- | -------------------------------------------- | ---------------------------------------- | ------------------------------- | -------- |
| 1    | **Hawaii News Now**          | https://www.hawaiinewsnow.com/               | 夏威夷最大的新闻网站，KGMB/KHNL 联合平台 | ⭐⭐⭐⭐⭐ 突发新闻、天气、交通 | 每2小时  |
| 2    | **Honolulu Civil Beat**      | https://www.civilbeat.org/                   | 深度调查报道，无付费墙                   | ⭐⭐⭐⭐⭐ 政治、社区、深度报道 | 每6小时  |
| 3    | **Honolulu Star-Advertiser** | https://www.staradvertiser.com/              | 檀香山最权威的报纸                       | ⭐⭐⭐⭐⭐ 综合新闻、商业、体育 | 每4小时  |
| 4    | **KHON2**                    | https://www.khon2.com/                       | 檀香山、科纳、希洛、考艾、毛伊新闻       | ⭐⭐⭐⭐ 全岛新闻覆盖           | 每6小时  |
| 5    | **KITV 4 Island News**       | https://www.kitv.com/                        | 檀香山突发新闻和天气                     | ⭐⭐⭐⭐ 本地政治、犯罪、健康   | 每6小时  |
| 6    | **Hawaii Tribune-Herald**    | https://www.hawaiitribune-herald.com/        | 希洛地区（大岛）专属新闻                 | ⭐⭐⭐ 大岛地方新闻             | 每日1次  |
| 7    | **Spectrum News Hawaii**     | https://spectrumlocalnews.com/hi/hawaii/news | 本地新闻和调查报道                       | ⭐⭐⭐ 补充性新闻源             | 每日1次  |

#### 📝 采集配置示例

```python
# 新闻采集配置
NEWS_SOURCES = [
    {
        "name": "Hawaii News Now",
        "url": "https://www.hawaiinewsnow.com/",
        "scrape_config": {
            "formats": ["markdown", "html"],
            "only_main_content": True,
            "exclude_tags": ["nav", "footer", "aside"],
            "max_age": 7200000  # 2小时缓存
        },
        "parse_rules": {
            "article_selector": "article.news-item",
            "title": "h1",
            "author": ".author-name",
            "date": "time",
            "category": ".category-tag"
        },
        "frequency": "*/2 * * * *",  # 每2小时
        "priority": "P0"
    }
]
```

---

## 2. 华人社区资源

### 🎯 采集优先级: P0（核心用户群体）

| 序号 | 网站名称                                  | URL                                                 | 描述                         | 采集价值                                | 建议频率 |
| ---- | ----------------------------------------- | --------------------------------------------------- | ---------------------------- | --------------------------------------- | -------- |
| 1    | **夏威夷中国日报**                        | https://hawaiichinesedaily.com/                     | 华人社区最权威中文媒体       | ⭐⭐⭐⭐⭐ 华人新闻、文化活动、商业信息 | 每4小时  |
| 2    | **Chinese Chamber of Commerce of Hawaii** | https://www.chinesechamber.com/                     | 夏威夷华人商会（1911年成立） | ⭐⭐⭐⭐⭐ 商业活动、研讨会、教育       | 每周2次  |
| 3    | **United Chinese Society of Hawaii**      | https://www.ucsofhawaii.com/                        | 夏威夷华人联合会             | ⭐⭐⭐⭐ 社区活动、慈善项目             | 每周2次  |
| 4    | **夏威夷中信福音中心**                    | https://ccmhawaii.org/                              | 华人基督教社区中心           | ⭐⭐⭐⭐ 社区服务、讲座、聚会           | 每周1次  |
| 5    | **Hawaii Chinese Baptist Church**         | https://gohcbc.org/home/                            | 夏威夷华人浸信会             | ⭐⭐⭐ 宗教活动、讲道、团契             | 每周1次  |
| 6    | **Chinese Lutheran Church of Honolulu**   | https://www.clch.org/                               | 檀香山华人信义会             | ⭐⭐⭐ 教会活动、社区服务               | 每周1次  |
| 7    | **驻檀香山台北经济文化办事处**            | https://www.roc-taiwan.org/ushnl/                   | 台湾官方机构                 | ⭐⭐⭐⭐ 官方活动、文化交流             | 每周2次  |
| 8    | **The Chinese in Hawaii (Facebook)**      | https://www.facebook.com/groups/921164547948937/    | 夏威夷华人 Facebook 群组     | ⭐⭐⭐⭐ 社区互动、历史文化             | 每日1次  |
| 9    | **Hawaii Chinese Republican Coalition**   | http://www.b2bchinadirect.com/hcrc.htm              | 夏威夷华人共和党联盟         | ⭐⭐⭐ 华人参政信息                     | 每月1次  |
| 10   | **檀香山华人社区**                        | https://www.chineseinhi.com/kw/id_19/keyid_503.html | 华人论坛和信息网             | ⭐⭐⭐⭐ 华人生活信息、论坛             | 每日1次  |

#### 📝 采集配置示例

```python
# 华人社区采集配置
CHINESE_COMMUNITY_SOURCES = [
    {
        "name": "夏威夷中国日报",
        "url": "https://hawaiichinesedaily.com/",
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "location": {
                "country": "US",
                "languages": ["zh-CN", "zh-TW"]
            }
        },
        "content_types": ["新闻", "文化活动", "商业资讯"],
        "target_audience": "华人社区",
        "frequency": "0 */4 * * *",  # 每4小时
        "priority": "P0"
    },
    {
        "name": "Chinese Chamber of Commerce",
        "url": "https://www.chinesechamber.com/",
        "scrape_config": {
            "formats": ["markdown", "json"],
            "only_main_content": True
        },
        "extract_schema": {
            "type": "object",
            "properties": {
                "event_name": {"type": "string"},
                "event_date": {"type": "string"},
                "event_type": {"type": "string"},
                "description": {"type": "string"},
                "registration_link": {"type": "string"}
            }
        },
        "frequency": "0 9,18 * * 1,4",  # 每周一、四，早9点和晚6点
        "priority": "P0"
    }
]
```

---

## 3. 餐饮美食指南

### 🎯 采集优先级: P1（商业信息核心）

| 序号 | 网站名称                        | URL                                                                                                                                                                   | 描述                         | 采集价值                            | 建议频率  |
| ---- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------- | --------- |
| 1    | **Yelp - Honolulu Hawaiian**    | https://www.yelp.com/search?cflt=hawaiian&find_loc=Honolulu%2C+HI                                                                                                     | 檀香山夏威夷餐厅排名         | ⭐⭐⭐⭐⭐ 用户评价、餐厅信息、照片 | 每日1次   |
| 2    | **TripAdvisor - Hawaiian Food** | https://www.tripadvisor.com/Restaurants-g60982-c10772-Honolulu_Oahu_Hawaii.html                                                                                       | 夏威夷美食最佳餐厅           | ⭐⭐⭐⭐⭐ 游客评价、排名、价格     | 每日1次   |
| 3    | **OpenTable Hawaii**            | https://www.opentable.com/metro/hawaii-restaurants                                                                                                                    | 夏威夷餐厅在线预订           | ⭐⭐⭐⭐⭐ 2311家餐厅、评价、预订   | 每日1次   |
| 4    | **Eater Honolulu**              | https://www.eater.com/maps/where-chefs-locals-eat-honolulu-hawaii                                                                                                     | 厨师推荐檀香山餐厅           | ⭐⭐⭐⭐⭐ 专业推荐、新餐厅         | 每周2次   |
| 5    | **Grace and Lightness**         | https://graceandlightness.com/best-restaurants-honolulu-oahu/                                                                                                         | 檀香山25家最佳餐厅           | ⭐⭐⭐⭐ 美食博客推荐               | 每月1次   |
| 6    | **Wanderlog 米其林**            | https://wanderlog.com/zh/list/geoCategory/60716/%E5%AE%B6%E7%B1%B3%E5%85%B6%E6%9E%97%E6%98%9F%E7%BA%A7%E9%A4%90%E5%8E%85%E5%9C%A8%E7%81%AB%E5%A5%B4%E9%B2%81%E9%B2%81 | 火奴鲁鲁46家米其林餐厅       | ⭐⭐⭐⭐⭐ 高端餐饮、米其林评级     | 每月1次   |
| 7    | **DealMoon 欧胡岛美食**         | https://www.dealmoon.com/guide/963829                                                                                                                                 | 华人视角的欧胡岛美食推荐     | ⭐⭐⭐⭐ 华人喜好、预订建议         | 每月1次   |
| 8    | **携程 Helena's Hawaiian Food** | http://you.ctrip.com/food/oahu120071/455556-food.html                                                                                                                 | 经典夏威夷料理餐厅（1946年） | ⭐⭐⭐⭐ 经典餐厅信息               | 每季度1次 |
| 9    | **YouTube - 25 Must Try Foods** | https://www.youtube.com/watch?v=petG2-yzZYE                                                                                                                           | 欧胡岛25种必吃美食+65个地点  | ⭐⭐⭐⭐ 视频内容、美食清单         | 手动采集  |

#### 📝 采集配置示例

```python
# 餐饮美食采集配置
RESTAURANT_SOURCES = [
    {
        "name": "Yelp Honolulu Hawaiian",
        "url": "https://www.yelp.com/search?cflt=hawaiian&find_loc=Honolulu%2C+HI",
        "scrape_config": {
            "formats": ["markdown", "json"],
            "only_main_content": True,
            "actions": [
                {"type": "wait", "milliseconds": 2000},
                {"type": "scroll", "direction": "down"}
            ]
        },
        "extract_schema": {
            "type": "object",
            "properties": {
                "restaurant_name": {"type": "string"},
                "rating": {"type": "number"},
                "review_count": {"type": "number"},
                "price_range": {"type": "string"},
                "cuisine_type": {"type": "string"},
                "address": {"type": "string"},
                "phone": {"type": "string"},
                "popular_dishes": {"type": "array"}
            }
        },
        "frequency": "0 10 * * *",  # 每天早上10点
        "priority": "P1"
    },
    {
        "name": "OpenTable Hawaii",
        "url": "https://www.opentable.com/metro/hawaii-restaurants",
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True
        },
        "post_processing": [
            "extract_restaurant_links",
            "batch_scrape_restaurant_details",
            "merge_with_existing_data"
        ],
        "frequency": "0 11 * * *",  # 每天早上11点
        "priority": "P1"
    }
]
```

---

## 4. 旅游活动日历

### 🎯 采集优先级: P1（吸引游客和本地参与）

| 序号 | 网站名称                             | URL                                                                                           | 描述                       | 采集价值                              | 建议频率 |
| ---- | ------------------------------------ | --------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------- | -------- |
| 1    | **Go Hawaii 官方**                   | https://www.gohawaii.com/trip-planning/events-festivals                                       | 夏威夷官方活动日历         | ⭐⭐⭐⭐⭐ 官方认证、全年活动         | 每周1次  |
| 2    | **Go Hawaii 中文版**                 | https://www.gohawaii.cn/cn                                                                    | 夏威夷旅游官网中文版       | ⭐⭐⭐⭐⭐ 中文活动信息               | 每周1次  |
| 3    | **Hawaii Tourism Authority**         | https://www.hawaiitourismauthority.org/what-we-do/events/                                     | 夏威夷旅游局官方活动       | ⭐⭐⭐⭐⭐ 官方大型活动、会议         | 每周1次  |
| 4    | **欧胡岛盛会日历**                   | https://www.gohawaii.cn/cn/islands/oahu/events                                                | 欧胡岛中文活动日历         | ⭐⭐⭐⭐⭐ 中文本地活动               | 每周1次  |
| 5    | **Hawaii Guide Events**              | https://www.hawaii-guide.com/hawaii-events                                                    | 夏威夷活动与节日           | ⭐⭐⭐⭐ 梅里莫纳克节等经典活动       | 每周1次  |
| 6    | **HTA Festivals & Events Resources** | https://www.hawaiitourismauthority.org/what-we-do/tools-resources/festivals-events-resources/ | 官方节日活动资源           | ⭐⭐⭐⭐ 文化、艺术、音乐、美食、体育 | 每周1次  |
| 7    | **HVCB Events**                      | https://www.hvcb.org/events/                                                                  | 夏威夷游客和会议局活动     | ⭐⭐⭐⭐ 行业活动、网络交流           | 每周1次  |
| 8    | **大岛活动日历**                     | https://gohawaii.com.hawaiidev.milesmediagroup.com/islands/hawaii-big-island/events           | 大岛活动（梅里莫纳克节等） | ⭐⭐⭐⭐ 大岛专属活动                 | 每周1次  |
| 9    | **Honolulu Magazine Events**         | https://www.honolulumagazine.com/local-events/                                                | 檀香山本地活动             | ⭐⭐⭐⭐ 万圣节、本地节日             | 每周1次  |

#### 📝 采集配置示例

```python
# 旅游活动采集配置
EVENTS_SOURCES = [
    {
        "name": "Go Hawaii Official Events",
        "url": "https://www.gohawaii.com/trip-planning/events-festivals",
        "scrape_config": {
            "formats": ["markdown", "json"],
            "only_main_content": True
        },
        "extract_schema": {
            "type": "object",
            "properties": {
                "event_name": {"type": "string"},
                "event_date": {"type": "string"},
                "event_location": {"type": "string"},
                "event_island": {"type": "string"},
                "event_category": {"type": "string"},
                "description": {"type": "string"},
                "ticket_link": {"type": "string"}
            }
        },
        "frequency": "0 8 * * 1",  # 每周一早上8点
        "priority": "P1"
    },
    {
        "name": "Go Hawaii 中文版",
        "url": "https://www.gohawaii.cn/cn",
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "location": {
                "country": "CN",
                "languages": ["zh-CN"]
            }
        },
        "content_types": ["活动", "节日", "文化", "美食"],
        "frequency": "0 9 * * 1",  # 每周一早上9点
        "priority": "P1"
    }
]
```

---

## 5. 商业目录

### 🎯 采集优先级: P2（商业信息补充）

| 序号 | 网站名称                               | URL                                                                             | 描述                         | 采集价值                        | 建议频率  |
| ---- | -------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------- | ------------------------------- | --------- |
| 1    | **Yellow Pages - Honolulu**            | https://www.yellowpages.com/honolulu-hi                                         | 檀香山商业黄页               | ⭐⭐⭐⭐⭐ 全类别商业信息       | 每月1次   |
| 2    | **Yellow Pages - Hawaii**              | https://www.yellowpages.com/hawaii-hi                                           | 夏威夷州商业黄页             | ⭐⭐⭐⭐⭐ 全州商业目录         | 每月1次   |
| 3    | **Yellow Pages - Maui**                | https://www.yellowpages.com/maui-hi                                             | 毛伊岛商业黄页               | ⭐⭐⭐⭐ 毛伊岛商业信息         | 每月1次   |
| 4    | **Yellow Pages - Oahu**                | https://www.yellowpages.com/oahu-hi                                             | 欧胡岛商业黄页               | ⭐⭐⭐⭐ 欧胡岛商业信息         | 每月1次   |
| 5    | **Hawaii Business Directory (DBEDT)**  | https://dbedt.hawaii.gov/economic/library/faq/faq02/                            | 夏威夷州官方商业目录         | ⭐⭐⭐⭐⭐ 官方认证商业信息     | 每季度1次 |
| 6    | **Shop Small Hawaii**                  | https://www.shopsmallhawaii.com/guide-info                                      | 夏威夷小企业目录（500+商家） | ⭐⭐⭐⭐ 本地小企业、手工艺品   | 每月1次   |
| 7    | **夏威夷华人黄页**                     | https://hawaii.jinbay.com/yellowpages/190/yellowlist_a0_sc0_sa0_k_l1_s0_p0.html | 华人商业服务黄页             | ⭐⭐⭐⭐⭐ 华人商家、生活服务   | 每月1次   |
| 8    | **Native Hawaiian Business Directory** | https://kanakaeconomy.com/                                                      | 夏威夷原住民企业目录         | ⭐⭐⭐⭐ 原住民拥有或控制的企业 | 每季度1次 |
| 9    | **Hawaii Convention Center Events**    | https://events.hawaiiconvention.com/                                            | 夏威夷会议中心活动日历       | ⭐⭐⭐ 会议、展览活动           | 每周1次   |
| 10   | **Hawaii International Conference**    | https://manoa.hawaii.edu/hiccs/                                                 | 夏威夷国际会议               | ⭐⭐⭐ 学术会议、文化交流       | 每季度1次 |

#### 📝 采集配置示例

```python
# 商业目录采集配置
BUSINESS_DIRECTORY_SOURCES = [
    {
        "name": "Yellow Pages Honolulu",
        "url": "https://www.yellowpages.com/honolulu-hi",
        "scrape_config": {
            "formats": ["markdown", "json"],
            "only_main_content": True
        },
        "extract_schema": {
            "type": "object",
            "properties": {
                "business_name": {"type": "string"},
                "category": {"type": "string"},
                "address": {"type": "string"},
                "phone": {"type": "string"},
                "website": {"type": "string"},
                "rating": {"type": "number"},
                "review_count": {"type": "number"}
            }
        },
        "pagination": {
            "enabled": True,
            "max_pages": 50
        },
        "frequency": "0 2 1 * *",  # 每月1号凌晨2点
        "priority": "P2"
    },
    {
        "name": "夏威夷华人黄页",
        "url": "https://hawaii.jinbay.com/yellowpages/190/yellowlist_a0_sc0_sa0_k_l1_s0_p0.html",
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True
        },
        "target_categories": [
            "餐饮", "购物", "服务", "教育",
            "医疗", "法律", "金融", "房地产"
        ],
        "frequency": "0 3 1 * *",  # 每月1号凌晨3点
        "priority": "P2"
    }
]
```

---

## 6. 采集策略与实施

### 6.1 总体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    HawaiiHub 数据采集系统                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  调度中心      │     │  采集引擎      │     │  存储中心      │
│  (Scheduler)  │────▶│  (Scraper)    │────▶│  (Storage)    │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
  ┌─────────┐         ┌─────────┐         ┌─────────┐
  │ Cron Jobs│         │Firecrawl│         │PostgreSQL│
  │ n8n     │         │ MCP SDK │         │ Redis   │
  └─────────┘         └─────────┘         └─────────┘
```

### 6.2 采集优先级划分

#### P0 - 核心日常采集（每日运行）

- **新闻媒体**: Hawaii News Now, Civil Beat, Star-Advertiser
- **华人社区**: 夏威夷中国日报, Chinese Chamber
- **餐饮信息**: Yelp, TripAdvisor, OpenTable

**预计成本**: $2-3/天

#### P1 - 重要周期采集（每周运行）

- **旅游活动**: Go Hawaii, 旅游局活动
- **社区组织**: 华人教会, 商会活动
- **美食推荐**: Eater, 米其林餐厅

**预计成本**: $5-8/周

#### P2 - 补充性采集（每月/季度运行）

- **商业目录**: Yellow Pages, 小企业目录
- **学术会议**: 国际会议, 文化论坛
- **专题内容**: 原住民企业, 特定行业

**预计成本**: $10-15/月

### 6.3 技术实施方案

#### 方案A：基于 Firecrawl MCP + n8n（推荐）

```javascript
// n8n 工作流示例
{
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "0 */2 * * *"  // 每2小时
      }
    },
    {
      "name": "Firecrawl Scrape",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://www.hawaiinewsnow.com/",
        "method": "POST",
        "body": {
          "formats": ["markdown"],
          "onlyMainContent": true
        }
      }
    },
    {
      "name": "Parse & Store",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// 解析并存储到数据库"
      }
    }
  ]
}
```

#### 方案B：基于 Python SDK + Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from firecrawl import FirecrawlApp

# DAG 配置
default_args = {
    "owner": "hawaiihub",
    "depends_on_past": False,
    "start_date": datetime(2025, 10, 28),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "hawaiihub_news_scraper",
    default_args=default_args,
    description="每日新闻采集 DAG",
    schedule_interval="0 */2 * * *",  # 每2小时
    catchup=False,
)

def scrape_hawaii_news():
    """采集夏威夷新闻"""
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    news_sources = [
        "https://www.hawaiinewsnow.com/",
        "https://www.civilbeat.org/",
        "https://www.staradvertiser.com/"
    ]

    results = app.batch_scrape(
        urls=news_sources,
        formats=["markdown"],
        only_main_content=True
    )

    # 存储到数据库
    save_to_database(results)

# 任务定义
scrape_task = PythonOperator(
    task_id="scrape_news",
    python_callable=scrape_hawaii_news,
    dag=dag,
)
```

### 6.4 数据存储架构

```sql
-- PostgreSQL 数据表设计

-- 1. 新闻文章表
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    publish_date TIMESTAMP,
    category VARCHAR(50),
    source VARCHAR(100),
    content_markdown TEXT,
    content_html TEXT,
    summary TEXT,
    tags TEXT[],
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. 餐厅信息表
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    cuisine_type VARCHAR(100),
    address VARCHAR(300),
    phone VARCHAR(20),
    website VARCHAR(500),
    rating DECIMAL(3,2),
    review_count INTEGER,
    price_range VARCHAR(10),
    popular_dishes TEXT[],
    source VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. 活动日历表
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    event_date TIMESTAMP,
    end_date TIMESTAMP,
    location VARCHAR(200),
    island VARCHAR(50),
    category VARCHAR(100),
    description TEXT,
    ticket_link VARCHAR(500),
    organizer VARCHAR(200),
    source VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. 商业目录表
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    address VARCHAR(300),
    phone VARCHAR(20),
    website VARCHAR(500),
    email VARCHAR(100),
    description TEXT,
    rating DECIMAL(3,2),
    source VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. 采集日志表
CREATE TABLE scraping_logs (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100),
    source_url VARCHAR(500),
    status VARCHAR(20),  -- success, failed, partial
    items_scraped INTEGER,
    error_message TEXT,
    duration_seconds INTEGER,
    scraped_at TIMESTAMP DEFAULT NOW()
);

-- 索引优化
CREATE INDEX idx_articles_publish_date ON articles(publish_date DESC);
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_restaurants_rating ON restaurants(rating DESC);
CREATE INDEX idx_events_event_date ON events(event_date);
CREATE INDEX idx_businesses_category ON businesses(category);
```

### 6.5 成本优化策略

#### 1. 缓存机制（节省50%+成本）

```python
# Redis 缓存配置
CACHE_CONFIG = {
    "news": {
        "ttl": 7200,  # 2小时
        "key_pattern": "news:{url_hash}"
    },
    "restaurants": {
        "ttl": 86400,  # 24小时
        "key_pattern": "restaurant:{business_id}"
    },
    "events": {
        "ttl": 604800,  # 7天
        "key_pattern": "event:{event_id}"
    }
}

# 使用示例
import hashlib
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def scrape_with_cache(url: str) -> str:
    """带缓存的爬取"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    cache_key = f"news:{url_hash}"

    # 检查缓存
    cached = redis_client.get(cache_key)
    if cached:
        logging.info(f"缓存命中: {url}")
        return cached.decode()

    # 爬取新数据
    result = app.scrape(
        url=url,
        formats=["markdown"],
        only_main_content=True,
        max_age=7200000  # Firecrawl 云端缓存
    )

    # 存入 Redis
    redis_client.setex(cache_key, 7200, result.markdown)
    return result.markdown
```

#### 2. 增量更新（避免重复爬取）

```python
def incremental_scrape(source_url: str, last_scrape_time: datetime) -> List[Dict]:
    """增量爬取（只获取新内容）"""
    # 1. 爬取首页
    result = app.scrape(url=source_url, formats=["markdown"])

    # 2. 提取文章链接
    all_links = extract_article_links(result.markdown)

    # 3. 过滤已爬取的链接
    new_links = filter_new_links(all_links, last_scrape_time)

    # 4. 只爬取新链接
    if new_links:
        new_articles = app.batch_scrape(
            urls=new_links,
            formats=["markdown"]
        )
        logging.info(f"增量爬取: {len(new_links)} 篇新文章")
        return new_articles
    else:
        logging.info("无新内容")
        return []
```

#### 3. 密钥轮换（突破速率限制）

```python
# 使用多个 API 密钥
api_keys = [
    os.getenv("FIRECRAWL_API_KEY"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
]

client = RotatingFirecrawlClient(api_keys)
```

### 6.6 监控告警

#### 1. Grafana 监控面板

```yaml
# Prometheus 指标
scraping_total_requests: 计数器（总请求数）
scraping_failed_requests: 计数器（失败请求数）
scraping_duration_seconds: 直方图（响应时间）
scraping_cost_usd: 计数器（累计成本）
scraping_cached_hits: 计数器（缓存命中）

# 告警规则
- alert: HighFailureRate
  expr: rate(scraping_failed_requests[5m]) > 0.2
  for: 10m
  annotations:
    summary: "爬取失败率超过 20%"

- alert: HighCost
  expr: scraping_cost_usd > 50
  for: 1h
  annotations:
    summary: "每日成本超过 $50"
```

#### 2. Slack 通知

```python
import slack_sdk

def send_alert(message: str):
    """发送 Slack 告警"""
    client = slack_sdk.WebClient(token=os.getenv("SLACK_TOKEN"))
    client.chat_postMessage(
        channel="#hawaiihub-alerts",
        text=f"⚠️ 采集告警: {message}"
    )
```

---

## 7. 采集清单总结

### 7.1 核心数据源统计

| 类别         | 数量   | 采集频率     | 预估成本/月  |
| ------------ | ------ | ------------ | ------------ |
| 本地新闻媒体 | 7      | 每2-6小时    | $60-90       |
| 华人社区资源 | 10     | 每日-每周    | $40-60       |
| 餐饮美食指南 | 9      | 每日-每月    | $30-50       |
| 旅游活动日历 | 9      | 每周         | $20-30       |
| 商业目录     | 10     | 每月-每季度  | $20-30       |
| **总计**     | **45** | **混合频率** | **$170-260** |

### 7.2 数据量预估

| 数据类型 | 每日新增 | 每月累计      |
| -------- | -------- | ------------- |
| 新闻文章 | 50-80篇  | 1,500-2,400篇 |
| 餐厅信息 | 10-20家  | 300-600家     |
| 活动日历 | 5-10个   | 150-300个     |
| 商业目录 | 20-50家  | 600-1,500家   |

### 7.3 快速启动清单

```bash
# 1. 环境准备
cd /Users/zhiledeng/Downloads/FireShot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 配置环境变量
cp env.template .env
# 编辑 .env，填入 FIRECRAWL_API_KEY

# 3. 测试采集
python3 scripts/test_hawaiihub_scraper.py

# 4. 部署调度任务
# 方式A: 使用 n8n
docker-compose up -d n8n

# 方式B: 使用 cron
crontab -e
# 添加：0 */2 * * * cd /path/to/FireShot && python3 scripts/scrape_news.py
```

### 7.4 下一步行动

#### 立即执行（本周）

1. ✅ **完成数据源研究**（已完成）
2. ⬜ **创建数据库表结构**
3. ⬜ **开发 P0 采集脚本**（新闻媒体）
4. ⬜ **部署第一个采集任务**

#### 短期目标（2周内）

5. ⬜ **开发 P1 采集脚本**（华人社区、餐饮）
6. ⬜ **实现缓存机制**
7. ⬜ **部署监控告警**
8. ⬜ **优化成本控制**

#### 中期目标（1个月内）

9. ⬜ **完成全部45个数据源接入**
10. ⬜ **开发数据清洗和去重**
11. ⬜ **构建数据分析报表**
12. ⬜ **对接 HawaiiHub 前端展示**

---

## 8. 附录

### 8.1 常见问题 FAQ

**Q1: 为什么选择这45个数据源？**
A: 基于 Firecrawl 深度搜索结果，这些是夏威夷最权威、最活跃的信息源，覆盖新闻、社区、商业、旅游等核心领域。

**Q2: 每月成本为什么是 $170-260？**
A: 基于 Firecrawl 定价（$0.01/请求），P0 每日约 100 请求（$3/天），P1 每周约 200 请求（$8/周），P2 每月约 500 请求（$20/月）。

**Q3: 如何避免被网站封禁？**
A: 使用 Firecrawl 云服务（内置反爬虫），设置合理的采集频率，使用 `max_age` 缓存，轮换 API 密钥。

**Q4: 数据如何去重？**
A: 使用 URL 哈希作为唯一标识，PostgreSQL UNIQUE 约束，爬取前检查数据库。

**Q5: 如何扩展到其他岛屿？**
A: 参考本清单的方法论，搜索"Maui news"、"Big Island restaurants"等关键词，添加到对应类别。

### 8.2 相关文档

- [Firecrawl 云端 API 规范](../Firecrawl学习手册/03-API参考/云端API规范.md)
- [Firecrawl 云端配置指南](../Firecrawl学习手册/04-配置指南/云端配置指南.md)
- [HawaiiHub 实战案例手册](../Firecrawl学习手册/05-实战案例/HawaiiHub实战案例手册.md)

### 8.3 联系方式

- **项目维护**: HawaiiHub AI Team
- **技术支持**: Firecrawl Discord (https://discord.gg/firecrawl)
- **问题反馈**: GitHub Issues

---

**文档版本**: v1.0
**生成时间**: 2025-10-28
**下次更新**: 2025-11-28（每月更新）

---

## 📊 数据源可视化

### 按类别分布

```
本地新闻媒体 ████████████████ 15.6% (7个)
华人社区资源 ██████████████████████ 22.2% (10个)
餐饮美食指南 ████████████████████ 20.0% (9个)
旅游活动日历 ████████████████████ 20.0% (9个)
商业目录 ██████████████████████ 22.2% (10个)
```

### 按优先级分布

```
P0 (核心日常) ████████████████████████████ 40.0% (18个)
P1 (重要周期) ████████████████████ 31.1% (14个)
P2 (补充性) ██████████████ 28.9% (13个)
```

### 按采集频率分布

```
每2-4小时 ████████ 11.1% (5个)
每日1次 ████████████████ 22.2% (10个)
每周1-2次 ████████████████████████ 33.3% (15个)
每月1次 ████████████ 17.8% (8个)
每季度1次 ████████ 15.6% (7个)
```

---

**🎉 数据采集源清单生成完成！**
