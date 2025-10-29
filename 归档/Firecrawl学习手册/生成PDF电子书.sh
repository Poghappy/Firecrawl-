#!/bin/bash

echo "📚 开始生成 Firecrawl 学习手册 PDF 电子书"
echo "=================================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}🔍 检查依赖...${NC}"
    
    # 检查 Pandoc
    if ! command -v pandoc &> /dev/null; then
        echo -e "${RED}❌ 未安装 Pandoc${NC}"
        echo -e "${YELLOW}请安装: brew install pandoc${NC}"
        exit 1
    fi
    
    # 检查 LaTeX (用于PDF生成)
    if ! command -v pdflatex &> /dev/null; then
        echo -e "${RED}❌ 未安装 LaTeX${NC}"
        echo -e "${YELLOW}请安装: brew install --cask basictex${NC}"
        echo -e "${YELLOW}或安装完整版: brew install --cask mactex${NC}"
        exit 1
    fi
    
    # 检查 Mermaid CLI (可选，用于图表)
    if ! command -v mmdc &> /dev/null; then
        echo -e "${YELLOW}⚠️  未安装 Mermaid CLI (可选)${NC}"
        echo -e "${YELLOW}推荐安装: npm install -g @mermaid-js/mermaid-cli${NC}"
        echo -e "${YELLOW}跳过 Mermaid 图表渲染...${NC}"
    fi
    
    echo -e "${GREEN}✅ 依赖检查完成${NC}"
    echo ""
}

# 创建临时目录
create_temp_dir() {
    echo -e "${BLUE}📁 创建临时目录...${NC}"
    TEMP_DIR="temp_pdf_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$TEMP_DIR"
    echo -e "${GREEN}✅ 临时目录: $TEMP_DIR${NC}"
    echo ""
}

# 合并 Markdown 文件
merge_markdown() {
    echo -e "${BLUE}📝 合并 Markdown 文件...${NC}"
    
    OUTPUT_FILE="$TEMP_DIR/complete_manual.md"
    
    # 1. 封面
    echo -e "${YELLOW}  添加: 封面${NC}"
    cat "00-手册导读/PDF封面.md" > "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 2. 手册使用指南
    echo -e "${YELLOW}  添加: 手册使用指南${NC}"
    echo -e "\n# 第一部分：手册导读\n" >> "$OUTPUT_FILE"
    cat "00-手册导读/手册使用指南.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 3. 学习路线图
    echo -e "${YELLOW}  添加: 学习路线图${NC}"
    cat "00-手册导读/完整学习路线图.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 4. 快速开始
    echo -e "${YELLOW}  添加: 快速开始${NC}"
    cat "00-手册导读/快速开始指南.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 5. 核心教程
    echo -e "${YELLOW}  添加: 核心教程${NC}"
    echo -e "\n# 第二部分：基础入门\n" >> "$OUTPUT_FILE"
    cat "01-基础入门/Firecrawl完整学习手册.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 6. API 参考
    echo -e "${YELLOW}  添加: API 规范${NC}"
    echo -e "\n# 第三部分：API 参考\n" >> "$OUTPUT_FILE"
    cat "03-API参考/云端API规范.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 7. 配置指南
    echo -e "${YELLOW}  添加: 配置指南${NC}"
    echo -e "\n# 第四部分：配置指南\n" >> "$OUTPUT_FILE"
    cat "04-配置指南/云端配置指南.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 8. HawaiiHub 实战案例
    echo -e "${YELLOW}  添加: HawaiiHub 实战案例${NC}"
    echo -e "\n# 第五部分：实战案例\n" >> "$OUTPUT_FILE"
    cat "05-实战案例/HawaiiHub实战案例手册.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 9. 案例架构图
    echo -e "${YELLOW}  添加: 案例架构图集${NC}"
    cat "05-实战案例/案例架构图集.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 10. 项目索引
    echo -e "${YELLOW}  添加: 完整项目索引${NC}"
    cat "05-实战案例/完整项目总索引.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    # 11. 更新日志
    echo -e "${YELLOW}  添加: 更新日志${NC}"
    echo -e "\n# 第六部分：进阶主题\n" >> "$OUTPUT_FILE"
    cat "06-进阶主题/Firecrawl更新日志汇总.md" >> "$OUTPUT_FILE"
    echo -e "\n<div style=\"page-break-after: always;\"></div>\n" >> "$OUTPUT_FILE"
    
    echo -e "${GREEN}✅ Markdown 文件合并完成${NC}"
    echo -e "${GREEN}   输出文件: $OUTPUT_FILE${NC}"
    echo -e "${GREEN}   文件大小: $(du -h "$OUTPUT_FILE" | cut -f1)${NC}"
    echo ""
}

