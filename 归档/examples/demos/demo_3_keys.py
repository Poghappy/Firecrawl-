#!/usr/bin/env python3
"""使用 3 个不同 API 密钥进行爬取演示.

每次爬取强制切换密钥，展示密钥轮换效果
"""

from datetime import datetime
from typing import Any

from firecrawl import FirecrawlApp


def mask_key(key: str) -> str:
    """隐藏 API 密钥.

    Args:
        key: 完整的 API 密钥

    Returns:
        隐藏后的密钥字符串
    """
    return f"{key[:8]}...{key[-4:]}"


def scrape_with_key(
    api_key: str,
    key_name: str,
    url: str,
) -> dict[str, Any]:
    """使用指定密钥爬取网页.

    Args:
        api_key: API 密钥
        key_name: 密钥名称
        url: 要爬取的 URL

    Returns:
        包含爬取结果的字典
    """
    print(f"\n{'=' * 60}")
    print(f"🔑 使用密钥: {key_name} ({mask_key(api_key)})")
    print(f"🎯 目标 URL: {url}")
    print(f"{'=' * 60}")

    # 初始化客户端
    app = FirecrawlApp(api_key=api_key)

    # 记录开始时间
    start_time = datetime.now()

    try:
        # 爬取
        result = app.scrape(
            url=url,
            formats=["markdown"],
            only_main_content=True,
            max_age=172800000,  # 2天缓存
        )

        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()

        # 获取内容
        content = str(getattr(result, "markdown", ""))
        title = getattr(result.metadata, "title", "N/A")

        print("✅ 爬取成功！")
        print(f"⏱️  耗时: {elapsed:.2f}秒")
        print(f"📄 标题: {title[:60]}")
        print(f"📝 内容长度: {len(content):,} 字符")

        return {
            "success": True,
            "key_name": key_name,
            "masked_key": mask_key(api_key),
            "url": url,
            "elapsed": elapsed,
            "content_length": len(content),
            "title": title,
        }

    except Exception as e:
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"❌ 爬取失败: {e}")

        return {
            "success": False,
            "key_name": key_name,
            "masked_key": mask_key(api_key),
            "url": url,
            "elapsed": elapsed,
            "error": str(e),
        }


def main() -> None:
    """主函数.

    使用 3 个不同的 API 密钥爬取 3 个不同的网站
    """
    print("\n" + "🔥" * 30)
    print("Firecrawl 3 密钥轮换演示")
    print("🔥" * 30)

    # 3 个 API 密钥
    keys = [
        {
            "name": "密钥 #1 (main)",
            "key": "fc-31ebbe4647b84fdc975318d372eebea8",
        },
        {
            "name": "密钥 #2 (backup_1)",
            "key": "fc-00857d82ec534e8598df1bae9af9fb28",
        },
        {
            "name": "密钥 #3 (backup_2)",
            "key": "fc-9eb380b0dec74d6ebb6c756ee4de4c5a",
        },
    ]

    # 3 个不同的夏威夷新闻网站
    urls = [
        "https://www.hawaiinewsnow.com/",  # 夏威夷新闻
        "https://www.staradvertiser.com/",  # 檀香山星报
        "https://www.civilbeat.org/",  # 民声报
    ]

    print(f"\n将使用 {len(keys)} 个不同的 API 密钥")
    print(f"爬取 {len(urls)} 个夏威夷新闻网站\n")

    # 执行爬取
    results = []
    for i, (key_info, url) in enumerate(zip(keys, urls), 1):
        print(f"\n{'🔥' * 30}")
        print(f"第 {i}/3 次爬取")
        print(f"{'🔥' * 30}")

        result = scrape_with_key(
            api_key=key_info["key"],
            key_name=key_info["name"],
            url=url,
        )
        results.append(result)

    # 打印总结
    print("\n" + "=" * 60)
    print("📊 爬取总结")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['key_name']} ({result['masked_key']})")
        print(f"   URL: {result['url']}")

        if result["success"]:
            print("   ✅ 成功")
            print(f"   耗时: {result['elapsed']:.2f}秒")
            print(f"   内容: {result['content_length']:,} 字符")
        else:
            print(f"   ❌ 失败: {result.get('error', '未知错误')}")

    # 统计
    print("\n" + "=" * 60)
    print("📈 统计数据")
    print("=" * 60)

    successful = [r for r in results if r["success"]]
    total_time = sum(r["elapsed"] for r in results)
    avg_time = total_time / len(results) if results else 0

    print(f"总请求数: {len(results)}")
    print(f"成功: {len(successful)}")
    print(f"失败: {len(results) - len(successful)}")
    print(f"成功率: {len(successful) / len(results) * 100:.1f}%")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均耗时: {avg_time:.2f}秒/请求")

    if successful:
        fastest = min(successful, key=lambda x: x["elapsed"])
        print(f"\n⚡ 最快的密钥: {fastest['key_name']} ({fastest['elapsed']:.2f}秒)")

    print("\n" + "=" * 60)
    print("💡 密钥轮换优势")
    print("=" * 60)
    print("✅ 每个密钥独立的速率限制配额")
    print("✅ 一个密钥失败可自动切换到备用密钥")
    print("✅ 并发爬取时可分散负载")
    print("✅ 提高系统整体可用性和性能")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
