# Firecrawl数据采集器 - 一键命令

.PHONY: help setup lint test format cov clean install dev build deploy

# 默认目标
help: ## 显示帮助信息
	@echo "Firecrawl数据采集器 - 可用命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 环境设置
setup: ## 安装依赖/初始化项目
	@echo "🚀 设置开发环境..."
	python3 -m venv firecrawl_env || true
	@echo "✅ 虚拟环境创建完成"
	@echo "请运行: source firecrawl_env/bin/activate"
	@echo "然后运行: make install"

install: ## 安装Python依赖
	@echo "📦 安装Python依赖..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

dev: ## 开发环境快速设置
	@echo "🔧 设置开发环境..."
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt || true
	pre-commit install || true
	@echo "✅ 开发环境设置完成"

# 代码质量
lint: ## 代码风格&静态检查
	@echo "🔍 运行代码检查..."
	ruff check . || true
	mypy src/ || true
	flake8 src/ || true
	@echo "✅ 代码检查完成"

format: ## 自动格式化代码
	@echo "🎨 格式化代码..."
	ruff format . || true
	black src/ tests/ || true
	isort src/ tests/ || true
	@echo "✅ 代码格式化完成"

# 测试
test: ## 运行所有测试
	@echo "🧪 运行测试..."
	pytest tests/ -v --tb=short
	@echo "✅ 测试完成"

test-unit: ## 运行单元测试
	@echo "🧪 运行单元测试..."
	pytest tests/unit/ -v
	@echo "✅ 单元测试完成"

test-integration: ## 运行集成测试
	@echo "🧪 运行集成测试..."
	pytest tests/integration/ -v
	@echo "✅ 集成测试完成"

test-e2e: ## 运行端到端测试
	@echo "🧪 运行端到端测试..."
	pytest tests/e2e/ -v
	@echo "✅ 端到端测试完成"

cov: ## 生成覆盖率报告
	@echo "📊 生成覆盖率报告..."
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "✅ 覆盖率报告生成完成"
	@echo "📁 详细报告: htmlcov/index.html"

# 文档
docs: ## 生成文档
	@echo "📚 生成文档..."
	pdoc --html src --output-dir docs/api
	@echo "✅ 文档生成完成"

docs-serve: ## 启动文档服务器
	@echo "🌐 启动文档服务器..."
	pdoc --http localhost:8080 src
	@echo "✅ 文档服务器启动: http://localhost:8080"

# 数据库
db-init: ## 初始化数据库
	@echo "🗄️ 初始化数据库..."
	python scripts/init-db.py
	@echo "✅ 数据库初始化完成"

db-migrate: ## 运行数据库迁移
	@echo "🔄 运行数据库迁移..."
	alembic upgrade head
	@echo "✅ 数据库迁移完成"

db-reset: ## 重置数据库
	@echo "🗑️ 重置数据库..."
	alembic downgrade base
	alembic upgrade head
	@echo "✅ 数据库重置完成"

# 应用
run: ## 启动开发服务器
	@echo "🚀 启动开发服务器..."
	python src/api_server.py
	@echo "✅ 开发服务器启动完成"

run-worker: ## 启动任务处理worker
	@echo "👷 启动任务处理worker..."
	python src/task_scheduler.py
	@echo "✅ 任务处理worker启动完成"

# 构建和部署
build: ## 构建Docker镜像
	@echo "🐳 构建Docker镜像..."
	docker build -t firecrawl-collector:latest .
	@echo "✅ Docker镜像构建完成"

build-prod: ## 构建生产环境镜像
	@echo "🐳 构建生产环境镜像..."
	docker build -f Dockerfile.production -t firecrawl-collector:prod .
	@echo "✅ 生产环境镜像构建完成"

deploy: ## 部署到生产环境
	@echo "🚀 部署到生产环境..."
	docker-compose -f docker-compose.production.yml up -d
	@echo "✅ 生产环境部署完成"

