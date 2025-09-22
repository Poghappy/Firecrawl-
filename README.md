# 🔥 Firecrawl数据采集器

[![CI/CD](https://github.com/Poghappy/Firecrawl-/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Poghappy/Firecrawl-/actions)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

基于 [Firecrawl API](https://firecrawl.dev/) 构建的智能数据采集系统，专为火鸟门户系统设计，提供高效、智能的网页内容监控和数据采集服务。

## ✨ 核心特性

### 🎯 智能监控
- **实时变化检测** - 基于内容哈希的高效变化检测
- **AI内容过滤** - 集成OpenAI GPT模型进行内容重要性分析
- **多源监控** - 支持单页面和网站爬取两种模式
- **定时任务** - 灵活的调度系统，支持cron表达式

### 📊 监控面板
- **Web Dashboard** - 实时监控面板，支持用户认证
- **状态监控** - 系统运行状态、变化统计、源状态监控
- **变化历史** - 详细的变化记录和分析结果
- **响应式设计** - 支持桌面和移动设备访问

### 🔔 通知系统
- **多渠道通知** - 邮件、Webhook、Dashboard多种通知方式
- **智能过滤** - 基于AI分析结果的通知优先级
- **模板化邮件** - 美观的HTML邮件模板
- **批量通知** - 支持即时和批量通知模式

### 🔗 火鸟门户集成
- **API集成** - 直接推送到火鸟门户系统
- **自动分类** - 基于AI分析的智能内容分类
- **关键词提取** - 自动提取和标记内容关键词
- **发布控制** - 支持自动发布和人工审核模式

## 📋 文件清单

### 核心源码
- **firecrawl_collector.py** - Firecrawl采集器主程序
- **firecrawl_config.py** - 配置管理模块
- **data_processor.py** - 数据处理模块
- **api_integration.py** - API集成模块
- **task_scheduler.py** - 任务调度模块

### 配置文件
- **config_example.json** - 配置文件示例

### 测试文件
- **integration_test.py** - 集成测试脚本

### 文档
- **Firecrawl SDK爬虫脚本.md** - Firecrawl SDK使用说明和爬虫脚本文档

## 🎯 功能特性

### 数据采集
- 支持多种网站内容采集
- 智能内容提取和清洗
- 批量URL处理能力
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

## 🔗 相关链接

- **GitHub仓库**: [Poghappy/Firecrawl-](https://github.com/Poghappy/Firecrawl-)
- **Firecrawl官方文档**: [Firecrawl.dev](https://firecrawl.dev/)
- **API文档**: [Firecrawl API Reference](https://docs.firecrawl.dev/)
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
1. 参考API集成模块
2. 实现火鸟系统接口
3. 配置数据同步机制
4. 测试集成功能

## 🔄 更新记录

- 2024-01-XX 创建目录说明文档
- 2024-01-XX 完善功能特性说明
- 2024-01-XX 添加快速开始指南