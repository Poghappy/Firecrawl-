# 火鸟门户API集成配置说明

## 📋 概述

本文档详细说明如何配置Firecrawl数据采集器与火鸟门户系统的API集成参数，实现数据的自动采集和发布。

## 🔧 配置文件位置

- **主配置文件**: `config.json`
- **示例配置文件**: `config_example.json`

## 🚀 核心配置参数

### 1. Firecrawl API配置

```json
{
  "firecrawl": {
    "api_key": "fc-your_firecrawl_api_key_here",
    "base_url": "https://api.firecrawl.dev",
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 1.0
  }
}
```

**参数说明**:
- `api_key`: Firecrawl API密钥，需要从 https://firecrawl.dev 获取
- `base_url`: Firecrawl API基础URL，通常为官方地址
- `timeout`: 请求超时时间（秒）
- `max_retries`: 最大重试次数
- `retry_delay`: 重试延迟时间（秒）

### 2. 火鸟门户API集成配置

```json
{
  "api_integration": {
    "base_url": "https://hawaiihub.net/api/",
    "api_key": "your_huoniao_api_key_here",
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 2.0,
    "default_category_id": 1,
    "default_author_id": 1,
    "auto_publish": false,
    "rate_limit": {
      "requests_per_minute": 60,
      "requests_per_hour": 1000
    }
  }
}
```

**参数说明**:
- `base_url`: 火鸟门户API基础URL
- `api_key`: 火鸟门户API密钥
- `timeout`: API请求超时时间
- `max_retries`: 最大重试次数
- `retry_delay`: 重试延迟时间
- `default_category_id`: 默认文章分类ID
- `default_author_id`: 默认作者ID
- `auto_publish`: 是否自动发布文章
- `rate_limit`: API调用频率限制

## 🔑 API密钥获取方法

### Firecrawl API密钥

1. 访问 https://firecrawl.dev
2. 注册账户并登录
3. 进入Dashboard
4. 在API Keys页面生成新的API密钥
5. 复制密钥并配置到 `config.json` 中

### 火鸟门户API密钥

根据火鸟门户系统的API文档，API调用方式为：

```
/api/index.php?service={模块名}&method={方法名}&param={参数}
```

**配置步骤**:

1. **确认API接口地址**
   - 生产环境: `https://hawaiihub.net/api/`
   - 测试环境: 根据实际部署地址配置

2. **获取API访问权限**
   - 联系火鸟门户系统管理员
   - 申请API访问权限和密钥
   - 确认可访问的模块和方法

3. **配置认证参数**
   - 根据系统要求配置API密钥
   - 设置合适的超时和重试参数

## 📊 模块映射配置

### 新闻模块 (Article)

```json
{
  "module_mapping": {
    "article": {
      "service": "article",
      "methods": {
        "create": "add",
        "update": "edit",
        "delete": "del",
        "list": "getList"
      },
      "required_fields": ["title", "content", "category_id"],
      "optional_fields": ["author_id", "tags", "summary"]
    }
  }
}
```

### 信息模块 (Info)

```json
{
  "module_mapping": {
    "info": {
      "service": "info",
      "methods": {
        "create": "add",
        "update": "edit",
        "delete": "del",
        "list": "getList"
      },
      "required_fields": ["title", "content", "info_type"],
      "optional_fields": ["contact", "phone", "address"]
    }
  }
}
```

## 🔄 数据处理配置

### 内容处理选项

```json
{
  "processing": {
    "enable_content_cleaning": true,
    "enable_keyword_extraction": true,
    "enable_auto_categorization": true,
    "enable_summary_generation": true,
    "min_content_length": 100,
    "max_content_length": 50000,
    "quality_threshold": 0.6,
    "language_detection": true,
    "duplicate_detection": true
  }
}
```

### 任务调度配置

```json
{
  "task_scheduler": {
    "max_concurrent_tasks": 5,
    "task_timeout": 300,
    "cleanup_interval": 3600,
    "max_task_history": 1000,
    "enable_persistence": true,
    "storage_backend": "file"
  }
}
```

## 🛡️ 安全配置

### SSL和代理设置

```json
{
  "security": {
    "enable_ssl_verification": true,
    "user_agent": "FirecrawlCollector/1.0",
    "request_headers": {
      "Accept": "application/json",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    },
    "proxy_config": {
      "enable_proxy": false,
      "http_proxy": null,
      "https_proxy": null,
      "no_proxy": ["localhost", "127.0.0.1"]
    }
  }
}
```

## 📝 配置验证

### 1. 配置文件语法检查

```bash
# 在虚拟环境中运行
source firecrawl_env/bin/activate
python -c "import json; json.load(open('config.json'))"
```

### 2. API连接测试

```bash
# 测试Firecrawl API连接
python -c "from firecrawl import FirecrawlApp; app = FirecrawlApp(api_key='your_key'); print('Firecrawl API连接成功')"

# 测试火鸟门户API连接
curl -X GET "https://hawaiihub.net/api/index.php?service=siteConfig&method=getConfig"
```

### 3. 运行集成测试

```bash
# 运行完整的集成测试
python integration_test.py
```

## 🚨 常见问题

### 1. API密钥无效
- 检查密钥格式是否正确
- 确认密钥是否已激活
- 验证API访问权限

### 2. 连接超时
- 增加timeout值
- 检查网络连接
- 确认API服务状态

### 3. 频率限制
- 调整rate_limit配置
- 增加retry_delay时间
- 减少并发任务数

## 📞 技术支持

- **Firecrawl官方文档**: https://docs.firecrawl.dev
- **火鸟门户API文档**: 参考项目知识库
- **项目Issues**: 通过GitHub提交问题

---

*配置完成后，请运行集成测试确保所有参数配置正确。*