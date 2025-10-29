"""
檀香山租房信息采集系统 - 主程序

版本: v1.0
创建日期: 2025-10-29

使用方法:
    python main.py
"""

import logging
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from honolulu_rentals.config import (
    LOGGING_CONFIG, PLATFORMS, DATA_DIR, RAW_DATA_DIR,
    PROCESSED_DATA_DIR, EXPORT_DIR, LOG_DIR, FIRECRAWL_API_KEYS
)
from honolulu_rentals.models import RentalListingBatch
from honolulu_rentals.scrapers.craigslist_scraper import CraigslistScraper

# 配置日志
os.makedirs(LOG_DIR, exist_ok=True)
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def ensure_directories():
    """确保所有必要的目录存在"""
    directories = [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXPORT_DIR, LOG_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"确保目录存在: {directory}")


def scrape_all_platforms() -> RentalListingBatch:
    """
    采集所有平台的房源

    Returns:
        RentalListingBatch 对象
    """
    logger.info("=" * 60)
    logger.info("开始采集檀香山租房信息")
    logger.info("=" * 60)

    batch = RentalListingBatch(total=0, filtered=0)

    # 1. 采集 Craigslist
    if PLATFORMS["craigslist"]["enabled"]:
        logger.info("\n" + "=" * 60)
        logger.info("📋 采集 Craigslist Honolulu")
        logger.info("=" * 60)

        try:
            scraper = CraigslistScraper(api_key=PLATFORMS["craigslist"]["api_key"])
            listings = scraper.scrape_all()

            for listing in listings:
                batch.add_listing(listing)

            # 更新成本统计
            stats = scraper.get_stats()
            batch.cost_credits += stats["credits_used"]

            logger.info(f"✅ Craigslist 完成: {len(listings)} 个房源")
            logger.info(f"📊 统计: {stats}")

        except Exception as e:
            logger.error(f"❌ Craigslist 采集失败: {str(e)}")

    # TODO: 2. 采集 Zillow
    # TODO: 3. 采集 Apartments.com

    # 计算成本
    batch.cost_usd = batch.cost_credits * 0.01
    batch.filtered = len(batch.listings)

    logger.info("\n" + "=" * 60)
    logger.info("📊 采集完成总结")
    logger.info("=" * 60)
    summary = batch.get_summary()
    logger.info(f"总房源数: {summary['total']}")
    logger.info(f"平均价格: ${summary['avg_price']:.2f}/月")
    logger.info(f"价格区间: ${summary['min_price']:.2f} - ${summary['max_price']:.2f}")
    logger.info(f"消耗 Credits: {batch.cost_credits}")
    logger.info(f"消耗费用: ${batch.cost_usd:.2f}")
    logger.info("=" * 60)

    return batch


def export_results(batch: RentalListingBatch):
    """
    导出结果

    Args:
        batch: 房源批次
    """
    logger.info("\n" + "=" * 60)
    logger.info("📤 导出数据")
    logger.info("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 导出为 JSON
    import json
    json_file = os.path.join(EXPORT_DIR, f"rentals_{timestamp}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        data = {
            "summary": batch.get_summary(),
            "listings": [listing.to_dict() for listing in batch.listings]
        }
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"✅ JSON 导出完成: {json_file}")

    # 2. 导出为 Markdown
    md_file = os.path.join(EXPORT_DIR, f"rentals_{timestamp}.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# 檀香山租房信息 - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**总房源数**: {len(batch.listings)}\n\n")
        f.write(f"**平均价格**: ${batch.get_summary()['avg_price']:.2f}/月\n\n")
        f.write("---\n\n")

        for idx, listing in enumerate(batch.listings, 1):
            f.write(f"## {idx}. {listing.title}\n\n")
            f.write(f"- **价格**: ${listing.price}/月\n")
            f.write(f"- **房型**: {listing.property_type or 'N/A'}\n")
            f.write(f"- **地区**: {listing.neighborhood or 'N/A'}\n")
            f.write(f"- **图片数**: {len(listing.images)}\n")
            if listing.contact.phone:
                f.write(f"- **电话**: {listing.contact.phone}\n")
            if listing.contact.email:
                f.write(f"- **邮箱**: {listing.contact.email}\n")
            f.write(f"- **链接**: {listing.url}\n\n")

            if listing.images:
                f.write(f"![房源图片]({listing.images[0]})\n\n")

            f.write("---\n\n")

    logger.info(f"✅ Markdown 导出完成: {md_file}")

    logger.info("=" * 60)


def main():
    """主函数"""
    try:
        # 确保目录存在
        ensure_directories()

        logger.info("🏠 檀香山租房信息采集系统 v1.0")
        logger.info(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S HST')}")
        logger.info(f"🔑 API Keys: {len(FIRECRAWL_API_KEYS)} 个")

        # 采集所有平台
        batch = scrape_all_platforms()

        if batch.listings:
            # 导出结果
            export_results(batch)

            logger.info("\n" + "=" * 60)
            logger.info("✅ 全部完成！")
            logger.info(f"📁 数据已保存到: {EXPORT_DIR}")
            logger.info("=" * 60)
        else:
            logger.warning("⚠️  没有采集到任何房源")

    except KeyboardInterrupt:
        logger.warning("\n⚠️  用户中断")
    except Exception as e:
        logger.error(f"❌ 程序异常: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
