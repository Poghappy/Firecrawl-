"""
基础采集器 - 所有平台采集器的父类

版本: v1.0
创建日期: 2025-10-29
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from firecrawl import FirecrawlApp

from ..models import RentalListing, ContactMethod, Platform, PropertyType, ScraperStats
from ..config import SCRAPE_CONFIG, BATCH_SCRAPE_CONFIG, PRICE_RANGE

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """基础采集器抽象类"""

    def __init__(self, api_key: str, platform: Platform):
        """
        初始化采集器

        Args:
            api_key: Firecrawl API Key
            platform: 平台枚举
        """
        self.api_key = api_key
        self.platform = platform
        self.app = FirecrawlApp(api_key=api_key)
        self.stats = ScraperStats(
            platform=platform,
            start_time=datetime.now()
        )
        logger.info(f"初始化 {platform} 采集器")

    @abstractmethod
    def get_listing_urls(self) -> List[str]:
        """
        获取房源列表页的 URLs

        Returns:
            URL 列表
        """
        pass

    @abstractmethod
    def parse_listing(self, url: str, content: dict) -> Optional[RentalListing]:
        """
        解析单个房源页面

        Args:
            url: 房源 URL
            content: Firecrawl 返回的内容

        Returns:
            RentalListing 对象或 None
        """
        pass

    def scrape_all(self) -> List[RentalListing]:
        """
        采集所有房源

        Returns:
            房源列表
        """
        logger.info(f"开始采集 {self.platform} 房源...")

        # 1. 获取所有房源 URLs
        urls = self.get_listing_urls()
        self.stats.total_urls = len(urls)
        logger.info(f"发现 {len(urls)} 个房源 URL")

        if not urls:
            logger.warning(f"{self.platform} 没有发现任何房源")
            return []

        # 2. 批量采集
        listings = self._batch_scrape(urls)

        # 3. 标记完成
        self.stats.mark_complete()
        logger.info(f"{self.platform} 采集完成: 成功 {self.stats.successful}/{self.stats.total_urls}, "
                   f"耗时 {self.stats.get_duration():.1f}秒")

        return listings

    def _batch_scrape(self, urls: List[str]) -> List[RentalListing]:
        """
        批量采集房源详情

        Args:
            urls: URL 列表

        Returns:
            房源列表
        """
        listings = []

        try:
            # 使用 Firecrawl Batch Scrape API
            logger.info(f"开始批量采集 {len(urls)} 个页面...")

            # 分批处理（每批 20 个，避免超时）
            batch_size = 20
            for i in range(0, len(urls), batch_size):
                batch_urls = urls[i:i + batch_size]
                logger.info(f"采集第 {i//batch_size + 1} 批（{len(batch_urls)} 个 URL）...")

                try:
                    # 调用 Batch Scrape（使用关键字参数）
                    job = self.app.batch_scrape(
                        batch_urls,
                        formats=BATCH_SCRAPE_CONFIG.get("formats", ["markdown"]),
                        only_main_content=BATCH_SCRAPE_CONFIG.get("onlyMainContent", True),
                        proxy=BATCH_SCRAPE_CONFIG.get("proxy", "basic"),
                        max_age=BATCH_SCRAPE_CONFIG.get("maxAge", 43200000)
                    )

                    # 等待完成并获取结果
                    results = job.data if hasattr(job, 'data') else []

                    # 解析每个结果
                    for idx, result in enumerate(results):
                        url = batch_urls[idx] if idx < len(batch_urls) else "unknown"

                        try:
                            # 解析房源
                            listing = self.parse_listing(url, result)

                            if listing:
                                listings.append(listing)
                                self.stats.successful += 1
                            else:
                                self.stats.failed += 1
                                logger.warning(f"解析失败: {url}")

                        except Exception as e:
                            self.stats.failed += 1
                            error_msg = f"解析错误 {url}: {str(e)}"
                            self.stats.errors.append(error_msg)
                            logger.error(error_msg)

                    # 估算消耗的 Credits（每个请求 6 credits：1 base + 5 proxy）
                    self.stats.credits_used += len(batch_urls) * 6

                except Exception as e:
                    self.stats.failed += len(batch_urls)
                    error_msg = f"批量采集失败: {str(e)}"
                    self.stats.errors.append(error_msg)
                    logger.error(error_msg)

        except Exception as e:
            logger.error(f"批量采集异常: {str(e)}")

        return listings

    def _extract_price(self, text: str) -> Optional[float]:
        """
        从文本中提取价格

        Args:
            text: 文本内容

        Returns:
            价格（美元）或 None
        """
        if not text:
            return None

        # 匹配价格模式：$1,200 或 $1200 或 1200
        patterns = [
            r'\$\s?([\d,]+)',  # $1,200
            r'([\d,]+)\s?/\s?mo',  # 1200/mo
            r'([\d,]+)\s?per\s?month',  # 1200 per month
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    price = float(price_str)
                    # 价格合理性检查
                    if PRICE_RANGE["min"] <= price <= PRICE_RANGE["max"] * 2:
                        return price
                except ValueError:
                    continue

        return None

    def _extract_bedrooms(self, text: str) -> Optional[str]:
        """提取卧室数"""
        if not text:
            return None

        patterns = [
            r'(\d+)\s?br',  # 1br
            r'(\d+)\s?bed',  # 1 bed
            r'studio',  # Studio
        ]

        text_lower = text.lower()

        if 'studio' in text_lower:
            return 'Studio'

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)

        return None

    def _extract_bathrooms(self, text: str) -> Optional[str]:
        """提取浴室数"""
        if not text:
            return None

        patterns = [
            r'(\d+\.?\d*)\s?ba',  # 1ba, 1.5ba
            r'(\d+\.?\d*)\s?bath',  # 1 bath
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)

        return None

    def _extract_contact(self, text: str, links: List[str]) -> ContactMethod:
        """
        提取联系方式

        Args:
            text: 文本内容
            links: 链接列表

        Returns:
            ContactMethod 对象
        """
        contact = ContactMethod()

        # 提取电话
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
        if phone_match:
            contact.phone = phone_match.group(1)

        # 提取邮箱
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if email_match:
            contact.email = email_match.group(0)

        # 从链接中查找联系方式
        for link in links:
            if 'mailto:' in link:
                contact.email = link.replace('mailto:', '')
            elif 'tel:' in link:
                contact.phone = link.replace('tel:', '')

        return contact

    def _extract_images(self, content: dict) -> List[str]:
        """
        提取图片 URLs

        Args:
            content: Firecrawl 返回的内容

        Returns:
            图片 URL 列表
        """
        images = []

        # 从 HTML 中提取图片
        if 'html' in content:
            html = content['html']
            img_matches = re.findall(r'<img[^>]+src="([^"]+)"', html)
            images.extend(img_matches)

        # 从 links 中提取图片
        if 'links' in content:
            for link in content['links']:
                if any(ext in link.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    images.append(link)

        # 去重并过滤无效图片
        unique_images = []
        seen = set()
        for img in images:
            if img not in seen and len(img) > 20:  # 过滤掉太短的 URL
                unique_images.append(img)
                seen.add(img)

        return unique_images[:20]  # 最多保留 20 张图片

    def _generate_id(self, url: str) -> str:
        """
        生成唯一 ID

        Args:
            url: 房源 URL

        Returns:
            唯一标识
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # 从 URL 中提取 ID 或使用 hash
        url_id = url.split('/')[-1].split('.')[0] if '/' in url else str(hash(url))
        return f"{self.platform}_{timestamp}_{url_id}"

    def get_stats(self) -> Dict:
        """获取采集统计信息"""
        return {
            "platform": self.platform,
            "total_urls": self.stats.total_urls,
            "successful": self.stats.successful,
            "failed": self.stats.failed,
            "success_rate": self.stats.get_success_rate(),
            "duration": self.stats.get_duration(),
            "credits_used": self.stats.credits_used,
            "errors": self.stats.errors[:5],  # 只返回前 5 个错误
        }
