#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复GitHub Actions问题的脚本
解决Dependabot PR和工作流配置问题
"""

import os
import sys
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

def run_command(command, description=""):
    """运行命令并返回结果"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return result.stdout.strip()
        else:
            print(f"❌ {description} 失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return None

def check_workflow_files():
    """检查工作流文件"""
    print("🔍 检查GitHub Actions工作流文件...")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ .github/workflows 目录不存在")
        return False
    
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("❌ 没有找到工作流文件")
        return False
    
    print(f"✅ 找到 {len(workflow_files)} 个工作流文件:")
    for file in workflow_files:
        print(f"  - {file.name}")
    
    return True

def update_workflow_actions():
    """更新工作流中的GitHub Actions版本"""
    print("🔄 更新工作流中的GitHub Actions版本...")
    
    workflow_dir = Path(".github/workflows")
    updated_files = []
    
    # 需要更新的actions
    action_updates = {
        "actions/download-artifact": "v5",
        "actions/upload-artifact": "v4", 
        "actions/cache": "v4",
        "actions/setup-python": "v5",
        "actions/checkout": "v4",
        "docker/setup-buildx-action": "v3",
        "docker/login-action": "v3",
        "docker/build-push-action": "v6"
    }
    
    for workflow_file in workflow_dir.glob("*.yml"):
        print(f"📝 更新 {workflow_file.name}...")
        
        try:
            content = workflow_file.read_text(encoding='utf-8')
            original_content = content
            
            # 更新actions版本
            for action, version in action_updates.items():
                # 匹配 uses: action@version 格式
                import re
                pattern = rf'uses:\s*{re.escape(action)}@[^\s\n]+'
                replacement = f'uses: {action}@{version}'
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                workflow_file.write_text(content, encoding='utf-8')
                updated_files.append(workflow_file.name)
                print(f"✅ {workflow_file.name} 已更新")
            else:
                print(f"ℹ️  {workflow_file.name} 无需更新")
                
        except Exception as e:
            print(f"❌ 更新 {workflow_file.name} 失败: {e}")
    
    return updated_files

def check_dependabot_config():
    """检查Dependabot配置"""
    print("🔍 检查Dependabot配置...")
    
    dependabot_config = Path(".github/dependabot.yml")
    
    if not dependabot_config.exists():
        print("📝 创建Dependabot配置文件...")
        config_content = """version: 2
updates:
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    
  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
"""
        try:
            dependabot_config.parent.mkdir(parents=True, exist_ok=True)
            dependabot_config.write_text(config_content, encoding='utf-8')
            print("✅ Dependabot配置文件已创建")
            return True
        except Exception as e:
            print(f"❌ 创建Dependabot配置失败: {e}")
            return False
    else:
        print("✅ Dependabot配置文件已存在")
        return True

def create_github_actions_fix_script():
    """创建GitHub Actions修复脚本"""
    print("📝 创建GitHub Actions修复脚本...")
    
    script_content = """#!/bin/bash
# GitHub Actions修复脚本

echo "🔧 修复GitHub Actions问题..."

# 1. 更新工作流文件中的actions版本
echo "📝 更新工作流文件..."
find .github/workflows -name "*.yml" -exec sed -i.bak \\
  -e 's/actions\/download-artifact@v3/actions\/download-artifact@v5/g' \\
  -e 's/actions\/upload-artifact@v3/actions\/upload-artifact@v4/g' \\
  -e 's/actions\/cache@v3/actions\/cache@v4/g' \\
  -e 's/actions\/setup-python@v4/actions\/setup-python@v5/g' \\
  -e 's/actions\/checkout@v3/actions\/checkout@v4/g' \\
  {} \\;

# 2. 清理备份文件
find .github/workflows -name "*.bak" -delete

# 3. 提交更改
git add .github/workflows/
git commit -m "fix: update GitHub Actions versions

- Update actions/download-artifact to v5
- Update actions/upload-artifact to v4  
- Update actions/cache to v4
- Update actions/setup-python to v5
- Update actions/checkout to v4

Resolves dependabot PRs #1, #2, #3"

git push origin main

echo "✅ GitHub Actions修复完成"
"""
    
    script_path = Path("scripts/fix-github-actions.sh")
    script_path.write_text(script_content, encoding='utf-8')
    script_path.chmod(0o755)
    
    print("✅ GitHub Actions修复脚本已创建")
    return script_path

def main():
    """主函数"""
    print("🚀 开始修复GitHub Actions问题...")
    print("=" * 50)
    
    # 检查工作流文件
    if not check_workflow_files():
        print("❌ 工作流文件检查失败")
        return False
    
    # 更新工作流actions版本
    updated_files = update_workflow_actions()
    
    # 检查Dependabot配置
    check_dependabot_config()
    
    # 创建修复脚本
    script_path = create_github_actions_fix_script()
    
    print("=" * 50)
    print("📋 修复总结:")
    print(f"✅ 工作流文件检查: 通过")
    print(f"✅ 更新的文件: {len(updated_files)} 个")
    print(f"✅ Dependabot配置: 已检查/创建")
    print(f"✅ 修复脚本: {script_path}")
    
    print("\n🔧 下一步操作:")
    print("1. 运行修复脚本:")
    print(f"   bash {script_path}")
    print("2. 或者手动执行:")
    print("   git add .github/")
    print("   git commit -m 'fix: update GitHub Actions versions'")
    print("   git push origin main")
    
    print("\n📝 这将解决以下Dependabot PR:")
    print("   - PR #1: actions/upload-artifact v3 → v4")
    print("   - PR #2: actions/cache v3 → v4")
    print("   - PR #3: actions/download-artifact v3 → v5")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
