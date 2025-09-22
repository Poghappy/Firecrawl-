#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火鸟门户系统 Firecrawl 集成方案本地测试

本测试脚本验证核心模块的功能，不依赖外部API连接
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pipeline_config import ConfigManager, APIConfig, CrawlConfig
    from firecrawl_pipeline_manager import FirecrawlPipelineManager
    from database_models import CrawlJob, JobStatus, JobPriority
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class LocalTester:
    """本地测试类"""
    
    def __init__(self):
        self.test_results = []
        self.config_manager = None
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        status = "✅ 通过" if success else "❌ 失败"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {message}")
        
    def test_config_loading(self):
        """测试配置加载"""
        try:
            # 创建测试配置
            test_config = {
                "api": {
                    "base_url": "https://api.firecrawl.dev",
                    "firecrawl_api_key": "test_key_1234567890",
                    "timeout": 30,
                    "max_retries": 3
                },
                "crawl": {
                    "max_pages": 100,
                    "concurrent_requests": 5,
                    "delay_between_requests": 1.0,
                    "respect_robots_txt": True
                },
                "notification": {
                    "enabled": False,
                    "channels": []
                },
                "security": {
                    "enable_request_signing": False,
                    "encrypt_sensitive_data": False
                }
            }
            
            # 保存测试配置文件
            config_path = Path("test_config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(test_config, f, indent=2, ensure_ascii=False)
            
            # 测试配置管理器
            self.config_manager = ConfigManager(str(config_path))
            config = self.config_manager.load_config()
            
            # 验证配置
            assert config.api.base_url == "https://api.firecrawl.dev"
            assert config.api.firecrawl_api_key == "test_key_1234567890"
            assert config.crawl.default_limit == 100
            
            # 清理测试文件
            config_path.unlink()
            
            self.log_test("配置加载测试", True, "配置文件加载和验证成功")
            
        except Exception as e:
            self.log_test("配置加载测试", False, f"配置加载失败: {str(e)}")
            
    def test_data_models(self):
        """测试数据模型"""
        try:
            # 测试创建爬取任务
            job = CrawlJob(
                job_id="test_job_456",
                url="https://example.com",
                status=JobStatus.PENDING,
                priority=JobPriority.MEDIUM,
                limit=10
            )
            
            # 验证模型属性
            assert job.url == "https://example.com"
            assert job.status == JobStatus.PENDING
            assert job.priority == JobPriority.MEDIUM
            assert job.limit == 10
            
            self.log_test("数据模型测试", True, "数据模型创建和验证成功")
            
        except Exception as e:
            self.log_test("数据模型测试", False, f"数据模型测试失败: {str(e)}")
            
    def test_pipeline_manager_init(self):
        """测试管道管理器初始化"""
        try:
            if not self.config_manager:
                # 创建默认配置
                api_config = APIConfig(
                    base_url="https://api.firecrawl.dev",
                    api_key="test_key"
                )
                crawl_config = CrawlConfig()
                
                # 模拟配置管理器
                class MockConfigManager:
                    def load_config(self):
                        class MockConfig:
                            def __init__(self):
                                self.api = api_config
                                self.crawl = crawl_config
                        return MockConfig()
                        
                self.config_manager = MockConfigManager()
            
            # 测试管道管理器初始化（不连接数据库）
            # 这里只测试类的实例化，不测试数据库连接
            manager_class = FirecrawlPipelineManager
            
            # 验证类存在且可以导入
            assert hasattr(manager_class, '__init__')
            assert hasattr(manager_class, 'start_crawl_job')
            assert hasattr(manager_class, 'get_job_status')
            
            self.log_test("管道管理器初始化测试", True, "管道管理器类结构验证成功")
            
        except Exception as e:
            self.log_test("管道管理器初始化测试", False, f"管道管理器测试失败: {str(e)}")
            
    def test_api_server_structure(self):
        """测试API服务器结构"""
        try:
            # 检查API服务器文件是否存在
            api_server_path = Path("api_server.py")
            if not api_server_path.exists():
                raise FileNotFoundError("api_server.py 文件不存在")
                
            # 读取并验证API服务器代码结构
            with open(api_server_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查关键组件
            required_components = [
                "from fastapi import FastAPI",
                "@app.post",
                "@app.get",
                "async def",
                "uvicorn.run"
            ]
            
            missing_components = []
            for component in required_components:
                if component not in content:
                    missing_components.append(component)
                    
            if missing_components:
                raise ValueError(f"缺少关键组件: {missing_components}")
                
            self.log_test("API服务器结构测试", True, "API服务器代码结构验证成功")
            
        except Exception as e:
            self.log_test("API服务器结构测试", False, f"API服务器结构测试失败: {str(e)}")
            
    def test_docker_configuration(self):
        """测试Docker配置"""
        try:
            # 检查Docker配置文件
            docker_compose_path = Path("docker-compose.yml")
            dockerfile_path = Path("Dockerfile")
            
            if not docker_compose_path.exists():
                raise FileNotFoundError("docker-compose.yml 文件不存在")
                
            if not dockerfile_path.exists():
                raise FileNotFoundError("Dockerfile 文件不存在")
                
            # 读取Docker Compose配置
            with open(docker_compose_path, 'r', encoding='utf-8') as f:
                compose_content = f.read()
                
            # 检查关键服务
            required_services = [
                "firecrawl-api",
                "postgres",
                "redis",
                "nginx"
            ]
            
            missing_services = []
            for service in required_services:
                if service not in compose_content:
                    missing_services.append(service)
                    
            if missing_services:
                raise ValueError(f"缺少关键服务: {missing_services}")
                
            self.log_test("Docker配置测试", True, "Docker配置文件验证成功")
            
        except Exception as e:
            self.log_test("Docker配置测试", False, f"Docker配置测试失败: {str(e)}")
            
    def test_deployment_script(self):
        """测试部署脚本"""
        try:
            deploy_script_path = Path("deploy.sh")
            if not deploy_script_path.exists():
                raise FileNotFoundError("deploy.sh 文件不存在")
                
            # 检查脚本是否可执行
            if not os.access(deploy_script_path, os.X_OK):
                raise PermissionError("deploy.sh 文件不可执行")
                
            # 读取脚本内容
            with open(deploy_script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
                
            # 检查关键功能
            required_functions = [
                "install",
                "start",
                "stop",
                "docker-compose"
            ]
            
            missing_functions = []
            for func in required_functions:
                if func not in script_content:
                    missing_functions.append(func)
                    
            if missing_functions:
                raise ValueError(f"缺少关键功能: {missing_functions}")
                
            self.log_test("部署脚本测试", True, "部署脚本验证成功")
            
        except Exception as e:
            self.log_test("部署脚本测试", False, f"部署脚本测试失败: {str(e)}")
            
    def run_all_tests(self):
        """运行所有测试"""
        print("\n🚀 开始火鸟门户系统 Firecrawl 集成方案本地测试\n")
        print("=" * 60)
        
        # 执行所有测试
        self.test_config_loading()
        self.test_data_models()
        self.test_pipeline_manager_init()
        self.test_api_server_structure()
        self.test_docker_configuration()
        self.test_deployment_script()
        
        # 统计测试结果
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if "✅" in result["status"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 测试结果汇总:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过测试: {passed_tests}")
        print(f"   失败测试: {failed_tests}")
        print(f"   成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 所有测试通过！系统集成方案验证成功！")
        else:
            print("\n⚠️  部分测试失败，请检查相关组件")
            
        # 保存测试报告
        report_path = Path("test_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
                },
                "results": self.test_results
            }, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 详细测试报告已保存到: {report_path}")
        
        return failed_tests == 0

def main():
    """主函数"""
    tester = LocalTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()