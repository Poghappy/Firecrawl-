# HawaiiHub 数据采集快速上手指南

> **生成时间**: 2025-10-28
> **版本**: v1.0
> **前置文档**: [HAWAIIHUB_DATA_SOURCES_CATALOG.md](HAWAIIHUB_DATA_SOURCES_CATALOG.md)

---

## 🚀 快速开始（5分钟）

### 1. 检查环境

```bash
# 确认 Python 版本 >= 3.11
python3 --version

# 确认已安装 Firecrawl SDK
python3 -c "import firecrawl; print('Firecrawl SDK 已安装')"
```

### 2. 配置 API 密钥

```bash
# 编辑 .env 文件
nano .env

# 添加以下内容（替换为你的真实密钥）
FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxx
```

### 3. 测试采集

```bash
# 进入项目目录
cd /Users/zhiledeng/Downloads/FireShot

# 列出所有可用数据源
python3 scripts/hawaiihub_scraper.py --list

# 采集单个新闻源（测试）
python3 scripts/hawaiihub_scraper.py --source "Hawaii News Now"
```

### 4. 查看结果

```bash
# 查看 JSON 结果
ls -lh data/hawaiihub/*.json

# 查看 Markdown 结果
cat data/hawaiihub/single_source_news_*.md

# 查看日志
tail -f logs/hawaiihub_scraper.log
```

---

## 📖 使用示例

### 示例1: 采集所有新闻源

```bash
python3 scripts/hawaiihub_scraper.py --category news
```

**输出**:

```
开始采集: Hawaii News Now (https://www.hawaiinewsnow.com/)
采集成功: Hawaii News Now | 请求 #1 | 成本: $0.01
开始采集: Honolulu Civil Beat (https://www.civilbeat.org/)
采集成功: Honolulu Civil Beat | 请求 #2 | 成本: $0.02
...

📊 采集统计
============================================================
总请求数: 4
成功数: 4
失败数: 0
成功率: 100.0%
总成本: $0.04
============================================================
```

**生成文件**:

- `data/hawaiihub/category_news_20251028_191234.json` - JSON 格式
- `data/hawaiihub/category_news_news_20251028_191234.md` - Markdown 格式

### 示例2: 采集华人社区资源

```bash
python3 scripts/hawaiihub_scraper.py --category chinese_community
```

**用途**: 获取华人社区最新活动、新闻、商业信息

### 示例3: 采集 P0 优先级数据（核心日常）

```bash
python3 scripts/hawaiihub_scraper.py --priority P0
```

**用途**: 执行每日核心采集任务（新闻 + 华人社区 + 餐饮）

### 示例4: 采集所有数据源（谨慎使用）

```bash
python3 scripts/hawaiihub_scraper.py --all
```

**警告**:

- 将采集所有 45 个数据源
- 预计耗时: 5-10 分钟
- 预计成本: $0.45（45个请求 × $0.01）

### 示例5: 采集单个特定数据源

```bash
# 采集夏威夷中国日报
python3 scripts/hawaiihub_scraper.py --source "夏威夷中国日报"

# 采集 Yelp 餐厅信息
python3 scripts/hawaiihub_scraper.py --source "Yelp Honolulu Hawaiian"
```

---

## 📂 数据文件结构

采集完成后，数据保存在 `data/hawaiihub/` 目录：

```
data/hawaiihub/
├── category_news_20251028_191234.json          # JSON 格式（程序处理）
├── category_news_news_20251028_191234.md       # Markdown 格式（人类阅读）
├── priority_P0_20251028_192000.json
├── priority_P0_news_20251028_192000.md
├── priority_P0_chinese_community_20251028_192000.md
└── all_sources_20251028_193000.json
```

### JSON 数据格式

```json
[
  {
    "source_name": "Hawaii News Now",
    "source_url": "https://www.hawaiinewsnow.com/",
    "category": "news",
    "priority": "P0",
    "content": "# Hawaii News Now\n\n## Breaking News...",
    "metadata": {
      "title": "Hawaii News Now - Breaking News",
      "description": "..."
    },
    "scraped_at": "2025-10-28T19:12:34.567890"
  }
]
```

### Markdown 数据格式

```markdown
# NEWS 采集结果

> 采集时间: 2025-10-28 19:12:34
> 数据源数量: 4

---

## Hawaii News Now

- **URL**: https://www.hawaiinewsnow.com/
- **优先级**: P0
- **采集时间**: 2025-10-28T19:12:34.567890

### 内容

# Hawaii News Now

Breaking news from Hawaii...

---
```

