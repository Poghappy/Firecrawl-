#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
租房信息数据模型

用于房地产租赁系统的数据结构定义。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, field_validator


class RentalProperty(BaseModel):
    """房产基本信息"""
    property_id: Optional[str] = Field(None, description="房产ID")
    address: str = Field(..., min_length=1, max_length=500, description="地址")
    city: str = Field(..., max_length=100, description="城市")
    state: Optional[str] = Field(None, max_length=50, description="州/省")
    zip_code: Optional[str] = Field(None, max_length=20, description="邮编")

    # 地理位置
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90, description="纬度")
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180, description="经度")
    neighborhood: Optional[str] = Field(None, max_length=100, description="社区")

    # 房产类型
    property_type: str = Field(default="公寓", description="房产类型")
    building_name: Optional[str] = Field(None, max_length=200, description="楼盘名称")
    year_built: Optional[int] = Field(None, ge=1800, le=2100, description="建造年份")

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Main Street, Apt 4B",
                "city": "Honolulu",
                "state": "HI",
                "zip_code": "96813",
                "neighborhood": "Waikiki",
                "property_type": "公寓"
            }
        }


class RentalListing(BaseModel):
    """租房信息"""
    # 标题和描述
    title: str = Field(..., min_length=1, max_length=500, description="标题")
    description: str = Field(..., min_length=50, description="描述")

    # 房产信息
    property_info: Optional[RentalProperty] = Field(None, description="房产详情")

    # 租金信息
    rent_price: Decimal = Field(..., gt=0, description="月租金")
    deposit: Optional[Decimal] = Field(None, ge=0, description="押金")
    utilities_included: bool = Field(default=False, description="是否包含水电")

    # 房屋规格
    bedrooms: Optional[int] = Field(None, ge=0, description="卧室数")
    bathrooms: Optional[Decimal] = Field(None, ge=0, description="浴室数")
    area_sqft: Optional[int] = Field(None, gt=0, description="面积(平方英尺)")
    area_sqm: Optional[Decimal] = Field(None, gt=0, description="面积(平方米)")
    floor: Optional[int] = Field(None, description="楼层")
    total_floors: Optional[int] = Field(None, description="总楼层")

    # 设施和特点
    amenities: List[str] = Field(default_factory=list, description="设施")
    features: List[str] = Field(default_factory=list, description="特点")
    parking: Optional[str] = Field(None, max_length=100, description="停车")
    pet_policy: Optional[str] = Field(None, max_length=200, description="宠物政策")

    # 租赁条款
    lease_term: Optional[str] = Field(None, max_length=100, description="租期")
    available_date: Optional[datetime] = Field(None, description="可入住日期")
    min_lease_months: Optional[int] = Field(None, ge=1, description="最短租期(月)")

    # 联系方式
    contact_name: Optional[str] = Field(None, max_length=100, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=50, description="联系电话")
    contact_email: Optional[str] = Field(None, max_length=100, description="联系邮箱")

    # 图片和媒体
    images: List[HttpUrl] = Field(default_factory=list, description="房源图片")
    cover_image: Optional[HttpUrl] = Field(None, description="封面图")
    virtual_tour_url: Optional[HttpUrl] = Field(None, description="虚拟看房链接")

    # 来源信息
    source: str = Field(..., description="信息来源")
    source_url: HttpUrl = Field(..., description="原始链接")
    listing_id: Optional[str] = Field(None, description="房源ID")

    # 状态信息
    status: str = Field(default="可租", description="状态")
    is_verified: bool = Field(default=False, description="是否已验证")
    is_featured: bool = Field(default=False, description="是否精选")

    # 时间信息
    posted_date: Optional[datetime] = Field(None, description="发布时间")
    updated_date: Optional[datetime] = Field(None, description="更新时间")
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")

    # 统计信息
    view_count: int = Field(default=0, ge=0, description="浏览次数")
    inquiry_count: int = Field(default=0, ge=0, description="咨询次数")

    @field_validator('amenities', 'features', mode='before')
    @classmethod
    def split_amenities(cls, v):
        """将字符串或列表转换为列表"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(',') if item.strip()]
        return v

    @field_validator('area_sqm', mode='before')
    @classmethod
    def convert_sqft_to_sqm(cls, v, info):
        """自动从平方英尺转换为平方米"""
        if v is None and 'area_sqft' in info.data:
            sqft = info.data['area_sqft']
            if sqft:
                return Decimal(str(sqft * 0.092903))  # 1 sqft = 0.092903 sqm
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "市中心2室1厅精装公寓",
                "description": "位于市中心黄金地段，交通便利，周边配套齐全...",
                "rent_price": 2500.00,
                "deposit": 2500.00,
                "bedrooms": 2,
                "bathrooms": 1.0,
                "area_sqft": 850,
                "amenities": ["空调", "洗衣机", "冰箱", "健身房"],
                "features": ["采光好", "景观好", "安静"],
                "lease_term": "1年",
                "source": "Craigslist",
                "source_url": "https://honolulu.craigslist.org/123",
                "status": "可租"
            }
        }


# 使用示例
if __name__ == "__main__":
    # 创建房产信息
    property_info = RentalProperty(
        address="123 Kalakaua Ave, Apt 502",
        city="Honolulu",
        state="HI",
        zip_code="96815",
        neighborhood="Waikiki",
        property_type="公寓"
    )

    # 创建租房信息
    listing = RentalListing(
        title="威基基海景公寓，步行到海滩",
        description="位于威基基核心地段的精装公寓，拥有无敌海景，步行5分钟即可到达海滩。" * 3,
        property_info=property_info,
        rent_price=Decimal("3500"),
        deposit=Decimal("3500"),
        bedrooms=2,
        bathrooms=Decimal("2.0"),
        area_sqft=1000,
        amenities=["空调", "洗衣机", "烘干机", "停车位", "游泳池"],
        features=["海景", "阳台", "新装修"],
        source="Zillow",
        source_url="https://zillow.com/rental/123",
        status="可租"
    )

    print("租房信息创建成功:")
    print(f"  标题: {listing.title}")
    print(f"  租金: ${listing.rent_price}/月")
    print(f"  户型: {listing.bedrooms}室{listing.bathrooms}卫")
    print(f"  面积: {listing.area_sqft} sqft ({listing.area_sqm:.2f} sqm)")
    print(f"  地址: {listing.property_info.address}")
    print(f"  设施: {', '.join(listing.amenities)}")

    # 导出为 JSON
    print("\nJSON 格式:")
    print(listing.model_dump_json(indent=2))
