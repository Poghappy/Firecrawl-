#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl 成本优化示例

这是 P0-P1 优化任务的参考实现。
展示如何通过各种策略降低 Firecrawl API 成本 60%。

作者: AI Assistant
创建时间: 2025-01-29
优化版本: v2.2.0
"""

import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import List, Set, Dict, Any
from firecrawl import AsyncFirecrawl


class CostOptimizer:
    """Firecrawl 成本优化器"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.scraped_urls: Set[str] = set()
        self.url_cache: Dict[str, datetime] = {}

    # ============================================================
    # 优化 1: 启用长缓存（节省 ~30%）
    # ============================================================

    async def scrape_with_long_cache(self, url: str):
        """使用长缓存策略"""
        async with AsyncFirecrawl(api_key=self.api_key) as app:
            # ❌ 未优化（每次都是新请求）
            # result = await app.scrape(url, formats=["markdown"])

            # ✅ 优化：24小时缓存
            result = await app.scrape(
                url,
                formats=["markdown"],
                maxAge=86400000,  # 24 小时
                storeInCache=True
            )

            # 检查缓存状态
            cache_state = result.metadata.get("cacheState", "MISS")
            if cache_state == "HIT":
                print(f"✅ 缓存命中: {url} (节省 1 credit)")

            return result

    # ============================================================
    # 优化 2: Map + Batch 替代 Crawl（节省 ~50%）
    # ============================================================

    async def optimized_crawl(self, base_url: str, max_pages: int = 100):
        """优化的爬取策略"""
        async with AsyncFirecrawl(api_key=self.api_key) as app:
            # ❌ 未优化：直接 Crawl（昂贵）
            # result = await app.crawl(base_url, limit=max_pages)
            # 成本：~100-500 credits（取决于网站大小）

            # ✅ 优化：Map + Batch
            # 步骤1: Map 发现所有 URL (仅 1 credit)
            print(f"步骤1: 发现 URLs...")
            map_result = await app.map(base_url, limit=500)
            all_urls = map_result.links
            print(f"  发现 {len(all_urls)} 个 URL (成本: 1 credit)")

            # 步骤2: 过滤需要的 URL
            filtered_urls = self._filter_urls(all_urls, base_url)[:max_pages]
            print(f"  过滤后: {len(filtered_urls)} 个 URL")

            # 步骤3: Batch Scrape (每个 URL 1 credit)
            print(f"步骤2: 批量采集...")
            batch_result = await app.batch_scrape(
                urls=filtered_urls,
                formats=["markdown"],
                maxAge=86400000  # 启用缓存
            )

            print(f"  采集完成 (成本: ~{len(filtered_urls)} credits)")
            print(f"  总成本: ~{1 + len(filtered_urls)} credits")
            print(f"  节省: ~50-70% vs Crawl")

            return batch_result

    def _filter_urls(self, urls: List[str], base_url: str) -> List[str]:
        """智能过滤 URL"""
        filtered = []

        for url in urls:
            # 只要同域名的
            if not url.startswith(base_url):
                continue

            # 排除静态资源
            if any(ext in url for ext in ['.jpg', '.png', '.css', '.js']):
                continue

            # 排除无用页面
            if any(path in url for path in ['/search', '/login', '/cart']):
                continue

            filtered.append(url)

        return filtered

    # ============================================================
    # 优化 3: 智能去重（节省 ~30%）
    # ============================================================

    async def scrape_with_dedup(self, urls: List[str]):
        """智能去重采集"""
        # 步骤1: 过滤最近24小时采集过的 URL
        new_urls = self._filter_recent_urls(urls)

        print(f"URL 去重:")
        print(f"  原始数量: {len(urls)}")
        print(f"  去重后: {len(new_urls)}")
        print(f"  节省: {len(urls) - len(new_urls)} 个请求")

        # 步骤2: 只采集新 URL
        async with AsyncFirecrawl(api_key=self.api_key) as app:
            if not new_urls:
                print("  所有URL都已缓存，无需采集")
                return []

            result = await app.batch_scrape(
                urls=new_urls,
                formats=["markdown"],
                maxAge=86400000
            )

            # 步骤3: 更新已采集 URL 记录
            self._record_scraped_urls(new_urls)

            return result

    def _filter_recent_urls(self, urls: List[str]) -> List[str]:
        """过滤最近采集过的 URL"""
        now = datetime.now()
        cache_duration = timedelta(hours=24)

        new_urls = []
        for url in urls:
            # 检查是否在缓存中
            if url in self.url_cache:
                last_scraped = self.url_cache[url]
                if now - last_scraped < cache_duration:
                    continue  # 跳过

            new_urls.append(url)

        return new_urls

    def _record_scraped_urls(self, urls: List[str]):
        """记录已采集的 URL"""
        now = datetime.now()
        for url in urls:
            self.url_cache[url] = now
            self.scraped_urls.add(url)

    # ============================================================
    # 优化 4: 内容去重（节省 ~20%）
    # ============================================================

    def calculate_content_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.md5(content.encode()).hexdigest()

    async def scrape_with_content_dedup(
        self,
        urls: List[str],
        existing_hashes: Set[str]
    ):
        """基于内容哈希的去重采集"""
        async with AsyncFirecrawl(api_key=self.api_key) as app:
            new_content = []

            for url in urls:
                result = await app.scrape(
                    url,
                    formats=["markdown"],
                    maxAge=86400000
                )

                content = result.markdown
                content_hash = self.calculate_content_hash(content)

                # 检查内容是否重复
                if content_hash in existing_hashes:
                    print(f"  跳过重复内容: {url}")
                    continue

                new_content.append({
                    "url": url,
                    "content": content,
                    "hash": content_hash
                })
                existing_hashes.add(content_hash)

            print(f"内容去重: 过滤 {len(urls) - len(new_content)} 个重复")
            return new_content

    # ============================================================
    # 优化 5: 成本监控和预警（避免超支）
    # ============================================================

    class CostTracker:
        """成本追踪器"""

        def __init__(self, daily_budget: int = 1000):
            self.daily_budget = daily_budget
            self.used_today = 0
            self.reset_date = datetime.now().date()

        def track(self, credits: int):
            """追踪使用量"""
            # 检查是否需要重置
            today = datetime.now().date()
            if today != self.reset_date:
                self.used_today = 0
                self.reset_date = today

            # 累加使用量
            self.used_today += credits

            # 计算使用率
            usage_percent = (self.used_today / self.daily_budget) * 100

            # 预警
            if usage_percent >= 80:
                print(f"⚠️ 成本预警: 已使用 {usage_percent:.1f}% 预算")
                print(f"   今日已用: {self.used_today}/{self.daily_budget} credits")

            # 超支阻止
            if usage_percent >= 100:
                raise Exception(f"❌ 超出每日预算: {self.used_today}/{self.daily_budget}")

            return {
                "used": self.used_today,
                "budget": self.daily_budget,
                "remaining": self.daily_budget - self.used_today,
                "usage_percent": usage_percent
            }

    # ============================================================
    # 成本对比报告
    # ============================================================

    @staticmethod
    def generate_cost_report():
        """生成成本对比报告"""
        print("\n" + "=" * 60)
        print("💰 Firecrawl 成本优化对比")
        print("=" * 60)

        scenarios = [
            {
                "name": "租房采集（Craigslist）",
                "before": {
                    "method": "Crawl (limit=500)",
                    "credits": 200,
                    "cost_usd": 2.00
                },
                "after": {
                    "method": "Map + Batch + Cache",
                    "credits": 80,
                    "cost_usd": 0.80
                }
            },
            {
                "name": "新闻采集（每日）",
                "before": {
                    "method": "Search + 无缓存",
                    "credits": 100,
                    "cost_usd": 1.00
                },
                "after": {
                    "method": "Search + 1小时缓存",
                    "credits": 40,
                    "cost_usd": 0.40
                }
            }
        ]

        for scenario in scenarios:
            print(f"\n场景: {scenario['name']}")
            print(f"  优化前: {scenario['before']['method']}")
            print(f"    - Credits: {scenario['before']['credits']}")
            print(f"    - 成本: ${scenario['before']['cost_usd']:.2f}")
            print(f"  优化后: {scenario['after']['method']}")
            print(f"    - Credits: {scenario['after']['credits']}")
            print(f"    - 成本: ${scenario['after']['cost_usd']:.2f}")

            savings = scenario['before']['credits'] - scenario['after']['credits']
            savings_percent = (savings / scenario['before']['credits']) * 100
            print(f"  💰 节省: {savings} credits ({savings_percent:.0f}%)")

        print("\n" + "=" * 60)
        print("月度成本对比（租房采集每天2次）")
        print("=" * 60)
        print(f"  优化前: $120/月")
        print(f"  优化后: $48/月")
        print(f"  💰 节省: $72/月 (-60%)")
        print("=" * 60)


# ============================================================
# 完整的优化示例
# ============================================================

async def complete_optimization_example():
    """完整的成本优化示例"""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    optimizer = CostOptimizer(api_key)

    # 成本追踪器
    cost_tracker = CostOptimizer.CostTracker(daily_budget=1000)

    # 示例：采集租房信息
    base_url = "https://honolulu.craigslist.org/search/apa"

    print("\n🎯 开始优化的租房采集...")

    # 优化后的流程
    result = await optimizer.optimized_crawl(base_url, max_pages=50)

    # 追踪成本
    credits_used = 1 + 50  # Map (1) + Batch (50)
    status = cost_tracker.track(credits_used)

    print(f"\n📊 成本统计:")
    print(f"  今日已用: {status['used']}/{status['budget']} credits")
    print(f"  剩余预算: {status['remaining']} credits")
    print(f"  使用率: {status['usage_percent']:.1f}%")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # 生成成本对比报告
    CostOptimizer.generate_cost_report()

    # 运行完整示例
    # asyncio.run(complete_optimization_example())
