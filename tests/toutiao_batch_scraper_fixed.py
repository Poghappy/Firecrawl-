#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条新闻批量采集器 (修复版)
使用Firecrawl v2 API进行高效的新闻内容采集

修复内容:
1. 修复API响应结构解析错误
2. 修复配置参数冲突
3. 使用环境变量管理API密钥
4. 增强错误处理和输入验证
5. 完善日志记录

作者: AI代码审查助手
修复时间: 2025-01-22
版本: v2.0 (修复版)
"""

import requests
import json
import time
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ToutiaoBatchScraper:
    def __init__(self, api_key: Optional[str] = None):
        """初始化采集器
        
        Args:
            api_key: Firecrawl API密钥，如果未提供则从环境变量获取
        """
        # 修复：从环境变量获取API密钥
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        
        self.base_url = "https://api.firecrawl.dev/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
    
    def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索新闻获取URL列表
        
        Args:
            query: 搜索查询
            limit: 结果数量限制
            
        Returns:
            List[Dict]: 新闻URL列表
        """
        self.logger.info(f"搜索新闻: {query}")
        
        # 输入验证
        if not query or not isinstance(query, str):
            self.logger.error("查询参数无效")
            return []
        
        if not isinstance(limit, int) or limit <= 0:
            self.logger.error("限制参数无效")
            return []
        
        search_payload = {
            "query": query,
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True,
                "waitFor": 3000
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search", 
                json=search_payload, 
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                urls = []
                
                # 修复：正确解析API响应结构
                if 'data' in data and 'web' in data['data']:
                    for item in data['data']['web']:
                        if item.get('url'):  # 确保URL存在
                            urls.append({
                                'url': item.get('url'),
                                'title': item.get('title', ''),
                                'description': item.get('description', '')
                            })
                
                self.logger.info(f"搜索成功，找到 {len(urls)} 条新闻")
                return urls
            else:
                self.logger.error(f"搜索失败: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"网络请求错误: {e}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析错误: {e}")
            return []
        except Exception as e:
            self.logger.error(f"搜索未知错误: {e}")
            return []
    
    def batch_scrape_news(self, urls: List[str], **options) -> Dict:
        """批量抓取新闻内容
        
        Args:
            urls: URL列表
            **options: 自定义配置选项
            
        Returns:
            Dict: 批量抓取任务结果
        """
        self.logger.info(f"开始批量抓取 {len(urls)} 条新闻...")
        
        # 输入验证
        if not urls or not isinstance(urls, list):
            self.logger.error("URL列表无效")
            return {}
        
        # 修复：正确的配置参数
        default_options = {
            "maxConcurrency": 1,  # 降低并发数，避免API限制
            "ignoreInvalidURLs": True,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "waitFor": 2000,      # 2秒
            "timeout": 60000,     # 60秒 (waitFor的30倍)
            "removeBase64Images": True,
            "blockAds": True,
            "storeInCache": True,
            "location": {
                "country": "CN",  # 中国
                "languages": ["zh-CN"]  # 中文
            }
        }
        
        # 合并用户自定义选项
        default_options.update(options)
        
        # 验证配置
        if default_options["waitFor"] >= default_options["timeout"] / 2:
            self.logger.error("waitFor must be less than half of timeout")
            return {}
        
        payload = {
            "urls": urls,
            **default_options
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/batch/scrape",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"批量抓取任务已提交: {result.get('id', '未知')}")
                return result
            else:
                self.logger.error(f"批量抓取失败: {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"批量抓取网络错误: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"批量抓取JSON解析错误: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"批量抓取未知错误: {e}")
            return {}
    
    def check_batch_status(self, task_id: str) -> Dict:
        """检查批量抓取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            Dict: 任务状态信息
        """
        if not task_id or not isinstance(task_id, str):
            self.logger.error("任务ID无效")
            return {}
        
        try:
            response = requests.get(
                f"{self.base_url}/batch/scrape/{task_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"状态查询失败: {response.status_code}")
                return {}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"状态查询网络错误: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"状态查询JSON解析错误: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"状态查询未知错误: {e}")
            return {}
    
    def get_batch_results(self, task_id: str) -> List[Dict]:
        """获取批量抓取结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[Dict]: 成功抓取的新闻列表
        """
        self.logger.info(f"获取任务 {task_id} 的结果...")
        
        status = self.check_batch_status(task_id)
        
        if status.get('status') == 'completed':
            results = []
            for item in status.get('data', []):
                # 修复：检查内容是否为空，而不是success字段
                content = item.get('markdown', '')
                if content and len(content.strip()) > 0:
                    results.append({
                        'url': item.get('url'),
                        'title': item.get('title'),
                        'content': content,
                        'metadata': item.get('metadata', {})
                    })
            
            self.logger.info(f"获取到 {len(results)} 条成功抓取的新闻")
            return results
        else:
            self.logger.info(f"任务状态: {status.get('status', '未知')}")
            return []
    
    def scrape_toutiao_news(self, queries: List[str], limit_per_query: int = 5) -> List[Dict]:
        """完整的今日头条新闻采集流程
        
        Args:
            queries: 搜索查询列表
            limit_per_query: 每个查询的结果数量限制
            
        Returns:
            List[Dict]: 采集到的新闻列表
        """
        self.logger.info("开始今日头条新闻采集流程")
        
        # 输入验证
        if not queries or not isinstance(queries, list):
            self.logger.error("查询列表无效")
            return []
        
        all_news = []
        
        for query in queries:
            self.logger.info(f"处理查询: {query}")
            
            # 1. 搜索新闻
            news_urls = self.search_news(query, limit_per_query)
            
            if not news_urls:
                self.logger.warning(f"查询 '{query}' 未找到结果")
                continue
            
            # 2. 提取URL列表
            urls = [item['url'] for item in news_urls if item.get('url')]
            
            if not urls:
                self.logger.warning(f"查询 '{query}' 未找到有效URL")
                continue
            
            # 3. 批量抓取
            batch_result = self.batch_scrape_news(urls)
            
            if not batch_result.get('id'):
                self.logger.error(f"查询 '{query}' 批量抓取任务创建失败")
                continue
            
            task_id = batch_result['id']
            
            # 4. 等待任务完成
            self.logger.info("等待批量抓取完成...")
            max_wait = 300  # 最多等待5分钟
            wait_time = 0
            
            while wait_time < max_wait:
                status = self.check_batch_status(task_id)
                
                if status.get('status') == 'completed':
                    break
                elif status.get('status') == 'failed':
                    self.logger.error("批量抓取任务失败")
                    break
                
                time.sleep(10)  # 等待10秒
                wait_time += 10
                self.logger.info(f"等待中... ({wait_time}s)")
            
            # 5. 获取结果
            results = self.get_batch_results(task_id)
            
            # 6. 合并到总结果
            for result in results:
                # 添加搜索时的标题和描述
                for news_info in news_urls:
                    if news_info['url'] == result['url']:
                        result['search_title'] = news_info['title']
                        result['search_description'] = news_info['description']
                        break
                
                all_news.append(result)
        
        self.logger.info(f"采集完成! 总共获得 {len(all_news)} 条新闻")
        return all_news
    
    def save_results(self, results: List[Dict], filename: Optional[str] = None) -> str:
        """保存采集结果到文件
        
        Args:
            results: 采集结果列表
            filename: 文件名，如果未提供则自动生成
            
        Returns:
            str: 保存的文件名
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"toutiao_news_{timestamp}.json"
        
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
        # 创建采集器实例
        scraper = ToutiaoBatchScraper()
        
        # 定义搜索查询
        queries = [
            "人工智能 最新新闻",
            "科技资讯 头条",
            "AI技术发展"
        ]
        
        print("🔥 今日头条新闻批量采集器 (修复版)")
        print("=" * 50)
        
        # 执行采集
        results = scraper.scrape_toutiao_news(queries, limit_per_query=3)
        
        if results:
            # 显示结果摘要
            print(f"\n📊 采集结果摘要:")
            for i, news in enumerate(results[:5], 1):
                print(f"{i}. {news.get('search_title', news.get('title', '无标题'))}")
                print(f"   URL: {news.get('url', '无URL')}")
                print(f"   内容长度: {len(news.get('content', ''))} 字符")
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
