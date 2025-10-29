#!/usr/bin/env python3
"""火鸟门户系统新闻 JSON 格式示例

演示各种 JSON 格式的创建、转换和验证
"""

import json
from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field, HttpUrl, ValidationError


# =============================================================================
# 1. 数据模型定义（使用 Pydantic 验证）
# =============================================================================


class FirebirdArticle(BaseModel):
    """火鸟 API 发布格式"""

    title: str = Field(..., min_length=1, max_length=200, description="文章标题")
    description: Optional[str] = Field(
        None, max_length=500, description="文章摘要/导语"
    )
    body: str = Field(..., min_length=100, description="文章正文（HTML 或 Markdown）")
    keywords: Optional[str] = Field(
        None, max_length=200, description="关键词（逗号分隔）"
    )
    source: Optional[str] = Field(None, max_length=100, description="新闻来源")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "夏威夷租房价格创新高",
                "description": "檀香山平均租金达到 $2,500/月，同比上涨 15%",
                "body": "# 夏威夷租房价格创新高\n\n檀香山租房价格达到历史新高...",
                "keywords": "夏威夷,租房,房价,住房危机",
                "source": "Civil Beat",
            }
        }


class NewsAPIArticle(BaseModel):
    """NewsAPI 响应格式"""

    source_name: str = Field(..., description="新闻源名称")
    author: Optional[str] = Field(None, description="作者")
    title: str = Field(..., description="标题")
    description: Optional[str] = Field(None, description="摘要")
    url: HttpUrl = Field(..., description="原文链接")
    url_to_image: Optional[str] = Field(None, description="封面图 URL")
    published_at: str = Field(..., description="发布时间（ISO 8601）")
    content: Optional[str] = Field(None, description="内容片段")


class HawaiiHubArticle(BaseModel):
    """HawaiiHub 内部格式"""

    source_id: str = Field(..., description="新闻源 ID")
    source_name: str = Field(..., description="新闻源名称")
    url: HttpUrl = Field(..., description="文章 URL")
    title: str = Field(..., description="文章标题")
    description: Optional[str] = Field(None, description="文章摘要")
    content: str = Field(..., description="文章正文（Markdown）")
    scraped_at: str = Field(..., description="采集时间（ISO 8601）")


# =============================================================================
# 2. JSON 格式示例
# =============================================================================


def get_firebird_api_example() -> Dict:
    """火鸟 API 发布格式示例"""
    return {
        "title": "夏威夷租房价格创新高",
        "description": "檀香山平均租金达到 $2,500/月，同比上涨 15%。住房危机加剧，影响中低收入家庭。",
        "body": """# 夏威夷租房价格创新高

檀香山租房价格达到历史新高，平均月租金已达 $2,500，同比上涨 15%。

## 关键数据

- **平均租金**: $2,500/月
- **同比涨幅**: 15%
- **受影响人群**: 中低收入家庭

## 专家分析

房地产专家指出，供需失衡是主要原因：

1. 新建住房数量不足
2. 外地购房者增多
3. 短租房源占用市场

## 政府应对

夏威夷州政府计划：

- 增加保障性住房供应
- 限制短租房发展
- 为低收入家庭提供租房补贴

**相关链接**: [了解更多详情](https://civilbeat.org)""",
        "keywords": "夏威夷,租房,房价,住房危机,檀香山",
        "source": "Civil Beat",
    }


def get_newsapi_example() -> Dict:
    """NewsAPI 响应格式示例"""
    return {
        "status": "ok",
        "totalResults": 100,
        "articles": [
            {
                "source": {"id": None, "name": "Hawaii News Now"},
                "author": "John Doe",
                "title": "Breaking: Hawaii Weather Alert",
                "description": "A severe weather warning has been issued for Oahu",
                "url": "https://hawaiinewsnow.com/article/123",
                "urlToImage": "https://hawaiinewsnow.com/images/123.jpg",
                "publishedAt": "2025-10-28T10:00:00Z",
                "content": "A severe weather warning has been issued...",
            },
            {
                "source": {"id": None, "name": "Civil Beat"},
                "author": "Jane Smith",
                "title": "Hawaii Housing Crisis Deepens",
                "description": "Rent prices reach new record highs in Honolulu",
                "url": "https://civilbeat.org/article/456",
                "urlToImage": "https://civilbeat.org/images/456.jpg",
                "publishedAt": "2025-10-28T09:00:00Z",
                "content": "Rent prices in Honolulu have reached...",
            },
        ],
    }


