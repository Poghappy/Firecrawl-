#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl Pipeline Manager for 火鸟门户系统
基于 Open-WebUI-Pipelines 架构设计的企业级爬取管理器

@version: 2.0.0
@author: 火鸟门户开发团队
@description: 集成 Firecrawl API 的高性能爬取管理系统
"""

import os
import json
import asyncio
import aiohttp
import logging
import traceback
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, Field
import hashlib
import redis
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库模型
Base = declarative_base()

class CrawlJob(Base):
    __tablename__ = 'crawl_jobs'
    
    id = Column(String(50), primary_key=True)
    url = Column(String(500), nullable=False)
    status = Column(String(20), default='pending')
    config = Column(Text)  # JSON 配置
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    total_urls = Column(Integer, default=0)
    completed_urls = Column(Integer, default=0)
    credits_used = Column(Integer, default=0)
    error_message = Column(Text)
    result_data = Column(Text)  # JSON 结果数据

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Pydantic 模型
class CrawlRequest(BaseModel):
    url: str
    excludePaths: List[str] = Field(default_factory=list)
    includePaths: List[str] = Field(default_factory=list)
    maxDepth: int = 3
    ignoreSitemap: bool = False
    ignoreQueryParameters: bool = False
    limit: int = 100
    allowBackwardLinks: bool = False
    allowExternalLinks: bool = False
    scrapeOptions: Dict[str, Any] = Field(default_factory=dict)
    
class CrawlResponse(BaseModel):
    id: str
    success: bool
    url: Optional[str] = None
    message: Optional[str] = None

class CrawlStatusResponse(BaseModel):
    status: str
    total: int = 0
    completed: int = 0
    creditsUsed: int = 0
    expiresAt: Optional[str] = None
    data: List[Dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None

class PipelineConfig(BaseModel):
    # API 配置
    firecrawl_api_key: str
    base_url: str = "https://api.firecrawl.dev/v1"
    
    # 爬取配置
    default_max_depth: int = 3
    default_limit: int = 100
    default_format: str = "markdown"
    
    # 任务配置
    max_concurrent_jobs: int = 5
    job_timeout: int = 3600  # 1小时
    retry_attempts: int = 3
    
    # 存储配置
    cache_enabled: bool = True
    cache_ttl: int = 86400  # 24小时
    
    # 数据库配置
    database_url: str = "sqlite:///firecrawl_jobs.db"
    redis_url: str = "redis://localhost:6379/0"
    
    # 通知配置
    notification_enabled: bool = True
    webhook_url: Optional[str] = None
    email_notifications: bool = False

class FirecrawlClient:
    """Firecrawl API 客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Origin": "huoniao-portal",
                "X-Origin-Type": "integration",
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def start_crawl(self, request: CrawlRequest) -> CrawlResponse:
        """启动爬取任务"""
        url = f"{self.base_url}/crawl"
        payload = request.model_dump()
        
        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return CrawlResponse(**data)
                else:
                    error_text = await response.text()
                    logger.error(f"Crawl start failed: {response.status} - {error_text}")
                    return CrawlResponse(
                        id="",
                        success=False,
                        message=f"API Error: {response.status} - {error_text}"
                    )
        except Exception as e:
            logger.error(f"Crawl start exception: {str(e)}")
            return CrawlResponse(
                id="",
                success=False,
                message=f"Request failed: {str(e)}"
            )
    
    async def get_crawl_status(self, job_id: str) -> CrawlStatusResponse:
        """获取爬取状态"""
        url = f"{self.base_url}/crawl/{job_id}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return CrawlStatusResponse(**data)
                else:
                    error_text = await response.text()
                    logger.error(f"Status check failed: {response.status} - {error_text}")
                    return CrawlStatusResponse(
                        status="error",
                        error=f"API Error: {response.status} - {error_text}"
                    )
        except Exception as e:
            logger.error(f"Status check exception: {str(e)}")
            return CrawlStatusResponse(
                status="error",
                error=f"Request failed: {str(e)}"
            )

