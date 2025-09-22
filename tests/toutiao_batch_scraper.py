#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条新闻批量采集器
使用Firecrawl v2 API进行高效的新闻内容采集
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class ToutiaoBatchScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.dev/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索新闻获取URL列表"""
        print(f"🔍 搜索新闻: {query}")
        
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
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                urls = []
                
                for item in data.get('data', []):
                    urls.append({
                        'url': item.get('url'),
                        'title': item.get('title'),
                        'description': item.get('description')
                    })
                
                print(f"✅ 搜索成功，找到 {len(urls)} 条新闻")
                return urls
            else:
                print(f"❌ 搜索失败: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索错误: {e}")
            return []
    
    def batch_scrape_news(self, urls: List[str], **options) -> Dict:
        """批量抓取新闻内容"""
        print(f"📄 开始批量抓取 {len(urls)} 条新闻...")
        
        # 默认配置
        default_options = {
            "maxConcurrency": 3,  # 控制并发数，避免API限制
            "ignoreInvalidURLs": True,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "waitFor": 5000,  # 等待JS渲染
            "timeout": 30,
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
        
        payload = {
            "urls": urls,
            **default_options
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/batch/scrape",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 批量抓取任务已提交")
                print(f"任务ID: {result.get('id', '未知')}")
                print(f"状态: {result.get('status', '未知')}")
                return result
            else:
                print(f"❌ 批量抓取失败: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ 批量抓取错误: {e}")
            return {}
    
    def check_batch_status(self, task_id: str) -> Dict:
        """检查批量抓取任务状态"""
        try:
            response = requests.get(
                f"{self.base_url}/batch/scrape/{task_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 状态查询失败: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ 状态查询错误: {e}")
            return {}
    
    def get_batch_results(self, task_id: str) -> List[Dict]:
        """获取批量抓取结果"""
        print(f"📊 获取任务 {task_id} 的结果...")
        
        status = self.check_batch_status(task_id)
        
        if status.get('status') == 'completed':
            results = []
            for item in status.get('data', []):
                if item.get('success'):
                    results.append({
                        'url': item.get('url'),
                        'title': item.get('title'),
                        'content': item.get('markdown', ''),
                        'metadata': item.get('metadata', {})
                    })
            
            print(f"✅ 获取到 {len(results)} 条成功抓取的新闻")
            return results
        else:
            print(f"⏳ 任务状态: {status.get('status', '未知')}")
            return []
    
    def scrape_toutiao_news(self, queries: List[str], limit_per_query: int = 5) -> List[Dict]:
        """完整的今日头条新闻采集流程"""
        print("🚀 开始今日头条新闻采集流程")
        print("=" * 50)
        
        all_news = []
        
        for query in queries:
            print(f"\n📰 处理查询: {query}")
            
            # 1. 搜索新闻
            news_urls = self.search_news(query, limit_per_query)
            
            if not news_urls:
                continue
            
            # 2. 提取URL列表
            urls = [item['url'] for item in news_urls if item['url']]
            
            if not urls:
                continue
            
            # 3. 批量抓取
            batch_result = self.batch_scrape_news(urls)
            
            if not batch_result.get('id'):
                continue
            
            task_id = batch_result['id']
            
            # 4. 等待任务完成
            print("⏳ 等待批量抓取完成...")
            max_wait = 300  # 最多等待5分钟
            wait_time = 0
            
            while wait_time < max_wait:
                status = self.check_batch_status(task_id)
                
                if status.get('status') == 'completed':
                    break
                elif status.get('status') == 'failed':
                    print("❌ 批量抓取任务失败")
                    break
                
                time.sleep(10)  # 等待10秒
                wait_time += 10
                print(f"⏳ 等待中... ({wait_time}s)")
            
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
        
        print(f"\n🎉 采集完成! 总共获得 {len(all_news)} 条新闻")
        return all_news
    
    def save_results(self, results: List[Dict], filename: str = None):
        """保存采集结果到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"toutiao_news_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"💾 结果已保存到: {filename}")
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")

def main():
    """主函数 - 使用示例"""
    
    # 使用您的API密钥
    API_KEY = "fc-0a2c801f433d4718bcd8189f2742edf4"
    
    # 创建采集器实例
    scraper = ToutiaoBatchScraper(API_KEY)
    
    # 定义搜索查询
    queries = [
        "人工智能 最新新闻",
        "科技资讯 头条",
        "AI技术发展"
    ]
    
    print("🔥 今日头条新闻批量采集器")
    print("=" * 50)
    
    try:
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
            scraper.save_results(results)
            
        else:
            print("❌ 没有采集到任何新闻")
            
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断采集")
    except Exception as e:
        print(f"❌ 采集过程中发生错误: {e}")

if __name__ == "__main__":
    main()
