#!/usr/bin/env python3
"""Firecrawl Python SDK - Crawl 爬取示例.

演示如何使用 Firecrawl SDK 进行深度爬取。
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from dotenv import load_dotenv
from firecrawl import FirecrawlApp


def crawl_example() -> None:
    """Crawl 爬取示例."""
    print("=" * 60)
    print("  Firecrawl SDK - Crawl 深度爬取示例")
    print("=" * 60)

    # 加载环境变量
    load_dotenv()

    # 初始化 Firecrawl
    app = FirecrawlApp()

    # 示例 1: 简单爬取（阻塞式，等待完成）
    print("\n📝 示例 1: 简单爬取（限制5个页面）")
    print("-" * 60)

    job = app.crawl(
        url="https://docs.firecrawl.dev",
        limit=5,
        poll_interval=1,  # 每秒检查一次
        timeout=120,  # 最多等待120秒
    )

    print("✅ 爬取完成")
    print(f"📊 状态: {job.status}")
    print(f"📄 页面数: {job.completed}/{job.total}")
    print("\n🔗 爬取的页面:")

    for i, doc in enumerate(job.data, 1):
        print(f"  {i}. {doc.metadata.source_url}")
        print(f"     标题: {doc.metadata.title}")
        print(f"     内容: {len(doc.markdown)} 字符")

    # 示例 2: 非阻塞爬取（启动后检查）
    print("\n📝 示例 2: 非阻塞爬取（启动后手动检查）")
    print("-" * 60)

    # 启动任务
    started_job = app.start_crawl(
        url="https://docs.firecrawl.dev/introduction",
        limit=3,
        scrape_options={"formats": ["markdown"], "only_main_content": True},
    )

    print("✅ 任务已启动")
    print(f"🆔 任务 ID: {started_job.id}")
    print("⏳ 正在爬取...")

    # 检查状态
    while True:
        status = app.get_crawl_status(started_job.id)

        total = status.total if status.total > 0 else 1
        progress = (status.completed / total) * 100

        print(
            f"   进度: {status.completed}/{status.total} "
            f"({progress:.0f}%) - 状态: {status.status}"
        )

        if status.status in ["completed", "failed"]:
            break

        time.sleep(2)

    if status.status == "completed":
        print("\n✅ 爬取完成")
        print(f"📄 获取了 {len(status.data)} 个页面")
    else:
        print(f"\n❌ 爬取失败: {status.status}")

    # 示例 3: 高级爬取选项
    print("\n📝 示例 3: 高级爬取选项（路径过滤、深度控制）")
    print("-" * 60)

    job = app.crawl(
        url="https://docs.firecrawl.dev",
        limit=10,
        # 路径过滤
        include_paths=["/sdks/*", "/features/*"],
        exclude_paths=["/api-reference/*"],
        # 域名控制
        allow_subdomains=False,
        allow_external_links=False,
        # 去重
        ignore_query_parameters=True,
        # 深度和并发
        max_discovery_depth=2,
        max_concurrency=3,
        # 延迟（避免速率限制）
        delay=500,  # 500毫秒
        # Scrape 选项
        scrape_options={
            "formats": ["markdown"],
            "only_main_content": True,
            "remove_base64_images": True,
        },
        poll_interval=2,
        timeout=180,
    )

    print("✅ 爬取完成")
    data_count = len(job.data)
    print(f"📄 页面数: {data_count}")

    # 分析结果
    total_chars = sum(len(doc.markdown) for doc in job.data)
    avg_chars = total_chars // data_count if data_count > 0 else 0

    print(f"📊 总字符数: {total_chars:,}")
    print(f"📊 平均每页: {avg_chars:,} 字符")

    # 保存结果
    output_dir = Path(__file__).parent.parent / "data" / "crawl_results"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"crawl_{timestamp}.json"

    results = []
    for doc in job.data:
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
        crawl_example()
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
