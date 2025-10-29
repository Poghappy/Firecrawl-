#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习资源数据模型

用于学习网平台的数据结构定义。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, field_validator


class CourseModule(BaseModel):
    """课程模块"""
    module_id: Optional[str] = Field(None, description="模块ID")
    title: str = Field(..., max_length=200, description="模块标题")
    description: Optional[str] = Field(None, max_length=2000, description="模块描述")
    order: int = Field(..., ge=1, description="顺序")

    # 内容信息
    lessons: List[str] = Field(default_factory=list, description="课程列表")
    duration_minutes: Optional[int] = Field(None, ge=0, description="时长(分钟)")

    # 资源链接
    resources: List[HttpUrl] = Field(default_factory=list, description="学习资源")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python基础入门",
                "description": "学习Python基础语法",
                "order": 1,
                "lessons": ["变量和数据类型", "控制流", "函数"],
                "duration_minutes": 120
            }
        }


class Course(BaseModel):
    """课程信息"""
    # 基础信息
    title: str = Field(..., min_length=1, max_length=500, description="课程标题")
    subtitle: Optional[str] = Field(None, max_length=500, description="副标题")
    description: str = Field(..., min_length=50, description="课程描述")

    # 分类和标签
    category: str = Field(..., max_length=100, description="课程分类")
    subcategory: Optional[str] = Field(None, max_length=100, description="子分类")
    tags: List[str] = Field(default_factory=list, description="标签")

    # 讲师信息
    instructor_name: str = Field(..., max_length=200, description="讲师姓名")
    instructor_bio: Optional[str] = Field(None, max_length=2000, description="讲师简介")
    instructor_image: Optional[HttpUrl] = Field(None, description="讲师头像")

    # 课程内容
    modules: List[CourseModule] = Field(default_factory=list, description="课程模块")
    total_lessons: int = Field(default=0, ge=0, description="总课时数")
    total_duration_hours: Optional[Decimal] = Field(None, ge=0, description="总时长(小时)")

    # 难度和要求
    level: str = Field(default="初级", description="难度级别")
    prerequisites: List[str] = Field(default_factory=list, description="先修要求")
    target_audience: List[str] = Field(default_factory=list, description="目标学员")

    # 学习成果
    learning_outcomes: List[str] = Field(default_factory=list, description="学习成果")
    skills: List[str] = Field(default_factory=list, description="技能收获")

    # 价格信息
    price: Optional[Decimal] = Field(None, ge=0, description="课程价格")
    original_price: Optional[Decimal] = Field(None, ge=0, description="原价")
    is_free: bool = Field(default=False, description="是否免费")
    discount: Optional[Decimal] = Field(None, ge=0, le=100, description="折扣率(%)")

    # 评价信息
    rating: Optional[Decimal] = Field(None, ge=0, le=5, description="评分(0-5)")
    review_count: int = Field(default=0, ge=0, description="评论数")
    student_count: int = Field(default=0, ge=0, description="学员数")

    # 媒体内容
    cover_image: Optional[HttpUrl] = Field(None, description="封面图")
    promo_video: Optional[HttpUrl] = Field(None, description="宣传视频")
    sample_videos: List[HttpUrl] = Field(default_factory=list, description="试看视频")

    # 来源信息
    source: str = Field(..., description="来源平台")
    source_url: HttpUrl = Field(..., description="原始链接")
    course_id: Optional[str] = Field(None, description="课程ID")

    # 状态信息
    status: str = Field(default="已发布", description="状态")
    language: str = Field(default="中文", description="语言")
    has_certificate: bool = Field(default=False, description="是否提供证书")

    # 时间信息
    created_date: Optional[datetime] = Field(None, description="创建时间")
    updated_date: Optional[datetime] = Field(None, description="更新时间")
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")

    @field_validator('tags', 'prerequisites', 'learning_outcomes', 'skills', mode='before')
    @classmethod
    def split_list_fields(cls, v):
        """将字符串或列表转换为列表"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(',') if item.strip()]
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python全栈开发从入门到精通",
                "description": "从零基础学习Python编程，掌握Web开发全栈技能...",
                "category": "编程开发",
                "subcategory": "Python",
                "instructor_name": "张老师",
                "level": "初级-中级",
                "total_lessons": 120,
                "total_duration_hours": 40,
                "price": 299.00,
                "rating": 4.8,
                "student_count": 5000,
                "source": "Coursera",
                "source_url": "https://coursera.org/course/123"
            }
        }


class LearningResource(BaseModel):
    """学习资源"""
    # 基础信息
    title: str = Field(..., min_length=1, max_length=500, description="资源标题")
    description: Optional[str] = Field(None, max_length=5000, description="资源描述")

    # 资源类型
    resource_type: str = Field(..., description="资源类型")
    format: str = Field(..., description="格式")

    # 分类和标签
    category: str = Field(..., max_length=100, description="分类")
    tags: List[str] = Field(default_factory=list, description="标签")

    # 资源详情
    author: Optional[str] = Field(None, max_length=200, description="作者")
    publisher: Optional[str] = Field(None, max_length=200, description="发布者")
    language: str = Field(default="中文", description="语言")

    # 难度和时长
    level: str = Field(default="初级", description="难度级别")
    duration_minutes: Optional[int] = Field(None, ge=0, description="时长(分钟)")

    # 链接和文件
    resource_url: HttpUrl = Field(..., description="资源链接")
    download_url: Optional[HttpUrl] = Field(None, description="下载链接")
    cover_image: Optional[HttpUrl] = Field(None, description="封面图")

    # 评价信息
    rating: Optional[Decimal] = Field(None, ge=0, le=5, description="评分")
    view_count: int = Field(default=0, ge=0, description="浏览次数")
    download_count: int = Field(default=0, ge=0, description="下载次数")

    # 状态信息
    is_free: bool = Field(default=True, description="是否免费")
    price: Optional[Decimal] = Field(None, ge=0, description="价格")

    # 来源信息
    source: str = Field(..., description="来源")
    source_url: HttpUrl = Field(..., description="原始链接")

    # 时间信息
    publish_date: Optional[datetime] = Field(None, description="发布时间")
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python 编程指南 PDF",
                "description": "完整的Python学习资料",
                "resource_type": "文档",
                "format": "PDF",
                "category": "编程",
                "author": "张三",
                "level": "初级",
                "resource_url": "https://example.com/python-guide.pdf",
                "is_free": True,
                "source": "GitHub",
                "source_url": "https://github.com/repo/python-guide"
            }
        }


# 使用示例
if __name__ == "__main__":
    # 创建课程模块
    module1 = CourseModule(
        title="Python基础",
        description="学习Python基础语法",
        order=1,
        lessons=["变量", "数据类型", "运算符"],
        duration_minutes=120
    )

    # 创建课程
    course = Course(
        title="Python 全栈开发",
        description="从零开始学习Python全栈开发，包括前端、后端、数据库等完整技术栈。" * 2,
        category="编程开发",
        instructor_name="李老师",
        modules=[module1],
        total_lessons=80,
        total_duration_hours=Decimal("30"),
        level="初级-中级",
        price=Decimal("299"),
        rating=Decimal("4.8"),
        student_count=3000,
        source="在线教育平台",
        source_url="https://edu.example.com/course/123"
    )

    print("课程创建成功:")
    print(f"  课程: {course.title}")
    print(f"  讲师: {course.instructor_name}")
    print(f"  级别: {course.level}")
    print(f"  课时: {course.total_lessons}")
    print(f"  时长: {course.total_duration_hours}小时")
    print(f"  价格: ¥{course.price}")
    print(f"  评分: {course.rating} ({course.student_count}人学习)")

    # 导出为 JSON
    print("\nJSON 格式:")
    print(course.model_dump_json(indent=2, exclude={'modules'}))