# 生成 PDF
generate_pdf() {
    echo -e "${BLUE}📄 生成 PDF 电子书...${NC}"
    
    INPUT_FILE="$TEMP_DIR/complete_manual.md"
    OUTPUT_PDF="Firecrawl学习手册_v2.0_$(date +%Y%m%d).pdf"
    
    # Pandoc 参数
    pandoc "$INPUT_FILE" \
        -o "$OUTPUT_PDF" \
        --pdf-engine=xelatex \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --highlight-style=tango \
        -V documentclass=book \
        -V papersize=a4 \
        -V geometry:"top=2cm, bottom=2cm, left=2.5cm, right=2.5cm" \
        -V mainfont="PingFang SC" \
        -V monofont="Menlo" \
        -V fontsize=11pt \
        -V linestretch=1.5 \
        -V colorlinks=true \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -V toccolor=black \
        --metadata title="Firecrawl 完整学习手册" \
        --metadata author="HawaiiHub AI Team" \
        --metadata date="$(date +%Y年%m月%d日)" \
        --metadata keywords="Firecrawl,网页爬虫,数据采集,Python,AI,LLM" \
        --metadata lang="zh-CN" \
        2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PDF 生成成功！${NC}"
        echo -e "${GREEN}   文件: $OUTPUT_PDF${NC}"
        echo -e "${GREEN}   大小: $(du -h "$OUTPUT_PDF" | cut -f1)${NC}"
        echo ""
    else
        echo -e "${RED}❌ PDF 生成失败${NC}"
        echo -e "${YELLOW}请检查错误信息${NC}"
        exit 1
    fi
}

# 清理临时文件
cleanup() {
    echo -e "${BLUE}🧹 清理临时文件...${NC}"
    rm -rf "$TEMP_DIR"
    echo -e "${GREEN}✅ 清理完成${NC}"
    echo ""
}

# 打开 PDF
open_pdf() {
    echo -e "${BLUE}📖 打开 PDF...${NC}"
    OUTPUT_PDF="Firecrawl学习手册_v2.0_$(date +%Y%m%d).pdf"
    open "$OUTPUT_PDF"
    echo ""
}

# 显示统计信息
show_stats() {
    echo -e "${BLUE}📊 手册统计信息${NC}"
    echo "=================================================="
    
    # 统计文件数量
    echo -e "${YELLOW}文件统计:${NC}"
    echo "  Markdown 文件: $(find . -name "*.md" -type f | wc -l | tr -d ' ')"
    echo "  示例项目: 96 个"
    echo "  HawaiiHub 案例: 15 个"
    echo ""
    
    # 统计字数
    echo -e "${YELLOW}内容统计:${NC}"
    TOTAL_WORDS=$(find . -name "*.md" -type f -exec wc -w {} + | tail -1 | awk '{print $1}')
    echo "  总字数: $TOTAL_WORDS 字"
    echo "  预计阅读: $((TOTAL_WORDS / 300)) 分钟"
    echo ""
    
    # PDF 信息
    OUTPUT_PDF="Firecrawl学习手册_v2.0_$(date +%Y%m%d).pdf"
    if [ -f "$OUTPUT_PDF" ]; then
        echo -e "${YELLOW}PDF 信息:${NC}"
        echo "  文件名: $OUTPUT_PDF"
        echo "  大小: $(du -h "$OUTPUT_PDF" | cut -f1)"
        echo "  创建时间: $(date +"%Y-%m-%d %H:%M:%S")"
    fi
    
    echo ""
}

# 主流程
main() {
    echo ""
    echo "🔥 Firecrawl 学习手册 PDF 生成器 v2.0"
    echo "=================================================="
    echo ""
    
    # 1. 检查依赖
    check_dependencies
    
    # 2. 创建临时目录
    create_temp_dir
    
    # 3. 合并 Markdown
    merge_markdown
    
    # 4. 生成 PDF
    generate_pdf
    
    # 5. 清理临时文件
    cleanup
    
    # 6. 显示统计
    show_stats
    
    # 7. 打开 PDF
    echo -e "${GREEN}🎉 PDF 电子书生成完成！${NC}"
    echo ""
    echo -e "${BLUE}是否现在打开 PDF？(y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        open_pdf
    fi
    
    echo ""
    echo -e "${GREEN}✅ 全部完成！${NC}"
    echo ""
}

# 执行主流程
main
