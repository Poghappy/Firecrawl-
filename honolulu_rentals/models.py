"""
檀香山租房信息采集系统 - 数据模型

版本: v1.0
创建日期: 2025-10-29
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PropertyType(str, Enum):
    """房型枚举"""
    STUDIO = "Studio"
    ONE_BED_ONE_BATH = "1B1B"
    ONE_BED_TWO_BATH = "1B2B"
    TWO_BED_ONE_BATH = "2B1B"
    TWO_BED_TWO_BATH = "2B2B"
    THREE_BED = "3B+"
    OTHER = "Other"


class Platform(str, Enum):
    """平台枚举"""
    CRAIGSLIST = "craigslist"
    ZILLOW = "zillow"
    APARTMENTS = "apartments"


class ContactMethod(BaseModel):
    """联系方式"""
    phone: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None  # 平台内联系链接

    @validator('phone')
    def validate_phone(cls, v):
        """验证电话号码格式"""
        if v:
            # 简单验证：移除所有非数字字符后应该是10位
            digits = ''.join(filter(str.isdigit, v))
            if len(digits) != 10:
                return None  # 无效电话返回 None
        return v

    @validator('email')
    def validate_email(cls, v):
        """验证邮箱格式"""
        if v and '@' not in v:
            return None
        return v


class RentalListing(BaseModel):
    """租房信息核心数据模型"""

    # ============================================================
    # 基础信息（必填）
    # ============================================================
    id: str = Field(..., description="唯一标识（平台_时间戳_索引）")
    title: str = Field(..., min_length=1, max_length=500, description="房源标题")
    price: float = Field(..., ge=0, description="月租金（美元）")
    url: str = Field(..., description="原始房源链接")
    platform: Platform = Field(..., description="来源平台")

    # ============================================================
    # 房屋信息
    # ============================================================
    property_type: Optional[PropertyType] = None
    bedrooms: Optional[str] = Field(None, description="卧室数（如 1, 2, Studio）")
    bathrooms: Optional[str] = Field(None, description="浴室数（如 1, 1.5, 2）")
    area_sqft: Optional[int] = Field(None, ge=0, description="面积（平方英尺）")

    # ============================================================
    # 位置信息
    # ============================================================
    neighborhood: Optional[str] = Field(None, description="社区名称")
    address: Optional[str] = Field(None, description="详细地址")
    zipcode: Optional[str] = Field(None, description="邮编")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    # ============================================================
    # 媒体资源
    # ============================================================
    images: List[str] = Field(default_factory=list, description="房屋图片 URLs")
    thumbnail: Optional[str] = Field(None, description="缩略图 URL")

    # ============================================================
    # 联系方式
    # ============================================================
    contact: ContactMethod = Field(default_factory=ContactMethod)

    # ============================================================
    # 详细信息
    # ============================================================
    description: Optional[str] = Field(None, max_length=10000, description="房源描述")
    amenities: List[str] = Field(default_factory=list, description="设施列表")
    utilities_included: List[str] = Field(default_factory=list, description="包含费用")
    pets_allowed: Optional[bool] = None
    parking_available: Optional[bool] = None
    laundry: Optional[str] = Field(None, description="洗衣设施（In-unit/Shared/None）")

    # ============================================================
    # 日期信息
    # ============================================================
    available_date: Optional[datetime] = None
    posted_date: Optional[datetime] = None
    scraped_at: datetime = Field(default_factory=datetime.now)

    # ============================================================
    # 元数据
    # ============================================================
    is_verified: bool = Field(default=False, description="是否已验证联系方式")
    is_duplicate: bool = Field(default=False, description="是否重复房源")
    duplicate_of: Optional[str] = Field(None, description="重复的原始房源 ID")
    similarity_score: Optional[float] = Field(None, ge=0, le=1, description="相似度分数")

    # 原始数据（用于调试）
    raw_data: Optional[dict] = Field(default=None, description="原始采集数据")

    class Config:
        use_enum_values = True

    @validator('price')
    def validate_price(cls, v):
        """验证价格合理性"""
        if v < 100 or v > 10000:
            raise ValueError(f"价格不合理: ${v}")
        return v

    @validator('images')
    def validate_images(cls, v):
        """确保图片列表不为空"""
        # 移除无效的图片 URL
        valid_images = [img for img in v if img and len(img) > 10]
        return valid_images

    def to_dict(self) -> dict:
        """转换为字典（用于导出）"""
        data = self.dict()
        # 转换日期为字符串
        if self.available_date:
            data['available_date'] = self.available_date.isoformat()
        if self.posted_date:
            data['posted_date'] = self.posted_date.isoformat()
        data['scraped_at'] = self.scraped_at.isoformat()
        return data


class RentalListingBatch(BaseModel):
    """批量房源数据"""
    total: int = Field(..., description="总数")
    filtered: int = Field(..., description="筛选后数量")
    duplicates_removed: int = Field(default=0, description="去重数量")
    listings: List[RentalListing] = Field(default_factory=list)
    scraped_at: datetime = Field(default_factory=datetime.now)

    # 成本统计
    cost_credits: int = Field(default=0, description="消耗的 Firecrawl Credits")
    cost_usd: float = Field(default=0.0, description="消耗的费用（美元）")

    # 平台统计
    platform_stats: dict = Field(default_factory=dict, description="各平台统计")

    class Config:
        use_enum_values = True

    def add_listing(self, listing: RentalListing):
        """添加房源"""
        self.listings.append(listing)
        self.total += 1

        # 更新平台统计
        platform = listing.platform
        if platform not in self.platform_stats:
            self.platform_stats[platform] = {
                "count": 0,
                "avg_price": 0,
                "min_price": float('inf'),
                "max_price": 0,
            }

        stats = self.platform_stats[platform]
        stats["count"] += 1
        stats["min_price"] = min(stats["min_price"], listing.price)
        stats["max_price"] = max(stats["max_price"], listing.price)

    def get_summary(self) -> dict:
        """获取统计摘要"""
        if not self.listings:
            return {
                "total": 0,
                "avg_price": 0,
                "min_price": 0,
                "max_price": 0,
            }

        prices = [l.price for l in self.listings]
        return {
            "total": len(self.listings),
            "filtered": self.filtered,
            "duplicates_removed": self.duplicates_removed,
            "avg_price": sum(prices) / len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "platforms": self.platform_stats,
            "cost_credits": self.cost_credits,
            "cost_usd": self.cost_usd,
        }


class ScraperStats(BaseModel):
    """采集器统计信息"""
    platform: Platform
    start_time: datetime
    end_time: Optional[datetime] = None
    total_urls: int = 0
    successful: int = 0
    failed: int = 0
    duplicates: int = 0
    credits_used: int = 0
    errors: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True

    def mark_complete(self):
        """标记完成"""
        self.end_time = datetime.now()

    def get_duration(self) -> float:
        """获取耗时（秒）"""
        if not self.end_time:
            return 0
        return (self.end_time - self.start_time).total_seconds()

    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.total_urls == 0:
            return 0
        return self.successful / self.total_urls