def get_hawaiihub_example() -> Dict:
    """HawaiiHub 内部格式示例"""
    return {
        "source_id": "civil-beat",
        "source_name": "Honolulu Civil Beat",
        "source_url": "https://www.civilbeat.org/",
        "status": "success",
        "homepage": {
            "url": "https://www.civilbeat.org/",
            "metadata": {
                "title": "Civil Beat - News for Hawaii",
                "description": "Investigative journalism for Hawaii",
                "status_code": 200,
                "cache_state": "HIT",
            },
            "content": {"markdown": "# Civil Beat\n\nLatest news...", "links": []},
            "scraped_at": "2025-10-28T10:00:00.000Z",
        },
        "articles": [
            {
                "url": "https://civilbeat.org/article/456",
                "metadata": {
                    "source_url": "https://civilbeat.org/article/456",
                    "title": "Hawaii Housing Crisis Deepens",
                    "description": "Rent prices reach new record highs",
                    "status_code": 200,
                    "cache_state": "MISS",
                },
                "content": {
                    "markdown": "# Hawaii Housing Crisis Deepens\n\nRent prices...",
                    "html": "<h1>Hawaii Housing Crisis Deepens</h1>...",
                    "links": ["https://example.com/related"],
                },
                "scraped_at": "2025-10-28T10:30:00.123Z",
                "attempt": 1,
            }
        ],
        "stats": {
            "total_articles": 1,
            "duration_seconds": 45.2,
            "articles_per_minute": 1.3,
        },
        "scraped_at": "2025-10-28T10:45:00.000Z",
    }


# =============================================================================
# 3. 格式转换函数
# =============================================================================


def newsapi_to_hawaiihub(newsapi_article: Dict) -> Dict:
    """NewsAPI 格式 → HawaiiHub 格式

    Args:
        newsapi_article: NewsAPI 文章格式

    Returns:
        HawaiiHub 标准格式
    """
    return {
        "source_id": newsapi_article["source"]["name"].lower().replace(" ", "-"),
        "source_name": newsapi_article["source"]["name"],
        "url": newsapi_article["url"],
        "title": newsapi_article["title"],
        "description": newsapi_article.get("description"),
        "content": newsapi_article.get("content", ""),  # 需要 Firecrawl 补充完整内容
        "scraped_at": datetime.now().isoformat(),
    }


def hawaiihub_to_firebird(hawaiihub_article: Dict) -> Dict:
    """HawaiiHub 格式 → 火鸟 API 格式

    Args:
        hawaiihub_article: HawaiiHub 文章格式

    Returns:
        火鸟 API 发布格式
    """
    # 从标题和内容中提取关键词（简化版本）
    keywords = extract_keywords_simple(
        hawaiihub_article["title"], hawaiihub_article["content"]
    )

    return {
        "title": hawaiihub_article["title"],
        "description": hawaiihub_article.get("description", ""),
        "body": hawaiihub_article["content"],
        "keywords": keywords,
        "source": hawaiihub_article["source_name"],
    }


def extract_keywords_simple(title: str, content: str, max_keywords: int = 5) -> str:
    """简单的关键词提取（基于词频）

    Args:
        title: 标题
        content: 内容
        max_keywords: 最大关键词数

    Returns:
        逗号分隔的关键词字符串
    """
    import re
    from collections import Counter

    # 合并文本
    text = f"{title} {content}"

    # 简单分词（中文按字，英文按词）
    words = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z]+", text)

    # 过滤停用词
    stopwords = {
        "的",
        "了",
        "在",
        "是",
        "和",
        "有",
        "与",
        "为",
        "等",
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
    }
    words = [w for w in words if w not in stopwords and len(w) > 1]

    # 统计词频
    counter = Counter(words)

    # 返回 Top N
    top_keywords = [word for word, count in counter.most_common(max_keywords)]
    return ",".join(top_keywords)


# =============================================================================
# 4. 数据验证
# =============================================================================


