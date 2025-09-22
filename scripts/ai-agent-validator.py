#!/usr/bin/env python3
"""
AI Agent配置验证工具
用于验证.cursor配置的完整性和正确性
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from dataclasses import dataclass
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """验证结果"""
    success: bool
    message: str
    details: List[str]
    errors: List[str]
    warnings: List[str]

class AIAgentValidator:
    """AI Agent配置验证器"""
    
    def __init__(self, project_root: str = "."):
        """初始化验证器"""
        self.project_root = Path(project_root)
        self.cursor_dir = self.project_root / ".cursor"
        self.rules_dir = self.cursor_dir / "rules"
        
        # 必需文件列表
        self.required_files = [
            ".cursor/rules/main.md",
            ".cursor/rules/firecrawl-project.md",
            ".cursor/rules/tech-stack.md",
            ".cursor/rules/workflow.md",
            ".cursor/rules/file-patterns.md",
            ".cursor/rules/ai-assistant.md",
            ".cursor/rules/agent-system.md",
            ".cursor/rules/development-guide.md",
            ".cursor/rules/team-collaboration.md",
            ".cursor/agent-config.json",
            ".cursor/templates.py"
        ]
        
        # 必需内容检查
        self.required_content = {
            "main.md": ["角色定义", "项目目标", "开发规范", "技术栈"],
            "firecrawl-project.md": ["项目概述", "项目结构", "开发规范"],
            "tech-stack.md": ["核心技术栈", "依赖管理", "部署配置"],
            "workflow.md": ["工作流程", "分支管理", "代码审查"],
            "file-patterns.md": ["文件命名", "目录结构", "内容规范"],
            "ai-assistant.md": ["AI交互指南", "响应格式", "代码生成"],
            "agent-system.md": ["Agent角色", "行为准则", "工作流程"],
            "development-guide.md": ["快速开始", "项目架构", "开发规范"],
            "team-collaboration.md": ["团队协作", "质量标准", "知识管理"]
        }
    
    def validate_all(self) -> ValidationResult:
        """验证所有配置"""
        logger.info("🔍 开始AI Agent配置验证...")
        
        result = ValidationResult(
            success=True,
            message="AI Agent配置验证完成",
            details=[],
            errors=[],
            warnings=[]
        )
        
        # 1. 验证文件存在性
        file_result = self._validate_file_existence()
        self._merge_result(result, file_result)
        
        # 2. 验证文件内容
        content_result = self._validate_file_content()
        self._merge_result(result, content_result)
        
        # 3. 验证JSON配置
        json_result = self._validate_json_config()
        self._merge_result(result, json_result)
        
        # 4. 验证模板文件
        template_result = self._validate_template_file()
        self._merge_result(result, template_result)
        
        # 5. 验证项目集成
        integration_result = self._validate_project_integration()
        self._merge_result(result, integration_result)
        
        # 设置最终状态
        result.success = len(result.errors) == 0
        
        if result.success:
            result.message = "✅ AI Agent配置验证通过"
        else:
            result.message = f"❌ AI Agent配置验证失败，发现 {len(result.errors)} 个错误"
        
        return result
    
    def _validate_file_existence(self) -> ValidationResult:
        """验证文件存在性"""
        logger.info("📁 验证文件存在性...")
        
        result = ValidationResult(
            success=True,
            message="文件存在性验证",
            details=[],
            errors=[],
            warnings=[]
        )
        
        for file_path in self.required_files:
            full_path = self.project_root / file_path
            
            if full_path.exists():
                result.details.append(f"✅ 文件存在: {file_path}")
            else:
                result.errors.append(f"❌ 缺少文件: {file_path}")
                result.success = False
        
        return result
    
    def _validate_file_content(self) -> ValidationResult:
        """验证文件内容"""
        logger.info("📝 验证文件内容...")
        
        result = ValidationResult(
            success=True,
            message="文件内容验证",
            details=[],
            errors=[],
            warnings=[]
        )
        
        for filename, required_sections in self.required_content.items():
            file_path = self.rules_dir / filename
            
            if not file_path.exists():
                result.errors.append(f"❌ 文件不存在: {filename}")
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # 检查必需章节
                missing_sections = []
                for section in required_sections:
                    if section not in content:
                        missing_sections.append(section)
                
                if missing_sections:
                    result.errors.append(f"❌ {filename} 缺少章节: {', '.join(missing_sections)}")
                else:
                    result.details.append(f"✅ {filename} 内容完整")
                
                # 检查文件大小
                file_size = len(content)
                if file_size < 1000:
                    result.warnings.append(f"⚠️ {filename} 文件较小 ({file_size} 字符)")
                elif file_size > 50000:
                    result.warnings.append(f"⚠️ {filename} 文件较大 ({file_size} 字符)")
                
            except Exception as e:
                result.errors.append(f"❌ 读取文件失败 {filename}: {e}")
        
        return result
    
    def _validate_json_config(self) -> ValidationResult:
        """验证JSON配置文件"""
        logger.info("⚙️ 验证JSON配置...")
        
        result = ValidationResult(
            success=True,
            message="JSON配置验证",
            details=[],
            errors=[],
            warnings=[]
        )
        
        config_path = self.cursor_dir / "agent-config.json"
        
        if not config_path.exists():
            result.errors.append("❌ agent-config.json 文件不存在")
            return result
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证必需字段
            required_fields = [
                "version", "name", "description",
                "agent_profile", "project_context",
                "capabilities", "behavior_rules"
            ]
            
            for field in required_fields:
                if field not in config:
                    result.errors.append(f"❌ 缺少必需字段: {field}")
                else:
                    result.details.append(f"✅ 字段存在: {field}")
            
            # 验证版本格式
            if "version" in config:
                version = config["version"]
                if not isinstance(version, str) or not version.count('.') == 2:
                    result.errors.append("❌ 版本格式不正确，应为 'x.y.z' 格式")
                else:
                    result.details.append(f"✅ 版本格式正确: {version}")
            
            # 验证Agent配置完整性
            if "agent_profile" in config:
                profile = config["agent_profile"]
                if not isinstance(profile, dict):
                    result.errors.append("❌ agent_profile 应为字典类型")
                else:
                    result.details.append("✅ agent_profile 格式正确")
            
            result.details.append("✅ JSON配置格式正确")
            
        except json.JSONDecodeError as e:
            result.errors.append(f"❌ JSON格式错误: {e}")
        except Exception as e:
            result.errors.append(f"❌ 配置文件验证失败: {e}")
        
        return result
    
    def _validate_template_file(self) -> ValidationResult:
        """验证模板文件"""
        logger.info("🔧 验证模板文件...")
        
        result = ValidationResult(
            success=True,
            message="模板文件验证",
            details=[],
            errors=[],
            warnings=[]
        )
        
        template_path = self.cursor_dir / "templates.py"
        
        if not template_path.exists():
            result.errors.append("❌ templates.py 文件不存在")
            return result
        
        try:
            content = template_path.read_text(encoding='utf-8')
            
            # 检查必需的类
            required_classes = [
                "BaseResponse", "BaseService", "BaseCollector",
                "BaseProcessor", "BaseAPIServer", "BaseDatabaseService"
            ]
            
            for class_name in required_classes:
                if f"class {class_name}" in content:
                    result.details.append(f"✅ 模板类存在: {class_name}")
                else:
                    result.errors.append(f"❌ 缺少模板类: {class_name}")
            
            # 检查导入语句
            required_imports = [
                "from typing import", "from dataclasses import",
                "import logging", "import asyncio"
            ]
            
            for import_stmt in required_imports:
                if import_stmt in content:
                    result.details.append(f"✅ 导入语句存在: {import_stmt}")
                else:
                    result.warnings.append(f"⚠️ 缺少导入语句: {import_stmt}")
            
            result.details.append("✅ 模板文件结构正确")
            
        except Exception as e:
            result.errors.append(f"❌ 模板文件验证失败: {e}")
        
        return result
    
    def _validate_project_integration(self) -> ValidationResult:
        """验证项目集成"""
        logger.info("🔗 验证项目集成...")
        
        result = ValidationResult(
            success=True,
            message="项目集成验证",
            details=[],
            errors=[],
            warnings=[]
        )
        
        # 检查项目状态文件
        status_file = self.project_root / "project_status.md"
        if status_file.exists():
            result.details.append("✅ 项目状态文件存在")
        else:
            result.warnings.append("⚠️ 缺少项目状态文件")
        
        # 检查GitHub工作流
        workflow_dir = self.project_root / ".github" / "workflows"
        if workflow_dir.exists():
            workflow_files = list(workflow_dir.glob("*.yml"))
            if workflow_files:
                result.details.append(f"✅ GitHub工作流文件存在: {len(workflow_files)} 个")
            else:
                result.warnings.append("⚠️ GitHub工作流目录为空")
        else:
            result.warnings.append("⚠️ 缺少GitHub工作流目录")
        
        # 检查文档目录
        docs_dir = self.project_root / "docs"
        if docs_dir.exists():
            doc_files = list(docs_dir.rglob("*.md"))
            result.details.append(f"✅ 文档文件存在: {len(doc_files)} 个")
        else:
            result.warnings.append("⚠️ 缺少文档目录")
        
        # 检查测试目录
        tests_dir = self.project_root / "tests"
        if tests_dir.exists():
            test_files = list(tests_dir.glob("test_*.py"))
            result.details.append(f"✅ 测试文件存在: {len(test_files)} 个")
        else:
            result.warnings.append("⚠️ 缺少测试目录")
        
        return result
    
    def _merge_result(self, main_result: ValidationResult, sub_result: ValidationResult):
        """合并验证结果"""
        main_result.details.extend(sub_result.details)
        main_result.errors.extend(sub_result.errors)
        main_result.warnings.extend(sub_result.warnings)
        
        if not sub_result.success:
            main_result.success = False
    
    def generate_report(self, result: ValidationResult) -> str:
        """生成验证报告"""
        report = []
        report.append("# AI Agent配置验证报告")
        report.append("=========================")
        report.append("")
        report.append(f"**验证时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**项目路径**: {self.project_root.absolute()}")
        report.append(f"**验证结果**: {result.message}")
        report.append("")
        
        # 统计信息
        report.append("## 📊 统计信息")
        report.append("")
        report.append(f"- 总检查项: {len(result.details) + len(result.errors) + len(result.warnings)}")
        report.append(f"- 通过项目: {len(result.details)}")
        report.append(f"- 错误项目: {len(result.errors)}")
        report.append(f"- 警告项目: {len(result.warnings)}")
        report.append("")
        
        # 详细结果
        if result.details:
            report.append("## ✅ 通过项目")
            report.append("")
            for detail in result.details:
                report.append(f"- {detail}")
            report.append("")
        
        if result.errors:
            report.append("## ❌ 错误项目")
            report.append("")
            for error in result.errors:
                report.append(f"- {error}")
            report.append("")
        
        if result.warnings:
            report.append("## ⚠️ 警告项目")
            report.append("")
            for warning in result.warnings:
                report.append(f"- {warning}")
            report.append("")
        
        # 建议
        report.append("## 💡 改进建议")
        report.append("")
        if result.errors:
            report.append("1. 修复所有错误项目")
            report.append("2. 确保所有必需文件存在")
            report.append("3. 完善文件内容")
        else:
            report.append("1. 处理警告项目")
            report.append("2. 持续优化配置")
            report.append("3. 定期验证配置完整性")
        
        report.append("")
        report.append("---")
        report.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report)

def main():
    """主函数"""
    print("🤖 AI Agent配置验证工具")
    print("=" * 50)
    
    # 获取项目根目录
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # 创建验证器
    validator = AIAgentValidator(project_root)
    
    # 执行验证
    result = validator.validate_all()
    
    # 生成报告
    report = validator.generate_report(result)
    
    # 输出结果
    print(f"\n{result.message}")
    print(f"详细项目: {len(result.details)}")
    print(f"错误项目: {len(result.errors)}")
    print(f"警告项目: {len(result.warnings)}")
    
    # 保存报告
    report_path = Path(project_root) / "ai-agent-validation-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 验证报告已保存: {report_path}")
    
    # 返回退出码
    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()
