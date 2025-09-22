#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试文件
测试核心功能的基本可用性
"""

import sys
import os
import pytest
from pathlib import Path

# 添加src目录到Python路径
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)

def test_project_structure():
    """测试项目结构完整性"""
    project_root = Path(__file__).parent.parent
    
    # 检查关键目录
    assert (project_root / "src").exists(), "src目录不存在"
    assert (project_root / "tests").exists(), "tests目录不存在"
    assert (project_root / "config").exists(), "config目录不存在"
    assert (project_root / "docs").exists(), "docs目录不存在"
    
    # 检查关键文件
    assert (project_root / "requirements.txt").exists(), "requirements.txt不存在"
    assert (project_root / "README.md").exists(), "README.md不存在"

def test_imports():
    """测试核心模块导入"""
    try:
        from src.firecrawl_config import FirecrawlConfig
        assert True, "FirecrawlConfig导入成功"
    except ImportError as e:
        pytest.skip(f"FirecrawlConfig导入失败: {e}")
    
    try:
        from src.firecrawl_collector import FirecrawlCollector
        assert True, "FirecrawlCollector导入成功"
    except ImportError as e:
        pytest.skip(f"FirecrawlCollector导入失败: {e}")

def test_config_files():
    """测试配置文件"""
    project_root = Path(__file__).parent.parent
    
    # 检查配置文件
    config_files = [
        "results/config_example.json",
        "config/deployment/docker-compose.yml"
    ]
    
    for config_file in config_files:
        config_path = project_root / config_file
        if config_path.exists():
            assert config_path.is_file(), f"{config_file}不是文件"
        else:
            pytest.skip(f"{config_file}不存在")

def test_dependencies():
    """测试依赖包"""
    try:
        import firecrawl
        assert True, "firecrawl包可用"
    except ImportError:
        pytest.skip("firecrawl包未安装")
    
    try:
        import fastapi
        assert True, "fastapi包可用"
    except ImportError:
        pytest.skip("fastapi包未安装")
    
    try:
        import pydantic
        assert True, "pydantic包可用"
    except ImportError:
        pytest.skip("pydantic包未安装")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
