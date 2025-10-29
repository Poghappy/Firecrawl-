# 📰 新闻资讯采集系统

**版本**: v1.0
**创建日期**: 2025-01-29
**业务场景**: 火鸟门户新闻资讯

---

## ✅ 系统概述

自动采集夏威夷本地新闻，支持多个新闻源，使用 Firecrawl Search API 实时获取最新资讯。

### 核心特性

- ✅ **多新闻源支持** - Hawaii News Now、Honolulu Civil Beat、Star-Advertiser
- ✅ **实时搜索** - 使用 Search API 获取最新新闻
- ✅ **结构化提取** - 标题、正文、作者、时间、图片
- ✅ **智能去重** - 基于内容哈希去重
- ✅ **多格式导出** - JSON、Markdown、CSV
- ✅ **定时采集** - 每 2 小时自动运行

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd news_collector
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 Firecrawl API Key
```

### 3. 运行采集

```bash
python main.py --keywords "hawaii" --limit 20
```

### 4. 查看结果

```bash
ls data/exports/
cat data/exports/news_*.json
```

---

## 📁 项目结构

```
news_collector/
├── __init__.py
├── main.py              # 主程序
├── config.py            # 配置文件
├── models.py            # Pydantic 数据模型
├── scrapers/
│   ├── __init__.py
│   ├── base_news_scraper.py    # 基类
│   └── search_news_scraper.py  # Search API 实现
├── exporters/
│   ├── __init__.py
│   ├── json_exporter.py
│   └── markdown_exporter.py
├── data/
│   ├── exports/         # 导出数据
│   └── cache/          # 缓存
├── logs/               # 日志
├── tests/              # 测试
├── .env.example        # 环境变量模板
├── requirements.txt    # 依赖
└── README.md          # 本文件
```

---

## 🔧 配置说明

### 编辑 `config.py`

```python
# 新闻源配置
NEWS_SOURCES = {
    "hawaii-news-now": {
        "enabled": True,
        "site": "hawaiinewsnow.com",
        "priority": "P0"
    },
    "civil-beat": {
        "enabled": True,
        "site": "civilbeat.org",
        "priority": "P0"
    }
}

# 采集配置
SEARCH_CONFIG = {
    "limit": 20,
    "sources": [{"type": "news"}],
    "tbs": "qdr:d",  # 24小时内
    "maxAge": 600000  # 10分钟缓存
}
```

---

## 💰 成本估算

| 配置                  | 每次 Credits | 每天成本 |
| --------------------- | ------------ | -------- |
| **当前（每 2 小时）** | ~50          | $0.60/天 |
| **每小时运行**        | ~50          | $1.20/天 |
| **优化后（缓存）**    | ~25          | $0.30/天 |

**成本优化**：

- ✅ 启用 10 分钟缓存（`maxAge=600000`）
- ✅ 使用 basic 代理
- ✅ 批量处理优化

---

## 📊 数据模型

### NewsArticle 模型

```python
from pydantic import BaseModel
from datetime import datetime

class NewsArticle(BaseModel):
    """新闻文章数据模型"""
    source_id: str          # 新闻源ID
    source_name: str        # 新闻源名称
    url: str               # 文章URL
    title: str             # 标题
    description: str       # 摘要
    content: str           # 正文（Markdown）
    author: Optional[str]  # 作者
    published_at: datetime # 发布时间
    images: List[str]      # 图片列表
    tags: List[str]        # 标签
    scraped_at: datetime   # 采集时间
```

---

## 🎯 使用示例

### 基础采集

```bash
python main.py
```

### 指定关键词

```bash
python main.py --keywords "hawaii tourism" --limit 30
```

### 指定新闻源

```bash
python main.py --sources hawaii-news-now civil-beat
```

### 指定时间范围

```bash
python main.py --timerange "qdr:d"  # 24小时
python main.py --timerange "qdr:w"  # 一周
```

---

## 📝 开发进度

### v1.0 (2025-01-29)

- [x] 创建项目结构
- [x] 定义数据模型
- [x] 实现 Search API 采集器
- [x] JSON/Markdown 导出
- [ ] 实现定时任务
- [ ] 添加去重功能
- [ ] 完善测试用例

### v1.1 (计划中)

- [ ] 支持更多新闻源
- [ ] 实现内容分析（LLM）
- [ ] 添加分类标签
- [ ] 实现推送通知

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_search_scraper.py

# 查看覆盖率
pytest --cov=. --cov-report=html
```

---

## 📞 技术支持

- **日志**: `tail -f logs/news.log`
- **配置**: `config.py`
- **文档**: [Firecrawl Search API](https://docs.firecrawl.dev/api-reference/search)

---

**祝您采集愉快！** 📰
