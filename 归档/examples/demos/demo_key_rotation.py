#!/usr/bin/env python3
"""API 密钥轮换演示脚本.

演示如何使用多个 API 密钥实现：
1. 负载均衡
2. 速率限制突破
3. 高可用性
"""

import itertools
import logging
import time
from typing import Any, List, Optional

from firecrawl import FirecrawlApp


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 您的 4 个有效 API 密钥
API_KEYS = [
    "fc-31ebbe4647b84fdc975318d372eebea8",  # main
    "fc-00857d82ec534e8598df1bae9af9fb28",  # backup_1（最快）
    "fc-9eb380b0dec74d6ebb6c756ee4de4c5a",  # backup_2
    "fc-0a2c801f433d4718bcd8189f2742edf4",  # backup_3
]


class RotatingFirecrawlClient:
    """支持密钥轮换的 Firecrawl 客户端.

    特性：
    - 自动密钥轮换（循环使用）
    - 速率限制自动切换
    - 请求统计和监控
    - 错误自动重试
    """

    def __init__(self, api_keys: List[str]) -> None:
        """初始化客户端.

        Args:
            api_keys: API 密钥列表
        """
        if not api_keys:
            raise ValueError("至少需要提供一个 API 密钥")

        self.api_keys = api_keys
        self.key_cycle = itertools.cycle(api_keys)
        self.current_key = next(self.key_cycle)
        self.app = FirecrawlApp(api_key=self.current_key)

        # 统计信息
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.key_switches = 0
        self.key_usage = {self._mask_key(key): 0 for key in api_keys}

        logging.info(f"✅ 初始化完成，共 {len(api_keys)} 个密钥可用")

    def _mask_key(self, key: str) -> str:
        """隐藏 API 密钥.

        Args:
            key: 完整的 API 密钥

        Returns:
            隐藏后的密钥字符串
        """
        return f"{key[:8]}...{key[-4:]}"

    def _switch_key(self) -> None:
        """切换到下一个 API 密钥."""
        self.current_key = next(self.key_cycle)
        self.app = FirecrawlApp(api_key=self.current_key)
        self.key_switches += 1

        masked_key = self._mask_key(self.current_key)
        logging.info(f"🔄 切换密钥: {masked_key}")

    def scrape(
        self,
        url: str,
        max_retries: int = 3,
        **kwargs: Any,
    ) -> Optional[Any]:
        """爬取网页（带重试和密钥轮换）.

        Args:
            url: 要爬取的 URL
            max_retries: 最大重试次数
            **kwargs: 传递给 scrape 的其他参数

        Returns:
            爬取结果，失败返回 None
        """
        self.total_requests += 1
        masked_key = self._mask_key(self.current_key)

        for attempt in range(max_retries):
            try:
                # 记录密钥使用
                self.key_usage[masked_key] = self.key_usage.get(masked_key, 0) + 1

                # 执行爬取
                result = self.app.scrape(url=url, **kwargs)

                self.successful_requests += 1
                logging.info(f"✅ 成功爬取: {url[:50]} (密钥: {masked_key})")
                return result

            except Exception as e:
                error_msg = str(e).lower()

                # 判断是否为速率限制
                if "rate limit" in error_msg or "429" in error_msg:
                    logging.warning(
                        f"⚠️ 速率限制，切换密钥... (尝试 {attempt + 1}/{max_retries})"
                    )
                    self._switch_key()
                    masked_key = self._mask_key(self.current_key)
                    time.sleep(1)  # 短暂延迟
                    continue

                # 其他错误
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logging.warning(
                        f"⚠️ 爬取失败，{wait_time}秒后重试... "
                        f"({attempt + 1}/{max_retries}): {e}"
                    )
                    time.sleep(wait_time)
                else:
                    self.failed_requests += 1
                    logging.error(f"❌ 爬取失败（{max_retries}次重试后）: {url}")

        return None

    def batch_scrape(
        self,
        urls: List[str],
        **kwargs: Any,
    ) -> Any:
        """批量爬取（自动负载均衡）.

        Args:
            urls: URL 列表
            **kwargs: 传递给 batch_scrape 的其他参数

        Returns:
            批量爬取结果
        """
        self.total_requests += len(urls)
        masked_key = self._mask_key(self.current_key)

        logging.info(f"📦 批量爬取 {len(urls)} 个 URL (密钥: {masked_key})")

        try:
            result = self.app.batch_scrape(urls=urls, **kwargs)
            self.successful_requests += len(urls)
            return result

        except Exception as e:
            self.failed_requests += len(urls)
            logging.error(f"❌ 批量爬取失败: {e}")
            raise

    def get_stats(self) -> dict:
        """获取统计信息.

        Returns:
            包含各项统计数据的字典
        """
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (
                self.successful_requests / self.total_requests * 100
                if self.total_requests > 0
                else 0
            ),
            "key_switches": self.key_switches,
            "key_usage": self.key_usage,
        }

    def print_stats(self) -> None:
        """打印统计信息."""
        stats = self.get_stats()

        print("\n" + "=" * 60)
        print("📊 密钥轮换统计")
        print("=" * 60)
        print(f"总请求数: {stats['total_requests']}")
        print(f"成功: {stats['successful_requests']}")
        print(f"失败: {stats['failed_requests']}")
        print(f"成功率: {stats['success_rate']:.1f}%")
        print(f"密钥切换次数: {stats['key_switches']}")

        print("\n密钥使用分布:")
        for key, count in stats["key_usage"].items():
            print(f"  {key}: {count} 次")
        print("=" * 60)


