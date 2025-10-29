#!/usr/bin/env python3
"""Firecrawl Python SDK - 基础 Scrape 示例.

演示如何使用 Firecrawl SDK 进行单页采集。
"""

from __future__ import annotations

import sys
from typing import NoReturn

from dotenv import load_dotenv
from firecrawl import FirecrawlApp


def basic_scrape_example() -> None:
    """基础 Scrape 示例."""
    print("=" * 60)
    print("  Firecrawl SDK - 基础 Scrape 示例")
    print("=" * 60)

    # 加载环境变量
    load_dotenv()

    # 初始化 Firecrawl（自动读取 FIRECRAWL_API_KEY）
    app = FirecrawlApp()

    # 示例 1: 最简单的用法
    print("\n📝 示例 1: 最简单的爬取")
    print("-" * 60)

    result = app.scrape("https://firecrawl.dev")

    print("✅ 爬取成功")
    print(f"📊 内容长度: {len(result.markdown)} 字符")
    print(f"🔗 源 URL: {result.metadata.source_url}")
    print(f"📰 标题: {result.metadata.title}")
    print(f"\n内容预览:\n{result.markdown[:200]}...\n")

    # 示例 2: 指定多种格式
    print("\n📝 示例 2: 多种返回格式")
    print("-" * 60)

    result = app.scrape(
        url="https://firecrawl.dev",
        formats=["markdown", "html", "links"],
    )

    print("✅ 爬取成功")
    print(f"📊 Markdown: {len(result.markdown)} 字符")
    print(f"📊 HTML: {len(result.html)} 字符")

    links_count = len(result.links) if hasattr(result, "links") else 0
    print(f"📊 链接数: {links_count}")

    # 显示前 5 个链接
    if hasattr(result, "links") and result.links:
        print("\n🔗 前 5 个链接:")
        for i, link in enumerate(result.links[:5], 1):
            print(f"  {i}. {link}")

    # 示例 3: 只提取主要内容
    print("\n📝 示例 3: 只提取主要内容（去除导航、广告等）")
    print("-" * 60)

    result_main = app.scrape(
        url="https://firecrawl.dev",
        formats=["markdown"],
        only_main_content=True,
    )

    result_full = app.scrape(
        url="https://firecrawl.dev",
        formats=["markdown"],
        only_main_content=False,
    )

    print("✅ 爬取成功")
    full_len = len(result_full.markdown)
    main_len = len(result_main.markdown)
    saved = full_len - main_len
    save_percent = (1 - main_len / full_len) * 100 if full_len > 0 else 0

    print(f"📊 完整内容: {full_len} 字符")
    print(f"📊 主要内容: {main_len} 字符")
    print(f"💰 节省: {saved} 字符 ({save_percent:.1f}%)")

    # 示例 4: 使用缓存（节省成本）
    print("\n📝 示例 4: 使用缓存（2天有效期）")
    print("-" * 60)

    result = app.scrape(
        url="https://firecrawl.dev",
        formats=["markdown"],
        only_main_content=True,
        max_age=172800000,  # 2天缓存（毫秒）
    )

    # 检查是否命中缓存
    cache_status = result.metadata.get("cacheState", "unknown")
    print("✅ 爬取成功")
    print(f"💾 缓存状态: {cache_status}")

    if cache_status == "hit":
        print("🎉 命中缓存！此次请求免费")
    else:
        print("📥 新数据，已缓存2天")

    # 示例 5: 完整配置示例
    print("\n📝 示例 5: 完整配置（所有常用选项）")
    print("-" * 60)

    result = app.scrape(
        url="https://docs.firecrawl.dev/introduction",
        formats=["markdown"],
        only_main_content=True,
        include_tags=["article", "main", "p", "h1", "h2", "h3"],
        exclude_tags=["nav", "footer", "aside"],
        wait_for=2000,  # 等待2秒（让JS加载）
        remove_base64_images=True,  # 移除Base64图片（减少响应大小）
        max_age=172800000,  # 2天缓存
    )

    print("✅ 爬取成功")
    print(f"📰 标题: {result.metadata.title}")
    print(f"📊 内容长度: {len(result.markdown)} 字符")
    print(f"💾 缓存状态: {result.metadata.get('cacheState', 'unknown')}")

    print("\n" + "=" * 60)
    print("  ✅ 所有示例完成！")
    print("=" * 60)


def run_example() -> NoReturn:
    """运行示例并处理异常."""
    try:
        basic_scrape_example()
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
