#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境依赖检查脚本

快速验证项目环境是否正确配置。

使用方法:
    python scripts/check_environment.py

    # 或在虚拟环境中
    source venv/bin/activate
    python scripts/check_environment.py
"""

import sys
import os
from pathlib import Path


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_python_version():
    """检查 Python 版本"""
    print_header("🐍 Python 环境检查")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python 版本: {version_str}")
    print(f"Python 路径: {sys.executable}")

    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python 版本符合要求 (>= 3.9)")
        return True
    else:
        print(f"❌ Python 版本不符合要求 (需要 >= 3.9)")
        return False


def check_dependencies():
    """检查核心依赖"""
    print_header("📦 核心依赖检查")

    dependencies = {
        "Firecrawl SDK": "firecrawl",
        "FastAPI": "fastapi",
        "Pydantic": "pydantic",
        "AsyncIO": "asyncio",
        "AIOHTTP": "aiohttp",
        "SQLAlchemy": "sqlalchemy",
        "Alembic": "alembic",
        "Redis": "redis",
        "BeautifulSoup4": "bs4",
        "LXML": "lxml",
        "Python-dotenv": "dotenv",
        "PyYAML": "yaml",
        "Requests": "requests",
        "Schedule": "schedule",
        "APScheduler": "apscheduler",
        "Pytest": "pytest",
        "Black": "black",
        "Rich": "rich",
    }

    success_count = 0
    failed_deps = []

    for name, module in dependencies.items():
        try:
            __import__(module)
            version = ""
            try:
                mod = __import__(module)
                if hasattr(mod, '__version__'):
                    version = f" v{mod.__version__}"
            except:
                pass
            print(f"✅ {name:20s}{version}")
            success_count += 1
        except ImportError:
            print(f"❌ {name:20s} - 未安装")
            failed_deps.append((name, module))

    print(f"\n📊 依赖检查结果: {success_count}/{len(dependencies)} 已安装")

    if failed_deps:
        print("\n⚠️  未安装的依赖:")
        for name, module in failed_deps:
            print(f"  - {name} ({module})")
        print("\n运行以下命令安装:")
        print("  pip install -r requirements.txt")
        return False

    return True


def check_core_modules():
    """检查核心模块"""
    print_header("🔧 核心模块检查")

    modules = [
        ("智能体基类", "src.core.base_agent", "BaseAgent"),
        ("智能体注册表", "src.core.agent_registry", "AgentRegistry"),
        ("智能体管理器", "src.core.agent_manager", "AgentManager"),
        ("新闻模型", "src.models.news", "NewsArticle"),
        ("电商模型", "src.models.ecommerce", "Product"),
        ("招聘模型", "src.models.recruitment", "JobPosting"),
        ("租房模型", "src.models.rental", "RentalListing"),
        ("学习模型", "src.models.learning", "Course"),
    ]

    success_count = 0

    for name, module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {name:20s} ({class_name})")
            success_count += 1
        except Exception as e:
            print(f"❌ {name:20s} - 导入失败: {e}")

    print(f"\n📊 模块检查结果: {success_count}/{len(modules)} 可用")
    return success_count == len(modules)


def check_config_files():
    """检查配置文件"""
    print_header("📄 配置文件检查")

    config_files = [
        (".env.example", "环境变量模板"),
        (".env", "环境配置文件"),
        ("config/agents/news_agent.yaml", "新闻智能体配置"),
        ("config/agents/ecommerce_agent.yaml", "电商智能体配置"),
        ("config/agents/recruitment_agent.yaml", "招聘智能体配置"),
        ("config/agents/rental_agent.yaml", "租房智能体配置"),
        ("config/agents/learning_agent.yaml", "学习智能体配置"),
    ]

    success_count = 0

    for file_path, description in config_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {description:25s} ({size} bytes)")
            success_count += 1
        else:
            print(f"❌ {description:25s} - 不存在")

    print(f"\n📊 配置文件检查: {success_count}/{len(config_files)} 存在")
    return success_count == len(config_files)


def check_environment_variables():
    """检查环境变量"""
    print_header("🔐 环境变量检查")

    # 尝试加载 .env 文件
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env 文件已加载")
    except Exception as e:
        print(f"⚠️  .env 文件加载失败: {e}")

    required_vars = {
        "FIRECRAWL_API_KEY": "Firecrawl API 密钥",
    }

    optional_vars = {
        "POSTGRES_HOST": "PostgreSQL 主机",
        "REDIS_URL": "Redis 连接",
        "LOG_LEVEL": "日志级别",
    }

    # 检查必需变量
    print("\n必需的环境变量:")
    all_required = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != "fc-your-api-key-here":
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var:25s} - 已配置 ({masked})")
        else:
            print(f"❌ {var:25s} - 未配置")
            all_required = False

    # 检查可选变量
    print("\n可选的环境变量:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var:25s} - 已配置")
        else:
            print(f"⚪ {var:25s} - 使用默认值")

    if not all_required:
        print("\n⚠️  请编辑 .env 文件，配置必需的环境变量")

    return all_required


def check_directory_structure():
    """检查目录结构"""
    print_header("📁 目录结构检查")

    required_dirs = [
        "src/core",
        "src/models",
        "config/agents",
        "tests",
        "logs",
        "data",
        "output",
    ]

    success_count = 0

    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"✅ {dir_path:30s} - 存在")
            success_count += 1
        else:
            print(f"❌ {dir_path:30s} - 不存在")
            # 自动创建
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"   ↳ 已自动创建")
                success_count += 1
            except Exception as e:
                print(f"   ↳ 创建失败: {e}")

    print(f"\n📊 目录检查结果: {success_count}/{len(required_dirs)} 就绪")
    return success_count == len(required_dirs)


def generate_summary():
    """生成检查总结"""
    print_header("📋 环境检查总结")

    checks = [
        ("Python 版本", check_python_version()),
        ("核心依赖", check_dependencies()),
        ("核心模块", check_core_modules()),
        ("配置文件", check_config_files()),
        ("环境变量", check_environment_variables()),
        ("目录结构", check_directory_structure()),
    ]

    print("\n最终结果:")
    passed = sum(1 for _, result in checks if result)
    total = len(checks)

    for name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name:15s}: {status}")

    print("\n" + "=" * 70)
    if passed == total:
        print(f"🎉 环境检查完成！{passed}/{total} 项全部通过")
        print("\n✨ 项目已准备就绪，可以开始开发！")
        print("\n下一步:")
        print("  1. 确认 .env 中配置了真实的 FIRECRAWL_API_KEY")
        print("  2. 阅读 PROJECT_INITIALIZATION_COMPLETE.md 了解后续步骤")
        print("  3. 开始实现第一个智能体（建议从 NewsAgent 开始）")
    else:
        print(f"⚠️  环境检查未完全通过: {passed}/{total}")
        print("\n请根据上述错误信息进行修复")
    print("=" * 70)


if __name__ == "__main__":
    try:
        generate_summary()
    except KeyboardInterrupt:
        print("\n\n❌ 检查已中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 检查过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
