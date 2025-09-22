#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl API Server for 火鸟门户系统
基于 FastAPI 的高性能 API 服务器

@version: 2.0.0
@author: 火鸟门户开发团队
@description: 提供 RESTful API 接口供火鸟门户系统调用
"""

import os
import json
import asyncio
import logging
import traceback
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

from firecrawl_pipeline_manager import (
    FirecrawlPipelineManager, 
    CrawlRequest, 
    PipelineConfig,
    JobStatus
)
from pipeline_config import ConfigManager, get_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus 指标 - 避免重复注册
try:
    REQUEST_COUNT = Counter('firecrawl_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
    REQUEST_DURATION = Histogram('firecrawl_request_duration_seconds', 'Request duration')
    ACTIVE_JOBS = Gauge('firecrawl_active_jobs', 'Number of active crawl jobs')
    COMPLETED_JOBS = Counter('firecrawl_completed_jobs_total', 'Total completed jobs', ['status'])
    API_ERRORS = Counter('firecrawl_api_errors_total', 'Total API errors', ['error_type'])
except ValueError as e:
    # 指标已存在，使用现有的
    from prometheus_client import REGISTRY
    REQUEST_COUNT = REGISTRY._names_to_collectors.get('firecrawl_requests_total')
    REQUEST_DURATION = REGISTRY._names_to_collectors.get('firecrawl_request_duration_seconds')
    ACTIVE_JOBS = REGISTRY._names_to_collectors.get('firecrawl_active_jobs')
    COMPLETED_JOBS = REGISTRY._names_to_collectors.get('firecrawl_completed_jobs_total')
    API_ERRORS = REGISTRY._names_to_collectors.get('firecrawl_api_errors_total')

# 安全认证
security = HTTPBearer(auto_error=False)

# 全局变量
pipeline_manager: Optional[FirecrawlPipelineManager] = None
config: Optional[PipelineConfig] = None

# API 模型
class APIResponse(BaseModel):
    """标准 API 响应"""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None

class CrawlJobRequest(BaseModel):
    """爬取任务请求"""
    url: str = Field(..., description="目标URL")
    max_depth: int = Field(default=3, ge=1, le=10, description="最大爬取深度")
    limit: int = Field(default=100, ge=1, le=10000, description="页面数量限制")
    exclude_paths: List[str] = Field(default_factory=list, description="排除路径")
    include_paths: List[str] = Field(default_factory=list, description="包含路径")
    ignore_sitemap: bool = Field(default=False, description="忽略站点地图")
    ignore_query_parameters: bool = Field(default=False, description="忽略查询参数")
    allow_backward_links: bool = Field(default=False, description="允许反向链接")
    allow_external_links: bool = Field(default=False, description="允许外部链接")
    
    # 内容提取选项
    include_html: bool = Field(default=True, description="包含HTML")
    include_raw_html: bool = Field(default=False, description="包含原始HTML")
    include_screenshot: bool = Field(default=False, description="包含截图")
    include_links: bool = Field(default=True, description="包含链接")
    only_main_content: bool = Field(default=True, description="仅主要内容")
    
    # 高级选项
    custom_headers: Dict[str, str] = Field(default_factory=dict, description="自定义请求头")
    wait_for: Optional[str] = Field(default=None, description="等待元素")
    timeout: int = Field(default=30, ge=5, le=300, description="页面超时")
    
    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class JobStatusResponse(BaseModel):
    """任务状态响应"""
    job_id: str
    status: str
    url: str
    total_urls: int = 0
    completed_urls: int = 0
    credits_used: int = 0
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    progress_percent: float = 0.0
    estimated_completion: Optional[datetime] = None

class JobResultResponse(BaseModel):
    """任务结果响应"""
    job_id: str
    status: str
    total_urls: int
    completed_urls: int
    credits_used: int
    data: List[Dict[str, Any]]
    summary: Dict[str, Any]
    created_at: datetime
    completed_at: datetime
    processing_time: float

class JobListResponse(BaseModel):
    """任务列表响应"""
    jobs: List[JobStatusResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: datetime
    version: str
    uptime: float
    active_jobs: int
    total_jobs: int
    system_info: Dict[str, Any]

class MetricsResponse(BaseModel):
    """指标响应"""
    requests_total: int
    active_jobs: int
    completed_jobs: int
    failed_jobs: int
    average_response_time: float
    system_metrics: Dict[str, Any]

# 中间件
class RequestLoggingMiddleware:
    """请求日志中间件"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        request_id = f"req_{int(start_time * 1000000)}"
        
        # 添加请求ID到scope
        scope["request_id"] = request_id
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # 记录请求指标
                duration = time.time() - start_time
                method = scope["method"]
                path = scope["path"]
                status_code = message["status"]
                
                REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
                REQUEST_DURATION.observe(duration)
                
                # 添加响应头
                headers = dict(message.get("headers", []))
                headers[b"x-request-id"] = request_id.encode()
                message["headers"] = list(headers.items())
                
                logger.info(f"Request {request_id}: {method} {path} - {status_code} ({duration:.3f}s)")
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global pipeline_manager, config
    
    # 启动时初始化
    logger.info("Starting Firecrawl API Server...")
    
    try:
        # 加载配置
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # 验证配置
        errors = config_manager.validate_config()
        if errors:
            logger.error(f"Configuration errors: {errors}")
            raise RuntimeError(f"Configuration validation failed: {errors}")
        
        # 初始化 Pipeline 管理器
        pipeline_manager = FirecrawlPipelineManager(config)
        
        # 启动监控
        await pipeline_manager.start_monitoring()
        
        logger.info("Firecrawl API Server started successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
    
    finally:
        # 关闭时清理
        logger.info("Shutting down Firecrawl API Server...")
        
        if pipeline_manager:
            await pipeline_manager.stop_monitoring()
        
        logger.info("Firecrawl API Server stopped")

# 创建 FastAPI 应用
app = FastAPI(
    title="火鸟门户系统 Firecrawl API",
    description="基于 Firecrawl 的高性能数据采集 API 服务",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RequestLoggingMiddleware)

# 依赖注入
async def get_pipeline_manager() -> FirecrawlPipelineManager:
    """获取 Pipeline 管理器"""
    if not pipeline_manager:
        raise HTTPException(status_code=503, detail="Pipeline manager not initialized")
    return pipeline_manager

async def get_current_config() -> PipelineConfig:
    """获取当前配置"""
    if not config:
        raise HTTPException(status_code=503, detail="Configuration not loaded")
    return config

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """验证 API 密钥"""
    if not config or not config.security:
        return True  # 如果没有配置安全设置，允许访问
    
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    
    # 这里可以实现更复杂的认证逻辑
    # 目前简单验证是否提供了 token
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return True

def get_request_id(request: Request) -> str:
    """获取请求ID"""
    return getattr(request.scope, 'request_id', 'unknown')

# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    request_id = get_request_id(request)
    error_type = type(exc).__name__
    
    API_ERRORS.labels(error_type=error_type).inc()
    
    logger.error(f"Request {request_id} failed: {str(exc)}\n{traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error=f"Internal server error: {str(exc)}",
            request_id=request_id
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 异常处理"""
    request_id = get_request_id(request)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            error=exc.detail,
            request_id=request_id
        ).dict()
    )

# API 路由
@app.get("/", response_model=APIResponse)
async def root():
    """根路径"""
    return APIResponse(
        success=True,
        message="火鸟门户系统 Firecrawl API 服务正在运行",
        data={
            "version": "2.0.0",
            "docs": "/docs",
            "health": "/health"
        }
    )

@app.get("/health", response_model=HealthCheckResponse)
async def health_check(
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager)
):
    """健康检查"""
    import psutil
    
    # 获取系统信息
    system_info = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }
    
    # 获取任务统计
    active_jobs = 0  # 这里应该从数据库获取实际数据
    total_jobs = 0
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="2.0.0",
        uptime=time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0,
        active_jobs=active_jobs,
        total_jobs=total_jobs,
        system_info=system_info
    )

@app.get("/metrics")
async def metrics():
    """Prometheus 指标"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/crawl", response_model=APIResponse)
async def start_crawl(
    request: CrawlJobRequest,
    background_tasks: BackgroundTasks,
    req: Request,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """启动爬取任务"""
    request_id = get_request_id(req)
    
    try:
        # 转换请求格式
        crawl_request = CrawlRequest(
            url=request.url,
            maxDepth=request.max_depth,
            limit=request.limit,
            excludePaths=request.exclude_paths,
            includePaths=request.include_paths,
            ignoreSitemap=request.ignore_sitemap,
            ignoreQueryParameters=request.ignore_query_parameters,
            allowBackwardLinks=request.allow_backward_links,
            allowExternalLinks=request.allow_external_links,
            scrapeOptions={
                "includeHtml": request.include_html,
                "includeRawHtml": request.include_raw_html,
                "includeScreenshot": request.include_screenshot,
                "includeLinks": request.include_links,
                "onlyMainContent": request.only_main_content,
                "headers": request.custom_headers,
                "waitFor": request.wait_for,
                "timeout": request.timeout
            }
        )
        
        # 启动爬取任务
        result = await manager.start_crawl_job(crawl_request)
        
        if result['success']:
            ACTIVE_JOBS.inc()
            
            return APIResponse(
                success=True,
                message="爬取任务已启动",
                data={
                    "job_id": result['job_id'],
                    "status": "pending",
                    "url": request.url
                },
                request_id=request_id
            )
        else:
            raise HTTPException(status_code=400, detail=result.get('error', 'Unknown error'))
    
    except Exception as e:
        logger.error(f"Error starting crawl job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crawl/{job_id}/status", response_model=APIResponse)
async def get_job_status(
    job_id: str,
    req: Request,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """获取任务状态"""
    request_id = get_request_id(req)
    
    try:
        status_result = await manager.get_job_status(job_id)
        
        if 'error' in status_result:
            raise HTTPException(status_code=404, detail=status_result['error'])
        
        # 计算进度百分比
        progress_percent = 0.0
        if status_result.get('total', 0) > 0:
            progress_percent = (status_result.get('completed', 0) / status_result['total']) * 100
        
        # 估算完成时间
        estimated_completion = None
        if status_result.get('status') == 'running' and progress_percent > 0:
            # 简单的线性估算
            remaining_percent = 100 - progress_percent
            if remaining_percent > 0:
                # 这里需要更复杂的算法来估算剩余时间
                estimated_minutes = (remaining_percent / progress_percent) * 10  # 假设已用10分钟
                estimated_completion = datetime.now() + timedelta(minutes=estimated_minutes)
        
        return APIResponse(
            success=True,
            data={
                "job_id": job_id,
                "status": status_result.get('status', 'unknown'),
                "total_urls": status_result.get('total', 0),
                "completed_urls": status_result.get('completed', 0),
                "credits_used": status_result.get('creditsUsed', 0),
                "progress_percent": progress_percent,
                "estimated_completion": estimated_completion.isoformat() if estimated_completion else None,
                "error_message": status_result.get('error')
            },
            request_id=request_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crawl/{job_id}/results", response_model=APIResponse)
async def get_job_results(
    job_id: str,
    req: Request,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """获取任务结果"""
    request_id = get_request_id(req)
    
    try:
        results = await manager.get_job_results(job_id)
        
        if not results['success']:
            raise HTTPException(status_code=404, detail=results.get('error', 'Job not found'))
        
        # 生成结果摘要
        data = results.get('data', [])
        summary = {
            "total_pages": len(data),
            "total_content_length": sum(len(item.get('content', '')) for item in data),
            "unique_domains": len(set(item.get('metadata', {}).get('domain', '') for item in data)),
            "content_types": list(set(item.get('metadata', {}).get('contentType', '') for item in data)),
            "languages": list(set(item.get('metadata', {}).get('language', '') for item in data if item.get('metadata', {}).get('language')))
        }
        
        COMPLETED_JOBS.labels(status='completed').inc()
        ACTIVE_JOBS.dec()
        
        return APIResponse(
            success=True,
            data={
                "job_id": job_id,
                "total_urls": results.get('total_urls', 0),
                "completed_urls": results.get('completed_urls', 0),
                "credits_used": results.get('credits_used', 0),
                "data": data,
                "summary": summary
            },
            request_id=request_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crawl/{job_id}/cancel", response_model=APIResponse)
async def cancel_job(
    job_id: str,
    req: Request,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """取消任务"""
    request_id = get_request_id(req)
    
    try:
        # 这里需要实现任务取消逻辑
        # 目前 Firecrawl API 可能不支持取消，所以只能标记为取消状态
        
        return APIResponse(
            success=True,
            message="任务取消请求已提交",
            data={"job_id": job_id, "status": "cancelling"},
            request_id=request_id
        )
    
    except Exception as e:
        logger.error(f"Error cancelling job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs", response_model=APIResponse)
async def list_jobs(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    req: Request = None,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """获取任务列表"""
    request_id = get_request_id(req)
    
    try:
        # 这里需要实现从数据库获取任务列表的逻辑
        # 目前返回示例数据
        
        jobs = []  # 从数据库获取任务列表
        total = 0  # 总任务数
        
        return APIResponse(
            success=True,
            data={
                "jobs": jobs,
                "total": total,
                "page": page,
                "page_size": page_size,
                "has_next": page * page_size < total,
                "has_prev": page > 1
            },
            request_id=request_id
        )
    
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=APIResponse)
async def get_stats(
    req: Request,
    manager: FirecrawlPipelineManager = Depends(get_pipeline_manager),
    authenticated: bool = Depends(verify_api_key)
):
    """获取统计信息"""
    request_id = get_request_id(req)
    
    try:
        # 这里需要实现统计信息获取逻辑
        stats = {
            "total_jobs": 0,
            "active_jobs": 0,
            "completed_jobs": 0,
            "failed_jobs": 0,
            "total_pages_crawled": 0,
            "total_credits_used": 0,
            "average_job_duration": 0,
            "success_rate": 0
        }
        
        return APIResponse(
            success=True,
            data=stats,
            request_id=request_id
        )
    
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config/reload", response_model=APIResponse)
async def reload_config(
    req: Request,
    authenticated: bool = Depends(verify_api_key)
):
    """重新加载配置"""
    request_id = get_request_id(req)
    
    try:
        global config
        config_manager = ConfigManager()
        config_changed = config_manager.reload_config()
        config = config_manager.get_config()
        
        return APIResponse(
            success=True,
            message="配置重新加载成功" if config_changed else "配置无变化",
            data={"config_changed": config_changed},
            request_id=request_id
        )
    
    except Exception as e:
        logger.error(f"Error reloading config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 启动服务器
def start_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    workers: int = 1,
    reload: bool = False
):
    """启动 API 服务器"""
    # 设置启动时间
    app.state.start_time = time.time()
    
    # 配置 uvicorn
    uvicorn_config = {
        "app": "api_server:app",
        "host": host,
        "port": port,
        "workers": workers,
        "reload": reload,
        "access_log": True,
        "log_level": "info"
    }
    
    logger.info(f"Starting Firecrawl API Server on {host}:{port}")
    uvicorn.run(**uvicorn_config)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Firecrawl API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--config", help="Configuration file path")
    
    args = parser.parse_args()
    
    # 设置配置文件路径
    if args.config:
        os.environ['FIRECRAWL_CONFIG_PATH'] = args.config
    
    start_server(
        host=args.host,
        port=args.port,
        workers=args.workers,
        reload=args.reload
    )