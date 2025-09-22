#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 使用Firecrawl v2 API批量采集今日头条新闻
"""

import requests
import json
import time

def quick_test_batch_scrape():
    """快速测试批量抓取功能"""
    
    # 配置
    API_KEY = "fc-0a2c801f433d4718bcd8189f2742edf4"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🔥 Firecrawl v2 批量抓取快速测试")
    print("=" * 50)
    
    # 1. 先搜索获取URL列表
    print("\n📰 步骤1: 搜索今日头条新闻")
    search_payload = {
        "query": "今日头条 科技新闻",
        "limit": 3,
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True,
            "waitFor": 3000
        }
    }
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v2/search",
            json=search_payload,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            urls = [item['url'] for item in data.get('data', []) if item.get('url')]
            print(f"✅ 搜索成功，找到 {len(urls)} 个URL")
            
            for i, url in enumerate(urls, 1):
                print(f"  {i}. {url}")
                
        else:
            print(f"❌ 搜索失败: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 搜索错误: {e}")
        return
    
    if not urls:
        print("❌ 没有找到可用的URL")
        return
    
    # 2. 批量抓取
    print(f"\n📄 步骤2: 批量抓取 {len(urls)} 个URL")
    
    batch_payload = {
        "urls": urls,
        "maxConcurrency": 2,  # 控制并发数
        "ignoreInvalidURLs": True,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": 5000,  # 等待JS渲染
        "timeout": 30,
        "removeBase64Images": True,
        "blockAds": True,
        "location": {
            "country": "CN",
            "languages": ["zh-CN"]
        }
    }
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v2/batch/scrape",
            json=batch_payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get('id')
            print(f"✅ 批量抓取任务已提交")
            print(f"任务ID: {task_id}")
            
            # 3. 等待并检查状态
            print(f"\n⏳ 步骤3: 等待任务完成...")
            
            for attempt in range(30):  # 最多等待5分钟
                time.sleep(10)
                
                status_response = requests.get(
                    f"https://api.firecrawl.dev/v2/batch/scrape/{task_id}",
                    headers=headers
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    task_status = status_data.get('status')
                    
                    print(f"  状态检查 {attempt + 1}: {task_status}")
                    
                    if task_status == 'completed':
                        print("✅ 任务完成!")
                        
                        # 4. 获取结果
                        print(f"\n📊 步骤4: 获取采集结果")
                        
                        successful_results = []
                        for item in status_data.get('data', []):
                            if item.get('success'):
                                successful_results.append({
                                    'url': item.get('url'),
                                    'title': item.get('title'),
                                    'content_length': len(item.get('markdown', '')),
                                    'content_preview': item.get('markdown', '')[:200] + '...'
                                })
                        
                        print(f"✅ 成功采集 {len(successful_results)} 条新闻")
                        
                        for i, result in enumerate(successful_results, 1):
                            print(f"\n📰 新闻 {i}:")
                            print(f"  标题: {result['title']}")
                            print(f"  URL: {result['url']}")
                            print(f"  内容长度: {result['content_length']} 字符")
                            print(f"  内容预览: {result['content_preview']}")
                        
                        # 保存结果
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        filename = f"quick_test_results_{timestamp}.json"
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(successful_results, f, ensure_ascii=False, indent=2)
                        
                        print(f"\n💾 结果已保存到: {filename}")
                        break
                        
                    elif task_status == 'failed':
                        print("❌ 任务失败")
                        break
                        
                else:
                    print(f"❌ 状态查询失败: {status_response.status_code}")
                    break
            else:
                print("⏰ 等待超时")
                
        else:
            print(f"❌ 批量抓取失败: {response.status_code}")
            print(f"错误信息: {response.text[:300]}")
            
    except Exception as e:
        print(f"❌ 批量抓取错误: {e}")

if __name__ == "__main__":
    quick_test_batch_scrape()
