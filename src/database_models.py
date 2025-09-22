#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl Database Models for 火鸟门户系统
数据库模型定义和数据访问层

@version: 2.0.0
@author: 火鸟门户开发团队
@description: 提供完整的数据库模型和 ORM 支持
"""

import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from enum import Enum

from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, DateTime, 
    Text, JSON, ForeignKey, Index, UniqueConstraint, CheckConstraint,
    event, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 数据库基类
Base = declarative_base()

# 枚举类型
class JobStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class JobPriority(str, Enum):
    """任务优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class ContentType(str, Enum):
    """内容类型枚举"""
    HTML = "text/html"
    TEXT = "text/plain"
    JSON = "application/json"
    XML = "application/xml"
    PDF = "application/pdf"
    IMAGE = "image/*"
    OTHER = "other"

class NotificationStatus(str, Enum):
    """通知状态枚举"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"

# 基础模型类
class BaseModel(Base):
    """基础模型类"""
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Enum):
                value = value.value
            result[column.name] = value
        return result
    
    def update_from_dict(self, data: Dict[str, Any]):
        """从字典更新属性"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)

# 爬取任务模型
class CrawlJob(BaseModel):
    """爬取任务模型"""
    __tablename__ = 'crawl_jobs'
    
    # 基本信息
    job_id = Column(String(100), unique=True, nullable=False, index=True)
    url = Column(Text, nullable=False)
    status = Column(String(20), default=JobStatus.PENDING.value, nullable=False, index=True)
    priority = Column(String(20), default=JobPriority.NORMAL.value, nullable=False)
    
    # 配置参数
    max_depth = Column(Integer, default=3, nullable=False)
    limit = Column(Integer, default=100, nullable=False)
    exclude_paths = Column(JSON, default=list)
    include_paths = Column(JSON, default=list)
    ignore_sitemap = Column(Boolean, default=False)
    ignore_query_parameters = Column(Boolean, default=False)
    allow_backward_links = Column(Boolean, default=False)
    allow_external_links = Column(Boolean, default=False)
    
    # 抓取选项
    scrape_options = Column(JSON, default=dict)
    custom_headers = Column(JSON, default=dict)
    
    # 执行信息
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    
    # 统计信息
    total_urls = Column(Integer, default=0)
    completed_urls = Column(Integer, default=0)
    failed_urls = Column(Integer, default=0)
    credits_used = Column(Integer, default=0)
    
    # 错误信息
    error_message = Column(Text)
    error_details = Column(JSON)
    
    # 元数据
    job_metadata = Column(JSON, default=dict)
    tags = Column(JSON, default=list)
    
    # 关联关系
    pages = relationship("CrawledPage", back_populates="job", cascade="all, delete-orphan")
    notifications = relationship("JobNotification", back_populates="job", cascade="all, delete-orphan")
    
    # 索引
    __table_args__ = (
        Index('idx_crawl_jobs_status_created', 'status', 'created_at'),
        Index('idx_crawl_jobs_url_status', 'url', 'status'),
        Index('idx_crawl_jobs_priority_created', 'priority', 'created_at'),
        CheckConstraint('total_urls >= 0', name='check_total_urls_positive'),
        CheckConstraint('completed_urls >= 0', name='check_completed_urls_positive'),
        CheckConstraint('failed_urls >= 0', name='check_failed_urls_positive'),
        CheckConstraint('credits_used >= 0', name='check_credits_used_positive'),
    )
    
    @property
    def progress_percent(self) -> float:
        """计算进度百分比"""
        if self.total_urls == 0:
            return 0.0
        return (self.completed_urls / self.total_urls) * 100
    
    @property
    def success_rate(self) -> float:
        """计算成功率"""
        if self.completed_urls == 0:
            return 0.0
        return ((self.completed_urls - self.failed_urls) / self.completed_urls) * 100
    
    @property
    def duration(self) -> Optional[float]:
        """计算执行时长（秒）"""
        if not self.started_at:
            return None
        end_time = self.completed_at or self.failed_at or datetime.now(timezone.utc)
        return (end_time - self.started_at).total_seconds()
    
    def is_active(self) -> bool:
        """检查任务是否活跃"""
        return self.status in [JobStatus.PENDING.value, JobStatus.RUNNING.value, JobStatus.PAUSED.value]
    
    def can_be_cancelled(self) -> bool:
        """检查任务是否可以取消"""
        return self.status in [JobStatus.PENDING.value, JobStatus.RUNNING.value, JobStatus.PAUSED.value]

