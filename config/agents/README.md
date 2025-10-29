# 智能体配置文件说明

本目录包含各业务场景智能体的配置文件。

## 📋 配置文件列表

| 配置文件                 | 智能体类型  | 业务场景     | 主要端点     | 说明         |
| ------------------------ | ----------- | ------------ | ------------ | ------------ |
| `news_agent.yaml`        | news        | 火鸟门户新闻 | Search       | 新闻资讯采集 |
| `ecommerce_agent.yaml`   | ecommerce   | 省钱团购网   | Crawl        | 电商价格监控 |
| `recruitment_agent.yaml` | recruitment | Aloha 招聘网 | Batch Scrape | 招聘信息采集 |
| `rental_agent.yaml`      | rental      | 房地产租赁   | Crawl        | 租房信息采集 |
| `learning_agent.yaml`    | learning    | 学习网       | Map + Batch  | 学习资源聚合 |

## 🔧 配置结构

每个配置文件包含以下部分：

### 1. 智能体基础配置

```yaml
agent:
  name: "智能体名称"
  type: "智能体类型"
  description: "描述"
  enabled: true
```

### 2. API 配置

```yaml
api:
  endpoint: "主要使用的端点"
  timeout: 超时时间（秒）
  max_retries: 最大重试次数
  retry_delay: 重试延迟（秒）
```

### 3. Firecrawl 参数

```yaml
firecrawl:
  max_age: 缓存时间（毫秒）
  proxy: "代理模式（basic/stealth）"
  formats: 输出格式列表
  actions: 页面交互操作（可选）
```

### 4. 数据源配置

```yaml
sources:
  - name: "数据源名称"
    url: "数据源URL"
    category: "分类"
    priority: 优先级（1-10）
    enabled: true
```

### 5. 并发控制

```yaml
concurrency:
  max_concurrent: 最大并发数
  batch_size: 批处理大小
  queue_size: 队列大小
```

### 6. 调度配置

```yaml
schedule:
  enabled: true
  cron: "cron表达式"
  timezone: "时区"
```

### 7. 成本控制

```yaml
cost:
  daily_budget: 每日预算（credits）
  alert_threshold: 预警阈值
```

## 🚀 使用方法

### 1. Python 代码加载配置

```python
from src.core import get_agent, AgentConfig
import yaml

# 加载配置文件
with open("config/agents/news_agent.yaml") as f:
    config_data = yaml.safe_load(f)

# 创建智能体配置
config = AgentConfig(
    name=config_data['agent']['name'],
    type=config_data['agent']['type'],
    api_key=os.getenv("FIRECRAWL_API_KEY"),
    **config_data.get('concurrency', {})
)

# 获取智能体实例
agent = get_agent(config_data['agent']['type'], config)
```

### 2. 命令行工具（待开发）

```bash
# 运行特定智能体
python -m src.agents.cli run news

# 列出所有智能体
python -m src.agents.cli list

# 测试配置文件
python -m src.agents.cli test news_agent.yaml
```

## 📝 配置最佳实践

### 1. 缓存策略

| 场景           | maxAge 设置      | 说明             |
| -------------- | ---------------- | ---------------- |
| 实时监控       | 0                | 强制刷新，无缓存 |
| 准实时（新闻） | 600000 (10 分钟) | 快速更新         |
| 定时更新       | 3600000 (1 小时) | 平衡成本和实时性 |
| 静态内容       | 172800000 (2 天) | 最大化节省成本   |

### 2. 代理选择

| 代理模式 | 成本       | 速度 | 成功率 | 适用场景                   |
| -------- | ---------- | ---- | ------ | -------------------------- |
| basic    | 无额外成本 | 快   | 90%+   | 大部分网站                 |
| stealth  | +4 credits | 较慢 | 98%+   | 电商、社交媒体等强反爬网站 |

### 3. 并发控制

| 场景     | max_concurrent | 说明             |
| -------- | -------------- | ---------------- |
| 友好网站 | 10-20          | 可以较高并发     |
| 严格限制 | 3-5            | 降低并发避免封禁 |
| 测试环境 | 1-2            | 便于调试         |

### 4. 成本估算

| 智能体 | 每日预算（credits） | 说明               |
| ------ | ------------------- | ------------------ |
| 新闻   | 1000                | 高频采集，使用缓存 |
| 电商   | 2000                | 实时价格 + stealth |
| 招聘   | 1500                | 批量处理           |
| 租房   | 1200                | 中频采集           |
| 学习   | 800                 | 低频采集（每周）   |

## ⚠️ 注意事项

1. **不要提交包含真实 API 密钥的配置文件**
2. **修改配置后需要重启智能体服务**
3. **测试新配置前先备份原配置**
4. **监控成本使用，避免超出预算**
5. **遵守目标网站的 robots.txt 和 ToS**

## 🔗 相关文档

- [智能体开发指南](../../docs/guides/agent-development.md)
- [Firecrawl API 参考](../../docs/official-docs/API.md)
- [数据模型定义](../../src/models/README.md)
- [部署配置指南](../../docs/deployment/README.md)
