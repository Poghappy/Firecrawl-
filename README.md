# 🔥 Firecrawl 数据采集器

[![CI/CD](https://github.com/Poghappy/Firecrawl-/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Poghappy/Firecrawl-/actions)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

基于 [Firecrawl API](https://firecrawl.dev/) 构建的智能数据采集系统，提供高效、智能的网页内容监控和数据采集服务。

## ✨ 核心特性

### 🎯 智能监控

- **实时变化检测** - 基于内容哈希的高效变化检测
- **AI 内容过滤** - 集成 OpenAI GPT 模型进行内容重要性分析
- **多源监控** - 支持单页面和网站爬取两种模式
- **定时任务** - 灵活的调度系统，支持 cron 表达式

### 📊 监控面板

- **Web Dashboard** - 实时监控面板，支持用户认证
- **状态监控** - 系统运行状态、变化统计、源状态监控
- **变化历史** - 详细的变化记录和分析结果
- **响应式设计** - 支持桌面和移动设备访问

### 🔔 通知系统

- **多渠道通知** - 邮件、Webhook、Dashboard 多种通知方式
- **智能过滤** - 基于 AI 分析结果的通知优先级
- **模板化邮件** - 美观的 HTML 邮件模板
- **批量通知** - 支持即时和批量通知模式

## 📋 项目结构

### 核心源码 (`src/`)

- **firecrawl_collector.py** - Firecrawl 采集器主程序
- **firecrawl_config.py** - 配置管理模块
- **data_processor.py** - 数据处理模块
- **task_scheduler.py** - 任务调度模块
- **api_server.py** - FastAPI 服务器

### 配置文件 (`config/`)

- **deployment/** - Docker 和部署配置
- **nginx/** - Nginx 配置
- **prometheus/** - Prometheus 监控配置
- **grafana/** - Grafana 仪表板配置

### 测试文件 (`tests/`)

详见 [tests/INDEX.md](./tests/INDEX.md)

### 文档 (`docs/`)

详见 [docs/INDEX.md](./docs/INDEX.md)

### 提示词 (`prompts/`)

详见 [prompts/INDEX.md](./prompts/INDEX.md)

## 🎯 功能特性

### 数据采集

- 支持多种网站内容采集
- 智能内容提取和清洗
- 批量 URL 处理能力
- 异步采集提升效率

### 配置管理

- 灵活的配置文件系统
- 多环境配置支持
- 动态配置更新
- 配置验证机制

### 任务调度

- 定时任务执行
- 任务队列管理
- 失败重试机制
- 任务状态监控

### 数据处理

- 内容格式化处理
- 数据质量检查
- 重复内容过滤
- 多格式输出支持

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 配置Firecrawl API密钥
cp config_example.json config.json
# 编辑config.json，填入API密钥
```

### 2. 基本使用

```python
# 导入采集器
from firecrawl_collector import FirecrawlCollector

# 初始化采集器
collector = FirecrawlCollector()

# 执行采集
result = collector.crawl_url('https://example.com')
```

### 3. 运行测试

```bash
# 执行集成测试
python integration_test.py
```

## 📚 文档导航

- **完整文档索引**: [docs/INDEX.md](./docs/INDEX.md)
- **API 文档**: [docs/API.md](./docs/API.md)
- **测试文档**: [tests/INDEX.md](./tests/INDEX.md)
- **项目状态**: [project_status.md](./project_status.md)
- **变更日志**: [CHANGELOG.md](./CHANGELOG.md)

## 🔗 相关链接

- **GitHub 仓库**: [Poghappy/Firecrawl-](https://github.com/Poghappy/Firecrawl-)
- **Firecrawl 官方文档**: [docs/official-docs/](./docs/official-docs/)
- **在线文档**: [Firecrawl.dev](https://firecrawl.dev/)
- **问题反馈**: [GitHub Issues](https://github.com/Poghappy/Firecrawl-/issues)

## 📖 开发指南

### 扩展采集器

1. 继承`FirecrawlCollector`基类
2. 重写特定的采集方法
3. 添加自定义数据处理逻辑
4. 更新配置文件支持新功能

### 自定义数据处理

1. 修改`data_processor.py`
2. 添加新的处理函数
3. 更新处理流程配置
4. 编写相应的测试用例

### 集成到火鸟系统

1. 参考 API 集成模块
2. 实现火鸟系统接口
3. 配置数据同步机制
4. 测试集成功能

## 🔄 更新记录

- 2024-01-XX 创建目录说明文档
- 2024-01-XX 完善功能特性说明
- 2024-01-XX 添加快速开始指南
