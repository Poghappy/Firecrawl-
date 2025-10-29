#!/usr/bin/env python3
"""HawaiiHub 新闻采集系统 - 主程序

一键运行完整的新闻采集流程
"""

import argparse
import logging
import logging.config
import sys
from datetime import datetime

from scraper import HawaiiHubNewsScraper
from storage import NewsStorage

# 本地模块导入（相对路径，无需修改 sys.path）
from config import (
    ALL_NEWS_SOURCES,
    LOGGING_CONFIG,
    get_enabled_sources,
    get_source_by_id,
    get_sources_by_priority,
)


# 配置日志
try:
    logging.config.dictConfig(LOGGING_CONFIG)  # type: ignore[arg-type]
except Exception as _e:
    # 回退到基本配置，避免因配置错误导致崩溃
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    logging.getLogger(__name__).warning("日志配置无效，已回退到 basicConfig: %s", _e)
logger = logging.getLogger(__name__)


def print_banner() -> None:
    """打印程序横幅"""
    print("\n" + "=" * 70)
    print("  🏝️  HawaiiHub 新闻采集系统")
    print("  📰 Hawaii News Scraping System")
    print("=" * 70)
    print(f"  启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")


def scrape_all_news(scraper: HawaiiHubNewsScraper, storage: NewsStorage) -> None:
    """采集所有新闻源

    Args:
        scraper: 采集器实例
        storage: 存储管理器实例
    """
    logger.info("🚀 开始采集所有新闻源")

    # 获取启用的新闻源
    sources = get_enabled_sources()
    logger.info(f"📋 共 {len(sources)} 个启用的新闻源")

    # 执行采集
    results = scraper.scrape_all_sources(sources)

    # 保存原始数据
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    storage.save_raw_data(results, f"all_sources_{timestamp}.json")

    # 导出到多种格式
    exported = storage.export_news_results(results, prefix="hawaiihub_news")

    # 打印统计
    stats = scraper.get_stats() or {}
    request_count = int(stats.get("request_count", 0) or 0)
    success_count = int(stats.get("success_count", 0) or 0)
    failure_count = int(stats.get("failure_count", 0) or 0)
    try:
        total_cost = float(stats.get("total_cost", 0.0) or 0.0)
    except (TypeError, ValueError):
        total_cost = 0.0
    try:
        remaining_budget = float(stats.get("remaining_budget", 0.0) or 0.0)
    except (TypeError, ValueError):
        remaining_budget = 0.0
    success_rate = (success_count / request_count * 100.0) if request_count else None

    logger.info("\n📊 最终统计:")
    logger.info(f"   总请求数: {request_count}")
    logger.info(f"   成功请求: {success_count}")
    logger.info(f"   失败请求: {failure_count}")
    logger.info(
        f"   成功率: {success_rate:.1f}%"
        if success_rate is not None
        else "   成功率: N/A"
    )
    logger.info(f"   总成本: ${total_cost:.2f}")
    logger.info(f"   剩余预算: ${remaining_budget:.2f}")

    if not exported:
        logger.warning("\n📁 未生成导出文件")
    else:
        logger.info("\n📁 导出文件:")
        for format_name, filepath in exported.items():
            logger.info(f"   {format_name.upper()}: {filepath}")


def scrape_by_priority(
    scraper: HawaiiHubNewsScraper,
    storage: NewsStorage,
    priority: str = "P0",
) -> None:
    """按优先级采集

    Args:
        scraper: 采集器实例
        storage: 存储管理器实例
        priority: 优先级（P0/P1/P2）
    """
    logger.info(f"🎯 采集 {priority} 优先级新闻源")

    sources = get_sources_by_priority(priority)
    logger.info(f"📋 共 {len(sources)} 个 {priority} 新闻源")

    if not sources:
        logger.warning(f"没有找到 {priority} 优先级的新闻源")
        return

    # 执行采集
    results = scraper.scrape_all_sources(sources)

    # 保存和导出
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    storage.save_raw_data(results, f"{priority.lower()}_{timestamp}.json")
    storage.export_news_results(results, prefix=f"news_{priority.lower()}")


