"""
演示系统 - 使用示例数据展示系统功能

这个脚本不调用 Firecrawl API，而是使用预定义的示例数据
来展示系统的完整工作流程和数据导出功能。
"""

import logging
import logging.config
from datetime import datetime
from pathlib import Path

from config import LOGGING_CONFIG, EXPORT_DIR
from models import RentalListing, RentalListingBatch, ContactMethod, Platform, PropertyType

# 配置日志
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def create_sample_listings() -> list:
    """创建示例房源数据"""

    sample_data = [
        {
            "title": "🏡 Cozy Studio in Makiki - Perfect for UH Students",
            "price": 1100.0,
            "property_type": PropertyType.STUDIO,
            "bedrooms": "Studio",
            "bathrooms": "1",
            "neighborhood": "Makiki",
            "address": "1234 Piikoi St, Honolulu, HI 96814",
            "images": [
                "https://images.craigslist.org/00G0G_example1.jpg",
                "https://images.craigslist.org/00H0H_example2.jpg",
                "https://images.craigslist.org/00I0I_example3.jpg",
            ],
            "contact_phone": "(808) 123-4567",
            "contact_email": "landlord1@example.com",
            "description": "Beautiful studio apartment in the heart of Makiki. Walking distance to UH Manoa. Includes parking, WiFi, and utilities.",
            "amenities": ["Parking", "WiFi", "Laundry", "A/C"],
        },
        {
            "title": "🌺 1BR/1BA Near Ala Moana - Ocean View",
            "price": 1350.0,
            "property_type": PropertyType.ONE_BED_ONE_BATH,
            "bedrooms": "1",
            "bathrooms": "1",
            "neighborhood": "Ala Moana",
            "address": "1441 Victoria St, Honolulu, HI 96822",
            "images": [
                "https://images.craigslist.org/00J0J_example4.jpg",
                "https://images.craigslist.org/00K0K_example5.jpg",
            ],
            "contact_phone": "(808) 234-5678",
            "description": "Spacious 1 bedroom with ocean view. Close to Ala Moana Center. Pet-friendly.",
            "amenities": ["Parking", "Pool", "Pet Friendly", "Dishwasher"],
        },
        {
            "title": "Affordable Studio in Kalihi - $850/mo",
            "price": 850.0,
            "property_type": PropertyType.STUDIO,
            "bedrooms": "Studio",
            "bathrooms": "1",
            "neighborhood": "Kalihi",
            "address": "2345 Kalihi St, Honolulu, HI 96819",
            "images": [
                "https://images.craigslist.org/00L0L_example6.jpg",
            ],
            "contact_email": "owner@example.com",
            "description": "Budget-friendly studio in Kalihi. Close to bus stops.",
            "amenities": ["Laundry"],
        },
        {
            "title": "✨ Luxury 2BR/2BA in Waikiki - Walk to Beach",
            "price": 2200.0,
            "property_type": PropertyType.TWO_BED_TWO_BATH,
            "bedrooms": "2",
            "bathrooms": "2",
            "neighborhood": "Waikiki",
            "address": "123 Kuhio Ave, Honolulu, HI 96815",
            "images": [
                "https://images.craigslist.org/00M0M_example7.jpg",
                "https://images.craigslist.org/00N0N_example8.jpg",
            ],
            "contact_phone": "(808) 345-6789",
            "contact_email": "luxury@example.com",
            "description": "Gorgeous 2BR/2BA condo in Waikiki. Steps from the beach. Fully furnished.",
            "amenities": ["Parking", "Pool", "Gym", "Furnished", "A/C", "WiFi"],
        },
        {
            "title": "1BR in Manoa Valley - Quiet Neighborhood",
            "price": 1200.0,
            "property_type": PropertyType.ONE_BED_ONE_BATH,
            "bedrooms": "1",
            "bathrooms": "1",
            "neighborhood": "Manoa",
            "address": "3456 Manoa Rd, Honolulu, HI 96822",
            "images": [
                "https://images.craigslist.org/00O0O_example9.jpg",
            ],
            "contact_phone": "(808) 456-7890",
            "description": "Peaceful 1 bedroom in Manoa. Great for students and professionals.",
            "amenities": ["Parking", "Laundry"],
        },
    ]

    listings = []
    for idx, data in enumerate(sample_data, 1):
        listing = RentalListing(
            id=f"demo_{datetime.now().strftime('%Y%m%d')}_{idx:03d}",
            title=data["title"],
            price=data["price"],
            url=f"https://honolulu.craigslist.org/hnl/apa/d/demo-listing-{idx}/1234567890.html",
            platform=Platform.CRAIGSLIST,
            property_type=data.get("property_type"),
            bedrooms=data.get("bedrooms"),
            bathrooms=data.get("bathrooms"),
            neighborhood=data.get("neighborhood"),
            address=data.get("address"),
            images=data.get("images", []),
            thumbnail=data.get("images", [None])[0],
            contact=ContactMethod(
                phone=data.get("contact_phone"),
                email=data.get("contact_email"),
            ),
            description=data.get("description"),
            amenities=data.get("amenities", []),
            posted_date=datetime.now(),
            scraped_at=datetime.now(),
        )
        listings.append(listing)

    return listings


