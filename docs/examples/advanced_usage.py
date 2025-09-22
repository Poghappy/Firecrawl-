#!/usr/bin/env python3
"""
Firecrawl数据采集器 - 高级使用示例

本示例展示如何使用Firecrawl数据采集器进行高级功能，包括监控、数据处理等。
"""

import asyncio
import json
import time
from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta

class AdvancedFirecrawlCollector:
    """高级Firecrawl采集器示例"""
    
    def __init__(self, api_base: str = "http://localhost:8000", api_key: str = None):
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def create_monitor(self, url: str, name: str, schedule: str = "0 */6 * * *") -> Dict:
        """
        创建监控任务
        
        Args:
            url: 监控的URL
            name: 监控任务名称
            schedule: Cron表达式
            
        Returns:
            创建结果
        """
        payload = {
            "url": url,
            "name": name,
            "schedule": schedule,
            "options": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "includeTags": ["h1", "h2", "h3", "p", "a", "img"]
            },
            "notifications": {
                "email": "admin@example.com",
                "webhook": "https://hooks.slack.com/services/..."
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/api/v1/monitor/create",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_monitors(self) -> Dict:
        """获取所有监控任务"""
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/monitor/list",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def update_monitor(self, monitor_id: str, updates: Dict) -> Dict:
        """
        更新监控任务
        
        Args:
            monitor_id: 监控任务ID
            updates: 更新内容
            
        Returns:
            更新结果
        """
        try:
            response = requests.put(
                f"{self.api_base}/api/v1/monitor/{monitor_id}",
                headers=self.headers,
                json=updates,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def delete_monitor(self, monitor_id: str) -> Dict:
        """删除监控任务"""
        try:
            response = requests.delete(
                f"{self.api_base}/api/v1/monitor/{monitor_id}",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def get_data_history(self, url: str = None, limit: int = 10) -> Dict:
        """
        获取采集历史
        
        Args:
            url: 特定URL的历史（可选）
            limit: 返回数量限制
            
        Returns:
            历史数据
        """
        params = {"limit": limit}
        if url:
            params["url"] = url
        
        try:
            response = requests.get(
                f"{self.api_base}/api/v1/data/history",
                headers=self.headers,
                params=params,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def analyze_content_changes(self, url: str, days: int = 7) -> Dict:
        """
        分析内容变化
        
        Args:
            url: 要分析的URL
            days: 分析天数
            
        Returns:
            变化分析结果
        """
        # 获取历史数据
        history = self.get_data_history(url, limit=100)
        
        if not history.get("success"):
            return history
        
        data_list = history.get("data", [])
        
        if len(data_list) < 2:
            return {"message": "数据不足，无法分析变化", "changes": []}
        
        # 按时间排序
        data_list.sort(key=lambda x: x.get("timestamp", ""))
        
        changes = []
        for i in range(1, len(data_list)):
            current = data_list[i]
            previous = data_list[i-1]
            
            # 简单的变化检测（实际应用中可以使用更复杂的算法）
            current_content = current.get("content", "")
            previous_content = previous.get("content", "")
            
            if current_content != previous_content:
                change = {
                    "timestamp": current.get("timestamp"),
                    "change_type": "content_updated",
                    "content_length_change": len(current_content) - len(previous_content),
                    "title_change": current.get("title") != previous.get("title")
                }
                changes.append(change)
        
        return {
            "success": True,
            "url": url,
            "analysis_period": f"{days} days",
            "total_changes": len(changes),
            "changes": changes
        }
    
    def export_data(self, format: str = "json", limit: int = 100) -> Dict:
        """
        导出数据
        
        Args:
            format: 导出格式 (json, csv, markdown)
            limit: 导出数量限制
            
        Returns:
            导出结果
        """
        # 获取数据
        history = self.get_data_history(limit=limit)
        
        if not history.get("success"):
            return history
        
        data = history.get("data", [])
        
        if format == "json":
            return {
                "success": True,
                "format": "json",
                "data": data,
                "count": len(data)
            }
        elif format == "csv":
            # 简单的CSV转换
            if not data:
                return {"success": True, "format": "csv", "data": "", "count": 0}
            
            csv_lines = ["url,title,timestamp,content_length"]
            for item in data:
                csv_line = f'"{item.get("url", "")}","{item.get("title", "")}","{item.get("timestamp", "")}",{len(item.get("content", ""))}'
                csv_lines.append(csv_line)
            
            return {
                "success": True,
                "format": "csv",
                "data": "\n".join(csv_lines),
                "count": len(data)
            }
        elif format == "markdown":
            # 简单的Markdown转换
            if not data:
                return {"success": True, "format": "markdown", "data": "", "count": 0}
            
            md_lines = ["# Firecrawl数据导出", f"导出时间: {datetime.now().isoformat()}", f"数据条数: {len(data)}", ""]
            
            for i, item in enumerate(data, 1):
                md_lines.extend([
                    f"## {i}. {item.get('title', 'Untitled')}",
                    f"**URL**: {item.get('url', 'N/A')}",
                    f"**时间**: {item.get('timestamp', 'N/A')}",
                    f"**内容长度**: {len(item.get('content', ''))}",
                    "",
                    "### 内容预览",
                    item.get('content', '')[:500] + "..." if len(item.get('content', '')) > 500 else item.get('content', ''),
                    "",
                    "---",
                    ""
                ])
            
            return {
                "success": True,
                "format": "markdown",
                "data": "\n".join(md_lines),
                "count": len(data)
            }
        else:
            return {"error": f"不支持的格式: {format}", "success": False}
    
    def crawl_with_retry(self, url: str, max_retries: int = 3, delay: int = 5) -> Dict:
        """
        带重试的采集
        
        Args:
            url: 要采集的URL
            max_retries: 最大重试次数
            delay: 重试延迟（秒）
            
        Returns:
            采集结果
        """
        for attempt in range(max_retries):
            print(f"尝试采集 {url} (第 {attempt + 1} 次)")
            
            result = self.crawl_single_url(url)
            
            if result.get("success"):
                return result
            
            if attempt < max_retries - 1:
                print(f"采集失败，{delay}秒后重试...")
                time.sleep(delay)
            else:
                print(f"采集失败，已达到最大重试次数")
        
        return {"error": "达到最大重试次数", "success": False}
    
    def crawl_single_url(self, url: str, options: Dict = None) -> Dict:
        """单页面采集（基础方法）"""
        if options is None:
            options = {
                "formats": ["markdown"],
                "onlyMainContent": True
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

def main():
    """主函数 - 演示高级用法"""
    
    # 初始化采集器
    collector = AdvancedFirecrawlCollector(
        api_base="http://localhost:8000",
        api_key="your_api_key_here"  # 替换为实际的API密钥
    )
    
    print("🔥 Firecrawl数据采集器 - 高级使用示例")
    print("=" * 50)
    
    # 1. 创建监控任务
    print("\n1. 创建监控任务...")
    monitor_result = collector.create_monitor(
        url="https://example.com",
        name="Example Site Monitor",
        schedule="0 */6 * * *"  # 每6小时检查一次
    )
    
    if monitor_result.get("success"):
        monitor_id = monitor_result.get("monitor_id")
        print(f"✅ 监控任务已创建，ID: {monitor_id}")
    else:
        print(f"❌ 创建监控任务失败: {monitor_result.get('error', 'Unknown error')}")
        monitor_id = None
    
    # 2. 获取监控任务列表
    print("\n2. 获取监控任务列表...")
    monitors = collector.get_monitors()
    
    if monitors.get("success"):
        monitor_list = monitors.get("data", [])
        print(f"✅ 找到 {len(monitor_list)} 个监控任务")
        
        for monitor in monitor_list:
            name = monitor.get("name", "Unnamed")
            url = monitor.get("url", "N/A")
            status = monitor.get("enabled", False)
            print(f"  - {name}: {url} ({'启用' if status else '禁用'})")
    else:
        print(f"❌ 获取监控任务失败: {monitors.get('error', 'Unknown error')}")
    
    # 3. 带重试的采集
    print("\n3. 带重试的采集示例...")
    test_url = "https://httpbin.org/html"
    
    result = collector.crawl_with_retry(test_url, max_retries=3, delay=2)
    
    if result.get("success"):
        print(f"✅ 采集成功！任务ID: {result.get('job_id')}")
    else:
        print(f"❌ 采集失败: {result.get('error', 'Unknown error')}")
    
    # 4. 获取采集历史
    print("\n4. 获取采集历史...")
    history = collector.get_data_history(limit=5)
    
    if history.get("success"):
        data_list = history.get("data", [])
        print(f"✅ 找到 {len(data_list)} 条历史记录")
        
        for i, item in enumerate(data_list[:3], 1):
            title = item.get("title", "Untitled")
            url = item.get("url", "N/A")
            timestamp = item.get("timestamp", "N/A")
            print(f"  {i}. {title} - {url} ({timestamp})")
    else:
        print(f"❌ 获取历史失败: {history.get('error', 'Unknown error')}")
    
    # 5. 内容变化分析
    print("\n5. 内容变化分析...")
    analysis_url = "https://example.com"
    
    changes = collector.analyze_content_changes(analysis_url, days=7)
    
    if changes.get("success"):
        total_changes = changes.get("total_changes", 0)
        print(f"✅ 分析完成！发现 {total_changes} 次变化")
        
        change_list = changes.get("changes", [])
        for change in change_list[:3]:  # 只显示前3次变化
            timestamp = change.get("timestamp", "N/A")
            change_type = change.get("change_type", "unknown")
            print(f"  - {timestamp}: {change_type}")
    else:
        print(f"❌ 分析失败: {changes.get('error', 'Unknown error')}")
    
    # 6. 数据导出
    print("\n6. 数据导出示例...")
    
    # 导出为JSON
    json_export = collector.export_data(format="json", limit=5)
    if json_export.get("success"):
        print(f"✅ JSON导出成功，包含 {json_export.get('count', 0)} 条数据")
    
    # 导出为Markdown
    md_export = collector.export_data(format="markdown", limit=3)
    if md_export.get("success"):
        print(f"✅ Markdown导出成功，包含 {md_export.get('count', 0)} 条数据")
        # 保存到文件
        with open("firecrawl_export.md", "w", encoding="utf-8") as f:
            f.write(md_export.get("data", ""))
        print("  📄 已保存到 firecrawl_export.md")
    
    # 7. 清理监控任务（如果创建了的话）
    if monitor_id:
        print(f"\n7. 清理监控任务 {monitor_id}...")
        delete_result = collector.delete_monitor(monitor_id)
        
        if delete_result.get("success"):
            print("✅ 监控任务已删除")
        else:
            print(f"❌ 删除监控任务失败: {delete_result.get('error', 'Unknown error')}")
    
    print("\n🎉 高级示例演示完成！")

if __name__ == "__main__":
    main()
