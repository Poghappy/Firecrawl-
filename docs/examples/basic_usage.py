#!/usr/bin/env python3
"""
Firecrawl数据采集器 - 基础使用示例

本示例展示如何使用Firecrawl数据采集器进行基本的网页内容采集。
"""

import asyncio
import json
from typing import Dict, List, Optional
import requests
from datetime import datetime

class FirecrawlCollectorExample:
    """Firecrawl采集器使用示例"""
    
    def __init__(self, api_base: str = "http://localhost:8000", api_key: str = None):
        """
        初始化采集器
        
        Args:
            api_base: API基础URL
            api_key: API密钥
        """
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def health_check(self) -> Dict:
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def crawl_single_url(self, url: str, options: Dict = None) -> Dict:
        """
        采集单个URL
        
        Args:
            url: 要采集的URL
            options: 采集选项
            
        Returns:
            采集结果
        """
        if options is None:
            options = {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "includeTags": ["h1", "h2", "h3", "p", "a"],
                "excludeTags": ["script", "style", "nav", "footer"]
            }
        
        payload = {
            "url": url,
            "options": options
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/api/v1/crawl/url",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def crawl_batch_urls(self, urls: List[str], options: Dict = None) -> Dict:
        """
        批量采集URLs
        
        Args:
            urls: URL列表
            options: 采集选项
            
        Returns:
            批量采集结果
        """
        if options is None:
            options = {
                "formats": ["markdown"],
                "onlyMainContent": True
            }
        
        payload = {
            "urls": urls,
            "options": options
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/api/v1/crawl/batch",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_job_status(self, job_id: str) -> Dict:
        """
        获取任务状态
        
        Args:
            job_id: 任务ID
            
        Returns:
            任务状态信息
        """
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/jobs/{job_id}",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def wait_for_completion(self, job_id: str, timeout: int = 300) -> Dict:
        """
        等待任务完成
        
        Args:
            job_id: 任务ID
            timeout: 超时时间（秒）
            
        Returns:
            最终任务状态
        """
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < timeout:
            status = self.get_job_status(job_id)
            
            if not status.get("success", True):
                return status
            
            job_status = status.get("status", "unknown")
            
            if job_status == "completed":
                return status
            elif job_status == "failed":
                return status
            elif job_status == "running":
                print(f"任务 {job_id} 正在运行中...")
                import time
                time.sleep(2)
            else:
                print(f"未知状态: {job_status}")
                import time
                time.sleep(2)
        
        return {"error": "任务超时", "success": False}
    
    def search_data(self, query: str, limit: int = 10) -> Dict:
        """
        搜索采集数据
        
        Args:
            query: 搜索关键词
            limit: 返回数量限制
            
        Returns:
            搜索结果
        """
        params = {
            "query": query,
            "limit": limit
        }
        
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/data/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}

def main():
    """主函数 - 演示基本用法"""
    
    # 初始化采集器
    collector = FirecrawlCollectorExample(
        api_base="http://localhost:8000",
        api_key="your_api_key_here"  # 替换为实际的API密钥
    )
    
    print("🔥 Firecrawl数据采集器 - 基础使用示例")
    print("=" * 50)
    
    # 1. 健康检查
    print("\n1. 检查服务健康状态...")
    health = collector.health_check()
    print(f"服务状态: {health.get('status', 'unknown')}")
    
    if health.get("status") != "healthy":
        print("❌ 服务不可用，请检查服务是否启动")
        return
    
    # 2. 单页面采集示例
    print("\n2. 单页面采集示例...")
    test_url = "https://example.com"
    
    print(f"正在采集: {test_url}")
    result = collector.crawl_single_url(test_url)
    
    if result.get("success"):
        job_id = result.get("job_id")
        print(f"✅ 任务已创建，ID: {job_id}")
        
        # 等待任务完成
        print("等待任务完成...")
        final_status = collector.wait_for_completion(job_id)
        
        if final_status.get("status") == "completed":
            data = final_status.get("result", {}).get("data", {})
            print(f"✅ 采集完成！")
            print(f"标题: {data.get('title', 'N/A')}")
            print(f"内容长度: {len(data.get('content', ''))}")
        else:
            print(f"❌ 任务失败: {final_status.get('error', 'Unknown error')}")
    else:
        print(f"❌ 采集失败: {result.get('error', 'Unknown error')}")
    
    # 3. 批量采集示例
    print("\n3. 批量采集示例...")
    test_urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml"
    ]
    
    print(f"正在批量采集 {len(test_urls)} 个URL...")
    batch_result = collector.crawl_batch_urls(test_urls)
    
    if batch_result.get("success"):
        job_id = batch_result.get("job_id")
        print(f"✅ 批量任务已创建，ID: {job_id}")
        
        # 等待任务完成
        print("等待批量任务完成...")
        final_status = collector.wait_for_completion(job_id)
        
        if final_status.get("status") == "completed":
            results = final_status.get("result", {}).get("results", [])
            success_count = sum(1 for r in results if r.get("status") == "success")
            print(f"✅ 批量采集完成！成功: {success_count}/{len(results)}")
            
            for i, result in enumerate(results):
                status = result.get("status", "unknown")
                url = result.get("url", "unknown")
                print(f"  {i+1}. {url} - {status}")
        else:
            print(f"❌ 批量任务失败: {final_status.get('error', 'Unknown error')}")
    else:
        print(f"❌ 批量采集失败: {batch_result.get('error', 'Unknown error')}")
    
    # 4. 数据搜索示例
    print("\n4. 数据搜索示例...")
    search_result = collector.search_data("example", limit=5)
    
    if search_result.get("success"):
        data = search_result.get("data", [])
        print(f"✅ 找到 {len(data)} 条相关数据")
        
        for i, item in enumerate(data[:3]):  # 只显示前3条
            title = item.get("title", "N/A")
            url = item.get("url", "N/A")
            print(f"  {i+1}. {title} - {url}")
    else:
        print(f"❌ 搜索失败: {search_result.get('error', 'Unknown error')}")
    
    print("\n🎉 示例演示完成！")

if __name__ == "__main__":
    main()