def export_results(batch: RentalListingBatch):
    """导出结果"""
    import json
    from pathlib import Path

    Path(EXPORT_DIR).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 导出 JSON
    json_file = Path(EXPORT_DIR) / f"rentals_demo_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        data = {
            "summary": batch.get_summary(),
            "listings": [listing.to_dict() for listing in batch.listings]
        }
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"✅ JSON 导出: {json_file}")

    # 2. 导出 Markdown
    md_file = Path(EXPORT_DIR) / f"rentals_demo_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        summary = batch.get_summary()
        f.write(f"# 檀香山租房信息 - 演示数据\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S HST')}\n\n")
        f.write(f"**总房源数**: {len(batch.listings)}\n\n")
        f.write(f"**平均价格**: ${summary['avg_price']:.2f}/月\n\n")
        f.write(f"**价格区间**: ${summary['min_price']:.2f} - ${summary['max_price']:.2f}\n\n")
        f.write("---\n\n")

        for idx, listing in enumerate(batch.listings, 1):
            f.write(f"## {idx}. {listing.title}\n\n")
            f.write(f"- **价格**: ${listing.price:.2f}/月\n")
            f.write(f"- **房型**: {listing.property_type or 'N/A'}\n")
            f.write(f"- **卧室/浴室**: {listing.bedrooms}/{listing.bathrooms}\n")
            f.write(f"- **地区**: {listing.neighborhood or 'N/A'}\n")
            f.write(f"- **地址**: {listing.address or 'N/A'}\n")
            f.write(f"- **图片数**: {len(listing.images)}\n")

            if listing.contact.phone:
                f.write(f"- **电话**: {listing.contact.phone}\n")
            if listing.contact.email:
                f.write(f"- **邮箱**: {listing.contact.email}\n")

            if listing.amenities:
                f.write(f"- **设施**: {', '.join(listing.amenities)}\n")

            f.write(f"- **链接**: {listing.url}\n\n")

            if listing.description:
                f.write(f"**描述**: {listing.description}\n\n")

            if listing.images:
                f.write(f"**房源图片**:\n")
                for img_url in listing.images[:3]:  # 只显示前3张
                    f.write(f"![房源图片]({img_url})\n\n")

            f.write("---\n\n")

    logger.info(f"✅ Markdown 导出: {md_file}")

    return json_file, md_file


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🏠 檀香山租房信息采集系统 - 演示模式")
    logger.info("=" * 60)
    logger.info("⚠️  注意: 使用示例数据演示系统功能")
    logger.info("")

    # 创建示例数据
    logger.info("📝 生成示例房源数据...")
    listings = create_sample_listings()

    # 创建批次
    batch = RentalListingBatch(total=len(listings), filtered=len(listings))
    for listing in listings:
        batch.add_listing(listing)

    # 显示统计
    logger.info("")
    logger.info("=" * 60)
    logger.info("📊 采集完成总结")
    logger.info("=" * 60)
    summary = batch.get_summary()
    logger.info(f"总房源数: {summary['total']}")
    logger.info(f"平均价格: ${summary['avg_price']:.2f}/月")
    logger.info(f"价格区间: ${summary['min_price']:.2f} - ${summary['max_price']:.2f}")
    logger.info("=" * 60)
    logger.info("")

    # 导出数据
    logger.info("=" * 60)
    logger.info("📤 导出数据")
    logger.info("=" * 60)
    json_file, md_file = export_results(batch)
    logger.info("")

    logger.info("=" * 60)
    logger.info("✅ 演示完成！")
    logger.info(f"📁 数据已保存到: {EXPORT_DIR}")
    logger.info("")
    logger.info("💡 查看结果:")
    logger.info(f"   cat {md_file}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
