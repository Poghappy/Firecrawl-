#!/usr/bin/env python3
"""
GitHub配置验证脚本
验证GitHub Secrets和Actions配置是否正确
"""

import os
import sys
import requests
import json
from datetime import datetime

def check_github_workflow():
    """检查GitHub Actions工作流状态"""
    print("🔍 检查GitHub Actions工作流...")
    
    # 检查工作流文件是否存在
    workflow_files = [
        '.github/workflows/ci-cd.yml',
        '.github/workflows/docker-build.yml'
    ]
    
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            print(f"✅ {workflow_file} 存在")
        else:
            print(f"❌ {workflow_file} 不存在")
            return False
    
    return True

def check_docker_config():
    """检查Docker配置"""
    print("\n🐳 检查Docker配置...")
    
    docker_files = [
        'config/deployment/Dockerfile',
        'config/deployment/docker-compose.yml',
        'config/deployment/docker-compose.production.yml'
    ]
    
    for docker_file in docker_files:
        if os.path.exists(docker_file):
            print(f"✅ {docker_file} 存在")
        else:
            print(f"❌ {docker_file} 不存在")
            return False
    
    return True

def check_environment_config():
    """检查环境配置"""
    print("\n🔧 检查环境配置...")
    
    # 检查requirements.txt
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt 存在")
    else:
        print("❌ requirements.txt 不存在")
        return False
    
    # 检查配置文件
    config_files = [
        'config.json',
        'results/config_example.json'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} 存在")
        else:
            print(f"⚠️  {config_file} 不存在（可选）")
    
    return True

def check_documentation():
    """检查文档完整性"""
    print("\n📚 检查文档完整性...")
    
    doc_files = [
        'README.md',
        'docs/API.md',
        'docs/GITHUB_SETUP.md',
        'docs/DOCKER_HUB_SETUP.md',
        'DEPLOYMENT.md',
        'CONTRIBUTING.md',
        'CODE_OF_CONDUCT.md'
    ]
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            print(f"✅ {doc_file} 存在")
        else:
            print(f"❌ {doc_file} 不存在")
            return False
    
    return True

def generate_verification_report():
    """生成验证报告"""
    print("\n" + "="*60)
    print("📊 GitHub配置验证报告")
    print("="*60)
    
    # 检查各项配置
    workflow_ok = check_github_workflow()
    docker_ok = check_docker_config()
    env_ok = check_environment_config()
    docs_ok = check_documentation()
    
    # 计算总体状态
    total_checks = 4
    passed_checks = sum([workflow_ok, docker_ok, env_ok, docs_ok])
    
    print(f"\n📈 验证结果: {passed_checks}/{total_checks} 项检查通过")
    
    if passed_checks == total_checks:
        print("🎉 所有配置检查通过！")
        print("\n✅ 下一步操作：")
        print("1. 在GitHub仓库设置中添加Secrets")
        print("2. 启用GitHub Actions的Read and write permissions")
        print("3. 推送代码触发CI/CD工作流")
        return True
    else:
        print("⚠️  部分配置需要完善")
        print("\n🔧 需要修复的问题：")
        if not workflow_ok:
            print("- 检查GitHub Actions工作流文件")
        if not docker_ok:
            print("- 检查Docker配置文件")
        if not env_ok:
            print("- 检查环境配置文件")
        if not docs_ok:
            print("- 检查文档文件")
        return False

def main():
    """主函数"""
    print("🚀 开始GitHub配置验证...")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 切换到项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(project_root))
    
    success = generate_verification_report()
    
    if success:
        print("\n🎯 配置验证完成！您的项目已准备好进行GitHub集成。")
        sys.exit(0)
    else:
        print("\n❌ 配置验证失败，请修复上述问题后重新运行。")
        sys.exit(1)

if __name__ == "__main__":
    main()
