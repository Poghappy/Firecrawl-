#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版API服务器
集成Firecrawl API，提供完整的数据采集服务
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from firecrawl import FirecrawlApp
    import uvicorn
    from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    from contextlib import asynccontextmanager
except ImportError as e:
    print(f"❌ 依赖包导入失败: {e}")
    print("请运行: pip install firecrawl-py fastapi uvicorn")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic模型
class CrawlRequest(BaseModel):
    """爬取请求模型"""
    url: str = Field(..., description="要爬取的URL")
    formats: List[str] = Field(default=["markdown"], description="输出格式")
    only_main_content: bool = Field(default=True, description="仅主要内容")
    max_depth: int = Field(default=1, description="最大爬取深度")
    timeout: int = Field(default=30, description="超时时间(秒)")

class CrawlResponse(BaseModel):
    """爬取响应模型"""
    success: bool
    url: str
    content: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    processing_time: float

class BatchCrawlRequest(BaseModel):
    """批量爬取请求模型"""
    urls: List[str] = Field(..., description="要爬取的URL列表")
    formats: List[str] = Field(default=["markdown"], description="输出格式")
    only_main_content: bool = Field(default=True, description="仅主要内容")
    max_concurrent: int = Field(default=5, description="最大并发数")

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    timestamp: str
    version: str
    firecrawl_status: str
    uptime: str

# 全局变量
app_start_time = datetime.now()
firecrawl_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global firecrawl_app
    
    # 启动时初始化
    logger.info("🚀 启动Firecrawl数据采集器API服务器")
    
    # 初始化Firecrawl客户端
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        logger.error("❌ 未找到FIRECRAWL_API_KEY环境变量")
        raise RuntimeError("FIRECRAWL_API_KEY环境变量未设置")
    
    try:
        firecrawl_app = FirecrawlApp(api_key=api_key)
        logger.info("✅ Firecrawl客户端初始化成功")
    except Exception as e:
        logger.error(f"❌ Firecrawl客户端初始化失败: {e}")
        raise
    
    yield
    
    # 关闭时清理
    logger.info("🛑 关闭Firecrawl数据采集器API服务器")

# 创建FastAPI应用
app = FastAPI(
    title="Firecrawl数据采集器",
    description="基于Firecrawl API的智能数据采集系统",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入
async def get_firecrawl_client():
    """获取Firecrawl客户端"""
    if firecrawl_app is None:
        raise HTTPException(status_code=503, detail="Firecrawl客户端未初始化")
    return firecrawl_app

# API路由
@app.get("/", response_model=Dict[str, str])
async def root():
    """根路径"""
    return {
        "message": "Firecrawl数据采集器API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check(client: FirecrawlApp = Depends(get_firecrawl_client)):
    """健康检查"""
    try:
        # 测试Firecrawl连接
        test_result = await asyncio.to_thread(
            client.scrape, 
            "https://example.com", 
            {"formats": ["markdown"], "onlyMainContent": True}
        )
        firecrawl_status = "healthy" if test_result else "unhealthy"
    except Exception as e:
        logger.error(f"Firecrawl健康检查失败: {e}")
        firecrawl_status = "unhealthy"
    
    uptime = str(datetime.now() - app_start_time)
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        firecrawl_status=firecrawl_status,
        uptime=uptime
    )

@app.post("/api/v1/crawl/url", response_model=CrawlResponse)
async def crawl_url(
    request: CrawlRequest,
    background_tasks: BackgroundTasks,
    client: FirecrawlApp = Depends(get_firecrawl_client)
):
    """爬取单个URL"""
    start_time = datetime.now()
    
    try:
        logger.info(f"开始爬取URL: {request.url}")
        
        # 构建爬取参数
        crawl_params = {
            "formats": request.formats,
            "onlyMainContent": request.only_main_content,
            "maxDepth": request.max_depth,
            "timeout": request.timeout * 1000  # Firecrawl使用毫秒
        }
        
        # 执行爬取
        result = await asyncio.to_thread(client.scrape, request.url, crawl_params)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"✅ URL爬取成功: {request.url}, 耗时: {processing_time:.2f}秒")
        
        return CrawlResponse(
            success=True,
            url=request.url,
            content=result,
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ URL爬取失败: {request.url}, 错误: {e}")
        
        return CrawlResponse(
            success=False,
            url=request.url,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time
        )

@app.post("/api/v1/crawl/batch", response_model=Dict[str, Any])
async def crawl_batch(
    request: BatchCrawlRequest,
    background_tasks: BackgroundTasks,
    client: FirecrawlApp = Depends(get_firecrawl_client)
):
    """批量爬取URL"""
    start_time = datetime.now()
    results = []
    
    # 创建信号量限制并发数
    semaphore = asyncio.Semaphore(request.max_concurrent)
    
    async def crawl_single_url(url: str) -> Dict[str, Any]:
        """爬取单个URL的异步函数"""
        async with semaphore:
            try:
                crawl_params = {
                    "formats": request.formats,
                    "onlyMainContent": request.only_main_content
                }
                
                result = await asyncio.to_thread(client.scrape, url, crawl_params)
                
                return {
                    "url": url,
                    "success": True,
                    "content": result,
                    "error": None
                }
            except Exception as e:
                return {
                    "url": url,
                    "success": False,
                    "content": None,
                    "error": str(e)
                }
    
    try:
        logger.info(f"开始批量爬取 {len(request.urls)} 个URL")
        
        # 并发执行爬取任务
        tasks = [crawl_single_url(url) for url in request.urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        success_count = sum(1 for r in results if r.get("success", False))
        
        logger.info(f"✅ 批量爬取完成: {success_count}/{len(request.urls)} 成功, 耗时: {processing_time:.2f}秒")
        
        return {
            "success": True,
            "total_urls": len(request.urls),
            "successful": success_count,
            "failed": len(request.urls) - success_count,
            "processing_time": processing_time,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ 批量爬取失败: {e}")
        
        return {
            "success": False,
            "error": str(e),
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/v1/stats")
async def get_stats():
    """获取统计信息"""
    uptime = datetime.now() - app_start_time
    
    return {
        "uptime": str(uptime),
        "start_time": app_start_time.isoformat(),
        "version": "1.0.0",
        "endpoints": [
            "/",
            "/health",
            "/api/v1/crawl/url",
            "/api/v1/crawl/batch",
            "/api/v1/stats"
        ]
    }

# 错误处理
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "接口不存在", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"内部服务器错误: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "内部服务器错误", "detail": str(exc)}
    )

if __name__ == "__main__":
    # 检查环境变量
    if not os.getenv("FIRECRAWL_API_KEY"):
        logger.error("❌ 请设置FIRECRAWL_API_KEY环境变量")
        sys.exit(1)
    
    # 启动服务器
    logger.info("🚀 启动Firecrawl数据采集器API服务器")
    uvicorn.run(
        "enhanced_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
