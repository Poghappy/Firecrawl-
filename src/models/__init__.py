"""
业务场景数据模型

提供各个业务场景的 Pydantic 数据模型。

支持的业务场景:
- 新闻资讯 (NewsArticle)
- 团购比价 (Product, PriceHistory)
- 招聘信息 (JobPosting)
- 租房信息 (RentalListing)
- 学习资源 (LearningResource)
"""

from .news import NewsArticle, NewsSource
from .ecommerce import Product, PriceHistory, ProductReview
from .recruitment import JobPosting, CompanyInfo
from .rental import RentalListing, RentalProperty
from .learning import LearningResource, Course, CourseModule

__all__ = [
    # 新闻
    "NewsArticle",
    "NewsSource",
    # 电商
    "Product",
    "PriceHistory",
    "ProductReview",
    # 招聘
    "JobPosting",
    "CompanyInfo",
    # 租房
    "RentalListing",
    "RentalProperty",
    # 学习
    "LearningResource",
    "Course",
    "CourseModule",
]
