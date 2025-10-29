#!/usr/bin/env python3
"""HawaiiHub 新闻采集系统 - 配置文件

定义所有新闻源、采集策略和系统配置
"""

import os
from typing import Dict, List

from dotenv import load_dotenv


# 加载环境变量
load_dotenv()


# =============================================================================
# API 配置
# =============================================================================

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_API_KEYS_BACKUP = [
    os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_3"),
]

# 成本控制
DAILY_BUDGET = float(os.getenv("FIRECRAWL_DAILY_BUDGET", "10.0"))
MONTHLY_BUDGET = float(os.getenv("FIRECRAWL_MONTHLY_BUDGET", "200.0"))


# =============================================================================
# 系统配置
# =============================================================================

# 数据存储路径
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")

# 确保目录存在
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, CACHE_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)


# =============================================================================
# 新闻源配置 - P0 优先级（每日更新）
# =============================================================================

NEWS_SOURCES_P0: List[Dict] = [
    {
        "id": "hawaii-news-now",
        "name": "Hawaii News Now",
        "url": "https://www.hawaiinewsnow.com/",
        "description": "夏威夷最大的新闻网站，KGMB/KHNL 联合平台",
        "priority": "P0",
        "rating": 5,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "exclude_tags": ["nav", "footer", "aside", "script"],
            "max_age": 7200000,  # 2小时缓存
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 20,
            "include_paths": ["/news/*", "/weather/*"],
            "exclude_paths": ["/video/*", "/advertise/*"],
            "max_discovery_depth": 2,
        },
        "frequency_hours": 2,  # 每2小时
        "enabled": True,
    },
    {
        "id": "civil-beat",
        "name": "Honolulu Civil Beat",
        "url": "https://www.civilbeat.org/",
        "description": "深度调查报道，无付费墙",
        "priority": "P0",
        "rating": 5,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 21600000,  # 6小时缓存
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 15,
            "include_paths": ["/category/*", "/posts/*"],
            "max_discovery_depth": 2,
        },
        "frequency_hours": 6,  # 每6小时
        "enabled": True,
    },
    {
        "id": "star-advertiser",
        "name": "Honolulu Star-Advertiser",
        "url": "https://www.staradvertiser.com/",
        "description": "檀香山最权威的报纸",
        "priority": "P0",
        "rating": 5,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 14400000,  # 4小时缓存
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 20,
            "include_paths": ["/news/*", "/business/*", "/sports/*"],
            "exclude_paths": ["/subscribe/*"],
            "max_discovery_depth": 2,
        },
        "frequency_hours": 4,  # 每4小时
        "enabled": True,
    },
    {
        "id": "khon2",
        "name": "KHON2",
        "url": "https://www.khon2.com/",
        "description": "檀香山、科纳、希洛、考艾、毛伊新闻",
        "priority": "P0",
        "rating": 4,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 21600000,  # 6小时缓存
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 15,
            "include_paths": ["/news/*", "/weather/*"],
            "max_discovery_depth": 2,
        },
        "frequency_hours": 6,
        "enabled": True,
    },
    {
        "id": "kitv",
        "name": "KITV 4 Island News",
        "url": "https://www.kitv.com/",
        "description": "檀香山突发新闻和天气",
        "priority": "P0",
        "rating": 4,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 21600000,
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 15,
            "include_paths": ["/news/*"],
            "max_discovery_depth": 2,
        },
        "frequency_hours": 6,
        "enabled": True,
    },
]


# =============================================================================
# 华人社区新闻源配置 - P0 优先级
# =============================================================================

