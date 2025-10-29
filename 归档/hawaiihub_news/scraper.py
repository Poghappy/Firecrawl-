#!/usr/bin/env python3
"""HawaiiHub 新闻采集系统 - 核心采集器

实现新闻采集的核心逻辑，包括错误处理、重试机制和成本控制
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional

from firecrawl import FirecrawlApp
from firecrawl.exceptions import (
    AuthenticationError,
    RateLimitError,
    RequestTimeoutError,
)

from config import (
    DAILY_BUDGET,
    FIRECRAWL_API_KEY,
    FIRECRAWL_API_KEYS_BACKUP,
    SCRAPE_STRATEGY,
    get_enabled_sources,
)


# 配置日志
logger = logging.getLogger(__name__)


class HawaiiHubNewsScraper:
    """HawaiiHub 新闻采集器"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        backup_keys: Optional[List[str]] = None,
        daily_budget: float = DAILY_BUDGET,
    ):
        """初始化采集器

        Args:
            api_key: Firecrawl API 密钥（可选，从环境变量读取）
            backup_keys: 备用 API 密钥列表
            daily_budget: 每日预算（美元）
        """
        self.api_key = api_key or FIRECRAWL_API_KEY
        self.backup_keys = backup_keys or [k for k in FIRECRAWL_API_KEYS_BACKUP if k]
        self.daily_budget = daily_budget

        # 初始化 Firecrawl 客户端
        self.app = FirecrawlApp(api_key=self.api_key)

        # 统计信息
        self.request_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_cost = 0.0
        self.cost_per_request = 0.01  # 假设每次请求 $0.01

        logger.info("HawaiiHub 新闻采集器已初始化")
        logger.info(f"每日预算: ${self.daily_budget}")
        logger.info(f"备用密钥数: {len(self.backup_keys)}")

    def scrape_url(
        self, url: str, config: Optional[Dict] = None, max_retries: Optional[int] = None
    ) -> Optional[Dict]:
        """采集单个 URL

        Args:
            url: 要采集的 URL
            config: Scrape 配置（可选）
            max_retries: 最大重试次数（可选）

        Returns:
            采集结果字典，失败返回 None
        """
        max_retries = max_retries or SCRAPE_STRATEGY["max_retries"]
        config = config or {}

        for attempt in range(max_retries):
            try:
                # 检查预算
                if self.total_cost >= self.daily_budget:
                    logger.error(f"超出每日预算: ${self.daily_budget}")
                    return None

                # 执行采集
                logger.debug(f"采集 URL: {url} (尝试 {attempt + 1}/{max_retries})")
                result = self.app.scrape(url=url, **config)

                # 验证结果
                if not result or not hasattr(result, "markdown"):
                    raise ValueError("返回结果无效")

                # 更新统计
                self.request_count += 1
                self.success_count += 1
                self.total_cost += self.cost_per_request

                logger.info(f"✅ 成功采集: {url}")
                logger.debug(
                    f"📊 统计: 请求 {self.request_count}, "
                    f"成功 {self.success_count}, "
                    f"失败 {self.failure_count}, "
                    f"成本 ${self.total_cost:.2f}/{self.daily_budget}"
                )

                # 返回结构化数据
                return {
                    "url": url,
                    "metadata": {
                        "source_url": result.metadata.source_url,
                        "title": result.metadata.title,
                        "description": result.metadata.description,
                        "status_code": result.metadata.status_code,
                        "cache_state": result.metadata.get("cacheState", "unknown"),
                    },
                    "content": {
                        "markdown": result.markdown,
                        "html": getattr(result, "html", None),
                        "links": getattr(result, "links", []),
                    },
                    "scraped_at": datetime.now().isoformat(),
                    "attempt": attempt + 1,
                }

            except AuthenticationError as e:
                logger.error(f"❌ 认证失败: {e}")
                self.failure_count += 1
                return None  # 密钥问题，不重试

            except RateLimitError:
                if attempt < max_retries - 1:
                    wait_time = SCRAPE_STRATEGY["retry_delay_base"] ** attempt
                    logger.warning(
                        f"⏳ 速率限制，{wait_time}秒后重试... ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ 达到速率限制: {url}")
                    self.failure_count += 1
                    return None

            except RequestTimeoutError:
                if attempt < max_retries - 1:
                    wait_time = SCRAPE_STRATEGY["retry_delay_base"] ** attempt
                    logger.warning(
                        f"⏳ 超时，{wait_time}秒后重试... ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ 超时失败: {url}")
                    self.failure_count += 1
                    return None

            except Exception as e:
                logger.error(f"❌ 未知错误: {url} - {e}")
                self.failure_count += 1
                return None

        return None

    def batch_scrape_urls(
        self, urls: List[str], config: Optional[Dict] = None
    ) -> List[Dict]:
        """批量采集 URL 列表

        Args:
            urls: URL 列表
            config: Scrape 配置（可选）

        Returns:
            采集结果列表
        """
        results = []
        batch_size = SCRAPE_STRATEGY["batch_size"]

        logger.info(f"📦 批量采集 {len(urls)} 个 URL，批次大小: {batch_size}")

        for i in range(0, len(urls), batch_size):
            batch = urls[i : i + batch_size]
            batch_num = i // batch_size + 1

            logger.info(f"⏳ 处理批次 {batch_num} ({len(batch)} 个 URL)...")

            try:
                # 使用 Firecrawl batch_scrape
                job = self.app.batch_scrape(
                    urls=batch,
                    **config or {},
                    poll_interval=2,
                    timeout=SCRAPE_STRATEGY["batch_timeout"],
                )

                # 处理结果
                for doc in job.data:
                    results.append(
                        {
                            "url": doc.metadata.source_url,
                            "metadata": {
                                "title": doc.metadata.title,
                                "description": doc.metadata.description,
                                "status_code": doc.metadata.status_code,
                            },
                            "content": {"markdown": doc.markdown},
                            "scraped_at": datetime.now().isoformat(),
                            "batch_num": batch_num,
                        }
                    )

                self.request_count += len(batch)
                self.success_count += len(job.data)
                self.total_cost += len(batch) * self.cost_per_request

                logger.info(
                    f"   ✅ 批次 {batch_num}: {len(job.data)}/{len(batch)} 成功"
                )

            except Exception as e:
                logger.error(f"   ❌ 批次 {batch_num} 失败: {e}")

                # 逐个重试
                logger.info("   🔄 逐个重试...")
                for url in batch:
                    result = self.scrape_url(url, config)
                    if result:
                        results.append(result)

            # 延迟避免速率限制
            if i + batch_size < len(urls):
                delay = SCRAPE_STRATEGY["delay_between_batches"]
                logger.debug(f"   ⏸️  等待 {delay} 秒...")
                time.sleep(delay)

        logger.info(
            f"✅ 批量采集完成: {len(results)}/{len(urls)} 成功 "
            f"(成本: ${self.total_cost:.2f})"
        )

        return results

    def scrape_news_source(self, source_config: Dict) -> Dict:
        """采集单个新闻源

        Args:
            source_config: 新闻源配置

        Returns:
            采集结果字典
        """
        source_id = source_config["id"]
        source_name = source_config["name"]
        source_url = source_config["url"]

        logger.info(f"📰 开始采集新闻源: {source_name} ({source_id})")

        start_time = datetime.now()

        # 1. 爬取首页
        logger.info(f"   🔍 爬取首页: {source_url}")
        homepage = self.scrape_url(source_url, source_config.get("scrape_config"))

        if not homepage:
            logger.error(f"   ❌ 首页采集失败: {source_name}")
            return {
                "source_id": source_id,
                "source_name": source_name,
                "status": "failed",
                "error": "首页采集失败",
                "scraped_at": datetime.now().isoformat(),
            }

        # 2. 提取文章链接
        links = homepage.get("content", {}).get("links", [])
        article_links = [link for link in links if self._is_article_link(link)][:20]

        logger.info(f"   🔗 发现 {len(article_links)} 个文章链接")

        # 3. 批量采集文章
        if article_links:
            articles = self.batch_scrape_urls(
                article_links, source_config.get("scrape_config")
            )
        else:
            articles = []

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info(
            f"✅ 完成采集: {source_name} "
            f"(文章数: {len(articles)}, 耗时: {duration:.1f}秒)"
        )

        return {
            "source_id": source_id,
            "source_name": source_name,
            "source_url": source_url,
            "status": "success",
            "homepage": homepage,
            "articles": articles,
            "stats": {
                "total_articles": len(articles),
                "duration_seconds": duration,
                "articles_per_minute": len(articles) / (duration / 60)
                if duration > 0
                else 0,
            },
            "scraped_at": datetime.now().isoformat(),
        }

    def scrape_all_sources(self, sources: Optional[List[Dict]] = None) -> List[Dict]:
        """采集所有新闻源

        Args:
            sources: 新闻源列表（可选，默认使用所有启用的源）

        Returns:
            所有采集结果列表
        """
        sources = sources or get_enabled_sources()

        logger.info(f"🚀 开始采集 {len(sources)} 个新闻源")

        results = []
        for i, source in enumerate(sources, 1):
            logger.info(f"\n{'=' * 60}")
            logger.info(f"进度: {i}/{len(sources)}")
            logger.info(f"{'=' * 60}")

            result = self.scrape_news_source(source)
            results.append(result)

            # 检查预算
            if self.total_cost >= self.daily_budget:
                logger.warning(f"⚠️  已达每日预算: ${self.daily_budget}")
                break

        logger.info(f"\n{'=' * 60}")
        logger.info("✅ 所有采集完成")
        logger.info(f"{'=' * 60}")

        self._print_summary(results)

        return results

    def _is_article_link(self, link: str) -> bool:
        """判断是否为文章链接

        Args:
            link: URL 链接

        Returns:
            是否为文章链接
        """
        # 简单规则：包含常见文章路径
        article_patterns = [
            "/article/",
            "/news/",
            "/story/",
            "/post/",
            "category/",
            "/archives/",
        ]

        # 排除的模式
        exclude_patterns = [
            "/video/",
            "/advertise/",
            "/subscribe/",
            "/contact/",
            "/about/",
            ".pdf",
            ".jpg",
            ".png",
        ]

        link_lower = link.lower()

        # 检查排除模式
        for pattern in exclude_patterns:
            if pattern in link_lower:
                return False

        # 检查文章模式
        for pattern in article_patterns:
            if pattern in link_lower:
                return True

        return False

    def _print_summary(self, results: List[Dict]) -> None:
        """打印采集总结

        Args:
            results: 采集结果列表
        """
        total_sources = len(results)
        successful_sources = len([r for r in results if r["status"] == "success"])
        total_articles = sum(
            r.get("stats", {}).get("total_articles", 0) for r in results
        )

        logger.info("\n📊 采集统计:")
        logger.info(f"   新闻源: {successful_sources}/{total_sources} 成功")
        logger.info(f"   文章数: {total_articles}")
        logger.info(f"   请求数: {self.request_count}")
        logger.info(
            f"   成功率: {self.success_count}/{self.request_count} ({self.success_count / self.request_count * 100:.1f}%)"
            if self.request_count > 0
            else "   成功率: N/A"
        )
        logger.info(f"   总成本: ${self.total_cost:.2f}/{self.daily_budget}")
        logger.info(f"   剩余预算: ${self.daily_budget - self.total_cost:.2f}")

    def get_stats(self) -> Dict:
        """获取统计信息

        Returns:
            统计信息字典
        """
        return {
            "request_count": self.request_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.success_count / self.request_count
            if self.request_count > 0
            else 0,
            "total_cost": self.total_cost,
            "budget": self.daily_budget,
            "remaining_budget": self.daily_budget - self.total_cost,
        }