---

## ⏰ 定时采集（生产环境）

### 方式1: 使用 cron（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加以下任务
# 每2小时采集 P0 新闻
0 */2 * * * cd /Users/zhiledeng/Downloads/FireShot && python3 scripts/hawaiihub_scraper.py --category news >> logs/cron.log 2>&1

# 每6小时采集华人社区
0 */6 * * * cd /Users/zhiledeng/Downloads/FireShot && python3 scripts/hawaiihub_scraper.py --category chinese_community >> logs/cron.log 2>&1

# 每天早上10点采集餐厅信息
0 10 * * * cd /Users/zhiledeng/Downloads/FireShot && python3 scripts/hawaiihub_scraper.py --category restaurant >> logs/cron.log 2>&1

# 每周一早上8点采集活动日历
0 8 * * 1 cd /Users/zhiledeng/Downloads/FireShot && python3 scripts/hawaiihub_scraper.py --category events >> logs/cron.log 2>&1

# 每月1号凌晨2点采集商业目录
0 2 1 * * cd /Users/zhiledeng/Downloads/FireShot && python3 scripts/hawaiihub_scraper.py --category business >> logs/cron.log 2>&1
```

### 方式2: 使用 launchd（macOS 推荐）

创建 `~/Library/LaunchAgents/com.hawaiihub.scraper.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hawaiihub.scraper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/zhiledeng/Downloads/FireShot/scripts/hawaiihub_scraper.py</string>
        <string>--priority</string>
        <string>P0</string>
    </array>
    <key>StartInterval</key>
    <integer>7200</integer> <!-- 每2小时 -->
    <key>StandardOutPath</key>
    <string>/Users/zhiledeng/Downloads/FireShot/logs/scraper.out.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/zhiledeng/Downloads/FireShot/logs/scraper.err.log</string>
</dict>
</plist>
```

加载任务:

```bash
launchctl load ~/Library/LaunchAgents/com.hawaiihub.scraper.plist
launchctl list | grep hawaiihub
```

---

## 🔧 高级配置

### 自定义数据源

编辑 `scripts/hawaiihub_scraper.py`，添加新的数据源：

```python
CUSTOM_SOURCES = [
    {
        "name": "你的数据源名称",
        "url": "https://example.com",
        "category": "custom",
        "priority": "P1",
        "frequency": "0 12 * * *",  # 每天中午12点
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 86400000  # 24小时缓存
        }
    }
]

# 添加到 ALL_SOURCES
ALL_SOURCES = (
    NEWS_SOURCES +
    CHINESE_COMMUNITY_SOURCES +
    RESTAURANT_SOURCES +
    EVENT_SOURCES +
    BUSINESS_SOURCES +
    CUSTOM_SOURCES  # 新增
)
```

### 成本控制

```python
# 在 HawaiiHubScraper.__init__ 中添加预算限制
def __init__(self, api_key: Optional[str] = None, daily_budget: float = 10.0):
    self.daily_budget = daily_budget

    # 在 scrape_source 中检查预算
    if self.total_cost >= self.daily_budget:
        raise BudgetExceededError(f"超出每日预算: ${self.daily_budget}")
```

### 错误重试

```python
def scrape_source_with_retry(self, source: Dict, max_retries: int = 3) -> Optional[Dict]:
    """带重试的采集"""
    for attempt in range(max_retries):
        try:
            return self.scrape_source(source)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"重试 {attempt+1}/{max_retries}，等待 {wait_time}秒...")
                time.sleep(wait_time)
            else:
                logger.error(f"失败（{max_retries}次重试后）: {e}")
                return None
```

---

## 📊 数据处理流程

### 1. 采集 → 2. 清洗 → 3. 存储 → 4. 分析

```bash
# 1. 采集原始数据
python3 scripts/hawaiihub_scraper.py --category news

# 2. 清洗数据（TODO: 创建清洗脚本）
python3 scripts/clean_scraped_data.py data/hawaiihub/category_news_*.json

# 3. 导入数据库（TODO: 创建导入脚本）
python3 scripts/import_to_database.py data/hawaiihub/cleaned_*.json

# 4. 生成分析报告（TODO: 创建分析脚本）
python3 scripts/analyze_data.py --category news --date-range 7days
```

---

## 🛠️ 故障排查

### 问题1: 速率限制错误

```
Error: Rate limit exceeded. Consumed (req/min): 6, Remaining (req/min): 0
```

**解决方案**:

- 等待1分钟后重试
- 在脚本中增加 `time.sleep(2)` 延迟
- 使用多个 API 密钥轮换

### 问题2: API 密钥无效

```
Error: 未找到 FIRECRAWL_API_KEY，请设置环境变量
```

**解决方案**:

```bash
# 检查 .env 文件
cat .env | grep FIRECRAWL_API_KEY

