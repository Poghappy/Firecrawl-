#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一的 BaseAgent 示例代码

这是 P0-A1 优化任务的参考实现。
将 BaseScraper 和 BaseAgent 统一为一个类。

作者: AI Assistant
创建时间: 2025-01-29
优化版本: v2.2.0
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypeVar, Generic
from datetime import datetime
from dataclasses import dataclass, field

from firecrawl import AsyncFirecrawl
from pydantic import BaseModel


logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)  # 泛型：数据模型类型


@dataclass
class AgentConfig:
    """智能体配置"""
    name: str
    type: str
    api_key: str
    max_concurrent: int = 10
    timeout: int = 120
    max_retries: int = 3
    retry_delay: float = 2.0
    enable_cache: bool = True
    max_age: int = 172800000  # 2 天
    proxy: str = "basic"
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectionResult(Generic[T]):
    """采集结果（泛型）"""
    success: bool
    data: List[T]
    errors: List[str] = field(default_factory=list)
    credits_used: int = 0
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.now)


class BaseAgent(ABC, Generic[T]):
    """
    统一的智能体基类（泛型版本）

    所有业务场景的智能体都应继承此类。

    泛型参数:
        T: 数据模型类型（必须继承 BaseModel）

    使用示例:
        class NewsAgent(BaseAgent[NewsArticle]):
            async def collect(self, params: dict) -> List[dict]:
                # 采集逻辑
                pass

            async def parse(self, raw_data: List[dict]) -> List[NewsArticle]:
                # 解析逻辑
                return [NewsArticle(**item) for item in raw_data]
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client: Optional[AsyncFirecrawl] = None
        self.semaphore = asyncio.Semaphore(config.max_concurrent)
        self.logger = logging.getLogger(f"{__name__}.{config.name}")

        # 统计信息
        self.stats = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_credits": 0,
            "total_duration": 0.0,
        }

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.client = AsyncFirecrawl(api_key=self.config.api_key)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    @abstractmethod
    async def collect(self, params: Dict[str, Any]) -> List[dict]:
        """
        采集原始数据（必须实现）

        Args:
            params: 采集参数

        Returns:
            原始数据列表（dict 格式）
        """
        pass

    @abstractmethod
    async def parse(self, raw_data: List[dict]) -> List[T]:
        """
        解析原始数据为 Pydantic 模型（必须实现）

        Args:
            raw_data: 原始数据列表

        Returns:
            Pydantic 模型列表
        """
        pass

    async def execute(
        self,
        params: Dict[str, Any]
    ) -> CollectionResult[T]:
        """
        完整的执行流程

        流程:
            1. 采集原始数据 (collect)
            2. 解析为 Pydantic 模型 (parse)
            3. 验证数据 (validate)
            4. 返回结果

        Args:
            params: 采集参数

        Returns:
            CollectionResult: 包含采集结果的对象
        """
        start_time = datetime.now()
        errors = []

        try:
            # 步骤1: 采集
            self.logger.info(f"开始采集: {params}")
            raw_data = await self.collect(params)

            # 步骤2: 解析
            self.logger.info(f"解析数据: {len(raw_data)} 条原始记录")
            parsed_data = await self.parse(raw_data)

            # 步骤3: 验证
            self.logger.info(f"验证数据: {len(parsed_data)} 条解析记录")
            validated_data = await self.validate_batch(parsed_data)

            # 更新统计
            self.stats["successful_tasks"] += 1

            return CollectionResult(
                success=True,
                data=validated_data,
                duration=(datetime.now() - start_time).total_seconds(),
                completed_at=datetime.now()
            )

        except Exception as e:
            self.logger.error(f"执行失败: {str(e)}")
            errors.append(str(e))
            self.stats["failed_tasks"] += 1

            return CollectionResult(
                success=False,
                data=[],
                errors=errors,
                duration=(datetime.now() - start_time).total_seconds(),
                completed_at=datetime.now()
            )

        finally:
            self.stats["total_tasks"] += 1

    async def validate_batch(self, data: List[T]) -> List[T]:
        """
        批量验证数据

        Args:
            data: Pydantic 模型列表

        Returns:
            验证通过的数据列表
        """
        validated = []
        for item in data:
            try:
                # Pydantic 模型已自动验证
                validated.append(item)
            except Exception as e:
                self.logger.warning(f"数据验证失败: {e}")

        return validated

    async def retry_with_backoff(
        self,
        func,
        *args,
        **kwargs
    ) -> Any:
        """
        带指数退避的重试

        Args:
            func: 要执行的函数
            *args, **kwargs: 函数参数

        Returns:
            函数执行结果
        """
        for attempt in range(self.config.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise

                wait_time = self.config.retry_delay * (2 ** attempt)
                self.logger.warning(
                    f"重试 {attempt + 1}/{self.config.max_retries}，"
                    f"等待 {wait_time}s: {e}"
                )
                await asyncio.sleep(wait_time)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_tasks"] / self.stats["total_tasks"]
                if self.stats["total_tasks"] > 0 else 0
            ),
            "avg_duration": (
                self.stats["total_duration"] / self.stats["total_tasks"]
                if self.stats["total_tasks"] > 0 else 0
            )
        }


# ============================================================
# 使用示例：新闻采集智能体
# ============================================================

class NewsArticle(BaseModel):
    """新闻文章模型"""
    title: str
    content: str
    url: str
    publish_date: datetime
    author: Optional[str] = None


class NewsAgent(BaseAgent[NewsArticle]):
    """新闻采集智能体"""

    async def collect(self, params: Dict[str, Any]) -> List[dict]:
        """采集新闻数据"""
        keywords = params.get("keywords", "hawaii")
        limit = params.get("limit", 20)

        # 使用 Firecrawl Search API
        result = await self.client.search(
            query=f"{keywords} site:hawaiinewsnow.com",
            limit=limit,
            sources=[{"type": "news"}],
            scrapeOptions={
                "formats": ["markdown"],
                "onlyMainContent": True,
                "maxAge": self.config.max_age
            }
        )

        # 返回原始数据
        return result.data if hasattr(result, 'data') else []

    async def parse(self, raw_data: List[dict]) -> List[NewsArticle]:
        """解析为 NewsArticle 模型"""
        articles = []

        for item in raw_data:
            try:
                article = NewsArticle(
                    title=item.get("title", ""),
                    content=item.get("markdown", ""),
                    url=item.get("url", ""),
                    publish_date=datetime.now(),
                    author=item.get("author")
                )
                articles.append(article)
            except Exception as e:
                self.logger.warning(f"解析失败: {e}")

        return articles


# ============================================================
# 使用示例：租房采集智能体
# ============================================================

class RentalListing(BaseModel):
    """租房信息模型"""
    title: str
    price: float
    bedrooms: int
    url: str
    description: str


class RentalAgent(BaseAgent[RentalListing]):
    """租房采集智能体"""

    async def collect(self, params: Dict[str, Any]) -> List[dict]:
        """采集租房数据"""
        # 步骤1: Map 发现 URLs
        map_result = await self.client.map(
            "https://honolulu.craigslist.org/search/apa",
            limit=200
        )

        # 步骤2: 过滤房源 URLs
        listing_urls = [
            url for url in map_result.links
            if '/apa/' in url
        ][:50]  # 只采集前50个

        # 步骤3: Batch Scrape
        batch_result = await self.client.batch_scrape(
            urls=listing_urls,
            formats=["markdown"]
        )

        return batch_result.data if hasattr(batch_result, 'data') else []

    async def parse(self, raw_data: List[dict]) -> List[RentalListing]:
        """解析为 RentalListing 模型"""
        listings = []

        for item in raw_data:
            # 从 markdown 中提取信息（简化示例）
            markdown = item.get("markdown", "")

            try:
                listing = RentalListing(
                    title=item.get("metadata", {}).get("title", ""),
                    price=self._extract_price(markdown),
                    bedrooms=self._extract_bedrooms(markdown),
                    url=item.get("metadata", {}).get("url", ""),
                    description=markdown[:500]
                )
                listings.append(listing)
            except Exception as e:
                self.logger.warning(f"解析失败: {e}")

        return listings

    def _extract_price(self, text: str) -> float:
        """从文本中提取价格"""
        import re
        match = re.search(r'\$(\d+,?\d*)', text)
        if match:
            return float(match.group(1).replace(',', ''))
        return 0.0

    def _extract_bedrooms(self, text: str) -> int:
        """从文本中提取卧室数"""
        import re
        match = re.search(r'(\d+)\s*br', text.lower())
        if match:
            return int(match.group(1))
        return 1


# ============================================================
# 测试代码
# ============================================================

async def test_news_agent():
    """测试新闻智能体"""
    config = AgentConfig(
        name="测试新闻智能体",
        type="news",
        api_key=os.getenv("FIRECRAWL_API_KEY"),
        max_concurrent=5
    )

    async with NewsAgent(config) as agent:
        result = await agent.execute({
            "keywords": "hawaii tourism",
            "limit": 5
        })

        print(f"成功: {result.success}")
        print(f"采集数量: {len(result.data)}")
        print(f"耗时: {result.duration:.2f}s")

        for article in result.data[:3]:
            print(f"\n标题: {article.title}")
            print(f"链接: {article.url}")


async def test_rental_agent():
    """测试租房智能体"""
    config = AgentConfig(
        name="测试租房智能体",
        type="rental",
        api_key=os.getenv("FIRECRAWL_API_KEY"),
        max_concurrent=8
    )

    async with RentalAgent(config) as agent:
        result = await agent.execute({})

        print(f"成功: {result.success}")
        print(f"房源数量: {len(result.data)}")
        print(f"耗时: {result.duration:.2f}s")

        for listing in result.data[:3]:
            print(f"\n标题: {listing.title}")
            print(f"价格: ${listing.price}")
            print(f"卧室: {listing.bedrooms}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    print("=" * 60)
    print("测试统一的 BaseAgent")
    print("=" * 60)

    # 测试新闻智能体
    print("\n1. 测试新闻智能体...")
    asyncio.run(test_news_agent())

    # 测试租房智能体
    print("\n2. 测试租房智能体...")
    asyncio.run(test_rental_agent())

    print("\n✅ 测试完成")
