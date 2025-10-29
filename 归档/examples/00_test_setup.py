#!/usr/bin/env python3
"""Firecrawl SDK 配置测试脚本.

快速验证 SDK 是否正确配置。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import NoReturn

from dotenv import load_dotenv


def print_header(text: str) -> None:
    """打印标题."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def test_python_version() -> bool:
    """测试 Python 版本."""
    print_header("🐍 Python 版本检查")

    version = sys.version_info
    print(f"当前版本: Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ 需要 Python 3.11 或更高版本")
        return False

    print("✅ Python 版本符合要求")
    return True


def test_firecrawl_package() -> bool:
    """测试 firecrawl-py 包."""
    print_header("📦 Firecrawl 包检查")

    try:
        import firecrawl

        print("✅ firecrawl-py 已安装")
        print(f"📊 版本: {firecrawl.__version__}")
        return True
    except ImportError:
        print("❌ firecrawl-py 未安装")
        print("💡 安装命令: pip install firecrawl-py")
        return False


def test_dotenv_package() -> bool:
    """测试 python-dotenv 包."""
    print_header("📦 dotenv 包检查")

    try:
        import dotenv

        version = getattr(dotenv, "__version__", "未知版本")
        print("✅ python-dotenv 已安装")
        print(f"📊 版本: {version}")
        return True
    except ImportError:
        print("❌ python-dotenv 未安装")
        print("💡 安装命令: pip install python-dotenv")
        return False


def test_env_file() -> bool:
    """测试 .env 文件."""
    print_header("🔐 环境配置检查")

    env_file = Path(__file__).parent.parent / ".env"

    if not env_file.exists():
        print("❌ .env 文件不存在")
        print("💡 复制模板: cp env.template .env")
        return False

    print(f"✅ .env 文件存在: {env_file}")
    return True


def test_api_key() -> bool:
    """测试 API 密钥."""
    print_header("🔑 API 密钥检查")

    # 加载环境变量
    load_dotenv()

    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("❌ 未找到 FIRECRAWL_API_KEY 环境变量")
        print("💡 请在 .env 文件中设置 FIRECRAWL_API_KEY")
        return False

    print("✅ API 密钥已配置")
    print(f"📊 密钥前缀: {api_key[:10]}...")
    print(f"📊 密钥后缀: ...{api_key[-10:]}")

    # 检查备用密钥
    backup_keys = [
        os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
        os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
        os.getenv("FIRECRAWL_API_KEY_BACKUP_3"),
    ]

    valid_backups = [k for k in backup_keys if k]

    if valid_backups:
        print(f"📊 备用密钥: {len(valid_backups)}/3 个已配置")
    else:
        print("⚠️  备用密钥未配置（可选，用于负载均衡）")

    return True


def test_api_connection() -> bool:
    """测试 API 连接."""
    print_header("🌐 API 连接测试")

    try:
        from firecrawl import FirecrawlApp

        print("⏳ 正在测试 API 连接...")

        app = FirecrawlApp()

        # 测试简单的 scrape
        result = app.scrape(
            url="https://firecrawl.dev/",
            formats=["markdown"],
            only_main_content=True,
            max_age=172800000,  # 使用缓存
        )

        if result and hasattr(result, "markdown") and result.markdown:
            print("✅ API 连接成功！")
            print(f"📊 测试数据长度: {len(result.markdown)} 字符")

            cache_state = result.metadata.get("cacheState", "unknown")
            print(f"📊 缓存状态: {cache_state}")

            if cache_state == "hit":
                print("🎉 命中缓存！此次测试免费")

            return True

        print("❌ API 返回结果异常")
        return False

    except ImportError:
        print("❌ firecrawl-py 包未安装")
        return False
    except OSError as e:
        print(f"❌ 网络错误: {e}")
        return False
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False


def print_summary(passed: int, total: int) -> None:
    """打印测试总结."""
    print_header("📋 测试总结")

    success_rate = (passed / total) * 100 if total > 0 else 0

    print(f"✅ 通过: {passed}/{total} ({success_rate:.0f}%)")

    if passed == total:
        print("\n🎉 所有测试通过！SDK 配置完成！")
        print("\n📚 下一步:")
        print("   1. 运行基础示例: python3 examples/01_basic_scrape.py")
        print("   2. 运行爬取示例: python3 examples/02_crawl_website.py")
        print("   3. 运行批量示例: python3 examples/03_batch_scrape.py")
        print("\n📖 学习资源:")
        print("   - 完整指南: Firecrawl学习手册/03-API参考/08-Python-SDK完整指南.md")
        print("   - 示例文档: examples/README.md")
    else:
        print("\n⚠️  部分测试失败，请检查上述错误信息")
        print("\n💡 常见问题:")
        print("   - Python 版本过低 → 升级到 3.11+")
        print("   - 包未安装 → pip install firecrawl-py python-dotenv")
        print("   - 环境变量未配置 → 复制 env.template 为 .env 并填入 API 密钥")
        print("   - API 连接失败 → 检查网络连接和 API 密钥是否有效")


def main() -> None:
    """主函数."""
    print("\n" + "🔥" * 30)
    print("   Firecrawl SDK 配置测试")
    print("   FireShot 项目 - HawaiiHub")
    print("🔥" * 30)

    tests = [
        ("Python 版本", test_python_version),
        ("Firecrawl 包", test_firecrawl_package),
        ("dotenv 包", test_dotenv_package),
        ("环境配置文件", test_env_file),
        ("API 密钥", test_api_key),
        ("API 连接", test_api_connection),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except OSError as e:
            print(f"❌ {test_name} 网络错误: {e}")
        except Exception as e:
            print(f"❌ {test_name} 测试失败: {e}")

    print_summary(passed, total)

    if passed != total:
        sys.exit(1)


def run_tests() -> NoReturn:
    """运行测试并处理异常."""
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 未预期的错误: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