# 手动设置环境变量
export FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxx

# 测试 API 密钥
python3 test_api_keys.py
```

### 问题3: 采集超时

```
Error: Request timeout after 60 seconds
```

**解决方案**:

- 检查网络连接
- 增加超时时间（在 scrape_config 中添加 `timeout: 120`）
- 使用 `max_age` 参数利用缓存

### 问题4: 内容为空

```
Warning: 采集结果为空
```

**解决方案**:

- 检查目标网站是否可访问
- 尝试移除 `only_main_content: True`
- 查看网站是否需要登录或有反爬虫机制

---

## 📈 监控与告警

### 实时监控

```bash
# 监控日志
tail -f logs/hawaiihub_scraper.log

# 统计成功率
grep "采集成功" logs/hawaiihub_scraper.log | wc -l
grep "采集失败" logs/hawaiihub_scraper.log | wc -l

# 查看成本
grep "总成本" logs/hawaiihub_scraper.log | tail -1
```

### 成本跟踪

创建 `scripts/cost_tracker.sh`:

```bash
#!/bin/bash

# 统计每日成本
LOG_FILE="logs/hawaiihub_scraper.log"
TODAY=$(date +%Y-%m-%d)

echo "📊 每日成本统计 - $TODAY"
echo "================================"

# 提取今日的成本记录
grep "$TODAY" "$LOG_FILE" | grep "总成本" | tail -1

# 提取请求数
REQUEST_COUNT=$(grep "$TODAY" "$LOG_FILE" | grep "请求" | wc -l)
echo "总请求数: $REQUEST_COUNT"

# 预估成本
ESTIMATED_COST=$(echo "$REQUEST_COUNT * 0.01" | bc)
echo "预估成本: \$$ESTIMATED_COST"
```

---

## 🎯 最佳实践

### 1. 分阶段采集（推荐）

```bash
# 第一周：只采集 P0 数据源
python3 scripts/hawaiihub_scraper.py --priority P0

# 第二周：增加 P1 数据源
python3 scripts/hawaiihub_scraper.py --priority P1

# 第三周：全量采集
python3 scripts/hawaiihub_scraper.py --all
```

### 2. 使用缓存节省成本

```python
# 利用 Firecrawl 的缓存机制
scrape_config = {
    "formats": ["markdown"],
    "only_main_content": True,
    "max_age": 172800000  # 2天缓存，节省 50%+ 成本
}
```

### 3. 批量采集

```python
# 使用 batch_scrape（更高效）
urls = [source["url"] for source in NEWS_SOURCES]
results = app.batch_scrape(urls=urls, formats=["markdown"])
```

### 4. 增量更新

```python
# 只爬取新内容
def scrape_incremental(category: str, since: datetime):
    """增量采集（只获取指定时间后的新内容）"""
    # 实现逻辑...
```

---

## 📚 相关文档

- [HAWAIIHUB_DATA_SOURCES_CATALOG.md](HAWAIIHUB_DATA_SOURCES_CATALOG.md) - 完整数据源清单
- [Firecrawl 云端 API 规范](../Firecrawl学习手册/03-API参考/云端API规范.md)
- [Firecrawl 云端配置指南](../Firecrawl学习手册/04-配置指南/云端配置指南.md)

---

## 🆘 获取帮助

### 常见问题

- **Q: 如何添加新的数据源？**
  A: 编辑 `scripts/hawaiihub_scraper.py`，在对应的 `*_SOURCES` 列表中添加配置

- **Q: 如何修改采集频率？**
  A: 修改 crontab 或 launchd 配置文件中的时间表达式

- **Q: 如何查看历史采集记录？**
  A: 查看 `data/hawaiihub/` 目录下的 JSON 和 Markdown 文件

- **Q: 如何导出数据到数据库？**
  A: 参考 [数据处理流程](#数据处理流程) 章节（需要额外开发）

### 联系方式

- **项目维护**: HawaiiHub AI Team
- **技术支持**: Firecrawl Discord (https://discord.gg/firecrawl)
- **问题反馈**: GitHub Issues

---

**文档版本**: v1.0
**最后更新**: 2025-10-28
**维护者**: HawaiiHub AI Team
