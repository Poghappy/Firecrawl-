#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl v2 统一新闻采集器
基于深度问题诊断的完整解决方案

解决的核心问题:
1. API版本兼容性 - 统一使用v2 API
2. JavaScript渲染 - 优化等待时间和渲染策略
3. 中文内容处理 - 特殊编码和语言处理
4. 数据质量保证 - 智能内容过滤和验证

作者: AI代码审查助手 + 深度诊断分析
创建时间: 2025-01-22
版本: v3.0 (统一解决方案)
"""

import requests
import json
import time
import os
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from urllib.parse import urlparse
import hashlib

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class FirecrawlV2UnifiedScraper:
    """Firecrawl v2 统一新闻采集器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化采集器
        
        Args:
            api_key: Firecrawl API密钥
        """
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        
        self.base_url = "https://api.firecrawl.dev/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.logger = logging.getLogger(__name__)
        
        # 中文新闻采集优化配置
        self.chinese_config = {
            "waitFor": 5000,  # 增加等待时间处理JavaScript渲染
            "timeout": 90000,  # 增加超时时间
            "blockAds": True,
            "removeBase64Images": True,
            "location": {
                "country": "CN",
                "languages": ["zh-CN"]
            },
            "formats": ["markdown", "summary"],
            "onlyMainContent": True
        }
    
    def search_news_v2(self, query: str, limit: int = 10, sources: List[str] = None) -> List[Dict]:
        """使用v2 API搜索新闻
        
        Args:
            query: 搜索查询
            limit: 结果数量限制
            sources: 指定搜索源 ['web', 'images', 'news']
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        self.logger.info(f"搜索新闻: {query}")
        
        # 输入验证
        if not query or not isinstance(query, str):
            self.logger.error("查询参数无效")
            return []
        
        search_payload = {
            "query": query,
            "limit": limit,
            "scrapeOptions": self.chinese_config
        }
        
        # 如果指定了搜索源，添加到payload
        if sources:
            search_payload["sources"] = sources
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                json=search_payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # 统一处理v2 API响应结构
                for source_type in ['web', 'images', 'news']:
                    if 'data' in data and source_type in data['data']:
                        for item in data['data'][source_type]:
                            if item.get('url'):
                                results.append({
                                    'url': item.get('url'),
                                    'title': item.get('title', ''),
                                    'description': item.get('description', ''),
                                    'source_type': source_type,
                                    'position': item.get('position', 0)
                                })
                
                self.logger.info(f"搜索成功，找到 {len(results)} 条结果")
                return results
            else:
                self.logger.error(f"搜索失败: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"搜索网络错误: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"搜索JSON解析错误: {e}")
            return []
        except Exception as e:
            self.logger.error(f"搜索未知错误: {e}")
            return []
    
    def scrape_single_url(self, url: str, enhanced_config: Dict = None) -> Optional[Dict]:
        """抓取单个URL
        
        Args:
            url: 目标URL
            enhanced_config: 增强配置
            
        Returns:
            Optional[Dict]: 抓取结果
        """
        if not url:
            return None
        
        config = self.chinese_config.copy()
        if enhanced_config:
            config.update(enhanced_config)
        
        scrape_payload = {
            "url": url,
            **config
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/scrape",
                json=scrape_payload,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 检查内容质量
                content = data.get('markdown', '')
                if self._is_valid_content(content):
                    return {
                        'url': url,
                        'title': data.get('title', ''),
                        'content': content,
                        'summary': data.get('summary', ''),
                        'metadata': data.get('metadata', {}),
                        'success': True
                    }
                else:
                    self.logger.warning(f"内容质量不符合要求: {url}")
                    return None
            else:
                self.logger.error(f"抓取失败: {url} - {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"抓取错误: {url} - {e}")
            return None
    
    def batch_scrape_v2(self, urls: List[str], max_concurrency: int = 2) -> List[Dict]:
        """使用v2 API批量抓取
        
        Args:
            urls: URL列表
            max_concurrency: 最大并发数
            
        Returns:
            List[Dict]: 抓取结果列表
        """
        self.logger.info(f"开始批量抓取 {len(urls)} 个URL")
        
        if not urls:
            return []
        
        # 优化配置用于批量抓取
        batch_config = self.chinese_config.copy()
        batch_config.update({
            "maxConcurrency": max_concurrency,
            "ignoreInvalidURLs": True,
            "timeout": 120000,  # 增加批量抓取超时时间
        })
        
        batch_payload = {
            "urls": urls,
            **batch_config
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/batch/scrape",
                json=batch_payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('id')
                
                if task_id:
                    self.logger.info(f"批量抓取任务已提交: {task_id}")
                    return self._monitor_batch_task(task_id)
                else:
                    self.logger.error("批量抓取任务创建失败")
                    return []
            else:
                self.logger.error(f"批量抓取失败: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            self.logger.error(f"批量抓取错误: {e}")
            return []
    
    def _monitor_batch_task(self, task_id: str, max_wait: int = 300) -> List[Dict]:
        """监控批量抓取任务
        
        Args:
            task_id: 任务ID
            max_wait: 最大等待时间（秒）
            
        Returns:
            List[Dict]: 成功抓取的结果列表
        """
        self.logger.info(f"监控任务: {task_id}")
        
        wait_time = 0
        while wait_time < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/batch/scrape/{task_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('status')
                    
                    self.logger.info(f"任务状态: {status} (等待 {wait_time}s)")
                    
                    if status == 'completed':
                        return self._process_batch_results(data)
                    elif status == 'failed':
                        self.logger.error(f"任务失败: {data.get('error', '未知错误')}")
                        return []
                    
                    time.sleep(10)
                    wait_time += 10
                else:
                    self.logger.error(f"状态查询失败: {response.status_code}")
                    break
                    
            except Exception as e:
                self.logger.error(f"监控错误: {e}")
                break
        
        self.logger.warning("任务监控超时")
        return []
    
    def _process_batch_results(self, data: Dict) -> List[Dict]:
        """处理批量抓取结果
        
        Args:
            data: 任务结果数据
            
        Returns:
            List[Dict]: 处理后的结果列表
        """
        results = []
        raw_results = data.get('data', [])
        
        for item in raw_results:
            # 基于您的诊断：检查实际内容而非success字段
            content = item.get('markdown', '')
            if self._is_valid_content(content):
                results.append({
                    'url': item.get('url', ''),
                    'title': item.get('title', ''),
                    'content': content,
                    'summary': item.get('summary', ''),
                    'metadata': item.get('metadata', {}),
                    'success': True
                })
            else:
                self.logger.debug(f"跳过无效内容: {item.get('url', 'unknown')}")
        
        self.logger.info(f"处理完成: {len(results)}/{len(raw_results)} 条有效结果")
        return results
    
    def _is_valid_content(self, content: str, min_length: int = 100) -> bool:
        """验证内容质量
        
        Args:
            content: 内容文本
            min_length: 最小长度要求
            
        Returns:
            bool: 是否有效
        """
        if not content or not isinstance(content, str):
            return False
        
        content = content.strip()
        
        # 长度检查
        if len(content) < min_length:
            return False
        
        # 中文内容质量检查
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        if chinese_chars < 20:  # 至少20个中文字符
            return False
        
        # 检查是否包含有意义的内容
        meaningful_patterns = [
            r'[\u4e00-\u9fff]{2,}',  # 中文词汇
            r'[a-zA-Z]{3,}',         # 英文词汇
            r'\d+',                  # 数字
        ]
        
        meaningful_count = sum(len(re.findall(pattern, content)) for pattern in meaningful_patterns)
        if meaningful_count < 5:  # 至少5个有意义的内容片段
            return False
        
        return True
    
    def extract_news_content(self, url: str) -> Optional[Dict]:
        """提取新闻内容（针对新闻网站优化）
        
        Args:
            url: 新闻URL
            
        Returns:
            Optional[Dict]: 提取的新闻内容
        """
        # 针对新闻网站的增强配置
        news_config = self.chinese_config.copy()
        news_config.update({
            "waitFor": 8000,  # 新闻网站需要更长的等待时间
            "blockAds": True,
            "removeBase64Images": True,
            "formats": ["markdown", "summary", "links"],
            "onlyMainContent": True,
            "actions": [
                {"type": "wait", "milliseconds": 3000},
                {"type": "scroll", "direction": "down"},
                {"type": "wait", "milliseconds": 2000}
            ]
        })
        
        result = self.scrape_single_url(url, news_config)
        
        if result and result.get('success'):
            # 增强新闻内容处理
            content = result.get('content', '')
            
            # 提取新闻关键信息
            news_info = {
                'url': url,
                'title': result.get('title', ''),
                'content': content,
                'summary': result.get('summary', ''),
                'word_count': len(content),
                'chinese_char_count': len(re.findall(r'[\u4e00-\u9fff]', content)),
                'reading_time': max(1, len(content) // 200),  # 预估阅读时间
                'extracted_at': datetime.now().isoformat(),
                'metadata': result.get('metadata', {})
            }
            
            return news_info
        
        return None
    
    def comprehensive_news_collection(self, queries: List[str], limit_per_query: int = 5) -> List[Dict]:
        """综合新闻采集流程
        
        Args:
            queries: 搜索查询列表
            limit_per_query: 每个查询的结果数量
            
        Returns:
            List[Dict]: 采集到的新闻列表
        """
        self.logger.info("开始综合新闻采集流程")
        
        all_news = []
        
        for query in queries:
            self.logger.info(f"处理查询: {query}")
            
            # 1. 搜索新闻
            search_results = self.search_news_v2(query, limit_per_query, ['web', 'news'])
            
            if not search_results:
                self.logger.warning(f"查询 '{query}' 未找到结果")
                continue
            
            # 2. 提取URL列表
            urls = [item['url'] for item in search_results if item.get('url')]
            
            if not urls:
                self.logger.warning(f"查询 '{query}' 未找到有效URL")
                continue
            
            # 3. 批量抓取
            scrape_results = self.batch_scrape_v2(urls[:3])  # 限制并发数量
            
            # 4. 合并结果
            for result in scrape_results:
                # 添加搜索时的元数据
                for search_item in search_results:
                    if search_item['url'] == result['url']:
                        result['search_title'] = search_item['title']
                        result['search_description'] = search_item['description']
                        result['search_source_type'] = search_item['source_type']
                        break
                
                all_news.append(result)
        
        self.logger.info(f"综合采集完成: 获得 {len(all_news)} 条新闻")
        return all_news
    
    def save_results(self, results: List[Dict], filename: Optional[str] = None) -> str:
        """保存采集结果
        
        Args:
            results: 采集结果列表
            filename: 文件名
            
        Returns:
            str: 保存的文件名
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"firecrawl_v2_news_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"结果已保存到: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"保存失败: {e}")
            raise

def main():
    """主函数 - 使用示例"""
    
    # 检查环境变量
    if not os.getenv('FIRECRAWL_API_KEY'):
        print("❌ 请设置FIRECRAWL_API_KEY环境变量")
        print("例如: export FIRECRAWL_API_KEY='your-api-key'")
        return
    
    try:
        # 创建统一采集器
        scraper = FirecrawlV2UnifiedScraper()
        
        # 定义搜索查询
        queries = [
            "人工智能 最新新闻",
            "科技资讯 头条",
            "AI技术发展 2025"
        ]
        
        print("🔥 Firecrawl v2 统一新闻采集器")
        print("=" * 60)
        
        # 执行综合采集
        results = scraper.comprehensive_news_collection(queries, limit_per_query=3)
        
        if results:
            # 显示结果摘要
            print(f"\n📊 采集结果摘要:")
            for i, news in enumerate(results[:5], 1):
                print(f"{i}. {news.get('search_title', news.get('title', '无标题'))}")
                print(f"   URL: {news.get('url', '无URL')}")
                print(f"   内容长度: {news.get('word_count', len(news.get('content', '')))} 字符")
                print(f"   中文字符: {news.get('chinese_char_count', 0)} 个")
                print(f"   阅读时间: {news.get('reading_time', 0)} 分钟")
                print()
            
            # 保存结果
            filename = scraper.save_results(results)
            print(f"💾 结果已保存到: {filename}")
            
        else:
            print("❌ 没有采集到任何新闻")
            
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断采集")
    except Exception as e:
        print(f"❌ 采集过程中发生错误: {e}")

if __name__ == "__main__":
    main()