CHINESE_COMMUNITY_SOURCES_P0: List[Dict] = [
    {
        "id": "hawaii-chinese-daily",
        "name": "夏威夷中国日报",
        "url": "https://hawaiichinesedaily.com/",
        "description": "华人社区最权威中文媒体",
        "priority": "P0",
        "rating": 5,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 14400000,  # 4小时缓存
            "location": {"country": "US", "languages": ["zh-CN", "zh-TW"]},
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 20,
            "max_discovery_depth": 2,
        },
        "content_types": ["新闻", "文化活动", "商业资讯"],
        "target_audience": "华人社区",
        "frequency_hours": 4,
        "enabled": True,
    },
    {
        "id": "chinese-chamber",
        "name": "Chinese Chamber of Commerce of Hawaii",
        "url": "https://www.chinesechamber.com/",
        "description": "夏威夷华人商会（1911年成立）",
        "priority": "P0",
        "rating": 5,
        "scrape_config": {
            "formats": ["markdown"],
            "only_main_content": True,
            "max_age": 604800000,  # 7天缓存
            "remove_base64_images": True,
        },
        "crawl_config": {
            "limit": 10,
            "include_paths": ["/events/*", "/news/*"],
            "max_discovery_depth": 2,
        },
        "content_types": ["商业活动", "研讨会", "教育"],
        "frequency_hours": 84,  # 每周2次（每3.5天）
        "enabled": True,
    },
]


# =============================================================================
# 所有新闻源（合并）
# =============================================================================

ALL_NEWS_SOURCES = NEWS_SOURCES_P0 + CHINESE_COMMUNITY_SOURCES_P0


# =============================================================================
# 采集策略配置
# =============================================================================

SCRAPE_STRATEGY = {
    # 重试配置
    "max_retries": 3,
    "retry_delay_base": 2,  # 指数退避基数（秒）
    # 超时配置
    "scrape_timeout": 60,
    "crawl_timeout": 180,
    "batch_timeout": 120,
    # 并发配置
    "max_concurrency": 3,
    "batch_size": 5,
    "delay_between_batches": 2,  # 秒
    # 缓存配置
    "enable_cache": True,
    "default_cache_ttl": 14400000,  # 4小时（毫秒）
}


# =============================================================================
# 数据处理配置
# =============================================================================

DATA_PROCESSING = {
    # 内容清洗
    "min_content_length": 100,  # 最小内容长度（字符）
    "max_content_length": 100000,  # 最大内容长度
    "remove_patterns": [
        r"Subscribe to.*newsletter",
        r"Advertisement",
        r"Related Articles",
        r"Share on.*",
        r"Follow us on",
    ],
    # 元数据提取
    "extract_metadata": True,
    "metadata_fields": ["title", "author", "date", "category", "tags"],
    # 去重
    "enable_deduplication": True,
    "dedup_field": "url",  # 基于 URL 去重
}


# =============================================================================
# 导出配置
# =============================================================================

EXPORT_CONFIG = {
    "formats": ["json", "markdown", "csv"],  # 导出格式
    "json_indent": 2,
    "csv_encoding": "utf-8-sig",  # 支持中文
    "markdown_template": "templates/article.md.j2",  # Jinja2 模板
    # 文件命名
    "filename_pattern": "{source_id}_{timestamp}",
    "timestamp_format": "%Y%m%d_%H%M%S",
}


# =============================================================================
# 日志配置
# =============================================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": os.path.join(LOGS_DIR, "hawaiihub_news.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": os.path.join(LOGS_DIR, "errors.log"),
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file", "error_file"]},
}


# =============================================================================
# 辅助函数
# =============================================================================


def get_enabled_sources() -> List[Dict]:
    """获取所有启用的新闻源"""
    return [source for source in ALL_NEWS_SOURCES if source.get("enabled", True)]


def get_source_by_id(source_id: str) -> Dict | None:
    """根据 ID 获取新闻源配置"""
    for source in ALL_NEWS_SOURCES:
        if source["id"] == source_id:
            return source
    return None


def get_sources_by_priority(priority: str) -> List[Dict]:
    """根据优先级获取新闻源"""
    return [source for source in ALL_NEWS_SOURCES if source.get("priority") == priority]
