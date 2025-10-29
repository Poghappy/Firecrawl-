"""
檀香山房产数据模型
Real Estate Data Models for Honolulu Rental Listings
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class RentalListing(BaseModel):
    """房屋出租信息模型"""

    # 基本信息
    title: str = Field(..., description="房源标题")
    description: str = Field(..., description="房源描述")

    # 价格信息
    price: float = Field(..., description="租金（美元/月）")
    currency: str = Field(default="USD", description="货币单位")
    deposit: Optional[float] = Field(None, description="押金")

    # 位置信息
    address: str = Field(..., description="详细地址")
    neighborhood: str = Field(..., description="社区/地区")
    city: str = Field(default="Honolulu", description="城市")
    state: str = Field(default="HI", description="州")
    zipcode: Optional[str] = Field(None, description="邮编")

    # 房屋信息
    bedrooms: Optional[int] = Field(None, description="卧室数量")
    bathrooms: Optional[float] = Field(None, description="浴室数量")
    square_feet: Optional[int] = Field(None, description="面积（平方英尺）")
    property_type: Optional[str] = Field(None, description="房屋类型（公寓/独立屋/联排别墅）")

    # 图片
    images: List[str] = Field(default_factory=list, description="房源图片 URL 列表")
    main_image: Optional[str] = Field(None, description="主图片 URL")

    # 联系方式
    contact_name: Optional[str] = Field(None, description="联系人姓名")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[str] = Field(None, description="联系邮箱")

    # 其他信息
    amenities: List[str] = Field(default_factory=list, description="配套设施")
    pets_allowed: Optional[bool] = Field(None, description="是否允许养宠物")
    parking: Optional[str] = Field(None, description="停车位信息")
    available_date: Optional[str] = Field(None, description="可入住日期")
    lease_term: Optional[str] = Field(None, description="租期要求")

    # 元数据
    source_url: str = Field(..., description="来源 URL")
    source_platform: str = Field(..., description="来源平台（Craigslist/Zillow 等）")
    posted_date: Optional[str] = Field(None, description="发布时间")
    scraped_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="采集时间（ISO 格式）")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Beautiful 2BR Apartment in Waikiki",
                "description": "Spacious 2-bedroom apartment with ocean view",
                "price": 2500.0,
                "address": "123 Kuhio Ave, Honolulu, HI 96815",
                "neighborhood": "Waikiki",
                "bedrooms": 2,
                "bathrooms": 1.5,
                "images": ["https://example.com/img1.jpg"],
                "contact_phone": "(808) 555-1234",
                "source_url": "https://honolulu.craigslist.org/apa/d/...",
                "source_platform": "Craigslist"
            }
        }


class RentalSearchQuery(BaseModel):
    """房源搜索查询参数"""

    city: str = Field(default="Honolulu", description="城市")
    state: str = Field(default="HI", description="州")

    # 价格范围
    min_price: Optional[float] = Field(None, description="最低价格")
    max_price: Optional[float] = Field(None, description="最高价格")

    # 房间要求
    min_bedrooms: Optional[int] = Field(None, description="最少卧室数")
    max_bedrooms: Optional[int] = Field(None, description="最多卧室数")

    # 时间范围
    days_back: int = Field(default=14, description="搜索最近 N 天的房源")

    # 地区过滤
    neighborhoods: List[str] = Field(default_factory=list, description="指定社区列表")

    # 其他过滤
    pets_allowed: Optional[bool] = Field(None, description="是否允许宠物")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Honolulu",
                "min_price": 1000,
                "max_price": 3000,
                "min_bedrooms": 1,
                "days_back": 14,
                "neighborhoods": ["Waikiki", "Manoa", "Kaimuki"]
            }
        }


class RentalDataset(BaseModel):
    """房源数据集"""

    query: RentalSearchQuery = Field(..., description="搜索参数")
    listings: List[RentalListing] = Field(default_factory=list, description="房源列表")
    total_count: int = Field(default=0, description="总数量")
    collected_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="采集时间")
    timezone: str = Field(default="Pacific/Honolulu", description="时区")

    def add_listing(self, listing: RentalListing):
        """添加房源"""
        self.listings.append(listing)
        self.total_count = len(self.listings)

    def filter_by_price(self, min_price: float, max_price: float) -> List[RentalListing]:
        """按价格过滤"""
        return [
            listing for listing in self.listings
            if min_price <= listing.price <= max_price
        ]

    def filter_by_neighborhood(self, neighborhoods: List[str]) -> List[RentalListing]:
        """按社区过滤"""
        return [
            listing for listing in self.listings
            if listing.neighborhood in neighborhoods
        ]

    def get_statistics(self) -> dict:
        """获取统计信息"""
        if not self.listings:
            return {}

        prices = [listing.price for listing in self.listings]
        return {
            "total_count": self.total_count,
            "avg_price": sum(prices) / len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "neighborhoods": list(set(listing.neighborhood for listing in self.listings)),
        }
