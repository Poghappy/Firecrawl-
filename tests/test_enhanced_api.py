#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版API服务器测试
"""

import os
import sys
import json
import pytest
import asyncio
from datetime import datetime
from pathlib import Path

# 添加src目录到Python路径
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)

try:
    from src.enhanced_api_server import CrawlRequest, CrawlResponse, BatchCrawlRequest
    import httpx
except ImportError as e:
    pytest.skip(f"依赖包导入失败: {e}")

class TestEnhancedAPI:
    """增强版API测试类"""
    
    @pytest.fixture
    def api_base_url(self):
        """API基础URL"""
        return "http://localhost:8000"
    
    @pytest.fixture
    async def client(self, api_base_url):
        """HTTP客户端"""
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            yield client
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """测试健康检查"""
        response = await client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        """测试根路径"""
        response = await client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    @pytest.mark.asyncio
    async def test_stats_endpoint(self, client):
        """测试统计信息"""
        response = await client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "uptime" in data
        assert "start_time" in data
        assert "version" in data
        assert "endpoints" in data
    
    @pytest.mark.asyncio
    async def test_crawl_request_model(self):
        """测试爬取请求模型"""
        request = CrawlRequest(
            url="https://example.com",
            formats=["markdown"],
            only_main_content=True,
            max_depth=1,
            timeout=30
        )
        
        assert request.url == "https://example.com"
        assert request.formats == ["markdown"]
        assert request.only_main_content is True
        assert request.max_depth == 1
        assert request.timeout == 30
    
    @pytest.mark.asyncio
    async def test_batch_crawl_request_model(self):
        """测试批量爬取请求模型"""
        request = BatchCrawlRequest(
            urls=["https://example.com", "https://httpbin.org"],
            formats=["markdown"],
            only_main_content=True,
            max_concurrent=3
        )
        
        assert len(request.urls) == 2
        assert request.formats == ["markdown"]
        assert request.only_main_content is True
        assert request.max_concurrent == 3
    
    @pytest.mark.asyncio
    async def test_crawl_response_model(self):
        """测试爬取响应模型"""
        response = CrawlResponse(
            success=True,
            url="https://example.com",
            content={"markdown": "# Test content"},
            timestamp=datetime.now().isoformat(),
            processing_time=1.5
        )
        
        assert response.success is True
        assert response.url == "https://example.com"
        assert response.content is not None
        assert response.error is None
        assert response.processing_time == 1.5

class TestAPIEndpoints:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_single_url_crawl(self):
        """测试单URL爬取（需要API服务器运行）"""
        # 这个测试需要API服务器实际运行
        # 在实际使用中，可以通过pytest-xprocess启动服务器
        pytest.skip("需要API服务器运行，跳过集成测试")
    
    @pytest.mark.asyncio
    async def test_batch_url_crawl(self):
        """测试批量URL爬取（需要API服务器运行）"""
        # 这个测试需要API服务器实际运行
        pytest.skip("需要API服务器运行，跳过集成测试")

class TestErrorHandling:
    """错误处理测试"""
    
    def test_invalid_crawl_request(self):
        """测试无效的爬取请求"""
        with pytest.raises(ValueError):
            CrawlRequest()  # 缺少必需的url参数
    
    def test_invalid_batch_request(self):
        """测试无效的批量请求"""
        with pytest.raises(ValueError):
            BatchCrawlRequest()  # 缺少必需的urls参数

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