def scrape_single_source(
    scraper: HawaiiHubNewsScraper,
    storage: NewsStorage,
    source_id: str,
) -> None:
    """采集单个新闻源

    Args:
        scraper: 采集器实例
        storage: 存储管理器实例
        source_id: 新闻源 ID
    """
    logger.info(f"📰 采集单个新闻源: {source_id}")

    source_config = get_source_by_id(source_id)

    if not source_config:
        logger.error(f"未找到新闻源: {source_id}")
        logger.info("可用的新闻源:")
        for s in ALL_NEWS_SOURCES:
            logger.info(f"   - {s['id']}: {s['name']}")
        return

    # 执行采集
    result = scraper.scrape_news_source(source_config)

    # 保存和导出
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    storage.save_raw_data(result, f"{source_id}_{timestamp}.json")
    storage.export_news_results([result], prefix=source_id)


def list_sources() -> None:
    """列出所有新闻源"""
    print("\n" + "=" * 70)
    print("  📋 可用新闻源列表")
    print("=" * 70 + "\n")

    sources = ALL_NEWS_SOURCES

    for i, source in enumerate(sources, 1):
        status = "✅" if source.get("enabled", True) else "❌"
        priority = source.get("priority", "P?")
        name = source.get("name", "<未命名>")
        print(f"{i}. {status} [{priority}] {name}")
        print(f"   ID: {source.get('id', '<无>')}")
        print(f"   URL: {source.get('url', '<无>')}")
        rating_val = int(source.get("rating", 0) or 0)
        stars = "⭐" * max(rating_val, 0)
        print(f"   评分: {stars if stars else '无'}")
        freq = source.get("frequency_hours")
        freq_text = f"每 {freq} 小时" if isinstance(freq, (int, float)) else "未设置"
        print(f"   频率: {freq_text}")
        print()

    print(f"总计: {len(sources)} 个新闻源")
    print(f"启用: {len(get_enabled_sources())} 个")
    print()


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="HawaiiHub 新闻采集系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 采集所有新闻源
  python main.py --all

  # 按优先级采集
  python main.py --priority P0

  # 采集单个新闻源
  python main.py --source hawaii-news-now

  # 列出所有新闻源
  python main.py --list
        """,
    )

    parser.add_argument("--all", action="store_true", help="采集所有新闻源")
    parser.add_argument(
        "--priority",
        type=str,
        choices=["P0", "P1", "P2", "p0", "p1", "p2"],
        help="按优先级采集 (P0/P1/P2)",
    )
    parser.add_argument("--source", type=str, help="采集单个新闻源 (使用 ID)")
    parser.add_argument("--list", action="store_true", help="列出所有新闻源")
    parser.add_argument("--budget", type=float, help="设置每日预算（美元）")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")

    args = parser.parse_args()

    # 调试模式
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")

    # 列出新闻源
    if args.list:
        list_sources()
        return

    # 打印横幅
    print_banner()

    # 初始化
    scraper = HawaiiHubNewsScraper(daily_budget=args.budget or 10.0)
    storage = NewsStorage()

    try:
        if args.all:
            # 采集所有新闻源
            scrape_all_news(scraper, storage)

        elif args.priority:
            # 按优先级采集
            scrape_by_priority(scraper, storage, args.priority.upper())

        elif args.source:
            # 采集单个新闻源
            scrape_single_source(scraper, storage, args.source)

        else:
            # 默认：采集 P0 优先级
            logger.info("未指定参数，默认采集 P0 优先级新闻源")
            scrape_by_priority(scraper, storage, "P0")

    except KeyboardInterrupt:
        logger.warning("\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ 发生错误: {e}", exc_info=True)
        sys.exit(1)

    logger.info("\n✅ 采集任务完成！")


if __name__ == "__main__":
    main()
