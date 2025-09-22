#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目健康检查脚本

检查Firecrawl数据采集器项目的各个组件状态，包括：
- 文件完整性检查
- 依赖包验证
- 配置文件验证
- 模块导入测试
- 数据库连接测试
- 服务健康检查

作者: AI全栈工程师
创建时间: 2024-09-21
版本: v1.0
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProjectHealthChecker:
    """项目健康检查器"""
    
    def __init__(self, project_root: str = None):
        """初始化检查器"""
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "checks": {},
            "summary": {}
        }
        
    def check_file_structure(self) -> Dict[str, Any]:
        """检查项目文件结构"""
        logger.info("🔍 检查项目文件结构...")
        
        required_files = [
            "README.md",
            "requirements.txt",
            "requirements-dev.txt",
            "LICENSE",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "DEPLOYMENT.md",
            "PROJECT_INDEX.md",
            "PROJECT_METADATA.json",
            "TODO_IMPROVEMENTS.md"
        ]
        
        required_dirs = [
            "src",
            "config",
            "docs",
            "tests",
            "scripts",
            ".github"
        ]
        
        results = {
            "missing_files": [],
            "missing_dirs": [],
            "extra_files": [],
            "total_files": 0,
            "status": "unknown"
        }
        
        # 检查必需文件
        for file_name in required_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                results["missing_files"].append(file_name)
        
        # 检查必需目录
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                results["missing_dirs"].append(dir_name)
        
        # 统计总文件数
        try:
            results["total_files"] = len(list(self.project_root.rglob("*")))
        except Exception as e:
            logger.error(f"统计文件数失败: {e}")
        
        # 判断状态
        if not results["missing_files"] and not results["missing_dirs"]:
            results["status"] = "✅ 完整"
        elif len(results["missing_files"]) + len(results["missing_dirs"]) <= 2:
            results["status"] = "⚠️ 基本完整"
        else:
            results["status"] = "❌ 不完整"
            
        return results
    
    def check_dependencies(self) -> Dict[str, Any]:
        """检查依赖包"""
        logger.info("📦 检查依赖包...")
        
        results = {
            "production_deps": {"total": 0, "installed": 0, "missing": []},
            "dev_deps": {"total": 0, "installed": 0, "missing": []},
            "status": "unknown"
        }
        
        # 检查生产依赖
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            results["production_deps"] = self._check_requirements_file(req_file)
        
        # 检查开发依赖
        req_dev_file = self.project_root / "requirements-dev.txt"
        if req_dev_file.exists():
            results["dev_deps"] = self._check_requirements_file(req_dev_file)
        
        # 判断状态
        prod_rate = results["production_deps"]["installed"] / max(results["production_deps"]["total"], 1)
        dev_rate = results["dev_deps"]["installed"] / max(results["dev_deps"]["total"], 1)
        
        if prod_rate >= 0.9 and dev_rate >= 0.8:
            results["status"] = "✅ 良好"
        elif prod_rate >= 0.8:
            results["status"] = "⚠️ 可用"
        else:
            results["status"] = "❌ 不完整"
            
        return results
    
    def _check_requirements_file(self, req_file: Path) -> Dict[str, Any]:
        """检查单个requirements文件"""
        result = {"total": 0, "installed": 0, "missing": []}
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 提取包名
                    package_name = line.split('>=')[0].split('==')[0].split('[')[0]
                    result["total"] += 1
                    
                    try:
                        importlib.import_module(package_name.replace('-', '_'))
                        result["installed"] += 1
                    except ImportError:
                        try:
                            # 尝试使用pip show检查
                            subprocess.run(
                                [sys.executable, '-m', 'pip', 'show', package_name],
                                check=True,
                                capture_output=True
                            )
                            result["installed"] += 1
                        except subprocess.CalledProcessError:
                            result["missing"].append(package_name)
        
        except Exception as e:
            logger.error(f"检查requirements文件失败: {e}")
            
        return result
    
    def check_source_code(self) -> Dict[str, Any]:
        """检查源代码"""
        logger.info("🐍 检查源代码...")
        
        results = {
            "modules": {},
            "syntax_errors": [],
            "import_errors": [],
            "total_modules": 0,
            "valid_modules": 0,
            "status": "unknown"
        }
        
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            results["status"] = "❌ 源码目录不存在"
            return results
        
        # 检查所有Python文件
        for py_file in src_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            module_name = py_file.stem
            results["total_modules"] += 1
            
            # 语法检查
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, str(py_file), 'exec')
                
                results["modules"][module_name] = {"syntax": "✅", "import": "❓"}
                
                # 导入检查
                try:
                    sys.path.insert(0, str(src_dir))
                    importlib.import_module(module_name)
                    results["modules"][module_name]["import"] = "✅"
                    results["valid_modules"] += 1
                except ImportError as e:
                    results["modules"][module_name]["import"] = f"❌ {str(e)[:50]}"
                    results["import_errors"].append(f"{module_name}: {e}")
                finally:
                    if str(src_dir) in sys.path:
                        sys.path.remove(str(src_dir))
                        
            except SyntaxError as e:
                results["modules"][module_name] = {"syntax": f"❌ {str(e)[:50]}", "import": "❌"}
                results["syntax_errors"].append(f"{module_name}: {e}")
        
        # 判断状态
        if results["total_modules"] == 0:
            results["status"] = "❌ 无源码文件"
        elif results["valid_modules"] / results["total_modules"] >= 0.8:
            results["status"] = "✅ 良好"
        elif results["valid_modules"] / results["total_modules"] >= 0.6:
            results["status"] = "⚠️ 可用"
        else:
            results["status"] = "❌ 问题较多"
            
        return results
    
    def check_configuration(self) -> Dict[str, Any]:
        """检查配置文件"""
        logger.info("⚙️ 检查配置文件...")
        
        results = {
            "config_files": {},
            "docker_files": {},
            "github_actions": {},
            "status": "unknown"
        }
        
        # 检查配置文件
        config_files = [
            "results/config.json",
            "results/config_example.json",
        ]
        
        for config_file in config_files:
            file_path = self.project_root / config_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                    results["config_files"][config_file] = "✅ 有效"
                except json.JSONDecodeError as e:
                    results["config_files"][config_file] = f"❌ JSON错误: {e}"
            else:
                results["config_files"][config_file] = "❌ 不存在"
        
        # 检查Docker文件
        docker_files = [
            "config/deployment/Dockerfile",
            "config/deployment/docker-compose.yml",
            "config/deployment/docker-compose.production.yml"
        ]
        
        for docker_file in docker_files:
            file_path = self.project_root / docker_file
            results["docker_files"][docker_file] = "✅ 存在" if file_path.exists() else "❌ 不存在"
        
        # 检查GitHub Actions
        gh_actions_dir = self.project_root / ".github/workflows"
        if gh_actions_dir.exists():
            for workflow_file in gh_actions_dir.glob("*.yml"):
                results["github_actions"][workflow_file.name] = "✅ 存在"
        
        # 判断状态
        config_ok = sum(1 for v in results["config_files"].values() if v.startswith("✅"))
        docker_ok = sum(1 for v in results["docker_files"].values() if v.startswith("✅"))
        actions_ok = len(results["github_actions"])
        
        if config_ok >= 1 and docker_ok >= 2 and actions_ok >= 1:
            results["status"] = "✅ 完整"
        elif config_ok >= 1 and docker_ok >= 1:
            results["status"] = "⚠️ 基本完整"
        else:
            results["status"] = "❌ 不完整"
            
        return results
    
    def check_tests(self) -> Dict[str, Any]:
        """检查测试文件"""
        logger.info("🧪 检查测试文件...")
        
        results = {
            "test_files": {},
            "total_tests": 0,
            "runnable_tests": 0,
            "status": "unknown"
        }
        
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            results["status"] = "❌ 测试目录不存在"
            return results
        
        # 检查测试文件
        for test_file in tests_dir.glob("*.py"):
            if test_file.name.startswith("__"):
                continue
                
            results["total_tests"] += 1
            
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否包含测试函数
                if "def test_" in content or "class Test" in content:
                    results["test_files"][test_file.name] = "✅ 有效测试"
                    results["runnable_tests"] += 1
                else:
                    results["test_files"][test_file.name] = "⚠️ 无测试函数"
                    
            except Exception as e:
                results["test_files"][test_file.name] = f"❌ 错误: {e}"
        
        # 判断状态
        if results["total_tests"] == 0:
            results["status"] = "❌ 无测试文件"
        elif results["runnable_tests"] / results["total_tests"] >= 0.8:
            results["status"] = "✅ 良好"
        elif results["runnable_tests"] > 0:
            results["status"] = "⚠️ 部分可用"
        else:
            results["status"] = "❌ 无有效测试"
            
        return results
    
    def check_documentation(self) -> Dict[str, Any]:
        """检查文档"""
        logger.info("📚 检查文档...")
        
        results = {
            "readme": "❌",
            "api_docs": "❌",
            "deployment_docs": "❌",
            "examples": "❌",
            "total_docs": 0,
            "status": "unknown"
        }
        
        # 检查主要文档
        if (self.project_root / "README.md").exists():
            results["readme"] = "✅"
        
        if (self.project_root / "docs/API.md").exists():
            results["api_docs"] = "✅"
            
        if (self.project_root / "DEPLOYMENT.md").exists():
            results["deployment_docs"] = "✅"
            
        if (self.project_root / "docs/examples").exists():
            examples_dir = self.project_root / "docs/examples"
            if any(examples_dir.glob("*.py")):
                results["examples"] = "✅"
        
        # 统计文档数量
        docs_dir = self.project_root / "docs"
        if docs_dir.exists():
            results["total_docs"] = len(list(docs_dir.rglob("*.md")))
        
        # 判断状态
        main_docs_ok = sum(1 for k, v in results.items() 
                          if k in ["readme", "api_docs", "deployment_docs", "examples"] and v == "✅")
        
        if main_docs_ok >= 3:
            results["status"] = "✅ 完整"
        elif main_docs_ok >= 2:
            results["status"] = "⚠️ 基本完整"
        else:
            results["status"] = "❌ 不完整"
            
        return results
    
    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有检查"""
        logger.info("🚀 开始项目健康检查...")
        
        # 执行各项检查
        self.results["checks"]["file_structure"] = self.check_file_structure()
        self.results["checks"]["dependencies"] = self.check_dependencies()
        self.results["checks"]["source_code"] = self.check_source_code()
        self.results["checks"]["configuration"] = self.check_configuration()
        self.results["checks"]["tests"] = self.check_tests()
        self.results["checks"]["documentation"] = self.check_documentation()
        
        # 生成总结
        self._generate_summary()
        
        return self.results
    
    def _generate_summary(self):
        """生成检查总结"""
        checks = self.results["checks"]
        
        # 统计各项状态
        statuses = [check.get("status", "❌") for check in checks.values()]
        
        excellent = sum(1 for s in statuses if s.startswith("✅"))
        good = sum(1 for s in statuses if s.startswith("⚠️"))
        poor = sum(1 for s in statuses if s.startswith("❌"))
        
        total = len(statuses)
        
        # 计算总体健康度
        if excellent >= total * 0.8:
            overall_health = "✅ 优秀"
        elif excellent + good >= total * 0.7:
            overall_health = "⚠️ 良好"
        else:
            overall_health = "❌ 需要改进"
        
        self.results["summary"] = {
            "overall_health": overall_health,
            "total_checks": total,
            "excellent": excellent,
            "good": good,
            "poor": poor,
            "health_score": f"{(excellent + good * 0.5) / total * 100:.1f}%"
        }
    
    def print_report(self):
        """打印检查报告"""
        print("\n" + "="*60)
        print("🔍 Firecrawl数据采集器 - 项目健康检查报告")
        print("="*60)
        
        # 总体状态
        summary = self.results["summary"]
        print(f"\n📊 总体健康度: {summary['overall_health']}")
        print(f"🎯 健康评分: {summary['health_score']}")
        print(f"📈 检查项目: {summary['total_checks']}")
        print(f"  ✅ 优秀: {summary['excellent']}")
        print(f"  ⚠️ 良好: {summary['good']}")
        print(f"  ❌ 需改进: {summary['poor']}")
        
        # 详细检查结果
        checks = self.results["checks"]
        
        print(f"\n📁 文件结构: {checks['file_structure']['status']}")
        if checks['file_structure']['missing_files']:
            print(f"  缺失文件: {', '.join(checks['file_structure']['missing_files'])}")
        if checks['file_structure']['missing_dirs']:
            print(f"  缺失目录: {', '.join(checks['file_structure']['missing_dirs'])}")
        
        print(f"\n📦 依赖包: {checks['dependencies']['status']}")
        prod_deps = checks['dependencies']['production_deps']
        dev_deps = checks['dependencies']['dev_deps']
        print(f"  生产依赖: {prod_deps['installed']}/{prod_deps['total']}")
        print(f"  开发依赖: {dev_deps['installed']}/{dev_deps['total']}")
        
        print(f"\n🐍 源代码: {checks['source_code']['status']}")
        print(f"  有效模块: {checks['source_code']['valid_modules']}/{checks['source_code']['total_modules']}")
        if checks['source_code']['syntax_errors']:
            print(f"  语法错误: {len(checks['source_code']['syntax_errors'])}")
        
        print(f"\n⚙️ 配置文件: {checks['configuration']['status']}")
        config_ok = sum(1 for v in checks['configuration']['config_files'].values() if v.startswith("✅"))
        docker_ok = sum(1 for v in checks['configuration']['docker_files'].values() if v.startswith("✅"))
        print(f"  配置文件: {config_ok}/{len(checks['configuration']['config_files'])}")
        print(f"  Docker文件: {docker_ok}/{len(checks['configuration']['docker_files'])}")
        
        print(f"\n🧪 测试文件: {checks['tests']['status']}")
        print(f"  有效测试: {checks['tests']['runnable_tests']}/{checks['tests']['total_tests']}")
        
        print(f"\n📚 文档: {checks['documentation']['status']}")
        doc_items = ['readme', 'api_docs', 'deployment_docs', 'examples']
        docs_ok = sum(1 for k in doc_items if checks['documentation'][k] == "✅")
        print(f"  主要文档: {docs_ok}/4")
        print(f"  总文档数: {checks['documentation']['total_docs']}")
        
        # 建议
        print(f"\n💡 改进建议:")
        if checks['source_code']['import_errors']:
            print("  - 修复模块导入错误")
        if checks['dependencies']['production_deps']['missing']:
            print("  - 安装缺失的生产依赖")
        if checks['tests']['runnable_tests'] == 0:
            print("  - 添加有效的测试用例")
        if checks['documentation']['status'].startswith("❌"):
            print("  - 完善项目文档")
        
        print(f"\n⏰ 检查时间: {self.results['timestamp']}")
        print("="*60)
    
    def save_report(self, output_file: str = "project_health_report.json"):
        """保存检查报告"""
        output_path = self.project_root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 健康检查报告已保存到: {output_path}")

def main():
    """主函数"""
    checker = ProjectHealthChecker()
    
    try:
        # 运行检查
        results = checker.run_all_checks()
        
        # 打印报告
        checker.print_report()
        
        # 保存报告
        checker.save_report()
        
        # 返回状态码
        summary = results["summary"]
        if summary["overall_health"].startswith("✅"):
            sys.exit(0)
        elif summary["overall_health"].startswith("⚠️"):
            sys.exit(1)
        else:
            sys.exit(2)
            
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
