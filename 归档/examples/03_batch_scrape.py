#!/usr/bin/env python3
"""Firecrawl Python SDK - Batch Scrape 批量采集示例.

演示如何使用 Firecrawl SDK 进行批量采集。
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from dotenv import load_dotenv
from firecrawl import FirecrawlApp


def batch_scrape_example() -> None:
    """Batch Scrape 批量采集示例."""
    print("=" * 60)
    print("  Firecrawl SDK - Batch Scrape 批量采集示例")
    print("=" * 60)

    # 加载环境变量
    load_dotenv()

    # 初始化 Firecrawl
    app = FirecrawlApp()

    # 示例 1: 简单批量爬取
    print("\n📝 示例 1: 批量爬取多个页面")
    print("-" * 60)

    urls = [
        "https://firecrawl.dev",
        "https://docs.firecrawl.dev",
        "https://docs.firecrawl.dev/introduction",
    ]

    print(f"🔗 待爬取 URL ({len(urls)} 个):")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")

    print("\n⏳ 开始批量爬取...")

    job = app.batch_scrape(
        urls=urls,
        formats=["markdown"],
        poll_interval=1,
        timeout=60,
    )

    print("\n✅ 批量爬取完成")
    print(f"📊 状态: {job.status}")
    print(f"📄 完成: {job.completed}/{job.total}")

    print("\n📋 结果:")
    for i, doc in enumerate(job.data, 1):
        print(f"\n  {i}. {doc.metadata.source_url}")
        print(f"     标题: {doc.metadata.title}")
        print(f"     内容: {len(doc.markdown)} 字符")
        print(f"     预览: {doc.markdown[:100]}...")

    # 示例 2: 批量爬取 Firecrawl 相关页面
    print("\n📝 示例 2: 批量爬取 Firecrawl 文档页面")
    print("-" * 60)

    doc_urls = [
        "https://docs.firecrawl.dev/introduction",
        "https://docs.firecrawl.dev/features/scrape",
        "https://docs.firecrawl.dev/features/crawl",
        "https://docs.firecrawl.dev/features/map",
        "https://docs.firecrawl.dev/features/batch-scrape",
    ]

    print(f"🔗 文档 URL ({len(doc_urls)} 个)")
    print("⏳ 批量爬取中...")

    job = app.batch_scrape(
        urls=doc_urls,
        formats=["markdown"],
        poll_interval=2,
        timeout=120,
    )

    print(f"\n✅ 爬取完成: {job.completed}/{job.total}")

    # 分析结果
    total_chars = sum(len(doc.markdown) for doc in job.data)
    data_count = len(job.data)
    avg_chars = total_chars // data_count if data_count > 0 else 0

    print("\n📊 统计:")
    print(f"  总字符数: {total_chars:,}")
    print(f"  平均每页: {avg_chars:,} 字符")

    if job.data:
        max_len = max(len(doc.markdown) for doc in job.data)
        min_len = min(len(doc.markdown) for doc in job.data)
        print(f"  最长页面: {max_len:,} 字符")
        print(f"  最短页面: {min_len:,} 字符")

    # 示例 3: 智能批量处理（分批 + 错误处理）
    print("\n📝 示例 3: 智能批量处理（大列表分批处理）")
    print("-" * 60)

    # 模拟大量 URL
    large_url_list = [
        f"https://docs.firecrawl.dev/sdks/{sdk}"
        for sdk in ["overview", "python", "node"]
    ] + [
        f"https://docs.firecrawl.dev/features/{feature}"
        for feature in ["scrape", "crawl", "map", "batch-scrape", "extract"]
    ]

    print(f"🔗 待爬取: {len(large_url_list)} 个 URL")

    # 分批处理
    batch_size = 3
    all_results = []

    for i in range(0, len(large_url_list), batch_size):
        batch = large_url_list[i : i + batch_size]
        batch_num = i // batch_size + 1

        print(f"\n⏳ 处理批次 {batch_num} ({len(batch)} 个 URL)...")

        try:
            job = app.batch_scrape(
                urls=batch,
                formats=["markdown"],
                poll_interval=1,
                timeout=60,
            )

            all_results.extend(job.data)
            print(f"   ✅ 批次 {batch_num}: {len(job.data)} 个页面")

        except OSError as e:
            print(f"   ❌ 批次 {batch_num} 网络错误: {e}")

            # 逐个重试
            print("   🔄 逐个重试...")
            for url in batch:
                try:
                    result = app.scrape(url, formats=["markdown"])
                    all_results.append(result)
                    print(f"     ✅ {url}")
                except OSError as e2:
                    print(f"     ❌ {url}: {e2}")

    print("\n✅ 所有批次完成")
    print(f"📄 成功: {len(all_results)}/{len(large_url_list)} 个页面")

    # 保存结果
    output_dir = Path(__file__).parent.parent / "data" / "batch_results"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"batch_{timestamp}.json"

    results = []
    for doc in all_results:
        results.append(
            {
                "url": doc.metadata.source_url,
                "title": doc.metadata.title,
                "content": doc.markdown,
                "content_length": len(doc.markdown),
                "scraped_at": datetime.now().isoformat(),
            }
        )

    output_path = Path(output_file)
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n💾 结果已保存到: {output_file}")

    print("\n" + "=" * 60)
    print("  ✅ 所有示例完成！")
    print("=" * 60)


def run_example() -> NoReturn:
    """运行示例并处理异常."""
    try:
        batch_scrape_example()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        sys.exit(0)
    except OSError as e:
        print(f"\n❌ 网络错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_example()
