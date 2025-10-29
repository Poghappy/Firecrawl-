# 🚀 5 分钟快速开始

## 第 1 步：安装依赖（30 秒）

```bash
cd honolulu_rentals
pip3 install -r requirements.txt
```

## 第 2 步：运行采集（1 分钟）

```bash
python3 main.py
```

## 第 3 步：查看结果（30 秒）

```bash
# 查看最新的数据文件
ls -lt data/exports/

# 查看 Markdown 报告
cat data/exports/rentals_*.md | head -100
```

---

## 📊 预期输出

```
🏠 檀香山租房信息采集系统 v1.0
⏰ 开始时间: 2025-10-29 08:00:00 HST
🔑 API Keys: 4 个

============================================================
📋 采集 Craigslist Honolulu
============================================================
✅ Craigslist 完成: 28 个房源

============================================================
📊 采集完成总结
============================================================
总房源数: 28
平均价格: $1,234.50/月
价格区间: $850.00 - $1,500.00
消耗 Credits: 168
消耗费用: $1.68
============================================================

✅ 全部完成！
📁 数据已保存到: data/exports/
```

---

## 📁 导出文件

采集完成后，在 `data/exports/` 目录下会生成：

1. **`rentals_YYYYMMDD_HHMMSS.json`** - JSON 格式，方便程序处理
2. **`rentals_YYYYMMDD_HHMMSS.md`** - Markdown 格式，人类可读

---

## 🎯 下一步

### 设置定时任务（每天自动运行）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上 8:00 HST）
0 8 * * * cd /Users/zhiledeng/Movies/Firecrawl数据采集器/honolulu_rentals && /usr/bin/python3 main.py >> logs/cron.log 2>&1
```

### 修改配置

编辑 `config.py` 文件：

```python
# 修改价格范围
PRICE_RANGE = {
    "max": 1500,  # 改为您的预算
}

# 修改采集平台
PLATFORMS = {
    "craigslist": {"enabled": True},  # 改为 False 禁用
}
```

---

## ❓ 遇到问题？

查看日志文件：
```bash
tail -f logs/rentals.log
```

---

**就这么简单！** 🎉