# 爬取页面模型
class CrawledPage(BaseModel):
    """爬取页面模型"""
    __tablename__ = 'crawled_pages'
    
    # 关联信息
    job_id = Column(String(36), ForeignKey('crawl_jobs.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # 页面信息
    url = Column(Text, nullable=False)
    title = Column(Text)
    content = Column(Text)
    raw_html = Column(Text)
    markdown = Column(Text)
    
    # 元数据
    status_code = Column(Integer)
    content_type = Column(String(100))
    content_length = Column(Integer)
    language = Column(String(10))
    charset = Column(String(50))
    
    # 提取的链接
    links = Column(JSON, default=list)
    images = Column(JSON, default=list)
    
    # 截图
    screenshot_url = Column(Text)
    screenshot_data = Column(Text)  # Base64 编码的截图数据
    
    # 处理信息
    crawled_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    processing_time = Column(Float)  # 处理时间（秒）
    
    # 错误信息
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # 元数据和标签
    page_metadata = Column(JSON, default=dict)
    tags = Column(JSON, default=list)
    
    # 关联关系
    job = relationship("CrawlJob", back_populates="pages")
    
    # 索引
    __table_args__ = (
        Index('idx_crawled_pages_job_url', 'job_id', 'url'),
        Index('idx_crawled_pages_status_code', 'status_code'),
        Index('idx_crawled_pages_content_type', 'content_type'),
        Index('idx_crawled_pages_crawled_at', 'crawled_at'),
        UniqueConstraint('job_id', 'url', name='uq_job_url'),
        CheckConstraint('status_code >= 100 AND status_code < 600', name='check_valid_status_code'),
        CheckConstraint('content_length >= 0', name='check_content_length_positive'),
        CheckConstraint('processing_time >= 0', name='check_processing_time_positive'),
        CheckConstraint('retry_count >= 0', name='check_retry_count_positive'),
    )
    
    @property
    def is_successful(self) -> bool:
        """检查页面是否成功爬取"""
        return self.status_code and 200 <= self.status_code < 300
    
    @property
    def domain(self) -> Optional[str]:
        """提取域名"""
        try:
            from urllib.parse import urlparse
            return urlparse(self.url).netloc
        except:
            return None
    
    @property
    def word_count(self) -> int:
        """计算内容字数"""
        if not self.content:
            return 0
        return len(self.content.split())

# 任务通知模型
class JobNotification(BaseModel):
    """任务通知模型"""
    __tablename__ = 'job_notifications'
    
    # 关联信息
    job_id = Column(String(36), ForeignKey('crawl_jobs.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # 通知信息
    notification_type = Column(String(50), nullable=False)  # started, completed, failed, progress
    status = Column(String(20), default=NotificationStatus.PENDING.value, nullable=False)
    
    # 通知内容
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, default=dict)
    
    # 发送信息
    recipient = Column(String(200))  # 邮箱、手机号等
    channel = Column(String(50))  # email, sms, webhook, etc.
    
    # 执行信息
    sent_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # 错误信息
    error_message = Column(Text)
    
    # 关联关系
    job = relationship("CrawlJob", back_populates="notifications")
    
    # 索引
    __table_args__ = (
        Index('idx_job_notifications_job_type', 'job_id', 'notification_type'),
        Index('idx_job_notifications_status', 'status'),
        Index('idx_job_notifications_channel', 'channel'),
        CheckConstraint('retry_count >= 0', name='check_retry_count_positive'),
        CheckConstraint('max_retries >= 0', name='check_max_retries_positive'),
    )
    
    def can_retry(self) -> bool:
        """检查是否可以重试"""
        return self.retry_count < self.max_retries and self.status == NotificationStatus.FAILED.value

# 系统配置模型
class SystemConfig(BaseModel):
    """系统配置模型"""
    __tablename__ = 'system_configs'
    
    # 配置信息
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    description = Column(Text)
    category = Column(String(50), default='general', index=True)
    
    # 配置属性
    is_sensitive = Column(Boolean, default=False)  # 是否为敏感配置
    is_readonly = Column(Boolean, default=False)   # 是否只读
    requires_restart = Column(Boolean, default=False)  # 是否需要重启
    
    # 版本信息
    version = Column(Integer, default=1)
    
    # 索引
    __table_args__ = (
        Index('idx_system_configs_category', 'category'),
        Index('idx_system_configs_sensitive', 'is_sensitive'),
    )

# 任务统计模型
class JobStatistics(BaseModel):
    """任务统计模型"""
    __tablename__ = 'job_statistics'
    
    # 统计日期
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # 任务统计
    total_jobs = Column(Integer, default=0)
    completed_jobs = Column(Integer, default=0)
    failed_jobs = Column(Integer, default=0)
    cancelled_jobs = Column(Integer, default=0)
    
    # 页面统计
    total_pages = Column(Integer, default=0)
    successful_pages = Column(Integer, default=0)
    failed_pages = Column(Integer, default=0)
    
    # 性能统计
    average_job_duration = Column(Float, default=0.0)
    average_page_processing_time = Column(Float, default=0.0)
    total_credits_used = Column(Integer, default=0)
    
    # 系统统计
    peak_concurrent_jobs = Column(Integer, default=0)
    total_data_size = Column(Integer, default=0)  # 字节
    
    # 索引
    __table_args__ = (
        UniqueConstraint('date', name='uq_statistics_date'),
        CheckConstraint('total_jobs >= 0', name='check_total_jobs_positive'),
        CheckConstraint('completed_jobs >= 0', name='check_completed_jobs_positive'),
        CheckConstraint('failed_jobs >= 0', name='check_failed_jobs_positive'),
        CheckConstraint('total_pages >= 0', name='check_total_pages_positive'),
        CheckConstraint('total_credits_used >= 0', name='check_total_credits_positive'),
    )

# 数据库管理类
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, database_url: str, echo: bool = False):
        """初始化数据库管理器"""
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=echo, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # 注册事件监听器
        self._register_event_listeners()
    
    def _register_event_listeners(self):
        """注册数据库事件监听器"""
        
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """设置 SQLite 配置"""
            if 'sqlite' in self.database_url:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
        
        @event.listens_for(BaseModel, 'before_update', propagate=True)
        def receive_before_update(mapper, connection, target):
            """更新前自动设置 updated_at"""
            target.updated_at = datetime.now(timezone.utc)
    
    def create_tables(self):
        """创建所有表"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """删除所有表"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping database tables: {str(e)}")
            raise
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    def get_table_info(self) -> Dict[str, Any]:
        """获取表信息"""
        with self.get_session() as session:
            tables = {}
            for table_name in Base.metadata.tables.keys():
                try:
                    count = session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                    tables[table_name] = {
                        'count': count,
                        'columns': [col.name for col in Base.metadata.tables[table_name].columns]
                    }
                except Exception as e:
                    tables[table_name] = {'error': str(e)}
            return tables
    
    def cleanup_old_data(self, days: int = 30):
        """清理旧数据"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        with self.get_session() as session:
            try:
                # 清理已完成的旧任务
                deleted_jobs = session.query(CrawlJob).filter(
                    CrawlJob.status.in_([JobStatus.COMPLETED.value, JobStatus.FAILED.value, JobStatus.CANCELLED.value]),
                    CrawlJob.updated_at < cutoff_date
                ).delete(synchronize_session=False)
                
                # 清理旧的统计数据（保留最近一年）
                stats_cutoff = datetime.now(timezone.utc) - timedelta(days=365)
                deleted_stats = session.query(JobStatistics).filter(
                    JobStatistics.date < stats_cutoff
                ).delete(synchronize_session=False)
                
                session.commit()
                
                logger.info(f"Cleaned up {deleted_jobs} old jobs and {deleted_stats} old statistics")
                
            except Exception as e:
                session.rollback()
                logger.error(f"Error cleaning up old data: {str(e)}")
                raise
    
    def backup_database(self, backup_path: str):
        """备份数据库"""
        # 这里可以实现数据库备份逻辑
        # 具体实现取决于数据库类型
        pass
    
    def restore_database(self, backup_path: str):
        """恢复数据库"""
        # 这里可以实现数据库恢复逻辑
        # 具体实现取决于数据库类型
        pass

# 数据访问对象 (DAO)
class CrawlJobDAO:
    """爬取任务数据访问对象"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, job_data: Dict[str, Any]) -> CrawlJob:
        """创建任务"""
        job = CrawlJob(**job_data)
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job
    
    def get_by_id(self, job_id: str) -> Optional[CrawlJob]:
        """根据ID获取任务"""
        return self.session.query(CrawlJob).filter(CrawlJob.id == job_id).first()
    
    def get_by_job_id(self, job_id: str) -> Optional[CrawlJob]:
        """根据任务ID获取任务"""
        return self.session.query(CrawlJob).filter(CrawlJob.job_id == job_id).first()
    
    def update(self, job_id: str, update_data: Dict[str, Any]) -> Optional[CrawlJob]:
        """更新任务"""
        job = self.get_by_id(job_id)
        if job:
            job.update_from_dict(update_data)
            self.session.commit()
            self.session.refresh(job)
        return job
    
    def delete(self, job_id: str) -> bool:
        """删除任务"""
        job = self.get_by_id(job_id)
        if job:
            self.session.delete(job)
            self.session.commit()
            return True
        return False
    
    def list_jobs(
        self, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        order_by: str = 'created_at',
        order_desc: bool = True
    ) -> List[CrawlJob]:
        """获取任务列表"""
        query = self.session.query(CrawlJob)
        
        if status:
            query = query.filter(CrawlJob.status == status)
        
        if priority:
            query = query.filter(CrawlJob.priority == priority)
        
        # 排序
        order_column = getattr(CrawlJob, order_by, CrawlJob.created_at)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column)
        
        return query.offset(offset).limit(limit).all()
    
    def count_jobs(self, status: Optional[str] = None) -> int:
        """统计任务数量"""
        query = self.session.query(CrawlJob)
        if status:
            query = query.filter(CrawlJob.status == status)
        return query.count()
    
    def get_active_jobs(self) -> List[CrawlJob]:
        """获取活跃任务"""
        return self.session.query(CrawlJob).filter(
            CrawlJob.status.in_([JobStatus.PENDING.value, JobStatus.RUNNING.value, JobStatus.PAUSED.value])
        ).all()