deploy-dev: ## 部署到开发环境
	@echo "🚀 部署到开发环境..."
	docker-compose up -d
	@echo "✅ 开发环境部署完成"

# 监控
logs: ## 查看应用日志
	@echo "📋 查看应用日志..."
	docker-compose logs -f

status: ## 查看服务状态
	@echo "📊 查看服务状态..."
	docker-compose ps

health: ## 健康检查
	@echo "🏥 健康检查..."
	curl -f http://localhost:8000/health || echo "❌ 服务不健康"

# 清理
clean: ## 清理临时文件
	@echo "🧹 清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	@echo "✅ 清理完成"

clean-docker: ## 清理Docker资源
	@echo "🧹 清理Docker资源..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Docker清理完成"

# 安全
security: ## 安全检查
	@echo "🔒 运行安全检查..."
	bandit -r src/ || true
	safety check || true
	@echo "✅ 安全检查完成"

# 性能
benchmark: ## 性能基准测试
	@echo "⚡ 运行性能基准测试..."
	pytest tests/benchmark/ -v
	@echo "✅ 性能基准测试完成"

# 配置验证
validate-config: ## 验证配置文件
	@echo "✅ 验证配置文件..."
	python scripts/validate_config.py
	@echo "✅ 配置验证完成"

# 数据备份
backup: ## 备份数据
	@echo "💾 备份数据..."
	python scripts/backup.py
	@echo "✅ 数据备份完成"

# 完整检查
check-all: lint test cov security ## 运行所有检查
	@echo "✅ 所有检查完成"

# 发布准备
release-prep: check-all build ## 发布准备
	@echo "🎉 发布准备完成"

# 快速开发循环
dev-loop: format lint test ## 开发循环（格式化->检查->测试）
	@echo "🔄 开发循环完成"

# 环境信息
info: ## 显示环境信息
	@echo "📋 环境信息:"
	@echo "Python版本: $$(python --version)"
	@echo "Pip版本: $$(pip --version)"
	@echo "当前目录: $$(pwd)"
	@echo "虚拟环境: $$(which python)"
	@echo "依赖数量: $$(pip list | wc -l)"

# Cursor AI Prompts 管理
verify-cursor-config: ## 验证 Cursor Prompts 配置
	@echo "🤖 验证 Cursor Prompts 配置..."
	@bash .cursor/scripts/verify-prompts.sh
	@echo "✅ Cursor配置验证完成"

check-roles: ## 检查角色文件完整性
	@echo "👥 检查角色文件..."
	@bash .cursor/scripts/check-roles.sh
	@echo "✅ 角色检查完成"

cursor-setup: ## 设置 Cursor Prompts 系统
	@echo "🚀 设置 Cursor Prompts 系统..."
	@chmod +x .cursor/scripts/*.sh
	@chmod +x .cursor/hooks/*
	@bash .cursor/scripts/verify-prompts.sh
	@echo "✅ Cursor Prompts 系统设置完成"
	@echo "请重启 Cursor 以加载新配置"

cursor-info: ## 显示 Cursor配置信息
	@echo "📋 Cursor AI 配置信息:"
	@echo "主规则文件: .cursorrules"
	@echo "Prompts目录: .cursor/prompts/"
	@echo "环境配置: .cursor/environment.json"
	@echo "可用角色: PO PM BA PjM Arch LLME DEV QA Ops TW"
	@echo "工作流阶段: 7个标准阶段"

# 帮助信息
help-setup: ## 显示设置帮助
	@echo "🔧 环境设置步骤:"
	@echo "1. make setup     # 创建虚拟环境"
	@echo "2. source firecrawl_env/bin/activate  # 激活虚拟环境"
	@echo "3. make install   # 安装依赖"
	@echo "4. make dev       # 设置开发环境"
	@echo "5. make cursor-setup  # 设置 Cursor AI"
	@echo "6. make run       # 启动服务"
