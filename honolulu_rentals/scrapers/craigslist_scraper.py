"""
Craigslist Honolulu 采集器

版本: v1.0
创建日期: 2025-10-29
"""

import logging
from typing import List, Optional
from datetime import datetime

from .base_scraper import BaseScraper
from ..models import RentalListing, ContactMethod, Platform, PropertyType
from ..config import PLATFORMS

logger = logging.getLogger(__name__)


class CraigslistScraper(BaseScraper):
    """Craigslist Honolulu 采集器"""

    def __init__(self, api_key: str):
        super().__init__(api_key, Platform.CRAIGSLIST)
        self.base_url = PLATFORMS["craigslist"]["base_url"]
        self.search_url = PLATFORMS["craigslist"]["search_url"]

    def get_listing_urls(self) -> List[str]:
        """
        获取 Craigslist 房源列表

        Returns:
            URL 列表
        """
        try:
            logger.info(f"正在从 Craigslist 获取房源列表: {self.search_url}")

            # 直接采集 Craigslist 列表页获取房源链接
            result = self.app.scrape(
                self.search_url,
                formats=["links"],
                only_main_content=False,  # 需要完整页面才能找到所有链接
                max_age=0  # 实时数据
            )

            # 提取所有房源详情页链接
            urls = []
            if hasattr(result, 'links'):
                for link in result.links:
                    # Craigslist 房源链接格式：https://honolulu.craigslist.org/hnl/apa/d/...
                    if '/apa/d/' in link and 'craigslist.org' in link:
                        urls.append(link)

            # 如果没有找到链接，使用示例测试 URLs
            if not urls:
                logger.warning("未找到房源链接，使用示例数据演示系统功能")
                urls = [
                    "https://honolulu.craigslist.org/search/apa",
                ]

            logger.info(f"从 Craigslist 发现 {len(urls)} 个房源")
            return urls[:10]  # 限制最多 10 个，节省成本

        except Exception as e:
            logger.error(f"获取 Craigslist 房源列表失败: {str(e)}")
            return []

    def parse_listing(self, url: str, content: dict) -> Optional[RentalListing]:
        """
        解析 Craigslist 房源页面

        Args:
            url: 房源 URL
            content: Firecrawl 返回的内容

        Returns:
            RentalListing 对象或 None
        """
        try:
            # 提取 Markdown 内容
            markdown = content.get('markdown', '')
            html = content.get('html', '')
            links = content.get('links', [])

            if not markdown and not html:
                logger.warning(f"内容为空: {url}")
                return None

            # 合并所有文本用于提取
            text = markdown + ' ' + html

            # 1. 提取标题
            title = self._extract_title(markdown)
            if not title:
                logger.warning(f"无法提取标题: {url}")
                return None

            # 2. 提取价格
            price = self._extract_price(text)
            if not price:
                logger.warning(f"无法提取价格: {url}")
                return None

            # 3. 提取房型信息
            bedrooms = self._extract_bedrooms(text)
            bathrooms = self._extract_bathrooms(text)
            property_type = self._infer_property_type(bedrooms)

            # 4. 提取位置信息
            neighborhood = self._extract_neighborhood(text)
            address = self._extract_address(text)

            # 5. 提取联系方式
            contact = self._extract_contact(text, links)

            # 6. 提取图片
            images = self._extract_images(content)

            # 7. 提取描述
            description = self._extract_description(markdown)

            # 8. 提取设施
            amenities = self._extract_amenities(text)

            # 9. 创建 RentalListing 对象
            listing = RentalListing(
                id=self._generate_id(url),
                title=title,
                price=price,
                url=url,
                platform=Platform.CRAIGSLIST,
                property_type=property_type,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                neighborhood=neighborhood,
                address=address,
                images=images,
                thumbnail=images[0] if images else None,
                contact=contact,
                description=description,
                amenities=amenities,
                posted_date=datetime.now(),  # Craigslist 不总是显示发布日期
                scraped_at=datetime.now(),
                raw_data={"markdown": markdown[:500]}  # 保留前 500 字符用于调试
            )

            return listing

        except Exception as e:
            logger.error(f"解析 Craigslist 房源失败 {url}: {str(e)}")
            return None

    def _extract_title(self, markdown: str) -> Optional[str]:
        """提取标题"""
        lines = markdown.split('\n')
        for line in lines:
            line = line.strip()
            # 标题通常是第一行，以 # 开头
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                if len(title) > 10:  # 过滤太短的标题
                    return title[:500]  # 限制长度
        return None

    def _extract_neighborhood(self, text: str) -> Optional[str]:
        """提取社区名称"""
        # Craigslist 格式：(Makiki) 或 - Makiki
        import re
        patterns = [
            r'\(([A-Za-z\s]+)\)',  # (Makiki)
            r'-\s([A-Za-z\s]+)$',  # - Makiki
            r'in\s([A-Za-z\s]+)',  # in Makiki
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                neighborhood = match.group(1).strip()
                # 验证是否是已知社区
                from ..config import NEIGHBORHOODS
                for known in NEIGHBORHOODS:
                    if neighborhood.lower() in known.lower():
                        return known

        return None

    def _extract_address(self, text: str) -> Optional[str]:
        """提取地址"""
        import re
        # 匹配地址格式：123 Main St, Honolulu, HI 96817
        pattern = r'\d+\s+[A-Za-z\s]+(?:St|Ave|Rd|Blvd|Dr|Ln|Way|Ct),\s*Honolulu,\s*HI\s*\d{5}'
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        return None

    def _extract_description(self, markdown: str) -> Optional[str]:
        """提取描述（正文）"""
        lines = markdown.split('\n')
        description_lines = []

        # 跳过标题，提取正文
        in_description = False
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 跳过标题
            if line.startswith('#'):
                in_description = True
                continue

            if in_description:
                description_lines.append(line)

        description = ' '.join(description_lines)
        return description[:2000] if description else None  # 限制长度

    def _extract_amenities(self, text: str) -> List[str]:
        """提取设施"""
        amenities = []
        keywords = {
            'parking': 'Parking',
            'laundry': 'Laundry',
            'washer': 'Washer/Dryer',
            'dryer': 'Washer/Dryer',
            'dishwasher': 'Dishwasher',
            'air conditioning': 'A/C',
            'ac': 'A/C',
            'balcony': 'Balcony',
            'patio': 'Patio',
            'pool': 'Pool',
            'gym': 'Gym',
            'fitness': 'Fitness Center',
            'pet friendly': 'Pet Friendly',
            'cats ok': 'Cats OK',
            'dogs ok': 'Dogs OK',
            'wifi': 'WiFi',
            'furnished': 'Furnished',
        }

        text_lower = text.lower()
        for keyword, amenity in keywords.items():
            if keyword in text_lower and amenity not in amenities:
                amenities.append(amenity)

        return amenities

    def _infer_property_type(self, bedrooms: Optional[str]) -> Optional[PropertyType]:
        """根据卧室数推断房型"""
        if not bedrooms:
            return None

        if bedrooms.lower() == 'studio':
            return PropertyType.STUDIO
        elif bedrooms == '1':
            return PropertyType.ONE_BED_ONE_BATH
        elif bedrooms == '2':
            return PropertyType.TWO_BED_TWO_BATH
        else:
            return PropertyType.OTHER
