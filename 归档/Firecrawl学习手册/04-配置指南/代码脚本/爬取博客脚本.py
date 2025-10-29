#!/usr/bin/env python3
"""爬取 Firecrawl 博客内容

用途：演示如何使用 Firecrawl API 爬取博客文章列表
"""

import json
from datetime import datetime

from firecrawl import FirecrawlApp


# 使用性能最好的 API 密钥
API_KEY = "fc-00857d82ec534e8598df1bae9af9fb28"  # 最快的密钥 (1.08秒)

# 初始化客户端
app = FirecrawlApp(api_key=API_KEY)

# 目标 URL
BLOG_URL = "https://www.firecrawl.dev/blog"


def scrape_blog():
    """爬取 Firecrawl 博客"""
    print("=" * 70)
    print("🔥 Firecrawl 博客内容爬取")
    print("=" * 70)
    print(f"📰 目标 URL: {BLOG_URL}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 开始爬取
        print("\n🔄 正在爬取...")
        start_time = datetime.now()

        result = app.scrape(
            url=BLOG_URL,
            formats=["markdown"],  # 只要 markdown，更快
            only_main_content=True,  # 只要主要内容
            timeout=60,  # 增加超时时间到 60 秒
        )

        elapsed = (datetime.now() - start_time).total_seconds()

        # 提取结果
        markdown_content = result.markdown if hasattr(result, "markdown") else ""

        # 统计信息
        print("\n✅ 爬取成功！")
        print(f"⏱️  耗时: {elapsed:.2f} 秒")
        print(f"📝 Markdown 长度: {len(markdown_content):,} 字符")

        # 保存 Markdown 内容
        markdown_file = "firecrawl_blog.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write("# Firecrawl 博客内容\n\n")
            f.write(f"> 爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"> 来源: {BLOG_URL}\n\n")
            f.write("---\n\n")
            f.write(markdown_content)

        print(f"\n💾 Markdown 已保存到: {markdown_file}")

        # 分析博客文章
        print("\n" + "=" * 70)
        print("📊 博客内容分析")
        print("=" * 70)

        # 提取文章标题（简单解析）
        lines = markdown_content.split("\n")
        articles = []

        for i, line in enumerate(lines):
            # 查找文章标题（假设以 ## 或 ### 开头）
            if line.startswith("##") and not line.startswith("###"):
                title = line.replace("#", "").strip()
                if title and len(title) > 5:  # 过滤太短的标题
                    articles.append(title)

        print(f"\n📝 发现 {len(articles)} 篇文章标题:")
        for i, title in enumerate(articles[:20], 1):  # 只显示前 20 篇
            print(f"{i:2d}. {title[:80]}")

        if len(articles) > 20:
            print(f"... 还有 {len(articles) - 20} 篇")

        # 保存结构化数据
        metadata = {
            "url": BLOG_URL,
            "scraped_at": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "markdown_length": len(markdown_content),
            "article_count": len(articles),
            "articles": articles[:50],  # 保存前 50 篇
        }

        metadata_file = "firecrawl_blog_metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"\n💾 元数据已保存到: {metadata_file}")

        # 预览内容
        print("\n" + "=" * 70)
        print("📄 内容预览（前 500 字符）")
        print("=" * 70)
        print(markdown_content[:500])
        print("\n... (查看完整内容请打开 firecrawl_blog.md)")

        return result

    except Exception as e:
        print(f"\n❌ 爬取失败: {e}")
        import traceback

        traceback.print_exc()
        return None


def main():
    """主函数"""
    result = scrape_blog()

    if result:
        print("\n" + "=" * 70)
        print("✅ 任务完成！")
        print("=" * 70)
        print("\n📁 生成的文件:")
        print("  1. firecrawl_blog.md - Markdown 格式的博客内容")
        print("  2. firecrawl_blog_metadata.json - 元数据和文章列表")
        print("\n💡 下一步:")
        print("  - 使用编辑器打开 firecrawl_blog.md 查看内容")
        print("  - 查看 firecrawl_blog_metadata.json 了解文章列表")
    else:
        print("\n❌ 任务失败！")
        print("\n🔧 故障排查:")
        print("  1. 检查网络连接")
        print("  2. 验证 API 密钥: python3 test_api_keys.py")
        print("  3. 查看 FIRECRAWL_CLOUD_SETUP_GUIDE.md")


if __name__ == "__main__":
    main()
