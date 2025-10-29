# 🏠 檀香山租房信息采集系统

**版本**: v1.0  
**创建日期**: 2025-10-29  
**用户预算**: $1,200/月

---

## ✅ 系统已完成

✅ **Craigslist 采集器** - 自动采集檀香山 Craigslist 房源  
✅ **完整数据字段** - 图片、价格、地区、联系方式、房型、设施  
✅ **JSON/Markdown 导出** - 多格式数据导出  
✅ **4个API Key 轮换** - 避免限流，优化成本  
✅ **自动日志** - 详细运行日志和错误追踪  
✅ **定时任务脚本** - 每天早上 8:00 HST 自动运行

---

## 🚀 5分钟快速开始

### 1. 安装依赖
```bash
pip3 install -r requirements.txt
```

### 2. 运行采集
```bash
python3 main.py
```

### 3. 查看结果
```bash
# 数据保存在
ls data/exports/

# 查看 Markdown 报告
cat data/exports/rentals_*.md
```

---

## 📊 采集结果示例

```
总房源数: 28
平均价格: $1,234/月
价格区间: $850 - $1,500
消耗 Credits: 168 (~$1.68)
```

每条房源包含:
- ✅ 标题、价格、房型
- ✅ 地区、地址
- ✅ 图片列表（最多20张）
- ✅ 电话、邮箱
- ✅ 描述、设施
- ✅ 原始链接

---

## 📁 项目结构

```
honolulu_rentals/
├── main.py              # ⭐ 主程序（运行这个）
├── config.py            # 配置文件
├── models.py            # 数据模型
├── scrapers/            # 采集器
│   ├── craigslist_scraper.py  ✅
│   ├── zillow_scraper.py      ⏳
│   └── apartments_scraper.py  ⏳
├── data/exports/        # ⭐ 导出数据（结果在这里）
├── logs/                # 日志文件
├── README.md            # 本文件
├── QUICK_START.md       # 快速开始
└── setup_cron.sh        # 定时任务设置
```

---

## ⏰ 设置定时任务（每天自动运行）

运行自动化设置脚本：
```bash
./setup_cron.sh
```

或手动添加 crontab：
```bash
crontab -e
# 添加: 0 8 * * * cd /path/to/honolulu_rentals && python3 main.py >> logs/cron.log 2>&1
```

---

## 🔧 配置说明

编辑 `config.py` 修改：

### 修改价格范围
```python
PRICE_RANGE = {
    "min": 0,
    "max": 1500,  # 改为您的预算
}
```

### 启用/禁用平台
```python
PLATFORMS = {
    "craigslist": {"enabled": True},
    "zillow": {"enabled": False},  # 待开发
}
```

---

## 💰 成本估算

| 配置 | 每天 Credits | 每月成本 |
|------|-------------|----------|
| **当前（仅Craigslist）** | ~150 | $45/月 |
| **3个平台** | ~300 | $90/月 |
| **优化后（缓存）** | ~90 | $27/月 |

**成本优化**：
- ✅ 已启用 12 小时缓存（`maxAge=43200000`）
- ✅ 4个 API Key 轮换
- ✅ 批量采集优化

---

##  常见问题

**Q: 没有采集到房源？**  
A: 查看日志 `logs/rentals.log`，可能是网络问题或API限制

**Q: 如何只看某个价格范围？**  
A: 修改 `config.py` 中的 `PRICE_RANGE`

**Q: 如何添加更多平台？**  
A: Zillow 和 Apartments.com 采集器待开发（v1.1）

---

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md)

---

## 📞 技术支持

- 日志: `tail -f logs/rentals.log`
- 配置: `config.py`
- 文档: [Firecrawl Docs](https://docs.firecrawl.dev/)

---

**祝您找到理想的房子！** 🏡
