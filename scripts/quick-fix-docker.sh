#!/bin/bash
# 快速修复Docker构建问题

echo "🔧 快速修复Docker构建问题..."

# 1. 修复Docker标签问题
echo "📝 修复Docker标签格式..."
sed -i.bak 's/denzhile\/firecrawl/ghcr.io\/poghappy\/firecrawl/g' .github/workflows/ci-cd.yml

# 2. 创建简化的测试工作流
echo "📝 创建简化的测试工作流..."
cat > .github/workflows/test-simple.yml << 'EOF'
name: Simple Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-minimal.txt
    
    - name: Test basic functionality
      run: |
        python -c "import fastapi; print('FastAPI imported successfully')"
        python -c "import uvicorn; print('Uvicorn imported successfully')"
        echo "✅ Basic test passed"
    
    - name: Test API server
      run: |
        python -c "from src.api_server import app; print('API server imported successfully')"
        echo "✅ API server test passed"

  docker-test:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Build Docker image (test only)
      uses: docker/build-push-action@v6
      with:
        context: .
        file: ./Dockerfile
        push: false
        tags: test-firecrawl:latest
        platforms: linux/amd64
EOF

# 3. 提交更改
echo "💾 提交修复..."
git add .
git commit -m "fix: 修复Docker构建问题

- 修复Docker标签格式问题
- 使用有效的仓库名称格式
- 创建简化的测试工作流
- 使用最小化依赖减少构建时间

Resolves: Docker build tag format errors"

# 4. 推送到远程仓库
echo "🚀 推送到远程仓库..."
git push origin main

echo "✅ Docker构建问题修复完成！"
echo "📊 检查工作流状态: https://github.com/Poghappy/Firecrawl-/actions"
