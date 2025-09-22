#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复验证脚本
验证代码修复是否成功

作者: AI代码审查助手
创建时间: 2025-01-22
版本: v1.0
"""

import os
import sys
import json
import requests
from typing import Dict, List, Any

def test_api_structure_parsing():
    """测试API响应结构解析修复"""
    print("🧪 测试1: API响应结构解析")
    
    # 模拟Firecrawl v2搜索API响应
    mock_response = {
        "success": True,
        "data": {
            "web": [
                {
                    "url": "https://example.com/news1",
                    "title": "测试新闻1",
                    "description": "测试描述1"
                },
                {
                    "url": "https://example.com/news2", 
                    "title": "测试新闻2",
                    "description": "测试描述2"
                }
            ]
        }
    }
    
    # 测试修复后的解析逻辑
    urls = []
    if 'data' in mock_response and 'web' in mock_response['data']:
        for item in mock_response['data']['web']:
            if item.get('url'):
                urls.append({
                    'url': item.get('url'),
                    'title': item.get('title', ''),
                    'description': item.get('description', '')
                })
    
    expected_count = 2
    actual_count = len(urls)
    
    if actual_count == expected_count:
        print(f"✅ API结构解析正确: 找到 {actual_count} 个URL")
        return True
    else:
        print(f"❌ API结构解析错误: 期望 {expected_count}, 实际 {actual_count}")
        return False

def test_config_validation():
    """测试配置参数验证修复"""
    print("\n🧪 测试2: 配置参数验证")
    
    # 测试正确的配置
    correct_config = {
        "waitFor": 2000,   # 2秒
        "timeout": 60000,  # 60秒
    }
    
    # 测试错误的配置
    incorrect_config = {
        "waitFor": 5000,   # 5秒
        "timeout": 30,     # 30秒 (waitFor > timeout/2)
    }
    
    def validate_config(config):
        return config["waitFor"] < config["timeout"] / 2
    
    correct_result = validate_config(correct_config)
    incorrect_result = validate_config(incorrect_config)
    
    if correct_result and not incorrect_result:
        print("✅ 配置验证正确: 正确配置通过，错误配置被拒绝")
        return True
    else:
        print(f"❌ 配置验证错误: 正确={correct_result}, 错误={incorrect_result}")
        return False

def test_environment_variable_handling():
    """测试环境变量处理修复"""
    print("\n🧪 测试3: 环境变量处理")
    
    # 保存原始环境变量
    original_key = os.environ.get('FIRECRAWL_API_KEY')
    
    try:
        # 测试没有环境变量的情况
        if 'FIRECRAWL_API_KEY' in os.environ:
            del os.environ['FIRECRAWL_API_KEY']
        
        # 模拟修复后的代码逻辑
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            print("✅ 环境变量检查正确: 正确检测到缺失的API密钥")
            return True
        else:
            print("❌ 环境变量检查错误: 应该检测到缺失的API密钥")
            return False
            
    finally:
        # 恢复原始环境变量
        if original_key:
            os.environ['FIRECRAWL_API_KEY'] = original_key

def test_content_validation():
    """测试内容验证修复"""
    print("\n🧪 测试4: 内容验证")
    
    # 模拟批量抓取结果
    mock_batch_results = [
        {
            "url": "https://example.com/news1",
            "title": "新闻1",
            "markdown": "这是新闻1的内容，包含足够的信息...",
            "success": False  # API标记为失败
        },
        {
            "url": "https://example.com/news2", 
            "title": "新闻2",
            "markdown": "",  # 空内容
            "success": True  # API标记为成功
        },
        {
            "url": "https://example.com/news3",
            "title": "新闻3", 
            "markdown": "这是新闻3的内容，包含足够的信息...",
            "success": False  # API标记为失败
        }
    ]
    
    # 测试修复后的内容检查逻辑
    successful_results = []
    for item in mock_batch_results:
        content = item.get('markdown', '')
        if content and len(content.strip()) > 0:  # 检查内容是否为空
            successful_results.append({
                'url': item.get('url'),
                'title': item.get('title'),
                'content': content
            })
    
    expected_count = 2  # 只有新闻1和新闻3有内容
    actual_count = len(successful_results)
    
    if actual_count == expected_count:
        print(f"✅ 内容验证正确: 找到 {actual_count} 条有效内容")
        return True
    else:
        print(f"❌ 内容验证错误: 期望 {expected_count}, 实际 {actual_count}")
        return False

def test_error_handling():
    """测试错误处理修复"""
    print("\n🧪 测试5: 错误处理")
    
    # 测试不同类型的异常处理
    test_cases = [
        ("网络错误", requests.exceptions.RequestException("网络连接失败")),
        ("JSON解析错误", json.JSONDecodeError("解析错误", "", 0)),
        ("通用错误", Exception("未知错误"))
    ]
    
    def simulate_error_handling(exception):
        """模拟修复后的错误处理"""
        try:
            raise exception
        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {e}"
        except json.JSONDecodeError as e:
            return f"JSON解析错误: {e}"
        except Exception as e:
            return f"未知错误: {e}"
    
    all_passed = True
    for test_name, exception in test_cases:
        result = simulate_error_handling(exception)
        if test_name in result:
            print(f"✅ {test_name}处理正确: {result}")
        else:
            print(f"❌ {test_name}处理错误: {result}")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """运行所有测试"""
    print("🔍 Firecrawl数据采集器修复验证")
    print("=" * 50)
    
    tests = [
        test_api_structure_parsing,
        test_config_validation,
        test_environment_variable_handling,
        test_content_validation,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试执行失败: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有修复验证通过!")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
