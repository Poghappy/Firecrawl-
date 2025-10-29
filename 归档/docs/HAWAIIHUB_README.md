# HawaiiHub 数据采集系统文档

> **生成时间**: 2025-10-28
> **维护者**: HawaiiHub AI Team
> **状态**: ✅ 研究完成，可进入实施阶段

---

## 🎯 快速导航

### 📋 核心文档（按阅读顺序）

| 序号 | 文档名称                                            | 用途                   | 阅读时间 |
| ---- | --------------------------------------------------- | ---------------------- | -------- |
| 1️⃣   | [**研究完成报告**](HAWAIIHUB_RESEARCH_COMPLETE.md)  | 了解项目概况和成果     | 5 分钟   |
| 2️⃣   | [**数据源清单**](HAWAIIHUB_DATA_SOURCES_CATALOG.md) | 查看完整的 45 个数据源 | 15 分钟  |
| 3️⃣   | [**快速上手指南**](HAWAIIHUB_SCRAPER_QUICKSTART.md) | 学习如何使用采集工具   | 10 分钟  |

---

## 🚀 5分钟快速开始

### 第1步：查看数据源列表

```bash
cd /Users/zhiledeng/Downloads/FireShot
python3 scripts/hawaiihub_scraper.py --list
```

### 第2步：测试单个数据源

```bash
python3 scripts/hawaiihub_scraper.py --source "Hawaii News Now"
```

### 第3步：查看采集结果

```bash
# 查看 JSON 数据
cat data/hawaiihub/single_source_*.json

# 查看 Markdown 文档
cat data/hawaiihub/single_source_*.md
```

---

## 📊 数据源统计

### 总览

- **数据源总数**: 45 个
- **类别数**: 5 个（新闻、华人社区、餐饮、旅游、商业）
- **预估月成本**: $170-260
- **预估月数据量**: 2,550-4,800 条

### 按类别分布

```
本地新闻媒体 ████████████████ 15.6% (7个)
华人社区资源 ██████████████████████ 22.2% (10个)
餐饮美食指南 ████████████████████ 20.0% (9个)
旅游活动日历 ████████████████████ 20.0% (9个)
商业目录 ██████████████████████ 22.2% (10个)
```

### 按优先级分布

- **P0 核心日常** (40.0%): 18 个数据源，每日采集
- **P1 重要周期** (31.1%): 14 个数据源，每周采集
- **P2 补充性** (28.9%): 13 个数据源，每月采集

---

## 🎯 核心数据源（Top 10）

