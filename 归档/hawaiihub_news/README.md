# HawaiiHub 新闻采集系统

**版本**: v1.0.0
**创建时间**: 2025-10-28
**维护者**: HawaiiHub AI Team

---

## 🎯 项目简介

HawaiiHub 新闻采集系统是一个专为 HawaiiHub 平台设计的生产级新闻采集工具，基于 Firecrawl Python SDK 构建，支持采集夏威夷本地新闻和华人社区资讯。

### 核心特性

- ✅ **多新闻源支持**: 预配置 7 个夏威夷本地新闻源和多个华人社区资源
- ✅ **智能采集**: 自动识别文章链接，批量采集优化性能
- ✅ **错误处理**: 完善的重试机制和错误恢复
- ✅ **成本控制**: 内置预算管理和请求计数
- ✅ **多格式导出**: 支持 JSON、Markdown、CSV 三种格式
- ✅ **缓存优化**: 利用 Firecrawl 缓存节省 50%+ 成本
- ✅ **日志完善**: 详细的运行日志和统计信息

---

## 📋 目录

- [📚 新增文档](#新增文档)
- [快速开始](#快速开始)
- [安装配置](#安装配置)
- [使用指南](#使用指南)
- [配置说明](#配置说明)
- [API 文档](#api-文档)
- [常见问题](#常见问题)

---

## 📚 新增文档

### 🔥 火鸟门户系统 JSON 格式学习资料

**完成时间**: 2025-10-28

为帮助团队成员快速掌握火鸟门户系统的新闻 JSON 格式，我们创建了以下学习资料：

#### 1. [火鸟新闻 JSON 格式规范](./火鸟新闻JSON格式规范.md) ⭐⭐⭐⭐⭐

**📖 完整规范文档（30+ 页）**

涵盖内容：
- ✅ 4 种核心 JSON 格式详解（火鸟 API、NewsAPI、HawaiiHub、Firecrawl）
- ✅ 完整的字段说明和约束规则
- ✅ 格式转换映射关系
- ✅ 6 个完整示例（从采集到发布）
- ✅ 8 个最佳实践
- ✅ 数据验证、关键词提取、内容清洗代码

**适合**：深入学习、技术参考、新成员培训

---

#### 2. [火鸟 JSON 格式代码示例](./firebird_json_examples.py) ⭐⭐⭐⭐⭐

**💻 可运行的 Python 示例（400+ 行）**

功能包括：
- ✅ Pydantic 数据模型定义
- ✅ 3 种格式的完整示例
- ✅ 格式转换函数（NewsAPI → HawaiiHub → 火鸟 API）
- ✅ 数据验证工具
- ✅ 关键词提取算法
- ✅ 内容清洗工具
- ✅ 完整工作流演示

**运行方式**：
```bash
cd /Users/zhiledeng/Downloads/FireShot/hawaiihub_news
python3 firebird_json_examples.py
```

**适合**：实战练习、代码参考、快速验证

---

#### 3. [火鸟 JSON 格式快速参考卡](./火鸟JSON格式快速参考.md) ⭐⭐⭐⭐⭐

**⚡ 速查手册（5 秒找到你需要的）**

特色：
- ✅ 4 种格式速查表
- ✅ 字段约束一览
- ✅ 常用代码片段（复制即用）
- ✅ 完整工作流模板
- ✅ 快速决策树
- ✅ 常见问题解答

**适合**：日常查阅、快速编码、问题排查

**打印提示**: 建议打印此文档贴在显示器旁边，随时查阅 📄✨

---

### 🎓 学习路径推荐

#### 新手（第 1 天）
1. 阅读 [快速参考卡](./火鸟JSON格式快速参考.md)（10 分钟）
2. 运行 [代码示例](./firebird_json_examples.py)（5 分钟）
3. 查看输出结果，理解数据流转

#### 进阶（第 2-3 天）
1. 深入阅读 [完整规范](./火鸟新闻JSON格式规范.md)（1 小时）
2. 修改代码示例，尝试不同场景
3. 集成到实际项目中

#### 专家（第 4-7 天）
1. 掌握所有格式转换
2. 编写自定义验证规则
3. 优化关键词提取算法
4. 实现完整的采集-发布流程

---

### 📊 文档对比

| 文档 | 篇幅 | 深度 | 适用场景 |
|------|------|------|----------|
| **完整规范** | 30+ 页 | ⭐⭐⭐⭐⭐ | 深入学习、技术参考 |
| **代码示例** | 400+ 行 | ⭐⭐⭐⭐ | 实战练习、代码参考 |
| **快速参考** | 5 页 | ⭐⭐⭐ | 日常查阅、快速编码 |

---

### 💡 使用建议

1. **首次学习**：完整规范 → 代码示例 → 快速参考
2. **日常开发**：快速参考（查格式）→ 代码示例（复制代码）
3. **问题排查**：快速参考（常见问题）→ 完整规范（深入原理）

---

### 🎯 学习检查清单

#### 基础知识 ✅
- [ ] 理解火鸟 API 的 5 个核心字段
- [ ] 理解 NewsAPI 的数据格式
- [ ] 理解 Firecrawl 的返回格式
- [ ] 理解 HawaiiHub 的内部格式

#### 格式转换 ✅
- [ ] 掌握 NewsAPI → Firecrawl 转换
- [ ] 掌握 Firecrawl → HawaiiHub 转换
- [ ] 掌握 HawaiiHub → 火鸟 API 转换
- [ ] 理解字段映射关系

#### 实战技能 ✅
- [ ] 使用 Pydantic 验证数据
- [ ] 实现 Markdown → HTML 转换
- [ ] 实现关键词自动提取
- [ ] 实现内容清洗
- [ ] 编写完整的采集-发布流程

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install firecrawl-py python-dotenv
```

### 2. 配置环境变量

确保项目根目录的 `.env` 文件包含 Firecrawl API 密钥：

```bash
FIRECRAWL_API_KEY=fc-YOUR-API-KEY
```

### 3. 运行采集

```bash
# 采集所有 P0 优先级新闻源（默认）
python main.py

# 采集所有新闻源
python main.py --all

# 采集单个新闻源
python main.py --source hawaii-news-now

# 列出所有可用新闻源
python main.py --list
```

### 4. 查看结果

采集结果保存在 `data/processed/` 目录：

```
data/processed/
├── hawaiihub_news_20251028_120000.json      # JSON 格式
├── hawaiihub_news_20251028_120000.md        # Markdown 格式
└── hawaiihub_news_20251028_120000.csv       # CSV 格式
```

---

## 📦 安装配置

### 系统要求

- Python 3.11+
- firecrawl-py 4.5.0+
- python-dotenv

### 项目结构

```
hawaiihub_news/
├── __init__.py          # 包初始化
├── config.py            # 配置文件（新闻源、策略等）
├── scraper.py           # 核心采集器
├── storage.py           # 数据存储和导出
├── main.py              # 主程序入口
├── README.md            # 使用文档（本文件）
├── data/                # 数据目录
│   ├── raw/            # 原始数据
│   ├── processed/      # 处理后数据
│   └── cache/          # 缓存数据
└── logs/                # 日志目录
    ├── hawaiihub_news.log  # 主日志
    └── errors.log          # 错误日志
```

### 环境变量配置

创建 `.env` 文件（如果还没有）：

```bash
# API 密钥
FIRECRAWL_API_KEY=fc-YOUR-API-KEY
FIRECRAWL_API_KEY_BACKUP_1=fc-BACKUP-KEY-1
FIRECRAWL_API_KEY_BACKUP_2=fc-BACKUP-KEY-2
FIRECRAWL_API_KEY_BACKUP_3=fc-BACKUP-KEY-3

# 成本控制
FIRECRAWL_DAILY_BUDGET=10.0
FIRECRAWL_MONTHLY_BUDGET=200.0

# 其他配置
FIRECRAWL_TIMEOUT=60
FIRECRAWL_MAX_RETRIES=3
```

---

## 📖 使用指南

### 命令行参数

```bash
python main.py [options]

选项:
  --all                采集所有新闻源
  --priority P0        按优先级采集 (P0/P1/P2)
  --source ID          采集单个新闻源（使用 ID）
  --list               列出所有新闻源
  --budget AMOUNT      设置每日预算（美元）
  --debug              启用调试模式
```

### 使用示例

#### 1. 列出所有新闻源

```bash
python main.py --list
```

输出：
```
==================================================
  📋 可用新闻源列表
==================================================

1. ✅ [P0] Hawaii News Now
   ID: hawaii-news-now
   URL: https://www.hawaiinewsnow.com/
   评分: ⭐⭐⭐⭐⭐
   频率: 每 2 小时

2. ✅ [P0] Honolulu Civil Beat
   ID: civil-beat
   URL: https://www.civilbeat.org/
   评分: ⭐⭐⭐⭐⭐
   频率: 每 6 小时

...
```

#### 2. 采集所有新闻源

```bash
python main.py --all
```

#### 3. 按优先级采集

```bash
# 只采集 P0 优先级新闻源
python main.py --priority P0
```

#### 4. 采集单个新闻源

```bash
python main.py --source hawaii-news-now
```

#### 5. 设置预算

```bash
# 设置每日预算为 $5
python main.py --all --budget 5.0
```

### 编程接口

#### 基本使用

```python
from hawaiihub_news import HawaiiHubNewsScraper, NewsStorage

# 初始化
scraper = HawaiiHubNewsScraper(daily_budget=10.0)
storage = NewsStorage()

# 采集所有新闻源
results = scraper.scrape_all_sources()

# 导出结果
exported = storage.export_news_results(results)

# 查看统计
stats = scraper.get_stats()
print(f"成功率: {stats['success_rate']*100:.1f}%")
print(f"总成本: ${stats['total_cost']:.2f}")
```

#### 采集单个新闻源

```python
from hawaiihub_news import HawaiiHubNewsScraper, get_source_by_id

scraper = HawaiiHubNewsScraper()

# 获取新闻源配置
source_config = get_source_by_id("hawaii-news-now")

# 采集
result = scraper.scrape_news_source(source_config)

print(f"采集了 {len(result['articles'])} 篇文章")
```

#### 批量采集 URL

```python
from hawaiihub_news import HawaiiHubNewsScraper

scraper = HawaiiHubNewsScraper()

urls = [
    "https://www.hawaiinewsnow.com/article1",
    "https://www.hawaiinewsnow.com/article2",
    "https://www.hawaiinewsnow.com/article3",
]

results = scraper.batch_scrape_urls(urls)
print(f"成功采集 {len(results)} 篇文章")
```

---

## ⚙️ 配置说明

### 新闻源配置

在 `config.py` 中定义新闻源：

```python
{
    "id": "hawaii-news-now",
    "name": "Hawaii News Now",
    "url": "https://www.hawaiinewsnow.com/",
    "priority": "P0",
    "rating": 5,
    "scrape_config": {
        "formats": ["markdown"],
        "only_main_content": True,
        "max_age": 7200000,  # 2小时缓存
    },
    "crawl_config": {
        "limit": 20,
        "include_paths": ["/news/*"],
        "max_discovery_depth": 2,
    },
    "frequency_hours": 2,
    "enabled": True,
}
```

### 采集策略配置

```python
SCRAPE_STRATEGY = {
    "max_retries": 3,
    "retry_delay_base": 2,
    "scrape_timeout": 60,
    "batch_size": 5,
    "max_concurrency": 3,
}
```

### 数据处理配置

```python
DATA_PROCESSING = {
    "min_content_length": 100,
    "max_content_length": 100000,
    "enable_deduplication": True,
    "dedup_field": "url",
}
```

---

## 📊 API 文档

### HawaiiHubNewsScraper

核心采集器类。

#### 方法

##### `scrape_url(url, config=None, max_retries=None)`

采集单个 URL。

**参数**:
- `url` (str): 要采集的 URL
- `config` (dict, 可选): Scrape 配置
- `max_retries` (int, 可选): 最大重试次数

**返回**: `Dict` - 采集结果

##### `batch_scrape_urls(urls, config=None)`

批量采集 URL 列表。

**参数**:
- `urls` (List[str]): URL 列表
- `config` (dict, 可选): Scrape 配置

**返回**: `List[Dict]` - 采集结果列表

##### `scrape_news_source(source_config)`

采集单个新闻源。

**参数**:
- `source_config` (dict): 新闻源配置

**返回**: `Dict` - 采集结果

##### `scrape_all_sources(sources=None)`

采集所有新闻源。

**参数**:
- `sources` (List[Dict], 可选): 新闻源列表

**返回**: `List[Dict]` - 所有采集结果

##### `get_stats()`

获取统计信息。

**返回**: `Dict` - 统计信息（请求数、成功率、成本等）

### NewsStorage

数据存储管理器。

#### 方法

##### `export_to_json(data, filename)`

导出为 JSON 文件。

##### `export_to_markdown(data, filename)`

导出为 Markdown 文件。

##### `export_to_csv(data, filename)`

导出为 CSV 文件。

##### `export_news_results(results, prefix="news")`

导出新闻采集结果到多种格式。

---

## 💡 最佳实践

### 1. 成本控制

```python
# 设置每日预算
scraper = HawaiiHubNewsScraper(daily_budget=5.0)

# 采集会在达到预算时自动停止
results = scraper.scrape_all_sources()

# 检查剩余预算
stats = scraper.get_stats()
print(f"剩余预算: ${stats['remaining_budget']:.2f}")
```

### 2. 缓存优化

```python
# 使用 2 小时缓存（配置在新闻源中）
source_config = {
    "scrape_config": {
        "max_age": 7200000  # 2小时
    }
}

# 第二次采集相同 URL 会命中缓存，不计费
```

### 3. 批量处理

```python
# ✅ 推荐：使用批量采集
results = scraper.batch_scrape_urls(urls)

# ❌ 避免：逐个采集
for url in urls:
    result = scraper.scrape_url(url)  # 慢且贵
```

### 4. 错误处理

```python
try:
    results = scraper.scrape_all_sources()
except Exception as e:
    logger.error(f"采集失败: {e}")
    # 查看详细日志
    # tail -f logs/errors.log
```

---

## ❓ 常见问题

### Q1: 采集速度很慢？

**A**: 这是正常的。Firecrawl 需要渲染 JavaScript 和等待页面加载。优化方案：
- 使用缓存 (`max_age`)
- 批量处理 (`batch_scrape_urls`)
- 限制采集数量 (`limit`)

### Q2: 如何节省成本？

**A**: 3 个关键策略：
1. **缓存**: 设置 `max_age=7200000`（2小时）
2. **主要内容**: `only_main_content=True`
3. **批量处理**: 用 `batch_scrape` 代替多次 `scrape`

### Q3: 如何添加新的新闻源？

**A**: 在 `config.py` 中添加新闻源配置：

```python
NEW_SOURCE = {
    "id": "new-source-id",
    "name": "New Source Name",
    "url": "https://newsource.com/",
    "priority": "P0",
    "rating": 4,
    "scrape_config": {
        "formats": ["markdown"],
        "only_main_content": True,
    },
    "frequency_hours": 6,
    "enabled": True,
}

# 添加到列表
NEWS_SOURCES_P0.append(NEW_SOURCE)
```

### Q4: 如何查看日志？

**A**:
```bash
# 查看主日志
tail -f logs/hawaiihub_news.log

# 查看错误日志
tail -f logs/errors.log
```

### Q5: 如何定时运行？

**A**: 使用 cron（Linux/Mac）或 Task Scheduler（Windows）：

```bash
# crontab -e
# 每 2 小时运行一次
0 */2 * * * cd /path/to/FireShot/hawaiihub_news && python main.py --priority P0
```

---

## 📚 相关资源

- **Firecrawl SDK 学习指南**: `../Firecrawl学习手册/03-API参考/08-Python-SDK完整指南.md`
- **数据源清单**: `../docs/HAWAIIHUB_DATA_SOURCES_CATALOG.md`
- **快速参考**: `../QUICK_START_SDK.md`

---

## 🤝 贡献

欢迎提交问题和改进建议！

---

## 📄 许可证

MIT License

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28
