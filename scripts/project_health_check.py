#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目健康检查脚本

检查项目的各项指标，生成健康报告。

作者: AI Assistant
创建时间: 2025-01-29
版本: v1.0
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import re


class ProjectHealthChecker:
    """项目健康检查器"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "version": "v2.1.0",
            "checks": {},
            "overall_health": "unknown",
            "score": 0
        }

    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有检查"""
        print("🏥 项目健康检查")
        print("=" * 60)

        checks = [
            ("安全检查", self.check_security),
            ("代码质量", self.check_code_quality),
            ("测试覆盖率", self.check_test_coverage),
            ("依赖检查", self.check_dependencies),
            ("配置完整性", self.check_config),
            ("文档完整性", self.check_documentation),
            ("代码规范", self.check_code_style),
            ("性能指标", self.check_performance)
        ]

        total_score = 0
        max_score = len(checks) * 100

        for name, check_func in checks:
            print(f"\n📋 {name}...")
            try:
                result = check_func()
                self.report["checks"][name] = result
                total_score += result.get("score", 0)

                status = "✅" if result.get("passed", False) else "❌"
                print(f"   {status} 得分: {result.get('score', 0)}/100")

            except Exception as e:
                print(f"   ❌ 检查失败: {e}")
                self.report["checks"][name] = {
                    "passed": False,
                    "score": 0,
                    "error": str(e)
                }

        # 计算总分
        self.report["score"] = int((total_score / max_score) * 100)

        # 判断整体健康状况
        if self.report["score"] >= 80:
            self.report["overall_health"] = "excellent"
        elif self.report["score"] >= 60:
            self.report["overall_health"] = "good"
        elif self.report["score"] >= 40:
            self.report["overall_health"] = "fair"
        else:
            self.report["overall_health"] = "poor"

        return self.report

    def check_security(self) -> Dict[str, Any]:
        """安全检查"""
        issues = []
        score = 100

        # 1. 检查硬编码的 API Key
        for py_file in self.project_root.rglob("*.py"):
            if "归档" in str(py_file) or "venv" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                if re.search(r'fc-[a-z0-9]{32}', content):
                    issues.append(f"发现硬编码 API Key: {py_file}")
                    score -= 50
            except:
                pass

        # 2. 检查 .env 文件
        if not (self.project_root / ".env.example").exists():
            issues.append("缺少 .env.example 文件")
            score -= 10

        # 3. 检查 .gitignore
        gitignore = self.project_root / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            if ".env" not in content:
                issues.append(".gitignore 未排除 .env")
                score -= 10

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "issues": issues,
            "recommendations": [
                "使用环境变量存储敏感信息",
                "添加 pre-commit 钩子检测泄露",
                "定期审计代码"
            ] if issues else []
        }

    def check_code_quality(self) -> Dict[str, Any]:
        """代码质量检查"""
        issues = []
        score = 100

        # 1. 统计代码行数
        total_lines = 0
        py_files = 0

        for py_file in (self.project_root / "src").rglob("*.py"):
            py_files += 1
            total_lines += len(py_file.read_text().splitlines())

        # 2. 检查类型提示
        typed_files = 0
        for py_file in (self.project_root / "src").rglob("*.py"):
            content = py_file.read_text()
            if " -> " in content or "from typing import" in content:
                typed_files += 1

        type_hint_coverage = (typed_files / py_files * 100) if py_files > 0 else 0

        if type_hint_coverage < 70:
            issues.append(f"类型提示覆盖率低: {type_hint_coverage:.1f}%")
            score -= 20

        # 3. 检查文档字符串
        docstring_files = 0
        for py_file in (self.project_root / "src").rglob("*.py"):
            content = py_file.read_text()
            if '"""' in content or "'''" in content:
                docstring_files += 1

        docstring_coverage = (docstring_files / py_files * 100) if py_files > 0 else 0

        if docstring_coverage < 60:
            issues.append(f"文档字符串覆盖率低: {docstring_coverage:.1f}%")
            score -= 15

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "stats": {
                "total_files": py_files,
                "total_lines": total_lines,
                "type_hint_coverage": f"{type_hint_coverage:.1f}%",
                "docstring_coverage": f"{docstring_coverage:.1f}%"
            },
            "issues": issues
        }

    def check_test_coverage(self) -> Dict[str, Any]:
        """测试覆盖率检查"""
        issues = []
        score = 100

        # 统计测试文件
        test_files = list((self.project_root / "tests").rglob("test_*.py"))
        src_files = list((self.project_root / "src").rglob("*.py"))

        test_count = len(test_files)
        src_count = len(src_files)

        # 估算覆盖率（简化）
        estimated_coverage = min(100, (test_count / src_count * 100) * 2) if src_count > 0 else 0

        if estimated_coverage < 30:
            issues.append(f"测试覆盖率过低: ~{estimated_coverage:.0f}%")
            score = 30
        elif estimated_coverage < 50:
            issues.append(f"测试覆盖率偏低: ~{estimated_coverage:.0f}%")
            score = 50
        elif estimated_coverage < 80:
            score = 70

        return {
            "passed": score >= 70,
            "score": score,
            "stats": {
                "test_files": test_count,
                "source_files": src_count,
                "estimated_coverage": f"~{estimated_coverage:.0f}%"
            },
            "issues": issues,
            "recommendations": [
                "目标覆盖率: >80%",
                "添加单元测试",
                "添加集成测试"
            ] if issues else []
        }

    def check_dependencies(self) -> Dict[str, Any]:
        """依赖检查"""
        issues = []
        score = 100

        req_file = self.project_root / "requirements.txt"

        if not req_file.exists():
            return {"passed": False, "score": 0, "issues": ["缺少 requirements.txt"]}

        # 读取依赖
        dependencies = req_file.read_text().strip().split('\n')
        dependencies = [d for d in dependencies if d and not d.startswith('#')]

        # 检查版本固定
        pinned = sum(1 for d in dependencies if '>=' in d or '==' in d or '~=' in d)
        pin_rate = (pinned / len(dependencies) * 100) if dependencies else 0

        if pin_rate < 80:
            issues.append(f"依赖版本固定率低: {pin_rate:.0f}%")
            score -= 15

        # 检查核心依赖
        core_deps = ["firecrawl-py", "fastapi", "pydantic"]
        missing_deps = [d for d in core_deps if not any(d in dep for dep in dependencies)]

        if missing_deps:
            issues.append(f"缺少核心依赖: {', '.join(missing_deps)}")
            score -= 30

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "stats": {
                "total_dependencies": len(dependencies),
                "pinned_versions": f"{pin_rate:.0f}%"
            },
            "issues": issues
        }

    def check_config(self) -> Dict[str, Any]:
        """配置完整性检查"""
        issues = []
        score = 100

        required_configs = [
            ".cursorrules",
            "config/agents/news_agent.yaml",
            "config/agents/rental_agent.yaml",
            "config/deployment/docker-compose.yml"
        ]

        for config_file in required_configs:
            if not (self.project_root / config_file).exists():
                issues.append(f"缺少配置文件: {config_file}")
                score -= 20

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "issues": issues
        }

    def check_documentation(self) -> Dict[str, Any]:
        """文档完整性检查"""
        issues = []
        score = 100

        required_docs = [
            "README.md",
            "CHANGELOG.md",
            ".cursor/QUICK_START.md",
            "docs/INDEX.md"
        ]

        for doc_file in required_docs:
            if not (self.project_root / doc_file).exists():
                issues.append(f"缺少文档: {doc_file}")
                score -= 20

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "issues": issues
        }

    def check_code_style(self) -> Dict[str, Any]:
        """代码规范检查"""
        # 简化版本：检查是否有格式化工具配置
        score = 100
        issues = []

        if not (self.project_root / "pyproject.toml").exists():
            if not (self.project_root / "setup.cfg").exists():
                issues.append("缺少代码格式化配置")
                score -= 30

        return {
            "passed": score >= 70,
            "score": max(0, score),
            "issues": issues
        }

    def check_performance(self) -> Dict[str, Any]:
        """性能指标检查"""
        # 简化版本：检查是否使用异步
        async_usage = 0
        total_files = 0

        for py_file in (self.project_root / "src").rglob("*.py"):
            total_files += 1
            content = py_file.read_text()
            if "async def" in content or "await " in content:
                async_usage += 1

        async_rate = (async_usage / total_files * 100) if total_files > 0 else 0

        score = 100
        issues = []

        if async_rate < 50:
            issues.append(f"异步代码使用率低: {async_rate:.0f}%")
            score = 50

        return {
            "passed": score >= 70,
            "score": score,
            "stats": {
                "async_usage": f"{async_rate:.0f}%"
            },
            "issues": issues
        }

    def generate_report(self) -> str:
        """生成报告"""
        report_lines = [
            "# 项目健康检查报告",
            "",
            f"**生成时间**: {self.report['timestamp']}",
            f"**项目版本**: {self.report['version']}",
            f"**整体得分**: {self.report['score']}/100",
            f"**健康状况**: {self.report['overall_health'].upper()}",
            "",
            "---",
            ""
        ]

        # 添加各项检查结果
        for check_name, check_result in self.report["checks"].items():
            status = "✅" if check_result.get("passed", False) else "❌"
            score = check_result.get("score", 0)

            report_lines.append(f"## {status} {check_name} ({score}/100)")
            report_lines.append("")

            # 统计信息
            if "stats" in check_result:
                report_lines.append("**统计**:")
                for key, value in check_result["stats"].items():
                    report_lines.append(f"- {key}: {value}")
                report_lines.append("")

            # 问题列表
            if check_result.get("issues"):
                report_lines.append("**问题**:")
                for issue in check_result["issues"]:
                    report_lines.append(f"- {issue}")
                report_lines.append("")

            # 建议
            if check_result.get("recommendations"):
                report_lines.append("**建议**:")
                for rec in check_result["recommendations"]:
                    report_lines.append(f"- {rec}")
                report_lines.append("")

        # 总结
        report_lines.extend([
            "---",
            "",
            "## 总结",
            "",
            f"项目整体健康状况: **{self.report['overall_health'].upper()}**",
            ""
        ])

        if self.report["score"] >= 80:
            report_lines.append("✅ 项目状态优秀，继续保持！")
        elif self.report["score"] >= 60:
            report_lines.append("⚠️ 项目状态良好，建议处理上述问题。")
        else:
            report_lines.append("❌ 项目需要改进，请优先处理安全和质量问题。")

        return "\n".join(report_lines)

    def save_report(self, output_path: Path):
        """保存报告"""
        # Markdown 报告
        md_report = self.generate_report()
        md_path = output_path / "health_check_report.md"
        md_path.write_text(md_report)
        print(f"\n✅ Markdown 报告已保存: {md_path}")

        # JSON 报告
        json_path = output_path / "health_check_report.json"
        json_path.write_text(json.dumps(self.report, indent=2, ensure_ascii=False))
        print(f"✅ JSON 报告已保存: {json_path}")


def main():
    """主函数"""
    # 项目根目录
    project_root = Path(__file__).parent.parent

    # 创建检查器
    checker = ProjectHealthChecker(project_root)

    # 运行检查
    report = checker.run_all_checks()

    # 显示结果
    print("\n" + "=" * 60)
    print(f"🎯 整体得分: {report['score']}/100")
    print(f"🏥 健康状况: {report['overall_health'].upper()}")
    print("=" * 60)

    # 保存报告
    output_dir = project_root / "docs" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    checker.save_report(output_dir)

    print(f"\n完整报告: docs/reports/health_check_report.md")

    # 返回状态码
    sys.exit(0 if report['score'] >= 60 else 1)


if __name__ == "__main__":
    main()