| 排名 | 数据源                                                                        | 类别     | 优先级 | 采集频率 |
| ---- | ----------------------------------------------------------------------------- | -------- | ------ | -------- |
| 1    | [Hawaii News Now](https://www.hawaiinewsnow.com/)                             | 新闻     | P0     | 每2小时  |
| 2    | [Honolulu Civil Beat](https://www.civilbeat.org/)                             | 新闻     | P0     | 每6小时  |
| 3    | [Honolulu Star-Advertiser](https://www.staradvertiser.com/)                   | 新闻     | P0     | 每4小时  |
| 4    | [夏威夷中国日报](https://hawaiichinesedaily.com/)                             | 华人社区 | P0     | 每4小时  |
| 5    | [Chinese Chamber of Commerce](https://www.chinesechamber.com/)                | 华人社区 | P0     | 每周2次  |
| 6    | [Yelp Honolulu](https://www.yelp.com/search?cflt=hawaiian&find_loc=Honolulu)  | 餐饮     | P1     | 每天1次  |
| 7    | [OpenTable Hawaii](https://www.opentable.com/metro/hawaii-restaurants)        | 餐饮     | P1     | 每天1次  |
| 8    | [Go Hawaii Official](https://www.gohawaii.com/trip-planning/events-festivals) | 旅游     | P1     | 每周1次  |
| 9    | [Yellow Pages Honolulu](https://www.yellowpages.com/honolulu-hi)              | 商业     | P2     | 每月1次  |
| 10   | [夏威夷华人黄页](https://hawaii.jinbay.com/yellowpages/190/)                  | 商业     | P2     | 每月1次  |

---

## 🛠️ 采集工具使用

### 按类别采集

```bash
# 采集所有新闻
python3 scripts/hawaiihub_scraper.py --category news

# 采集华人社区资源
python3 scripts/hawaiihub_scraper.py --category chinese_community

# 采集餐厅信息
python3 scripts/hawaiihub_scraper.py --category restaurant

# 采集活动日历
python3 scripts/hawaiihub_scraper.py --category events

# 采集商业目录
python3 scripts/hawaiihub_scraper.py --category business
```

### 按优先级采集

```bash
# P0 核心日常采集
python3 scripts/hawaiihub_scraper.py --priority P0

# P1 重要周期采集
python3 scripts/hawaiihub_scraper.py --priority P1

# P2 补充性采集
python3 scripts/hawaiihub_scraper.py --priority P2
```

### 采集单个数据源

```bash
python3 scripts/hawaiihub_scraper.py --source "数据源名称"
```

---

## 📁 文档结构

```
docs/
├── HAWAIIHUB_README.md                    # 本文件（导航）
├── HAWAIIHUB_RESEARCH_COMPLETE.md         # 研究完成报告
├── HAWAIIHUB_DATA_SOURCES_CATALOG.md      # 完整数据源清单（1,200行）
└── HAWAIIHUB_SCRAPER_QUICKSTART.md        # 快速上手指南（500行）

scripts/
└── hawaiihub_scraper.py                   # 数据采集脚本（500行）

data/
└── hawaiihub/                             # 采集数据存储目录
    ├── *.json                             # JSON 格式数据
    └── *.md                               # Markdown 格式文档

logs/
└── hawaiihub_scraper.log                  # 采集日志
```

---

## 💰 成本预估

### 按采集方案

| 方案        | 数据源数 | 请求数/天 | 成本/天  | 成本/月 |
| ----------- | -------- | --------- | -------- | ------- |
| **仅 P0**   | 18       | 100-150   | $1-1.5   | $30-45  |
| **P0 + P1** | 32       | 150-220   | $1.5-2.2 | $45-66  |
| **全量**    | 45       | 250-350   | $2.5-3.5 | $75-105 |

### 成本优化

- ✅ **使用缓存**: 节省 50%+ 成本（`max_age` 参数）
- ✅ **增量更新**: 只爬新内容
- ✅ **密钥轮换**: 突破速率限制
- ✅ **批量采集**: 使用 `batch_scrape`

---

## 🎯 推荐采集策略

### 阶段1: 测试验证（第1周）

```bash
# 只采集 P0 核心数据源（18个）
python3 scripts/hawaiihub_scraper.py --priority P0
```

- **目标**: 验证数据质量和成本
- **频率**: 每天1次
- **成本**: ~$1/天

### 阶段2: 扩展覆盖（第2周）

```bash
# 增加 P1 数据源（32个）
python3 scripts/hawaiihub_scraper.py --priority P0  # 每日
python3 scripts/hawaiihub_scraper.py --priority P1  # 每周
```

- **目标**: 扩大数据覆盖范围
- **频率**: 混合频率
- **成本**: ~$1.5-2/天

### 阶段3: 全量采集（第3周起）

```bash
# 部署完整的定时任务
crontab -e

# 添加 cron 任务（参考快速上手指南）
```

- **目标**: 完整数据采集系统
- **频率**: 自动化定时
- **成本**: ~$2.5-3.5/天

---

## 📚 延伸阅读

### 项目内文档

1. [Firecrawl 学习手册](../Firecrawl学习手册/README.md)
2. [Firecrawl 云端 API 规范](../Firecrawl学习手册/03-API参考/云端API规范.md)
3. [Firecrawl 云端配置指南](../Firecrawl学习手册/04-配置指南/云端配置指南.md)
4. [HawaiiHub 实战案例](../Firecrawl学习手册/05-实战案例/HawaiiHub实战案例手册.md)

### 外部资源

- [Firecrawl 官方文档](https://docs.firecrawl.dev/)
- [Firecrawl GitHub](https://github.com/mendableai/firecrawl)
- [Firecrawl Discord 社区](https://discord.gg/firecrawl)
- [Go Hawaii 官网](https://www.gohawaii.com/)

---

## ❓ 常见问题

### Q1: 如何开始使用？

**A**: 按照以下顺序：

1. 阅读 [研究完成报告](HAWAIIHUB_RESEARCH_COMPLETE.md)（5分钟）
2. 阅读 [快速上手指南](HAWAIIHUB_SCRAPER_QUICKSTART.md)（10分钟）
3. 运行测试命令：`python3 scripts/hawaiihub_scraper.py --list`

### Q2: 每月成本是多少？

**A**: 根据采集方案：

- **仅 P0**: $30-45/月
- **P0 + P1**: $45-66/月
- **全量**: $75-105/月

使用缓存可节省 50%+ 成本。

### Q3: 如何添加新的数据源？

**A**: 编辑 `scripts/hawaiihub_scraper.py`，在对应的 `*_SOURCES` 列表中添加配置。详见快速上手指南。

### Q4: 数据存储在哪里？

**A**:

- JSON 格式：`data/hawaiihub/*.json`
- Markdown 格式：`data/hawaiihub/*.md`
- 日志文件：`logs/hawaiihub_scraper.log`

### Q5: 如何设置定时采集？

**A**: 使用 cron 或 launchd。详细配置参考快速上手指南的"定时采集"章节。

---

## 📞 获取帮助

### 遇到问题？

1. 查看 [快速上手指南 - 故障排查](HAWAIIHUB_SCRAPER_QUICKSTART.md#故障排查)
2. 查看日志：`tail -f logs/hawaiihub_scraper.log`
3. 测试 API 密钥：`python3 test_api_keys.py`
4. 加入 Firecrawl Discord: https://discord.gg/firecrawl

### 联系方式

- **项目维护**: HawaiiHub AI Team
- **技术支持**: Firecrawl Discord
- **问题反馈**: GitHub Issues

---

## ✅ 检查清单

使用前请确认：

- [ ] ✅ Python 3.11+ 已安装
- [ ] ✅ Firecrawl SDK 已安装（`pip3 install firecrawl-py`）
- [ ] ✅ 环境变量已配置（`FIRECRAWL_API_KEY` in `.env`）
- [ ] ✅ 已阅读快速上手指南
- [ ] ✅ 已测试单个数据源采集
- [ ] ✅ 已了解成本预估

---

## 🎉 开始使用

一切就绪！现在可以开始采集 HawaiiHub 数据了：

```bash
# 开始你的第一次采集
python3 scripts/hawaiihub_scraper.py --source "Hawaii News Now"
```

---

**文档版本**: v1.0
**最后更新**: 2025-10-28
**维护者**: HawaiiHub AI Team
**状态**: ✅ 可用