class AsyncTaskQueue:
    """异步任务队列管理器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pending_queue = "firecrawl:pending"
        self.processing_queue = "firecrawl:processing"
        self.completed_queue = "firecrawl:completed"
    
    async def add_task(self, job_id: str, request: CrawlRequest):
        """添加任务到队列"""
        task_data = {
            'job_id': job_id,
            'request': request.model_dump(),
            'created_at': datetime.now().isoformat()
        }
        
        await self.redis.lpush(self.pending_queue, json.dumps(task_data))
        logger.info(f"Task {job_id} added to pending queue")
    
    async def get_next_task(self) -> Optional[Dict]:
        """获取下一个待处理任务"""
        task_data = await self.redis.brpoplpush(
            self.pending_queue, 
            self.processing_queue, 
            timeout=1
        )
        
        if task_data:
            return json.loads(task_data)
        return None
    
    async def complete_task(self, job_id: str):
        """标记任务完成"""
        # 从处理队列移除并添加到完成队列
        processing_tasks = await self.redis.lrange(self.processing_queue, 0, -1)
        
        for task_data in processing_tasks:
            task = json.loads(task_data)
            if task['job_id'] == job_id:
                await self.redis.lrem(self.processing_queue, 1, task_data)
                task['completed_at'] = datetime.now().isoformat()
                await self.redis.lpush(self.completed_queue, json.dumps(task))
                logger.info(f"Task {job_id} moved to completed queue")
                break

class DataProcessor:
    """数据处理器"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
    
    async def process_crawl_data(self, crawl_data: List[Dict]) -> List[Dict]:
        """处理爬取数据"""
        processed_items = []
        
        for item in crawl_data:
            try:
                # 基础数据提取
                processed_item = {
                    'url': item.get('metadata', {}).get('sourceURL', ''),
                    'title': item.get('metadata', {}).get('title', ''),
                    'content': item.get('markdown', ''),
                    'html': item.get('html', ''),
                    'metadata': item.get('metadata', {}),
                    'processed_at': datetime.now().isoformat()
                }
                
                # 内容清理
                processed_item['cleaned_content'] = await self._clean_content(
                    processed_item['content']
                )
                
                # 生成内容摘要
                processed_item['summary'] = await self._generate_summary(
                    processed_item['cleaned_content']
                )
                
                # 提取关键词
                processed_item['keywords'] = await self._extract_keywords(
                    processed_item['cleaned_content']
                )
                
                processed_items.append(processed_item)
                
            except Exception as e:
                logger.error(f"Error processing item: {str(e)}")
                continue
        
        return processed_items
    
    async def _clean_content(self, content: str) -> str:
        """清理内容"""
        if not content:
            return ""
        
        # 移除多余的空白字符
        content = ' '.join(content.split())
        
        # 移除特殊字符（保留基本标点）
        import re
        content = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()\[\]{}"\'-]', '', content)
        
        return content.strip()
    
    async def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """生成内容摘要"""
        if not content or len(content) <= max_length:
            return content
        
        # 简单的摘要生成（取前N个字符）
        # 在实际应用中，可以集成更高级的摘要算法
        sentences = content.split('。')
        summary = ""
        
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + "。"
            else:
                break
        
        return summary.strip()
    
    async def _extract_keywords(self, content: str, max_keywords: int = 10) -> List[str]:
        """提取关键词"""
        if not content:
            return []
        
        # 简单的关键词提取（基于词频）
        import re
        from collections import Counter
        
        # 分词（简单实现）
        words = re.findall(r'\b\w+\b', content.lower())
        
        # 过滤停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 统计词频
        word_freq = Counter(words)
        
        # 返回最高频的关键词
        return [word for word, freq in word_freq.most_common(max_keywords)]

class StatusMonitor:
    """状态监控器"""
    
    def __init__(self, db_session, redis_client):
        self.db_session = db_session
        self.redis = redis_client
    
    async def update_job_status(self, job_id: str, status_response: CrawlStatusResponse):
        """更新任务状态"""
        try:
            job = self.db_session.query(CrawlJob).filter_by(id=job_id).first()
            if job:
                job.status = status_response.status
                job.total_urls = status_response.total
                job.completed_urls = status_response.completed
                job.credits_used = status_response.creditsUsed
                job.updated_at = datetime.now()
                
                if status_response.error:
                    job.error_message = status_response.error
                
                if status_response.status == 'completed':
                    job.completed_at = datetime.now()
                    if status_response.data:
                        job.result_data = json.dumps(status_response.data)
                
                self.db_session.commit()
                
                # 更新 Redis 缓存
                cache_key = f"job_status:{job_id}"
                await self.redis.setex(
                    cache_key, 
                    300,  # 5分钟缓存
                    json.dumps(status_response.model_dump())
                )
                
                logger.info(f"Job {job_id} status updated: {status_response.status}")
            
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
            self.db_session.rollback()

