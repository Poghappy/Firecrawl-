# HawaiiHub 新闻采集系统 - 快速开始

**5 分钟上手指南** 🚀

---

## 📋 前置检查

确保你已经完成了基本配置：

```bash
✅ Python 3.11+
✅ firecrawl-py 4.5.0+
✅ .env 文件中有 FIRECRAWL_API_KEY
```

---

## 🏃 立即开始

### 第 1 步：进入项目目录

```bash
cd /Users/zhiledeng/Downloads/FireShot/hawaiihub_news
```

### 第 2 步：列出所有新闻源

```bash
python main.py --list
```

你会看到：
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
   ...
```

### 第 3 步：采集一个新闻源（测试）

```bash
python main.py --source hawaii-news-now
```

这会：
1. 爬取 Hawaii News Now 首页
2. 提取最多 20 篇文章链接
3. 批量采集文章内容
4. 保存到 `data/processed/` 目录

### 第 4 步：查看结果

```bash
ls -lh data/processed/
```

你会看到 3 个文件：
```
hawaii-news-now_20251028_120000.json   # JSON 格式
hawaii-news-now_20251028_120000.md     # Markdown 格式
hawaii-news-now_20251028_120000.csv    # CSV 格式
```

---

## 🎯 常用命令

```bash
# 采集所有 P0 优先级新闻源（推荐）
python main.py --priority P0

# 采集所有新闻源
python main.py --all

# 采集单个新闻源
python main.py --source hawaii-news-now

# 采集华人社区新闻
python main.py --source hawaii-chinese-daily

# 设置预算（美元）
python main.py --priority P0 --budget 5.0

# 启用调试模式
python main.py --source hawaii-news-now --debug
```

---

## 📂 文件位置

```
hawaiihub_news/
├── data/
│   ├── raw/                  # 原始数据（JSON）
│   │   └── all_sources_*.json
│   ├── processed/            # 处理后数据（多格式）
│   │   ├── *.json           # JSON 格式
│   │   ├── *.md             # Markdown 格式
│   │   └── *.csv            # CSV 格式
│   └── cache/               # 缓存数据
└── logs/
    ├── hawaiihub_news.log   # 主日志
    └── errors.log           # 错误日志
```

---

## 💡 使用技巧

### 1. 查看实时日志

```bash
# 新终端窗口
tail -f logs/hawaiihub_news.log
```

### 2. 成本控制

```bash
# 设置每日预算 $5
python main.py --priority P0 --budget 5.0

# 程序会在达到预算时自动停止
```

### 3. 定时采集

#### Mac/Linux (cron)

```bash
# 编辑 crontab
crontab -e

# 每 2 小时采集一次 P0 新闻源
0 */2 * * * cd /Users/zhiledeng/Downloads/FireShot/hawaiihub_news && python main.py --priority P0
```

#### Windows (Task Scheduler)

1. 打开任务计划程序
2. 创建基本任务
3. 触发器：每 2 小时
4. 操作：运行程序
   - 程序：`python`
   - 参数：`main.py --priority P0`
   - 起始于：`C:\path\to\hawaiihub_news`

---

## 🔧 故障排查

### 问题 1: 找不到模块

**错误**: `ModuleNotFoundError: No module named 'firecrawl'`

**解决**:
```bash
pip install firecrawl-py python-dotenv
```

### 问题 2: API 密钥错误

**错误**: `❌ 认证失败`

**解决**:
```bash
# 检查 .env 文件
cat ../.env | grep FIRECRAWL_API_KEY

# 确保密钥有效
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('FIRECRAWL_API_KEY'))"
```

### 问题 3: 采集很慢

**原因**: Firecrawl 需要渲染 JavaScript 和加载页面，这是正常的。

**优化**:
1. 使用缓存（配置中已启用）
2. 减少采集数量（修改 `limit` 参数）
3. 使用批量采集（已默认启用）

---

## 📊 查看结果

### JSON 格式

```bash
cat data/processed/news_p0_20251028_120000.json | jq '.[0]'
```

### Markdown 格式

```bash
open data/processed/news_p0_20251028_120000.md
```

### CSV 格式

```bash
# Mac
open -a "Microsoft Excel" data/processed/news_p0_20251028_120000.csv

# Linux
libreoffice data/processed/news_p0_20251028_120000.csv
```

---

## 🎓 下一步

1. **阅读完整文档**: `README.md`
2. **自定义新闻源**: 编辑 `config.py`
3. **集成到应用**: 使用编程接口
4. **设置定时任务**: 自动化采集

---

## 💬 需要帮助？

- **完整文档**: `README.md`
- **配置说明**: `config.py` 中的注释
- **日志文件**: `logs/hawaiihub_news.log`
- **Firecrawl SDK**: `../Firecrawl学习手册/03-API参考/08-Python-SDK完整指南.md`

---

**开始采集吧！** 🚀

```bash
python main.py --priority P0
```
