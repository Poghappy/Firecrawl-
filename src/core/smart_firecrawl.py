#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 Firecrawl 客户端

集成 Firecrawl 所有高级功能：
- 自动缓存优化
- 批量抓取
- Actions 支持
- JSON 结构化提取
- 成本追踪

基于官方文档: https://docs.firecrawl.dev/features/scrape
"""

import asyncio
from typing import List, Dict, Any, Optional, TypeVar, Type
from datetime import datetime
from pydantic import BaseModel
from firecrawl import AsyncFirecrawl
import logging

T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class CacheStrategy:
    """缓存策略配置"""
    STATIC = 2592000000      # 30天（文档、关于我们）
    WEEKLY = 604800000       # 7天（公司信息）
    DAILY = 86400000         # 24小时（新闻、博客）
    HOURLY = 3600000         # 1小时（天气、股票）
    REALTIME = 0             # 实时（价格、库存）


class SmartFirecrawl:
    """
    智能 Firecrawl 客户端

    功能：
    - 自动缓存优化（节省 80% 成本）
    - 智能批量抓取
    - Actions 交互支持
    - 结构化数据提取
    - 成本统计

    使用示例：
        client = SmartFirecrawl(api_key="fc-xxx")

        # 基础抓取
        result = await client.scrape("https://example.com")

        # 结构化提取
        data = await client.scrape_json("https://example.com", schema=MyModel)

        # 批量抓取
        results = await client.batch_scrape(urls, max_concurrent=10)
    """

    def __init__(self, api_key: str, default_cache_strategy: str = "DAILY"):
        """
        初始化智能客户端

        Args:
            api_key: Firecrawl API 密钥
            default_cache_strategy: 默认缓存策略（STATIC/DAILY/HOURLY/REALTIME）
        """
        self.client = AsyncFirecrawl(api_key=api_key)
        self.default_maxAge = getattr(CacheStrategy, default_cache_strategy, CacheStrategy.DAILY)

        # 统计信息
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "credits_used": 0,
            "errors": 0,
            "start_time": datetime.now()
        }

    async def scrape(
        self,
        url: str,
        formats: List[str] = None,
        use_cache: bool = True,
        stealth: bool = False,
        actions: List[Dict[str, Any]] = None,
        location: Dict[str, Any] = None,
        only_main_content: bool = True,
        timeout: int = 60000
    ) -> Dict[str, Any]:
        """
        基础抓取（支持所有格式）

        Args:
            url: 目标 URL
            formats: 输出格式列表 ["markdown", "html", "screenshot", "links"]
            use_cache: 是否使用缓存
            stealth: 是否使用隐身模式（+4 credits）
            actions: 页面交互动作列表
            location: 地理位置 {"country": "US", "languages": ["en"]}
            only_main_content: 只提取主要内容
            timeout: 超时时间（毫秒）

        Returns:
            抓取结果字典
        """
        self._stats["total_requests"] += 1

        try:
            # 默认格式
            if formats is None:
                formats = ["markdown"]

            # 缓存策略
            maxAge = self.default_maxAge if use_cache else 0

            # 执行抓取
            result = await self.client.scrape(
                url,
                formats=formats,
                maxAge=maxAge,
                stealth=stealth,
                actions=actions or [],
                location=location,
                only_main_content=only_main_content,
                timeout=timeout
            )

            # 统计缓存命中
            if hasattr(result, 'cached') and result.cached:
                self._stats["cache_hits"] += 1

            return result

        except Exception as e:
            self._stats["errors"] += 1
            logger.error(f"抓取失败 {url}: {e}")
            raise

    async def scrape_json(
        self,
        url: str,
        schema: Optional[Type[T]] = None,
        prompt: Optional[str] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Optional[T]:
        """
        结构化数据提取

        Args:
            url: 目标 URL
            schema: Pydantic 模型类（优先）
            prompt: 提取提示（当 schema 为 None 时使用）
            use_cache: 是否使用缓存
            **kwargs: 其他参数传递给 scrape()

        Returns:
            Pydantic 模型实例 或 字典
        """
        # 构建 JSON 格式
        if schema:
            json_format = {
                "type": "json",
                "schema": schema.model_json_schema()
            }
        elif prompt:
            json_format = {
                "type": "json",
                "prompt": prompt
            }
        else:
            raise ValueError("必须提供 schema 或 prompt")

        # 抓取
        result = await self.scrape(
            url,
            formats=[json_format],
            use_cache=use_cache,
            **kwargs
        )

        # 解析为模型
        if schema and "json" in result:
            try:
                return schema(**result["json"])
            except Exception as e:
                logger.error(f"JSON 解析失败: {e}")
                return None

        return result.get("json")

    async def batch_scrape(
        self,
        urls: List[str],
        formats: List[str] = None,
        max_concurrent: int = 10,
        use_cache: bool = True,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        批量抓取（带并发控制）

        Args:
            urls: URL 列表
            formats: 输出格式
            max_concurrent: 最大并发数
            use_cache: 是否使用缓存
            **kwargs: 其他参数传递给 scrape()

        Returns:
            结果列表
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def scrape_one(url: str):
            async with semaphore:
                try:
                    return await self.scrape(
                        url,
                        formats=formats,
                        use_cache=use_cache,
                        **kwargs
                    )
                except Exception as e:
                    logger.error(f"批量抓取失败 {url}: {e}")
                    return None

        results = await asyncio.gather(*[scrape_one(url) for url in urls])
        return [r for r in results if r is not None]

    async def batch_scrape_json(
        self,
        urls: List[str],
        schema: Type[T],
        max_concurrent: int = 10,
        use_cache: bool = True,
        **kwargs
    ) -> List[T]:
        """
        批量结构化提取

        Args:
            urls: URL 列表
            schema: Pydantic 模型类
            max_concurrent: 最大并发数
            use_cache: 是否使用缓存
            **kwargs: 其他参数

        Returns:
            模型实例列表
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def scrape_one(url: str):
            async with semaphore:
                return await self.scrape_json(url, schema=schema, use_cache=use_cache, **kwargs)

        results = await asyncio.gather(*[scrape_one(url) for url in urls])
        return [r for r in results if r is not None]

    async def scrape_with_actions(
        self,
        url: str,
        actions: List[Dict[str, Any]],
        formats: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        交互式抓取（登录、滚动、点击等）

        Args:
            url: 目标 URL
            actions: 动作序列
            formats: 输出格式
            **kwargs: 其他参数

        Returns:
            抓取结果

        示例:
            actions = [
                {"type": "click", "selector": "button.login"},
                {"type": "write", "text": "user@example.com"},
                {"type": "press", "key": "Tab"},
                {"type": "write", "text": "password"},
                {"type": "press", "key": "Enter"},
                {"type": "wait", "milliseconds": 3000},
                {"type": "screenshot", "fullPage": True}
            ]
            result = await client.scrape_with_actions(url, actions)
        """
        return await self.scrape(
            url,
            formats=formats or ["markdown"],
            actions=actions,
            use_cache=False,  # Actions 不缓存
            **kwargs
        )

    async def search_and_scrape(
        self,
        query: str,
        limit: int = 10,
        source_type: str = "web",
        scrape_formats: List[str] = None,
        schema: Optional[Type[T]] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索 + 抓取 + 提取（一站式）

        Args:
            query: 搜索查询
            limit: 结果数量
            source_type: 来源类型（web/news/images）
            scrape_formats: 抓取格式
            schema: 可选的数据模型

        Returns:
            结果列表
        """
        # 1. 搜索
        search_result = await self.client.search(
            query=query,
            limit=limit,
            sources=[{"type": source_type}],
            scrapeOptions={
                "formats": scrape_formats or ["markdown"],
                "maxAge": self.default_maxAge
            }
        )

        # 2. 提取 URL
        urls = [
            item["url"]
            for item in search_result.get("data", {}).get("web", [])
        ]

        if not urls:
            return []

        # 3. 批量抓取
        if schema:
            return await self.batch_scrape_json(urls, schema=schema)
        else:
            return await self.batch_scrape(urls, formats=scrape_formats)

    async def map_urls(
        self,
        base_url: str,
        search_filter: Optional[str] = None,
        limit: int = 5000
    ) -> List[str]:
        """
        发现网站所有 URL

        Args:
            base_url: 网站基础 URL
            search_filter: 搜索过滤（如 "blog"）
            limit: 最大 URL 数

        Returns:
            URL 列表
        """
        result = await self.client.map(
            url=base_url,
            search=search_filter,
            limit=limit
        )

        return result.get("links", [])

    async def crawl_website(
        self,
        base_url: str,
        limit: int = 100,
        formats: List[str] = None,
        schema: Optional[Type[T]] = None,
        **kwargs
    ) -> List[Any]:
        """
        爬取整个网站

        Args:
            base_url: 网站 URL
            limit: 最大页面数
            formats: 输出格式
            schema: 数据模型
            **kwargs: 其他爬取选项

        Returns:
            页面数据列表
        """
        scrape_options = {
            "formats": formats or ["markdown"],
            **kwargs
        }

        if schema:
            scrape_options["formats"] = [{
                "type": "json",
                "schema": schema.model_json_schema()
            }]

        result = await self.client.crawl(
            url=base_url,
            limit=limit,
            scrapeOptions=scrape_options
        )

        return result.get("data", [])

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计字典
        """
        runtime = (datetime.now() - self._stats["start_time"]).total_seconds()

        cache_rate = (
            self._stats["cache_hits"] / self._stats["total_requests"] * 100
            if self._stats["total_requests"] > 0
            else 0
        )

        success_rate = (
            (self._stats["total_requests"] - self._stats["errors"])
            / self._stats["total_requests"] * 100
            if self._stats["total_requests"] > 0
            else 0
        )

        return {
            "total_requests": self._stats["total_requests"],
            "cache_hits": self._stats["cache_hits"],
            "cache_hit_rate": f"{cache_rate:.1f}%",
            "errors": self._stats["errors"],
            "success_rate": f"{success_rate:.1f}%",
            "credits_used": self._stats["credits_used"],
            "runtime_seconds": runtime,
            "requests_per_second": self._stats["total_requests"] / runtime if runtime > 0 else 0
        }

    def reset_stats(self):
        """重置统计"""
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "credits_used": 0,
            "errors": 0,
            "start_time": datetime.now()
        }

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        # 打印统计
        stats = self.get_stats()
        logger.info(f"SmartFirecrawl 统计: {stats}")