def demo_single_scrape(client: RotatingFirecrawlClient) -> None:
    """演示 1: 单个网页爬取.

    Args:
        client: Firecrawl 客户端实例
    """
    print("\n" + "🔥" * 30)
    print("演示 1: 单个网页爬取")
    print("🔥" * 30)

    url = "https://www.firecrawl.dev/"

    result = client.scrape(
        url=url,
        formats=["markdown"],
        only_main_content=True,
        max_age=172800000,  # 2天缓存
    )

    if result:
        content = str(getattr(result, "markdown", ""))
        print(f"✅ 爬取成功！内容长度: {len(content)} 字符")


def demo_multiple_scrapes(client: RotatingFirecrawlClient) -> None:
    """演示 2: 多次爬取（触发密钥轮换）.

    Args:
        client: Firecrawl 客户端实例
    """
    print("\n" + "🔥" * 30)
    print("演示 2: 多次爬取（密钥轮换）")
    print("🔥" * 30)

    # 爬取多个夏威夷新闻网站
    urls = [
        "https://www.hawaiinewsnow.com/",
        "https://www.staradvertiser.com/",
        "https://www.civilbeat.org/",
        "https://www.khon2.com/",
    ]

    for i, url in enumerate(urls, 1):
        print(f"\n爬取 {i}/{len(urls)}: {url}")
        result = client.scrape(
            url=url,
            formats=["markdown"],
            only_main_content=True,
        )

        if result:
            content = str(getattr(result, "markdown", ""))
            print(f"✅ 成功，内容: {len(content)} 字符")

        # 短暂延迟
        time.sleep(0.5)


def demo_batch_scrape(client: RotatingFirecrawlClient) -> None:
    """演示 3: 批量爬取.

    Args:
        client: Firecrawl 客户端实例
    """
    print("\n" + "🔥" * 30)
    print("演示 3: 批量爬取")
    print("🔥" * 30)

    urls = [
        "https://www.hawaiinewsnow.com/",
        "https://www.staradvertiser.com/",
        "https://www.civilbeat.org/",
    ]

    batch_job = client.batch_scrape(
        urls=urls,
        formats=["markdown"],
        only_main_content=True,
    )

    if batch_job and batch_job.data:
        print(f"✅ 批量爬取成功！获得 {len(batch_job.data)} 个结果")


def main() -> None:
    """主函数.

    演示密钥轮换的各种使用场景
    """
    print("\n" + "🎯" * 30)
    print("Firecrawl API 密钥轮换演示")
    print("🎯" * 30)

    # 初始化客户端
    client = RotatingFirecrawlClient(api_keys=API_KEYS)

    try:
        # 演示 1: 单个爬取
        demo_single_scrape(client)

        # 演示 2: 多次爬取
        demo_multiple_scrapes(client)

        # 演示 3: 批量爬取
        demo_batch_scrape(client)

        # 打印统计
        client.print_stats()

        # 总结
        print("\n" + "=" * 60)
        print("🎉 演示完成！")
        print("=" * 60)
        print("\n💡 密钥轮换的好处:")
        print("1. 突破单个密钥的速率限制")
        print("2. 提高系统可用性（故障转移）")
        print("3. 负载均衡，提升性能")
        print("4. 成本优化（使用不同计划的密钥）")

    except Exception as e:
        logging.error(f"❌ 演示过程中出错: {e}")
        client.print_stats()


if __name__ == "__main__":
    main()
