#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻资讯数据模型

用于火鸟门户新闻系统的数据结构定义。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, field_validator


class NewsSource(BaseModel):
    """新闻来源"""
    source_id: str = Field(..., description="来源ID")
    name: str = Field(..., description="来源名称")
    url: HttpUrl = Field(..., description="来源URL")
    category: str = Field(default="综合", description="分类")
    language: str = Field(default="zh-CN", description="语言")
    priority: int = Field(default=1, ge=0, le=10, description="优先级(0-10)")
    enabled: bool = Field(default=True, description="是否启用")


class NewsArticle(BaseModel):
    """新闻文章"""
    # 基础信息
    title: str = Field(..., min_length=1, max_length=500, description="标题")
    content: str = Field(..., min_length=100, description="正文内容")
    summary: Optional[str] = Field(None, max_length=1000, description="摘要")

    # 元信息
    author: Optional[str] = Field(None, max_length=100, description="作者")
    source: str = Field(..., description="来源")
    source_url: HttpUrl = Field(..., description="原文链接")
    publish_date: datetime = Field(..., description="发布时间")

    # 分类和标签
    category: str = Field(default="综合", description="分类")
    tags: List[str] = Field(default_factory=list, description="标签")
    keywords: List[str] = Field(default_factory=list, description="关键词")

    # 媒体内容
    images: List[HttpUrl] = Field(default_factory=list, description="图片列表")
    videos: List[HttpUrl] = Field(default_factory=list, description="视频列表")
    cover_image: Optional[HttpUrl] = Field(None, description="封面图")

    # 统计信息
    view_count: int = Field(default=0, ge=0, description="阅读数")
    like_count: int = Field(default=0, ge=0, description="点赞数")
    comment_count: int = Field(default=0, ge=0, description="评论数")

    # 系统字段
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")
    content_hash: Optional[str] = Field(None, description="内容哈希")
    language: str = Field(default="zh-CN", description="语言")

    @field_validator('tags', 'keywords', mode='before')
    @classmethod
    def split_comma_separated(cls, v):
        """将逗号分隔的字符串转换为列表"""
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(',') if tag.strip()]
        return v

    @field_validator('content')
    @classmethod
    def validate_content_length(cls, v):
        """验证内容长度"""
        if len(v) < 100:
            raise ValueError("文章内容不能少于100字符")
        if len(v) > 100000:
            raise ValueError("文章内容不能超过100000字符")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "夏威夷新闻：最新资讯",
                "content": "这是一篇关于夏威夷的新闻报道...",
                "summary": "简要概述新闻内容",
                "author": "记者张三",
                "source": "Hawaii News Now",
                "source_url": "https://hawaiinewsnow.com/article/123",
                "publish_date": "2025-10-29T10:00:00",
                "category": "本地新闻",
                "tags": ["夏威夷", "社区", "活动"],
                "keywords": ["夏威夷", "新闻", "最新"],
                "images": ["https://example.com/image.jpg"],
            }
        }


# 使用示例
if __name__ == "__main__":
    # 创建新闻文章
    article = NewsArticle(
        title="测试新闻标题",
        content="这是一篇测试新闻文章的内容，包含至少100个字符以满足验证要求。" * 5,
        author="测试作者",
        source="测试来源",
        source_url="https://example.com/news/1",
        publish_date=datetime.now(),
        category="科技",
        tags=["测试", "新闻"],
        keywords=["关键词1", "关键词2"]
    )

    print("新闻文章创建成功:")
    print(f"  标题: {article.title}")
    print(f"  作者: {article.author}")
    print(f"  来源: {article.source}")
    print(f"  分类: {article.category}")
    print(f"  标签: {', '.join(article.tags)}")

    # 导出为 JSON
    print("\nJSON 格式:")
    print(article.model_dump_json(indent=2))
