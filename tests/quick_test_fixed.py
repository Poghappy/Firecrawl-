#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 (修复版) - 使用Firecrawl v2 API批量采集今日头条新闻

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

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def quick_test_batch_scrape():
    """快速测试批量抓取功能"""
    
    # 修复：从环境变量获取API密钥
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("❌ 请设置FIRECRAWL_API_KEY环境变量")
        print("例如: export FIRECRAWL_API_KEY='your-api-key'")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    logger = logging.getLogger(__name__)
    
    print("🔥 Firecrawl v2 批量抓取快速测试 (修复版)")
    print("=" * 60)
    
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
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # 修复：正确解析API响应结构
            urls = []
            if 'data' in data and 'web' in data['data']:
                for item in data['data']['web']:
                    if item.get('url'):
                        urls.append(item['url'])
            
            print(f"✅ 搜索成功，找到 {len(urls)} 个URL")
            
            for i, url in enumerate(urls, 1):
                print(f"  {i}. {url}")
                
        else:
            print(f"❌ 搜索失败: {response.status_code}")
            logger.error(f"搜索失败: {response.text[:200]}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 搜索网络错误: {e}")
        logger.error(f"搜索网络错误: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ 搜索JSON解析错误: {e}")
        logger.error(f"搜索JSON解析错误: {e}")
        return
    except Exception as e:
        print(f"❌ 搜索未知错误: {e}")
        logger.error(f"搜索未知错误: {e}")
        return
    
    if not urls:
        print("❌ 没有找到可用的URL")
        return
    
    # 2. 批量抓取 (修复配置)
    print(f"\n📄 步骤2: 批量抓取 {len(urls)} 个URL")
    
    # 修复：正确的配置参数
    batch_payload = {
        "urls": urls,
        "maxConcurrency": 1,  # 降低并发数
        "ignoreInvalidURLs": True,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": 2000,      # 2秒
        "timeout": 60000,     # 60秒 (waitFor的30倍)
        "removeBase64Images": True,
        "blockAds": True,
        "location": {
            "country": "CN",
            "languages": ["zh-CN"]
        }
    }
    
    # 验证配置
    if batch_payload["waitFor"] >= batch_payload["timeout"] / 2:
        print("❌ 配置错误: waitFor must be less than half of timeout")
        return
    
    print(f"配置验证: waitFor={batch_payload['waitFor']}ms, timeout={batch_payload['timeout']}ms")
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v2/batch/scrape",
            json=batch_payload,
            headers=headers,
            timeout=30
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
                
                try:
                    status_response = requests.get(
                        f"https://api.firecrawl.dev/v2/batch/scrape/{task_id}",
                        headers=headers,
                        timeout=30
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        task_status = status_data.get('status')
                        
                        print(f"  状态检查 {attempt + 1}: {task_status}")
                        
                        if task_status == 'completed':
                            print("✅ 任务完成!")
                            
                            # 4. 获取结果 (修复：检查内容而非success字段)
                            print(f"\n📊 步骤4: 获取采集结果")
                            
                            successful_results = []
                            for item in status_data.get('data', []):
                                content = item.get('markdown', '')
                                if content and len(content.strip()) > 0:  # 检查内容是否为空
                                    successful_results.append({
                                        'url': item.get('url'),
                                        'title': item.get('title'),
                                        'content_length': len(content),
                                        'content_preview': content[:200] + '...' if len(content) > 200 else content
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
                            filename = f"quick_test_results_fixed_{timestamp}.json"
                            
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(successful_results, f, ensure_ascii=False, indent=2)
                            
                            print(f"\n💾 结果已保存到: {filename}")
                            
                            # 生成火鸟门户格式
                            huoniao_data = []
                            for result in successful_results:
                                huoniao_item = {
                                    'title': result['title'],
                                    'content': result['content_preview'],
                                    'url': result['url'],
                                    'source': 'Firecrawl采集',
                                    'category': '科技资讯',
                                    'tags': ['人工智能', '科技新闻'],
                                    'publish_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'status': 'published'
                                }
                                huoniao_data.append(huoniao_item)
                            
                            huoniao_filename = f"huoniao_format_fixed_{timestamp}.json"
                            with open(huoniao_filename, 'w', encoding='utf-8') as f:
                                json.dump(huoniao_data, f, ensure_ascii=False, indent=2)
                            
                            print(f"🏮 火鸟门户格式数据已保存到: {huoniao_filename}")
                            break
                            
                        elif task_status == 'failed':
                            print("❌ 任务失败")
                            error_info = status_data.get('error', '未知错误')
                            print(f"错误信息: {error_info}")
                            break
                            
                    else:
                        print(f"❌ 状态查询失败: {status_response.status_code}")
                        logger.error(f"状态查询失败: {status_response.text[:200]}")
                        break
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ 状态查询网络错误: {e}")
                    logger.error(f"状态查询网络错误: {e}")
                    break
                except json.JSONDecodeError as e:
                    print(f"❌ 状态查询JSON解析错误: {e}")
                    logger.error(f"状态查询JSON解析错误: {e}")
                    break
                except Exception as e:
                    print(f"❌ 状态查询未知错误: {e}")
                    logger.error(f"状态查询未知错误: {e}")
                    break
            else:
                print("⏰ 等待超时")
                
        else:
            print(f"❌ 批量抓取失败: {response.status_code}")
            print(f"错误信息: {response.text[:300]}")
            logger.error(f"批量抓取失败: {response.status_code} - {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 批量抓取网络错误: {e}")
        logger.error(f"批量抓取网络错误: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ 批量抓取JSON解析错误: {e}")
        logger.error(f"批量抓取JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 批量抓取未知错误: {e}")
        logger.error(f"批量抓取未知错误: {e}")

if __name__ == "__main__":
    quick_test_batch_scrape()
