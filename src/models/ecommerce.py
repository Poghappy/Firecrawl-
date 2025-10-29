#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商团购数据模型

用于省钱团购网的数据结构定义。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, field_validator


class Product(BaseModel):
    """商品信息"""
    # 基础信息
    title: str = Field(..., min_length=1, max_length=500, description="商品名称")
    description: Optional[str] = Field(None, max_length=5000, description="商品描述")

    # 价格信息
    current_price: Decimal = Field(..., gt=0, description="当前价格")
    original_price: Optional[Decimal] = Field(None, gt=0, description="原价")
    discount: Optional[Decimal] = Field(None, ge=0, le=100, description="折扣率(%)")

    # 商品详情
    sku: Optional[str] = Field(None, max_length=100, description="SKU编号")
    brand: Optional[str] = Field(None, max_length=100, description="品牌")
    category: str = Field(default="其他", description="分类")

    # 来源信息
    platform: str = Field(..., description="电商平台")
    product_url: HttpUrl = Field(..., description="商品链接")
    seller: Optional[str] = Field(None, max_length=200, description="商家")

    # 库存和销售
    stock_status: str = Field(default="有货", description="库存状态")
    sales_count: Optional[int] = Field(None, ge=0, description="销量")

    # 评价信息
    rating: Optional[Decimal] = Field(None, ge=0, le=5, description="评分(0-5)")
    review_count: Optional[int] = Field(None, ge=0, description="评论数")

    # 媒体内容
    images: List[HttpUrl] = Field(default_factory=list, description="商品图片")
    cover_image: Optional[HttpUrl] = Field(None, description="封面图")

    # 规格信息
    specifications: dict = Field(default_factory=dict, description="商品规格")
    variants: List[dict] = Field(default_factory=list, description="商品变体")

    # 系统字段
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")
    price_updated_at: datetime = Field(default_factory=datetime.now, description="价格更新时间")

    @field_validator('discount', mode='before')
    @classmethod
    def calculate_discount(cls, v, info):
        """自动计算折扣率"""
        if v is not None:
            return v

        values = info.data
        if 'original_price' in values and 'current_price' in values:
            original = values['original_price']
            current = values['current_price']
            if original and current and original > current:
                return ((original - current) / original * 100).quantize(Decimal('0.01'))
        return None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "iPhone 15 Pro Max 256GB",
                "description": "最新款苹果手机，强大性能",
                "current_price": 8999.00,
                "original_price": 9999.00,
                "discount": 10.00,
                "brand": "Apple",
                "category": "手机数码",
                "platform": "京东",
                "product_url": "https://jd.com/product/123",
                "stock_status": "有货",
                "rating": 4.8,
                "review_count": 1250
            }
        }


class PriceHistory(BaseModel):
    """价格历史记录"""
    product_id: str = Field(..., description="商品ID")
    platform: str = Field(..., description="平台")
    price: Decimal = Field(..., gt=0, description="价格")
    stock_status: str = Field(..., description="库存状态")
    recorded_at: datetime = Field(default_factory=datetime.now, description="记录时间")

    # 价格变化
    price_change: Optional[Decimal] = Field(None, description="价格变化")
    change_percentage: Optional[Decimal] = Field(None, description="变化百分比")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod-12345",
                "platform": "京东",
                "price": 8999.00,
                "stock_status": "有货",
                "recorded_at": "2025-10-29T10:00:00",
                "price_change": -100.00,
                "change_percentage": -1.10
            }
        }


class ProductReview(BaseModel):
    """商品评论"""
    product_id: str = Field(..., description="商品ID")
    reviewer_name: Optional[str] = Field(None, max_length=100, description="评论者")
    rating: Decimal = Field(..., ge=0, le=5, description="评分")
    content: str = Field(..., min_length=1, max_length=5000, description="评论内容")

    # 评论详情
    images: List[HttpUrl] = Field(default_factory=list, description="评论图片")
    pros: Optional[str] = Field(None, description="优点")
    cons: Optional[str] = Field(None, description="缺点")

    # 统计信息
    helpful_count: int = Field(default=0, ge=0, description="有用数")
    verified_purchase: bool = Field(default=False, description="已验证购买")

    # 时间信息
    review_date: datetime = Field(..., description="评论时间")
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod-12345",
                "reviewer_name": "用户123",
                "rating": 5.0,
                "content": "商品质量很好，性价比高！",
                "verified_purchase": True,
                "helpful_count": 15,
                "review_date": "2025-10-28T15:30:00"
            }
        }


# 使用示例
if __name__ == "__main__":
    # 创建商品
    product = Product(
        title="测试商品",
        current_price=Decimal("99.99"),
        original_price=Decimal("199.99"),
        platform="京东",
        product_url="https://jd.com/test",
        category="测试分类",
        rating=Decimal("4.5"),
        review_count=100
    )

    print("商品创建成功:")
    print(f"  名称: {product.title}")
    print(f"  当前价格: ¥{product.current_price}")
    print(f"  折扣: {product.discount}%")
    print(f"  评分: {product.rating}")

    # 创建价格历史
    history = PriceHistory(
        product_id="prod-001",
        platform="京东",
        price=Decimal("99.99"),
        stock_status="有货"
    )

    print(f"\n价格记录: ¥{history.price} ({history.recorded_at})")
