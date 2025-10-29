"""
檀香山租房信息采集系统 - 配置文件

版本: v1.0
创建日期: 2025-10-29
"""

import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================================
# Firecrawl API 配置
# ============================================================

# API Keys（4个轮换使用）
FIRECRAWL_API_KEYS = [
    "fc-31ebbe4647b84fdc975318d372eebea8",  # 主密钥
    "fc-00857d82ec534e8598df1bae9af9fb28",  # 备用密钥 1
    "fc-9eb380b0dec74d6ebb6c756ee4de4c5a",  # 备用密钥 2
    "fc-0a2c801f433d4718bcd8189f2742edf4",  # 备用密钥 3
]

# 当前使用的 Key 索引（自动轮换）
CURRENT_KEY_INDEX = 0

def get_next_api_key() -> str:
    """获取下一个可用的 API Key（轮换策略）"""
    global CURRENT_KEY_INDEX
    key = FIRECRAWL_API_KEYS[CURRENT_KEY_INDEX]
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(FIRECRAWL_API_KEYS)
    return key

# ============================================================
# 采集平台配置
# ============================================================

PLATFORMS = {
    "craigslist": {
        "name": "Craigslist Honolulu",
        "base_url": "https://honolulu.craigslist.org",
        "search_url": "https://honolulu.craigslist.org/search/apa",
        "enabled": True,
        "priority": 1,
        "api_key": FIRECRAWL_API_KEYS[0],
    },
    "zillow": {
        "name": "Zillow Honolulu",
        "base_url": "https://www.zillow.com",
        "search_url": "https://www.zillow.com/honolulu-hi/rentals/",
        "enabled": True,
        "priority": 2,
        "api_key": FIRECRAWL_API_KEYS[1],
    },
    "apartments": {
        "name": "Apartments.com",
        "base_url": "https://www.apartments.com",
        "search_url": "https://www.apartments.com/honolulu-hi/",
        "enabled": True,
        "priority": 3,
        "api_key": FIRECRAWL_API_KEYS[2],
    },
}

# ============================================================
# Firecrawl 采集参数
# ============================================================

# Scrape 配置（单页采集）
SCRAPE_CONFIG = {
    "formats": ["markdown", "html", "links"],
    "onlyMainContent": True,
    "includeTags": ["img", "a", "p", "h1", "h2", "h3", "div"],
    "waitFor": 2000,  # 等待 2 秒
    "timeout": 30000,  # 30 秒超时
    "proxy": {
        "type": "basic"  # 使用基础代理（5 credits/请求）
    },
    "maxAge": 43200000,  # 12 小时缓存
}

# Batch Scrape 配置（批量采集）
BATCH_SCRAPE_CONFIG = {
    "formats": ["markdown", "html"],
    "onlyMainContent": True,
    "maxConcurrency": 5,  # 并发数
    "ignoreInvalidURLs": True,
    "proxy": {
        "type": "basic"
    },
    "maxAge": 43200000,
}

# Map 配置（发现 URLs）
MAP_CONFIG = {
    "search": "",  # 搜索关键词（动态设置）
    "ignoreSitemap": False,
    "includeSubdomains": False,
    "limit": 100,
}

# ============================================================
# 筛选条件
# ============================================================

# 价格范围（美元/月）
PRICE_RANGE = {
    "min": 0,
    "max": 1500,
    "target": 1200,  # 用户预算
}

# 房型（全部）
PROPERTY_TYPES = ["Studio", "1B1B", "2B1B", "2B2B", "Other"]

# 檀香山主要区域（全部）
NEIGHBORHOODS = [
    # 市区/商业区
    "Downtown Honolulu",
    "Waikiki",
    "Ala Moana",
    "Kakaako",

    # 住宅区（推荐）
    "Makiki",
    "Manoa",
    "Kaimuki",
    "Moiliili",
    "McCully",

    # 东部
    "Kahala",
    "Diamond Head",
    "Kailua",

    # 西部
    "Kalihi",
    "Pearl City",
    "Aiea",
    "Ewa Beach",

    # 其他
    "Hawaii Kai",
    "Kaneohe",
]

# ============================================================
# 数据存储配置
# ============================================================

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
EXPORT_DIR = os.path.join(DATA_DIR, "exports")

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")

# SQLite 数据库
DATABASE_PATH = os.path.join(PROCESSED_DATA_DIR, "rentals.db")

# ============================================================
# 定时任务配置
# ============================================================

# 定时任务时间（夏威夷时区 HST，UTC-10）
SCHEDULE_TIME = "08:00"  # 每天早上 8:00 HST

# 夏威夷时区
TIMEZONE = "Pacific/Honolulu"

# ============================================================
# 去重配置
# ============================================================

# 去重策略
DEDUP_CONFIG = {
    "enabled": True,
    "similarity_threshold": 0.85,  # 相似度阈值（0-1）
    "price_tolerance": 50,  # 价格容差（美元）
    "address_match": True,  # 地址匹配
}

# ============================================================
# 导出配置
# ============================================================

# Excel 导出
EXCEL_CONFIG = {
    "filename_template": "檀香山租房信息_{date}.xlsx",
    "sheets": ["房源列表", "统计分析", "数据源"],
}

# HTML 导出
HTML_CONFIG = {
    "filename_template": "檀香山租房信息_{date}.html",
    "title": "檀香山租房信息",
    "responsive": True,
}

# ============================================================
# 成本控制
# ============================================================

# 每日预算（Credits）
DAILY_BUDGET = 350  # 约 $3.50/天

# 月度预算（美元）
MONTHLY_BUDGET = 57.0  # 标准型方案

# Credits 余额告警阈值
ALERT_THRESHOLD = 1000  # 少于 1000 Credits 时告警

# ============================================================
# 日志配置
# ============================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "rentals.log"),
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

# ============================================================
# 联系方式验证正则表达式
# ============================================================

import re

# 美国电话号码（支持多种格式）
PHONE_REGEX = re.compile(
    r"(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
)

# 邮箱地址
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

# 邮编（夏威夷）
ZIPCODE_REGEX = re.compile(r"968\d{2}")

# ============================================================
# 用户偏好（可通过 UI 修改）
# ============================================================

USER_PREFERENCES = {
    "max_price": PRICE_RANGE["target"],
    "preferred_neighborhoods": [],  # 空表示不限
    "preferred_types": [],  # 空表示不限
    "must_have_amenities": [],  # 必须有的设施
    "pets_allowed": None,  # None=不限，True=允许，False=不允许
}
