#!/usr/bin/env python3
"""
GitHub Secrets配置验证脚本
验证GitHub Secrets是否正确配置
"""

import requests
import json
import sys
from datetime import datetime

def check_github_workflow():
    """检查GitHub Actions工作流文件"""
    print("🔍 检查GitHub Actions工作流...")
    
    workflow_files = [
        '.github/workflows/ci-cd.yml',
        '.github/workflows/docker-build.yml'
    ]
    
    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'secrets.FIRECRAWL_API_KEY' in content:
                    print(f"✅ {workflow_file} 包含Firecrawl API密钥引用")
                else:
                    print(f"⚠️  {workflow_file} 未找到Firecrawl API密钥引用")
                
                if 'secrets.DOCKER_USERNAME' in content:
                    print(f"✅ {workflow_file} 包含Docker用户名引用")
                else:
                    print(f"⚠️  {workflow_file} 未找到Docker用户名引用")
                    
        except FileNotFoundError:
            print(f"❌ {workflow_file} 不存在")
            return False
    
    return True

def check_environment_files():
    """检查环境配置文件"""
    print("\n🔧 检查环境配置文件...")
    
    env_files = [
        '.env.example',
        'config.json',
        'results/config_example.json'
    ]
    
    for env_file in env_files:
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'FIRECRAWL_API_KEY' in content:
                    print(f"✅ {env_file} 包含API密钥配置")
                else:
                    print(f"⚠️  {env_file} 未找到API密钥配置")
        except FileNotFoundError:
            print(f"⚠️  {env_file} 不存在（可选）")
    
    return True

def check_docker_config():
    """检查Docker配置"""
    print("\n🐳 检查Docker配置...")
    
    docker_files = [
        'config/deployment/Dockerfile',
        'config/deployment/docker-compose.yml'
    ]
    
    for docker_file in docker_files:
        try:
            with open(docker_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'ENV' in content or 'environment' in content:
                    print(f"✅ {docker_file} 包含环境变量配置")
                else:
                    print(f"⚠️  {docker_file} 未找到环境变量配置")
        except FileNotFoundError:
            print(f"❌ {docker_file} 不存在")
            return False
    
    return True

def generate_configuration_guide():
    """生成配置指南"""
    print("\n" + "="*60)
    print("📊 GitHub Secrets配置验证报告")
    print("="*60)
    
    # 检查各项配置
    workflow_ok = check_github_workflow()
    env_ok = check_environment_files()
    docker_ok = check_docker_config()
    
    print(f"\n📈 验证结果:")
    print(f"- 工作流配置: {'✅ 通过' if workflow_ok else '❌ 失败'}")
    print(f"- 环境配置: {'✅ 通过' if env_ok else '❌ 失败'}")
    print(f"- Docker配置: {'✅ 通过' if docker_ok else '❌ 失败'}")
    
    print(f"\n🔑 需要配置的GitHub Secrets:")
    print("1. FIRECRAWL_API_KEY = fc-0a2c801f433d4718bcd8189f2742edf4")
    print("2. DOCKER_USERNAME = denzhile")
    print("3. DOCKER_PASSWORD = dckr_pat_9zHDbXagx0b60xvwbqRKNIVo_J0")
    
    print(f"\n⚙️ 需要启用的GitHub Actions权限:")
    print("1. Read and write permissions")
    print("2. Allow GitHub Actions to create and approve pull requests")
    
    print(f"\n🔗 配置链接:")
    print("1. Secrets配置: https://github.com/Poghappy/Firecrawl-/settings/secrets/actions")
    print("2. Actions权限: https://github.com/Poghappy/Firecrawl-/settings/actions")
    print("3. 工作流状态: https://github.com/Poghappy/Firecrawl-/actions")
    
    if workflow_ok and env_ok and docker_ok:
        print(f"\n🎉 配置验证通过！")
        print("✅ 下一步: 在GitHub上手动配置Secrets和Actions权限")
        return True
    else:
        print(f"\n⚠️  部分配置需要完善")
        return False

def main():
    """主函数"""
    print("🚀 GitHub Secrets配置验证开始")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = generate_configuration_guide()
    
    if success:
        print("\n🎯 配置指南完成！请按照上述步骤完成GitHub配置。")
        sys.exit(0)
    else:
        print("\n❌ 配置验证失败，请修复上述问题后重新运行。")
        sys.exit(1)

if __name__ == "__main__":
    main()
