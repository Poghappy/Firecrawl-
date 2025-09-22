# 📚 API文档

## 概述

Firecrawl数据采集器提供RESTful API接口，支持网页内容采集、数据处理和监控功能。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API版本**: v1
- **认证方式**: API Key (通过Header传递)
- **数据格式**: JSON

## 认证

所有API请求都需要在Header中包含API密钥：

```http
Authorization: Bearer your_api_key_here
```

或者通过查询参数：

```http
GET /api/v1/status?api_key=your_api_key_here
```

## 端点列表

### 1. 系统状态

#### 健康检查
```http
GET /health
```

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2024-09-21T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600
}
```

#### API状态
```http
GET /api/v1/status
```

**响应示例**:
```json
{
  "api_version": "1.0.0",
  "firecrawl_status": "connected",
  "database_status": "connected",
  "redis_status": "connected",
  "active_jobs": 5,
  "total_requests": 1250
}
```

### 2. 网页采集

#### 单页面采集
```http
POST /api/v1/crawl/url
Content-Type: application/json

{
  "url": "https://example.com",
  "options": {
    "formats": ["markdown", "html"],
    "onlyMainContent": true,
    "includeTags": ["h1", "h2", "p"],
    "excludeTags": ["script", "style"]
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "job_id": "job_123456",
  "data": {
    "url": "https://example.com",
    "title": "Example Page",
    "content": "# Example Page\n\nThis is example content...",
    "metadata": {
      "description": "Example page description",
      "keywords": ["example", "test"],
      "author": "Example Author"
    },
    "timestamp": "2024-09-21T10:30:00Z"
  }
}
```

#### 批量URL采集
```http
POST /api/v1/crawl/batch
Content-Type: application/json

{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
  ],
  "options": {
    "formats": ["markdown"],
    "onlyMainContent": true
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "job_id": "batch_job_789012",
  "total_urls": 3,
  "results": [
    {
      "url": "https://example.com/page1",
      "status": "success",
      "data": { /* 采集数据 */ }
    },
    {
      "url": "https://example.com/page2",
      "status": "success",
      "data": { /* 采集数据 */ }
    },
    {
      "url": "https://example.com/page3",
      "status": "error",
      "error": "Connection timeout"
    }
  ]
}
```

#### 网站爬取
```http
POST /api/v1/crawl/site
Content-Type: application/json

{
  "url": "https://example.com",
  "options": {
    "maxPages": 10,
    "includeSubdomains": false,
    "allowExternalLinks": false,
    "formats": ["markdown"]
  }
}
```

### 3. 任务管理

#### 获取任务状态
```http
GET /api/v1/jobs/{job_id}
```

**响应示例**:
```json
{
  "job_id": "job_123456",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-09-21T10:30:00Z",
  "completed_at": "2024-09-21T10:32:00Z",
  "result": {
    "success": true,
    "data": { /* 采集结果 */ }
  }
}
```

#### 获取任务列表
```http
GET /api/v1/jobs?status=completed&limit=10&offset=0
```

**查询参数**:
- `status`: 任务状态 (pending, running, completed, failed)
- `limit`: 返回数量限制 (默认: 20)
- `offset`: 偏移量 (默认: 0)

#### 取消任务
```http
DELETE /api/v1/jobs/{job_id}
```

### 4. 数据管理

#### 获取采集历史
```http
GET /api/v1/data/history?url=https://example.com&limit=10
```

#### 搜索采集数据
```http
GET /api/v1/data/search?query=keyword&format=markdown
```

**查询参数**:
- `query`: 搜索关键词
- `format`: 数据格式 (markdown, html, text)
- `date_from`: 开始日期 (ISO格式)
- `date_to`: 结束日期 (ISO格式)

#### 删除数据
```http
DELETE /api/v1/data/{data_id}
```

### 5. 监控配置

#### 创建监控任务
```http
POST /api/v1/monitor/create
Content-Type: application/json

{
  "url": "https://example.com",
  "name": "Example Monitor",
  "schedule": "0 */6 * * *",
  "options": {
    "formats": ["markdown"],
    "onlyMainContent": true
  },
  "notifications": {
    "email": "user@example.com",
    "webhook": "https://hooks.slack.com/..."
  }
}
```

#### 获取监控列表
```http
GET /api/v1/monitor/list
```

#### 更新监控任务
```http
PUT /api/v1/monitor/{monitor_id}
Content-Type: application/json

{
  "name": "Updated Monitor Name",
  "schedule": "0 */12 * * *",
  "enabled": true
}
```

#### 删除监控任务
```http
DELETE /api/v1/monitor/{monitor_id}
```

## 错误处理

### 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "INVALID_URL",
    "message": "The provided URL is invalid",
    "details": {
      "url": "invalid-url",
      "field": "url"
    }
  },
  "timestamp": "2024-09-21T10:30:00Z"
}
```

### 常见错误代码

| 错误代码          | HTTP状态码 | 描述              |
| ----------------- | ---------- | ----------------- |
| `INVALID_URL`     | 400        | URL格式无效       |
| `UNAUTHORIZED`    | 401        | 认证失败          |
| `FORBIDDEN`       | 403        | 权限不足          |
| `NOT_FOUND`       | 404        | 资源不存在        |
| `RATE_LIMITED`    | 429        | 请求频率超限      |
| `SERVER_ERROR`    | 500        | 服务器内部错误    |
| `FIRECRAWL_ERROR` | 502        | Firecrawl服务错误 |

## 使用示例

### Python示例

```python
import requests
import json

# 配置
API_BASE = "http://localhost:8000"
API_KEY = "your_api_key_here"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 单页面采集
def crawl_url(url):
    response = requests.post(
        f"{API_BASE}/api/v1/crawl/url",
        headers=headers,
        json={
            "url": url,
            "options": {
                "formats": ["markdown"],
                "onlyMainContent": True
            }
        }
    )
    return response.json()

# 批量采集
def crawl_batch(urls):
    response = requests.post(
        f"{API_BASE}/api/v1/crawl/batch",
        headers=headers,
        json={
            "urls": urls,
            "options": {
                "formats": ["markdown"]
            }
        }
    )
    return response.json()

# 获取任务状态
def get_job_status(job_id):
    response = requests.get(
        f"{API_BASE}/api/v1/jobs/{job_id}",
        headers=headers
    )
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 采集单个页面
    result = crawl_url("https://example.com")
    print(f"Job ID: {result['job_id']}")
    
    # 检查任务状态
    status = get_job_status(result['job_id'])
    print(f"Status: {status['status']}")
```

### JavaScript示例

```javascript
const API_BASE = 'http://localhost:8000';
const API_KEY = 'your_api_key_here';

const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
};

// 单页面采集
async function crawlUrl(url) {
    const response = await fetch(`${API_BASE}/api/v1/crawl/url`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            url: url,
            options: {
                formats: ['markdown'],
                onlyMainContent: true
            }
        })
    });
    return await response.json();
}

// 批量采集
async function crawlBatch(urls) {
    const response = await fetch(`${API_BASE}/api/v1/crawl/batch`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            urls: urls,
            options: {
                formats: ['markdown']
            }
        })
    });
    return await response.json();
}

// 使用示例
(async () => {
    try {
        const result = await crawlUrl('https://example.com');
        console.log('Job ID:', result.job_id);
        
        // 轮询任务状态
        const checkStatus = async (jobId) => {
            const status = await fetch(`${API_BASE}/api/v1/jobs/${jobId}`, {
                headers: headers
            });
            return await status.json();
        };
        
        let jobStatus = await checkStatus(result.job_id);
        while (jobStatus.status === 'running') {
            await new Promise(resolve => setTimeout(resolve, 1000));
            jobStatus = await checkStatus(result.job_id);
        }
        
        console.log('Final status:', jobStatus.status);
    } catch (error) {
        console.error('Error:', error);
    }
})();
```

### cURL示例

```bash
# 健康检查
curl -X GET http://localhost:8000/health

# 单页面采集
curl -X POST http://localhost:8000/api/v1/crawl/url \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "formats": ["markdown"],
      "onlyMainContent": true
    }
  }'

# 获取任务状态
curl -X GET http://localhost:8000/api/v1/jobs/job_123456 \
  -H "Authorization: Bearer your_api_key_here"

# 批量采集
curl -X POST http://localhost:8000/api/v1/crawl/batch \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com/page1",
      "https://example.com/page2"
    ],
    "options": {
      "formats": ["markdown"]
    }
  }'
```

## 速率限制

- **免费用户**: 100请求/小时
- **付费用户**: 1000请求/小时
- **企业用户**: 无限制

超出限制时返回429状态码。

## 更新日志

### v1.0.0 (2024-09-21)
- 初始API版本
- 支持单页面和批量采集
- 基础任务管理功能
- 监控配置支持

---

**注意**: 本文档会随着API的更新而持续维护。如有疑问，请查看 [GitHub Issues](https://github.com/Poghappy/Firecrawl-/issues) 或提交新的问题。
