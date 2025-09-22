#!/usr/bin/env python3
"""
Firecrawl API测试脚本
验证API密钥是否正常工作
"""

import requests
import json
import sys
from datetime import datetime

def test_firecrawl_api(api_key):
    """测试Firecrawl API连接"""
    print("🔍 测试Firecrawl API连接...")
    
    # API端点
    base_url = "https://api.firecrawl.dev/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 测试URL
    test_url = "https://example.com"
    
    try:
        # 测试scrape端点
        print(f"📡 测试scrape端点: {test_url}")
        
        payload = {
            "url": test_url,
            "formats": ["markdown"],
            "onlyMainContent": True
        }
        
        response = requests.post(
            f"{base_url}/scrape",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API连接成功！")
            print(f"📄 采集到内容长度: {len(data.get('data', {}).get('markdown', ''))}")
            print(f"🔗 目标URL: {data.get('data', {}).get('metadata', {}).get('sourceURL', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ API密钥无效或已过期")
            print("💡 请检查您的API密钥是否正确")
            return False
        elif response.status_code == 429:
            print("⚠️  API请求频率限制")
            print("💡 请稍后再试或检查您的API配额")
            return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"📝 错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
        print("💡 请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("🌐 连接错误")
        print("💡 请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False

def test_api_quota(api_key):
    """测试API配额"""
    print("\n📊 检查API配额...")
    
    base_url = "https://api.firecrawl.dev/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 尝试获取用户信息或配额信息
        response = requests.get(
            f"{base_url}/usage",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 配额信息获取成功")
            print(f"📈 使用情况: {json.dumps(data, indent=2)}")
        else:
            print(f"⚠️  无法获取配额信息: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  配额检查失败: {str(e)}")

def main():
    """主函数"""
    print("🚀 Firecrawl API测试开始")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # 从命令行参数或环境变量获取API密钥
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = "fc-0a2c801f433d4718bcd8189f2742edf4"
    
    print(f"🔑 使用API密钥: {api_key[:10]}...{api_key[-4:]}")
    
    # 测试API连接
    success = test_firecrawl_api(api_key)
    
    # 测试API配额
    test_api_quota(api_key)
    
    print("\n" + "="*50)
    if success:
        print("🎉 API测试成功！您的Firecrawl API密钥工作正常。")
        print("\n✅ 下一步操作：")
        print("1. 将API密钥添加到GitHub Secrets")
        print("2. 启用GitHub Actions")
        print("3. 推送代码触发CI/CD工作流")
        sys.exit(0)
    else:
        print("❌ API测试失败，请检查您的API密钥。")
        print("\n🔧 故障排除：")
        print("1. 确认API密钥是否正确")
        print("2. 检查API密钥是否已激活")
        print("3. 确认网络连接正常")
        print("4. 联系Firecrawl支持团队")
        sys.exit(1)

if __name__ == "__main__":
    main()
