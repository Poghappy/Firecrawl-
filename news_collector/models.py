"""
新闻采集系统 - 数据模型

版本: v1.0
创建日期: 2025-01-29
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NewsSource(str, Enum):
    """新闻源枚举"""
    HAWAII_NEWS_NOW = "hawaii-news-now"
    CIVIL_BEAT = "civil-beat"
    STAR_ADVERTISER = "star-advertiser"
    KHON2 = "khon2"
    KITV = "kitv"


class NewsPriority(str, Enum):
    """新闻优先级"""
    P0 = "P0"  # 核心新闻源
    P1 = "P1"  # 重要新闻源
    P2 = "P2"  # 可选新闻源


class NewsArticle(BaseModel):
    """新闻文章数据模型"""

    # 基础信息
    source_id: NewsSource = Field(..., description="新闻源ID")
    source_name: str = Field(..., description="新闻源名称")
    url: str = Field(..., description="文章URL")

    # 内容信息
    title: str = Field(..., min_length=1, max_length=500, description="标题")
    description: Optional[str] = Field(None, max_length=1000, description="摘要/描述")
    content: str = Field(..., min_length=10, description="正文内容（Markdown格式）")

    # 元数据
    author: Optional[str] = Field(None, description="作者")
    published_at: Optional[datetime] = Field(None, description="发布时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    # 媒体
    images: List[str] = Field(default_factory=list, description="图片URL列表")
    videos: List[str] = Field(default_factory=list, description="视频URL列表")

    # 分类
    category: Optional[str] = Field(None, description="分类")
    tags: List[str] = Field(default_factory=list, description="标签列表")

    # 采集信息
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")
    content_hash: Optional[str] = Field(None, description="内容哈希（用于去重）")

    @validator('url')
    def validate_url(cls, v):
        """验证URL格式"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL 必须以 http:// 或 https:// 开头')
        return v

    @validator('published_at', 'updated_at', pre=True)
    def parse_datetime(cls, v):
        """解析日期时间"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                return None
        return v

    def get_content_hash(self) -> str:
        """生成内容哈希"""
        import hashlib
        content = f"{self.title}{self.content}"
        return hashlib.md5(content.encode()).hexdigest()

    class Config:
        """Pydantic 配置"""
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class SearchQuery(BaseModel):
    """搜索查询配置"""

    keywords: str = Field(..., description="搜索关键词")
    sources: NewsSource = Field(..., description="新闻源")
    limit: int = Field(20, ge=1, le=100, description="返回数量")
    timerange: str = Field("qdr:d", description="时间范围（qdr:h/d/w/m/y）")
    location: str = Field("US", description="地理位置")

    class Config:
        """Pydantic 配置"""
        use_enum_values = True


class ScraperStats(BaseModel):
    """采集器统计信息"""

    source: NewsSource
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    # 统计数据
    total_found: int = Field(0, description="发现的新闻数")
    total_scraped: int = Field(0, description="成功采集数")
    total_failed: int = Field(0, description="失败数")
    total_duplicates: int = Field(0, description="去重数")

    # 成本
    credits_used: int = Field(0, description="消耗的 Credits")

    def mark_complete(self):
        """标记完成"""
        self.end_time = datetime.now()

    def get_duration(self) -> float:
        """获取耗时（秒）"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.total_found == 0:
            return 0.0
        return (self.total_scraped / self.total_found) * 100

    class Config:
        """Pydantic 配置"""
        use_enum_values = True


class ExportFormat(str, Enum):
    """导出格式枚举"""
    JSON = "json"
    MARKDOWN = "markdown"
    CSV = "csv"


class ExportConfig(BaseModel):
    """导出配置"""

    format: ExportFormat = Field(ExportFormat.JSON, description="导出格式")
    output_dir: str = Field("data/exports", description="输出目录")
    filename_prefix: str = Field("news", description="文件名前缀")
    include_timestamp: bool = Field(True, description="是否包含时间戳")

    def get_filename(self) -> str:
        """生成文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.include_timestamp:
            return f"{self.filename_prefix}_{timestamp}.{self.format.value}"
        return f"{self.filename_prefix}.{self.format.value}"

    class Config:
        """Pydantic 配置"""
        use_enum_values = True
