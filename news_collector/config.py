"""
新闻采集系统 - 配置文件

版本: v1.0
创建日期: 2025-01-29
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent

# API 配置
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

# API Key 轮换列表（可选，用于优化成本）
API_KEYS = [
    os.getenv("FIRECRAWL_API_KEY_1", FIRECRAWL_API_KEY),
    os.getenv("FIRECRAWL_API_KEY_2", ""),
    os.getenv("FIRECRAWL_API_KEY_3", ""),
    os.getenv("FIRECRAWL_API_KEY_4", ""),
]
# 过滤空的 API Key
API_KEYS = [key for key in API_KEYS if key]

# 新闻源配置
NEWS_SOURCES = {
    "hawaii-news-now": {
        "name": "Hawaii News Now",
        "site": "hawaiinewsnow.com",
        "enabled": True,
        "priority": "P0",
        "keywords": ["hawaii", "honolulu"]
    },
    "civil-beat": {
        "name": "Honolulu Civil Beat",
        "site": "civilbeat.org",
        "enabled": True,
        "priority": "P0",
        "keywords": ["hawaii", "政治", "社区"]
    },
    "star-advertiser": {
        "name": "Honolulu Star-Advertiser",
        "site": "staradvertiser.com",
        "enabled": True,
        "priority": "P0",
        "keywords": ["hawaii news"]
    },
    "khon2": {
        "name": "KHON2",
        "site": "khon2.com",
        "enabled": True,
        "priority": "P1",
        "keywords": ["hawaii", "breaking news"]
    },
    "kitv": {
        "name": "KITV 4 Island News",
        "site": "kitv.com",
        "enabled": False,  # 默认禁用
        "priority": "P1",
        "keywords": ["hawaii"]
    }
}

# Search API 配置
SEARCH_CONFIG = {
    "limit": 20,  # 每次搜索返回数量
    "sources": [{"type": "news"}],  # 搜索新闻
    "location": "US",  # 地理位置
    "tbs": "qdr:d",  # 时间范围（qdr:h=1小时, qdr:d=1天, qdr:w=1周）
    "scrapeOptions": {
        "formats": ["markdown", "links"],
        "onlyMainContent": True,
        "maxAge": 600000,  # 10分钟缓存
        "proxy": "basic"
    }
}

# JSON Mode 配置（结构化提取）
JSON_MODE_CONFIG = {
    "formats": [{
        "type": "json",
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "content": {"type": "string"},
                "author": {"type": "string"},
                "published_at": {"type": "string"},
                "images": {"type": "array", "items": {"type": "string"}},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "content"]
        }
    }],
    "onlyMainContent": True,
    "maxAge": 600000,  # 10分钟缓存
    "proxy": "basic"
}

# 导出配置
EXPORT_CONFIG = {
    "formats": ["json", "markdown"],  # 导出格式
    "output_dir": BASE_DIR / "data" / "exports",
    "include_timestamp": True
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": BASE_DIR / "logs" / "news.log",
    "max_bytes": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# 去重配置
DEDUP_CONFIG = {
    "enabled": True,
    "cache_dir": BASE_DIR / "data" / "cache",
    "cache_ttl": 86400  # 24小时
}

# 采集限制
SCRAPING_LIMITS = {
    "max_concurrent": 5,  # 最大并发数
    "retry_attempts": 3,  # 重试次数
    "retry_delay": 2,  # 重试延迟（秒）
    "timeout": 120  # 超时时间（秒）
}

# 成本控制
COST_CONFIG = {
    "daily_budget": 100,  # 每日预算（Credits）
    "alert_threshold": 80,  # 告警阈值（%）
    "enable_monitoring": True
}

# 定时任务配置
SCHEDULE_CONFIG = {
    "enabled": False,  # 是否启用定时任务
    "interval_hours": 2,  # 运行间隔（小时）
    "run_at": "08:00"  # 固定运行时间（可选）
}

# 创建必要的目录
def setup_directories():
    """创建必要的目录"""
    directories = [
        BASE_DIR / "data" / "exports",
        BASE_DIR / "data" / "cache",
        BASE_DIR / "logs"
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# 自动创建目录
setup_directories()