class FirecrawlPipelineManager:
    """Firecrawl Pipeline 管理器"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        
        # 初始化数据库
        database_url = config.database.url
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()
        
        # 初始化 Redis
        redis_url = config.cache.redis_url
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # 初始化组件
        self.task_queue = AsyncTaskQueue(self.redis_client)
        self.data_processor = DataProcessor(config)
        self.status_monitor = StatusMonitor(self.db_session, self.redis_client)
        
        # 运行状态
        self.is_running = False
        self.worker_tasks = []
    
    async def start_crawl_job(self, request: CrawlRequest) -> Dict[str, Any]:
        """启动爬取任务"""
        try:
            async with FirecrawlClient(self.config.api.firecrawl_api_key, self.config.api.base_url) as client:
                response = await client.start_crawl(request)
                
                if response.success and response.id:
                    # 保存任务到数据库
                    job = CrawlJob(
                        id=response.id,
                        url=request.url,
                        status=JobStatus.PENDING.value,
                        config=json.dumps(request.model_dump()),
                        created_at=datetime.now()
                    )
                    
                    self.db_session.add(job)
                    self.db_session.commit()
                    
                    # 添加到任务队列
                    await self.task_queue.add_task(response.id, request)
                    
                    logger.info(f"Crawl job {response.id} started successfully")
                    
                    return {
                        'success': True,
                        'job_id': response.id,
                        'message': 'Crawl job started successfully'
                    }
                else:
                    logger.error(f"Failed to start crawl job: {response.message}")
                    return {
                        'success': False,
                        'error': response.message or 'Unknown error'
                    }
                    
        except Exception as e:
            logger.error(f"Error starting crawl job: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        try:
            # 先检查缓存
            cache_key = f"job_status:{job_id}"
            cached_status = await self.redis_client.get(cache_key)
            
            if cached_status:
                return json.loads(cached_status)
            
            # 从数据库获取
            job = self.db_session.query(CrawlJob).filter_by(id=job_id).first()
            if not job:
                return {
                    'success': False,
                    'error': 'Job not found'
                }
            
            # 如果任务还在进行中，从 API 获取最新状态
            if job.status in ['pending', 'running']:
                async with FirecrawlClient(self.config.api.firecrawl_api_key, self.config.api.base_url) as client:
                    status_response = await client.get_crawl_status(job_id)
                    await self.status_monitor.update_job_status(job_id, status_response)
                    return status_response.model_dump()
            
            # 返回数据库中的状态
            return {
                'status': job.status,
                'total': job.total_urls,
                'completed': job.completed_urls,
                'creditsUsed': job.credits_used,
                'error': job.error_message
            }
            
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_job_results(self, job_id: str) -> Dict[str, Any]:
        """获取任务结果"""
        try:
            job = self.db_session.query(CrawlJob).filter_by(id=job_id).first()
            if not job:
                return {
                    'success': False,
                    'error': 'Job not found'
                }
            
            if job.status != 'completed':
                return {
                    'success': False,
                    'error': f'Job not completed. Current status: {job.status}'
                }
            
            if job.result_data:
                raw_data = json.loads(job.result_data)
                processed_data = await self.data_processor.process_crawl_data(raw_data)
                
                return {
                    'success': True,
                    'job_id': job_id,
                    'total_urls': job.total_urls,
                    'completed_urls': job.completed_urls,
                    'credits_used': job.credits_used,
                    'data': processed_data
                }
            else:
                return {
                    'success': False,
                    'error': 'No result data available'
                }
                
        except Exception as e:
            logger.error(f"Error getting job results: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def start_monitoring(self):
        """启动监控服务"""
        if self.is_running:
            logger.warning("Monitoring is already running")
            return
        
        self.is_running = True
        logger.info("Starting Firecrawl Pipeline Manager monitoring...")
        
        # 启动工作线程
        for i in range(self.config.task.max_concurrent_jobs):
            task = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(task)
        
        # 启动状态监控线程
        monitor_task = asyncio.create_task(self._status_monitor())
        self.worker_tasks.append(monitor_task)
        
        logger.info(f"Started {len(self.worker_tasks)} worker tasks")
    
    async def stop_monitoring(self):
        """停止监控服务"""
        if not self.is_running:
            return
        
        self.is_running = False
        logger.info("Stopping Firecrawl Pipeline Manager...")
        
        # 取消所有工作任务
        for task in self.worker_tasks:
            task.cancel()
        
        # 等待任务完成
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        
        logger.info("Firecrawl Pipeline Manager stopped")
    
    async def _worker(self, worker_name: str):
        """工作线程"""
        logger.info(f"Worker {worker_name} started")
        
        while self.is_running:
            try:
                # 获取下一个任务
                task = await self.task_queue.get_next_task()
                if not task:
                    await asyncio.sleep(1)
                    continue
                
                job_id = task['job_id']
                logger.info(f"Worker {worker_name} processing job {job_id}")
                
                # 监控任务直到完成
                await self._monitor_job(job_id)
                
                # 标记任务完成
                await self.task_queue.complete_task(job_id)
                
                logger.info(f"Worker {worker_name} completed job {job_id}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_name} error: {str(e)}")
                await asyncio.sleep(5)
        
        logger.info(f"Worker {worker_name} stopped")
    
    async def _monitor_job(self, job_id: str):
        """监控单个任务"""
        start_time = datetime.now()
        timeout = timedelta(seconds=self.config.task.job_timeout)
        
        while datetime.now() - start_time < timeout:
            try:
                async with FirecrawlClient(self.config.api.firecrawl_api_key, self.config.api.base_url) as client:
                    status_response = await client.get_crawl_status(job_id)
                    
                    # 更新状态
                    await self.status_monitor.update_job_status(job_id, status_response)
                    
                    # 检查是否完成
                    if status_response.status in ['completed', 'failed']:
                        logger.info(f"Job {job_id} finished with status: {status_response.status}")
                        break
                    
                    # 等待下次检查
                    await asyncio.sleep(10)
                    
            except Exception as e:
                logger.error(f"Error monitoring job {job_id}: {str(e)}")
                await asyncio.sleep(30)
        
        # 检查是否超时
        if datetime.now() - start_time >= timeout:
            logger.warning(f"Job {job_id} monitoring timeout")
    
    async def _status_monitor(self):
        """状态监控线程"""
        logger.info("Status monitor started")
        
        while self.is_running:
            try:
                # 检查长时间运行的任务
                cutoff_time = datetime.now() - timedelta(hours=2)
                stale_jobs = self.db_session.query(CrawlJob).filter(
                    CrawlJob.status.in_(['pending', 'running']),
                    CrawlJob.created_at < cutoff_time
                ).all()
                
                for job in stale_jobs:
                    logger.warning(f"Found stale job {job.id}, checking status...")
                    
                    async with FirecrawlClient(self.config.api.firecrawl_api_key, self.config.api.base_url) as client:
                        status_response = await client.get_crawl_status(job.id)
                        await self.status_monitor.update_job_status(job.id, status_response)
                
                await asyncio.sleep(300)  # 每5分钟检查一次
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Status monitor error: {str(e)}")
                await asyncio.sleep(60)
        
        logger.info("Status monitor stopped")
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'db_session'):
            self.db_session.close()
        if hasattr(self, 'redis_client'):
            self.redis_client.close()

# 使用示例
if __name__ == "__main__":
    async def main():
        # 配置
        config = PipelineConfig(
            firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY", ""),
            database_url=os.getenv("DATABASE_URL", "sqlite:///firecrawl_jobs.db"),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
        )
        
        # 创建管理器
        manager = FirecrawlPipelineManager(config)
        
        try:
            # 启动监控
            await manager.start_monitoring()
            
            # 示例：启动爬取任务
            request = CrawlRequest(
                url="https://example.com",
                maxDepth=2,
                limit=50
            )
            
            result = await manager.start_crawl_job(request)
            print(f"Job started: {result}")
            
            # 保持运行
            await asyncio.sleep(3600)  # 运行1小时
            
        finally:
            # 停止监控
            await manager.stop_monitoring()
    
    # 运行
    asyncio.run(main())