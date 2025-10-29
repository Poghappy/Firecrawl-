"""HawaiiHub 新闻采集系统

一个专为 HawaiiHub 设计的新闻采集系统，支持采集夏威夷本地新闻和华人社区资讯。
"""

__version__ = "1.0.0"
__author__ = "HawaiiHub AI Team"

from .config import (
    ALL_NEWS_SOURCES,
    CHINESE_COMMUNITY_SOURCES_P0,
    NEWS_SOURCES_P0,
    get_enabled_sources,
    get_source_by_id,
    get_sources_by_priority,
)
from .scraper import HawaiiHubNewsScraper
from .storage import NewsStorage, deduplicate_articles, process_article_content


__all__ = [
    "HawaiiHubNewsScraper",
    "NewsStorage",
    "ALL_NEWS_SOURCES",
    "NEWS_SOURCES_P0",
    "CHINESE_COMMUNITY_SOURCES_P0",
    "get_enabled_sources",
    "get_source_by_id",
    "get_sources_by_priority",
    "deduplicate_articles",
    "process_article_content",
]
