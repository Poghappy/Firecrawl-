#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招聘信息数据模型

用于 Aloha 招聘网的数据结构定义。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, EmailStr, field_validator


class CompanyInfo(BaseModel):
    """公司信息"""
    company_id: Optional[str] = Field(None, description="公司ID")
    name: str = Field(..., min_length=1, max_length=200, description="公司名称")
    website: Optional[HttpUrl] = Field(None, description="公司官网")
    logo: Optional[HttpUrl] = Field(None, description="公司Logo")

    # 公司详情
    industry: Optional[str] = Field(None, max_length=100, description="所属行业")
    scale: Optional[str] = Field(None, max_length=50, description="公司规模")
    location: Optional[str] = Field(None, max_length=200, description="公司地址")

    # 描述信息
    description: Optional[str] = Field(None, max_length=5000, description="公司简介")
    benefits: List[str] = Field(default_factory=list, description="福利待遇")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "科技有限公司",
                "website": "https://company.com",
                "industry": "互联网",
                "scale": "100-500人",
                "location": "北京市朝阳区",
                "benefits": ["五险一金", "年终奖", "弹性工作"]
            }
        }


class JobPosting(BaseModel):
    """职位信息"""
    # 基础信息
    title: str = Field(..., min_length=1, max_length=200, description="职位名称")
    description: str = Field(..., min_length=100, description="职位描述")

    # 公司信息
    company_name: str = Field(..., max_length=200, description="公司名称")
    company_info: Optional[CompanyInfo] = Field(None, description="公司详情")

    # 薪资信息
    salary_min: Optional[Decimal] = Field(None, ge=0, description="最低薪资")
    salary_max: Optional[Decimal] = Field(None, ge=0, description="最高薪资")
    salary_range: Optional[str] = Field(None, max_length=100, description="薪资范围(文本)")
    salary_type: str = Field(default="月薪", description="薪资类型")

    # 工作详情
    location: str = Field(..., max_length=200, description="工作地点")
    work_type: str = Field(default="全职", description="工作类型")
    experience_required: Optional[str] = Field(None, max_length=100, description="经验要求")
    education_required: Optional[str] = Field(None, max_length=100, description="学历要求")

    # 职位要求
    requirements: List[str] = Field(default_factory=list, description="任职要求")
    responsibilities: List[str] = Field(default_factory=list, description="工作职责")
    skills: List[str] = Field(default_factory=list, description="技能要求")

    # 福利待遇
    benefits: List[str] = Field(default_factory=list, description="福利待遇")

    # 联系方式
    contact_person: Optional[str] = Field(None, max_length=100, description="联系人")
    contact_email: Optional[EmailStr] = Field(None, description="联系邮箱")
    contact_phone: Optional[str] = Field(None, max_length=50, description="联系电话")

    # 来源信息
    source: str = Field(..., description="信息来源")
    source_url: HttpUrl = Field(..., description="原始链接")
    job_id: Optional[str] = Field(None, description="职位ID")

    # 时间信息
    publish_date: Optional[datetime] = Field(None, description="发布时间")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    scraped_at: datetime = Field(default_factory=datetime.now, description="采集时间")

    # 统计信息
    view_count: int = Field(default=0, ge=0, description="浏览次数")
    application_count: int = Field(default=0, ge=0, description="申请人数")

    @field_validator('requirements', 'responsibilities', 'skills', 'benefits', mode='before')
    @classmethod
    def split_list_fields(cls, v):
        """将字符串或列表转换为列表"""
        if isinstance(v, str):
            # 尝试多种分隔符
            for sep in ['\n', ';', '；']:
                if sep in v:
                    return [item.strip() for item in v.split(sep) if item.strip()]
            return [v.strip()] if v.strip() else []
        return v

    @field_validator('salary_max')
    @classmethod
    def validate_salary_range(cls, v, info):
        """验证薪资范围"""
        if v is not None and 'salary_min' in info.data:
            salary_min = info.data['salary_min']
            if salary_min is not None and v < salary_min:
                raise ValueError("最高薪资不能低于最低薪资")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python 后端工程师",
                "description": "负责后端系统开发和维护...",
                "company_name": "科技有限公司",
                "salary_min": 15000,
                "salary_max": 25000,
                "salary_range": "15k-25k",
                "location": "北京市海淀区",
                "work_type": "全职",
                "experience_required": "3-5年",
                "education_required": "本科及以上",
                "requirements": [
                    "熟练掌握Python",
                    "熟悉Django/Flask框架",
                    "了解数据库优化"
                ],
                "skills": ["Python", "Django", "MySQL", "Redis"],
                "source": "招聘网站",
                "source_url": "https://job.com/posting/123"
            }
        }


# 使用示例
if __name__ == "__main__":
    # 创建职位
    job = JobPosting(
        title="Python 开发工程师",
        description="负责公司核心产品的后端开发工作，需要有扎实的Python基础和良好的代码习惯。" * 3,
        company_name="测试科技公司",
        salary_min=Decimal("15000"),
        salary_max=Decimal("25000"),
        location="上海市浦东新区",
        work_type="全职",
        experience_required="3-5年",
        education_required="本科",
        requirements=[
            "3年以上Python开发经验",
            "熟悉Django或Flask框架",
            "熟悉MySQL数据库"
        ],
        skills=["Python", "Django", "MySQL", "Redis"],
        source="测试招聘网",
        source_url="https://job.example.com/123"
    )

    print("职位创建成功:")
    print(f"  职位: {job.title}")
    print(f"  公司: {job.company_name}")
    print(f"  薪资: {job.salary_min}-{job.salary_max}")
    print(f"  地点: {job.location}")
    print(f"  要求: {len(job.requirements)}条")
    print(f"  技能: {', '.join(job.skills)}")

    # 导出为 JSON
    print("\nJSON 格式:")
    print(job.model_dump_json(indent=2, exclude={'company_info'}))