def validate_firebird_article(data: Dict) -> bool:
    """验证火鸟 API 格式数据

    Args:
        data: 待验证的数据

    Returns:
        验证是否通过
    """
    try:
        article = FirebirdArticle(**data)
        print("✅ 火鸟 API 格式验证通过")
        print(f"   标题: {article.title}")
        print(f"   正文长度: {len(article.body)} 字符")
        print(f"   关键词: {article.keywords}")
        return True
    except ValidationError as e:
        print("❌ 火鸟 API 格式验证失败:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return False


def validate_hawaiihub_article(data: Dict) -> bool:
    """验证 HawaiiHub 格式数据

    Args:
        data: 待验证的数据

    Returns:
        验证是否通过
    """
    try:
        article = HawaiiHubArticle(**data)
        print("✅ HawaiiHub 格式验证通过")
        print(f"   来源: {article.source_name}")
        print(f"   标题: {article.title}")
        print(f"   URL: {article.url}")
        return True
    except ValidationError as e:
        print("❌ HawaiiHub 格式验证失败:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return False


# =============================================================================
# 5. 完整工作流示例
# =============================================================================


def complete_workflow_example():
    """完整的数据流转示例

    NewsAPI → Firecrawl 采集 → HawaiiHub 处理 → 火鸟 API 发布
    """
    print("\n" + "=" * 60)
    print("完整数据流转示例")
    print("=" * 60)

    # 1. 从 NewsAPI 获取文章列表
    print("\n📰 Step 1: 从 NewsAPI 获取文章")
    newsapi_data = get_newsapi_example()
    print(f"   获取到 {newsapi_data['totalResults']} 篇文章")
    article = newsapi_data["articles"][1]  # 选择第二篇（住房危机）
    print(f"   标题: {article['title']}")

    # 2. 转换为 HawaiiHub 格式（实际应用中需要 Firecrawl 采集完整内容）
    print("\n🔄 Step 2: 转换为 HawaiiHub 格式")
    hawaiihub_article = newsapi_to_hawaiihub(article)

    # 模拟 Firecrawl 采集的完整内容
    hawaiihub_article["content"] = """# Hawaii Housing Crisis Deepens

Rent prices in Honolulu have reached a new record high of $2,500 per month on average,
representing a 15% increase year-over-year. The housing crisis continues to impact
middle and low-income families across the state.

## Key Statistics

- Average monthly rent: $2,500
- Year-over-year increase: 15%
- Vacancy rate: 2.3%
- Median household income: $88,000

## Expert Analysis

Real estate experts point to several factors:

1. **Supply shortage**: New housing construction hasn't kept pace with demand
2. **External buyers**: Mainland investors competing for limited housing
3. **Short-term rentals**: Vacation rentals removing long-term housing stock

## Government Response

The Hawaii State Legislature is considering:

- Increasing affordable housing development
- Restricting short-term rental licenses
- Providing rental assistance for low-income families

**Sources**: Hawaii Housing Finance and Development Corporation, University of Hawaii Economic Research Organization"""

    print(f"   来源: {hawaiihub_article['source_name']}")
    print(f"   内容长度: {len(hawaiihub_article['content'])} 字符")

    # 验证 HawaiiHub 格式
    validate_hawaiihub_article(hawaiihub_article)

    # 3. 转换为火鸟 API 格式
    print("\n🔄 Step 3: 转换为火鸟 API 格式")
    firebird_data = hawaiihub_to_firebird(hawaiihub_article)
    print(f"   标题: {firebird_data['title']}")
    print(f"   关键词: {firebird_data['keywords']}")
    print(f"   来源: {firebird_data['source']}")

    # 验证火鸟 API 格式
    validate_firebird_article(firebird_data)

    # 4. 保存为 JSON 文件
    print("\n💾 Step 4: 保存为 JSON 文件")
    output_file = "firebird_article_example.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(firebird_data, f, ensure_ascii=False, indent=2)
    print(f"   已保存到: {output_file}")

    # 5. 模拟 API 响应
    print("\n📤 Step 5: 模拟发布到火鸟 API")
    mock_response = {"state": 100, "info": "发布成功", "id": 12345}
    print(f"   响应: {mock_response}")

    if mock_response["state"] == 100:
        article_url = f"https://hawaiihub.net/news/{mock_response['id']}"
        print("   ✅ 发布成功！")
        print(f"   文章链接: {article_url}")
    else:
        print(f"   ❌ 发布失败: {mock_response['info']}")

    print("\n" + "=" * 60)
    print("工作流完成 🎉")
    print("=" * 60)


# =============================================================================
# 6. 使用示例
# =============================================================================


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "🔥" * 30)
    print("火鸟门户系统新闻 JSON 格式示例")
    print("🔥" * 30)

    # 示例 1: 查看各种格式
    print("\n" + "=" * 60)
    print("示例 1: 各种 JSON 格式")
    print("=" * 60)

    print("\n1️⃣ 火鸟 API 发布格式:")
    firebird_example = get_firebird_api_example()
    print(json.dumps(firebird_example, ensure_ascii=False, indent=2))

    print("\n2️⃣ NewsAPI 响应格式:")
    newsapi_example = get_newsapi_example()
    print(json.dumps(newsapi_example, ensure_ascii=False, indent=2))

    print("\n3️⃣ HawaiiHub 内部格式:")
    hawaiihub_example = get_hawaiihub_example()
    print(json.dumps(hawaiihub_example, ensure_ascii=False, indent=2))

    # 示例 2: 数据验证
    print("\n" + "=" * 60)
    print("示例 2: 数据验证")
    print("=" * 60)

    print("\n✅ 正确的火鸟 API 格式:")
    valid_data = {
        "title": "夏威夷租房价格创新高",
        "description": "檀香山平均租金达到 $2,500/月",
        "body": "# 详细内容\n\n檀香山租房价格达到历史新高，平均月租金已达 $2,500，同比上涨 15%。"
        * 2,
        "keywords": "夏威夷,租房,房价",
        "source": "Civil Beat",
    }
    validate_firebird_article(valid_data)

    print("\n❌ 错误的火鸟 API 格式:")
    invalid_data = {
        "title": "",  # 标题为空（错误）
        "description": "x" * 600,  # 描述太长（错误）
        "body": "太短",  # 正文太短（错误）
    }
    validate_firebird_article(invalid_data)

    # 示例 3: 完整工作流
    complete_workflow_example()

    # 示例 4: 关键词提取
    print("\n" + "=" * 60)
    print("示例 4: 关键词提取")
    print("=" * 60)

    text = """夏威夷租房价格创新高。檀香山平均租金达到 $2,500/月，
    同比上涨 15%。住房危机加剧，影响中低收入家庭。"""

    keywords = extract_keywords_simple("夏威夷租房价格", text)
    print(f"\n文本: {text}")
    print(f"提取的关键词: {keywords}")


if __name__ == "__main__":
    main()