class CrawledPageDAO:
    """爬取页面数据访问对象"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, page_data: Dict[str, Any]) -> CrawledPage:
        """创建页面记录"""
        page = CrawledPage(**page_data)
        self.session.add(page)
        self.session.commit()
        self.session.refresh(page)
        return page
    
    def get_by_job_id(self, job_id: str) -> List[CrawledPage]:
        """根据任务ID获取页面列表"""
        return self.session.query(CrawledPage).filter(CrawledPage.job_id == job_id).all()
    
    def get_successful_pages(self, job_id: str) -> List[CrawledPage]:
        """获取成功爬取的页面"""
        return self.session.query(CrawledPage).filter(
            CrawledPage.job_id == job_id,
            CrawledPage.status_code >= 200,
            CrawledPage.status_code < 300
        ).all()
    
    def search_content(self, job_id: str, keyword: str) -> List[CrawledPage]:
        """搜索页面内容"""
        return self.session.query(CrawledPage).filter(
            CrawledPage.job_id == job_id,
            CrawledPage.content.contains(keyword)
        ).all()

# 工厂函数
def create_database_manager(config: Dict[str, Any]) -> DatabaseManager:
    """创建数据库管理器"""
    database_url = config.get('database_url', 'sqlite:///firecrawl.db')
    echo = config.get('echo', False)
    
    return DatabaseManager(database_url, echo)

def get_session_factory(database_manager: DatabaseManager):
    """获取会话工厂"""
    return database_manager.SessionLocal

# 数据库初始化脚本
def init_database(config: Dict[str, Any]):
    """初始化数据库"""
    db_manager = create_database_manager(config)
    
    # 创建表
    db_manager.create_tables()
    
    # 插入默认配置
    with db_manager.get_session() as session:
        default_configs = [
            {
                'key': 'firecrawl.api_key',
                'value': '',
                'description': 'Firecrawl API密钥',
                'category': 'api',
                'is_sensitive': True
            },
            {
                'key': 'firecrawl.base_url',
                'value': 'https://api.firecrawl.dev',
                'description': 'Firecrawl API基础URL',
                'category': 'api'
            },
            {
                'key': 'crawler.max_concurrent_jobs',
                'value': 5,
                'description': '最大并发任务数',
                'category': 'crawler'
            },
            {
                'key': 'crawler.default_timeout',
                'value': 30,
                'description': '默认超时时间（秒）',
                'category': 'crawler'
            },
            {
                'key': 'notification.email_enabled',
                'value': False,
                'description': '是否启用邮件通知',
                'category': 'notification'
            }
        ]
        
        for config_data in default_configs:
            existing = session.query(SystemConfig).filter(
                SystemConfig.key == config_data['key']
            ).first()
            
            if not existing:
                config_obj = SystemConfig(**config_data)
                session.add(config_obj)
        
        session.commit()
    
    logger.info("Database initialized successfully")

if __name__ == "__main__":
    # 测试数据库初始化
    test_config = {
        'database_url': 'sqlite:///test_firecrawl.db',
        'echo': True
    }
    
    init_database(test_config)