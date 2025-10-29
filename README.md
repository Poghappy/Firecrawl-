# 🔥 Firecrawl 数据采集器

**版本**: v2.2.0
**状态**: ✅ 生产就绪
**项目大小**: 573M（已优化 ⬇️ 38%）

---

## 📊 项目概览

基于 Python 3.9+、FastAPI、Firecrawl API 的智能数据采集系统，支持多业务场景。

**技术栈**: Python + AsyncFirecrawl + PostgreSQL + Redis + Docker
**架构模式**: 智能体架构（BaseAgent + 业务专用 Agent）
**核心代码**: 364K（精简高效）

---

## ✨ 核心特性

- 🌐 **多场景支持**: 新闻、招聘、电商、学习等 8+ 业务场景
- 🚀 **高性能**: 异步采集 + 并发控制 + 智能缓存
- 🎯 **智能体架构**: BaseAgent + AgentRegistry + AgentManager
- 📊 **完整监控**: Prometheus 指标 + 详细日志
- 🔧 **配置化**: YAML 配置 + 环境变量管理
- 🛡️ **安全可靠**: API Key 管理 + 错误重试 + 数据备份

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Firecrawl数据采集器

# 重建虚拟环境
bash scripts/setup_venv.sh

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 Firecrawl API Key
```

### 2. 运行示例

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行 honolulu_rentals 示例
cd honolulu_rentals
python main.py
```

### 3. API 服务器

```bash
# 启动 API 服务器
python src/api_server.py

# 访问文档
# http://localhost:8000/docs
```

---

## 📁 项目结构

```
573M 项目总大小
├── src/ (364K)              # 核心代码
│   ├── core/                # 核心模块
│   ├── models/              # 数据模型
│   └── *.py                 # 主要功能
│
├── honolulu_rentals/ (156K) # 业务示例
│   ├── scrapers/            # 采集器
│   ├── exporters/           # 导出器
│   └── config.py            # 配置
│
├── docs/ (45M)              # 文档
│   ├── official-docs/       # Firecrawl 官方文档
│   ├── reports/             # 项目报告
│   └── maintenance/         # 维护文档
│
├── backups/ (174M)          # 备份和归档
├── config/                  # 配置文件
├── scripts/                 # 自动化脚本
└── tests/                   # 测试文件
```

---

## 🎯 支持的业务场景

1. **火鸟门户新闻资讯** - Search API + JSON Mode
2. **省钱团购网** - Crawl + Actions + 价格监控
3. **Aloha 招聘网** - Batch Scrape + 结构化提取
4. **学习网** - Map + Crawl + 资源聚合
5. **广告公司** - Search + 竞品分析
6. **设计公司** - Lead Enrichment
7. **科技公司** - Deep Research
8. **房地产** - Crawl + 复杂交互

---

## 🛠️ 维护工具

### 定期维护

```bash
# 清理缓存（推荐每周执行）
bash scripts/slimming/cleanup_cache.sh

# 重建虚拟环境（需要时）
bash scripts/setup_venv.sh
```

### 恢复功能

```bash
# 恢复归档（如需要）
cd backups/archives
tar -xzf 归档-20250129.tar.gz -C ../../
```

---

## 📚 文档索引

### 快速开始

- **快速总览**: `瘦身成功_快速总览.md`
- **项目状态**: `project_status.md`
- **配置指南**: `docs/README.md`

### 开发文档

- **API 参考**: `docs/API_REFERENCE.md`
- **架构设计**: `docs/ARCHITECTURE.md`
- **开发指南**: `docs/DEVELOPMENT.md`

### 维护文档

- **清理指南**: `docs/maintenance/CLEANUP_COMPLETE_GUIDE.md`
- **瘦身计划**: `SLIMMING_PLAN.md`
- **最终报告**: `项目瘦身最终报告.md`

---

## 🎉 v2.2.0 更新（2025-01-29）

### 项目瘦身

- ✅ 项目大小: 931M → 573M（节省 38%）
- ✅ 清理 536 个 Python 缓存
- ✅ 压缩归档目录（177M → 120M）
- ✅ 删除虚拟环境（可重建）
- ✅ 整合清理文档（4 个 → 1 个）

### 工具改进

- ✅ 4 个自动化脚本
- ✅ 7 个详细报告
- ✅ 完整的文档系统

### 功能保证

- ✅ 所有功能 100% 保留
- ✅ 归档可恢复
- ✅ 虚拟环境可重建

---

## 🔧 技术配置

### 环境变量

```bash
# .env 文件
FIRECRAWL_API_KEY=fc-YOUR-API-KEY
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
```

### 依赖管理

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装最小依赖
pip install -r requirements-minimal.txt

# 安装完整依赖
pip install -r requirements.txt
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_api_server.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

---

## 📊 监控

- **Prometheus**: <http://localhost:8000/metrics>
- **日志**: `logs/app.log`
- **健康检查**: <http://localhost:8000/health>

---

## 🤝 贡献

欢迎贡献！请遵循：

1. Fork 项目
2. 创建功能分支
3. 提交 PR
4. 等待审核

---

## 📜 许可证

[MIT License](LICENSE)

---

## 📞 支持

- **文档**: `docs/`
- **报告**: `docs/reports/`
- **工具**: `scripts/`

---

**最后更新**: 2025-01-29
**维护者**: AI Team
**状态**: ✅ 生产就绪
