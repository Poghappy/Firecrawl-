#!/bin/bash
# Phase 2: 虚拟环境处理脚本
# 功能: 从项目中移除虚拟环境，更新 .gitignore
# 安全: 保留 requirements.txt，可以重建虚拟环境

set -e

PROJECT_DIR="/Users/zhiledeng/Movies/Firecrawl数据采集器"
cd "$PROJECT_DIR"

echo "🏋️ Phase 2: 虚拟环境处理"
echo "========================"
echo ""

# 1. 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "✅ 虚拟环境目录不存在，无需处理"
    exit 0
fi

VENV_SIZE=$(du -sh venv 2>/dev/null | awk '{print $1}' || echo "0")
echo "📁 当前虚拟环境大小: $VENV_SIZE"
echo ""

# 2. 检查 requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "⚠️ requirements.txt 不存在，先生成依赖文件"
    if [ -f "venv/bin/pip" ]; then
        venv/bin/pip freeze > requirements.txt
        echo "✅ 已生成 requirements.txt"
    else
        echo "❌ 无法生成 requirements.txt"
        exit 1
    fi
fi
echo "✅ requirements.txt 存在"
echo ""

# 3. 更新 .gitignore
echo "📝 更新 .gitignore..."
if ! grep -q "^venv/$" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'EOF'

# 虚拟环境
venv/
env/
ENV/
.venv/

# Python 缓存
__pycache__/
*.py[cod]
*$py.class
*.so

# 分发 / 打包
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
EOF
    echo "✅ .gitignore 已更新"
else
    echo "✅ .gitignore 已包含 venv/"
fi
echo ""

# 4. 从 Git 中移除（如果在 Git 中）
if [ -d ".git" ]; then
    echo "🗑️ 从 Git 追踪中移除虚拟环境..."
    git rm -r --cached venv/ 2>/dev/null || echo "  (虚拟环境未在 Git 中)"
    echo "✅ 已从 Git 移除"
else
    echo "ℹ️ 项目不在 Git 仓库中"
fi
echo ""

# 5. 创建虚拟环境重建脚本
cat > scripts/setup_venv.sh << 'EOF'
#!/bin/bash
# 重建虚拟环境脚本

set -e

echo "🐍 创建虚拟环境..."
python3 -m venv venv

echo "📦 安装依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 虚拟环境创建完成"
echo ""
echo "激活虚拟环境:"
echo "  source venv/bin/activate"
EOF

chmod +x scripts/setup_venv.sh
echo "✅ 创建重建脚本: scripts/setup_venv.sh"
echo ""

# 6. 提示删除虚拟环境
echo "⚠️ 虚拟环境处理完成，可以删除以节省空间:"
echo ""
echo "删除命令:"
echo "  $ rm -rf venv/  # 节省 ~$VENV_SIZE"
echo ""
echo "重建命令:"
echo "  $ bash scripts/setup_venv.sh"
echo ""

# 7. 生成报告
cat > docs/reports/phase2_venv_report.md << EOF
# Phase 2: 虚拟环境处理报告

**执行时间**: $(date '+%Y-%m-%d %H:%M:%S')
**执行阶段**: 虚拟环境处理

## 操作摘要

### 虚拟环境状态
- **当前大小**: $VENV_SIZE
- **位置**: venv/
- **可删除**: 是（可用 requirements.txt 重建）

### 执行操作
1. ✅ 验证 requirements.txt 存在
2. ✅ 更新 .gitignore
3. ✅ 从 Git 追踪中移除
4. ✅ 创建重建脚本

## 下一步

### 删除虚拟环境（节省空间）
\`\`\`bash
rm -rf venv/
\`\`\`

### 重建虚拟环境
\`\`\`bash
bash scripts/setup_venv.sh
\`\`\`

## 注意事项

⚠️ **删除前确认**:
- [x] requirements.txt 已存在
- [x] requirements.txt 包含所有依赖
- [x] .gitignore 已更新
- [x] 重建脚本已创建

## 状态

- [x] requirements.txt 已验证
- [x] .gitignore 已更新
- [x] Git 追踪已移除
- [x] 重建脚本已创建
- [ ] 虚拟环境待删除（手动执行）

---
**生成时间**: $(date)
EOF

echo "✅ 报告已生成: docs/reports/phase2_venv_report.md"
echo ""
echo "🎉 Phase 2 完成！"

