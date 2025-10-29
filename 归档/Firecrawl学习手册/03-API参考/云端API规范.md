# 🔥 Firecrawl 云 API 使用规范

> **专为 HawaiiHub 团队打造的 Firecrawl 云 API 最佳实践**
> **版本**: v1.0.0
> **更新**: 2025-10-27

---

## 📋 目录

1. [核心原则](#核心原则)
2. [API 密钥管理](#api-密钥管理)
3. [请求优化策略](#请求优化策略)
4. [成本控制](#成本控制)
5. [错误处理](#错误处理)
6. [性能优化](#性能优化)
7. [安全规范](#安全规范)
8. [监控与日志](#监控与日志)
9. [代码规范](#代码规范)
10. [应急预案](#应急预案)

---

## 🎯 核心原则

### 1. **最小化请求原则**
```python
# ✅ 好的做法 - 使用 batch_scrape
urls = [url1, url2, url3]
results = app.batch_scrape(urls, formats=['markdown'])

# ❌ 避免 - 循环调用
for url in urls:
    result = app.scrape(url)  # 浪费 API 配额
```

### 2. **缓存优先原则**
```python
# ✅ 使用 maxAge 参数启用缓存
result = app.scrape(
    url="https://example.com",
    formats=['markdown'],
    maxAge=3600000  # 1 小时缓存
)
```

### 3. **内容过滤原则**
```python
# ✅ 只提取需要的内容
result = app.scrape(
    url="https://example.com",
    formats=['markdown'],
    onlyMainContent=True,  # 过滤广告、导航栏等
    removeTags=['script', 'style', 'iframe']
)
```

---

## 🔑 API 密钥管理

### 环境变量配置

#### **开发环境** (`.env.development`)
```bash
# Firecrawl API 配置
FIRECRAWL_API_KEY=fc-dev-xxxxxxxxxxxxxxxx
FIRECRAWL_API_URL=https://api.firecrawl.dev
FIRECRAWL_TIMEOUT=30000
FIRECRAWL_MAX_RETRIES=3

# 功能开关
FIRECRAWL_ENABLE_CACHE=true
FIRECRAWL_CACHE_TTL=3600
FIRECRAWL_ENABLE_DEBUG=true
```

#### **生产环境** (`.env.production`)
```bash
# Firecrawl API 配置
FIRECRAWL_API_KEY=fc-prod-xxxxxxxxxxxxxxxx
FIRECRAWL_API_URL=https://api.firecrawl.dev
FIRECRAWL_TIMEOUT=60000
FIRECRAWL_MAX_RETRIES=5

# 功能开关
FIRECRAWL_ENABLE_CACHE=true
FIRECRAWL_CACHE_TTL=7200
FIRECRAWL_ENABLE_DEBUG=false

# 速率限制
FIRECRAWL_RATE_LIMIT=100  # 每分钟最大请求数
FIRECRAWL_BURST_LIMIT=20  # 突发流量限制
```

### 密钥轮换策略

```python
# config/firecrawl.py
import os
from datetime import datetime, timedelta

class FirecrawlConfig:
    """Firecrawl 配置管理"""

    # API 密钥（支持多密钥轮换）
    API_KEYS = [
        os.getenv('FIRECRAWL_API_KEY_1'),
        os.getenv('FIRECRAWL_API_KEY_2'),  # 备用密钥
        os.getenv('FIRECRAWL_API_KEY_3'),  # 备用密钥
    ]

    # 当前使用的密钥索引
    CURRENT_KEY_INDEX = 0

    # 密钥轮换时间（每 24 小时）
    KEY_ROTATION_INTERVAL = timedelta(hours=24)
    LAST_ROTATION = datetime.now()

    @classmethod
    def get_api_key(cls) -> str:
        """获取当前 API 密钥"""
        # 检查是否需要轮换
        if datetime.now() - cls.LAST_ROTATION > cls.KEY_ROTATION_INTERVAL:
            cls.rotate_key()

        return cls.API_KEYS[cls.CURRENT_KEY_INDEX]

    @classmethod
    def rotate_key(cls):
        """轮换到下一个密钥"""
        cls.CURRENT_KEY_INDEX = (cls.CURRENT_KEY_INDEX + 1) % len(cls.API_KEYS)
        cls.LAST_ROTATION = datetime.now()
        print(f"已轮换到密钥 #{cls.CURRENT_KEY_INDEX + 1}")
```

### 密钥安全规范

#### ✅ **必须遵守**
1. **绝不**将 API 密钥硬编码到代码中
2. **绝不**将 `.env` 文件提交到 Git
3. **必须**使用环境变量或密钥管理服务
4. **必须**定期轮换密钥（建议每月）
5. **必须**为不同环境使用不同密钥

#### ❌ **严禁行为**
```python
# ❌ 严禁硬编码
app = FirecrawlApp(api_key="fc-xxxxxxxxxxxxxxxx")

# ❌ 严禁打印密钥
print(f"API Key: {api_key}")

# ❌ 严禁在日志中记录密钥
logger.info(f"Using key: {api_key}")
```

#### ✅ **正确做法**
```python
# ✅ 使用环境变量
import os
from firecrawl import FirecrawlApp

api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    raise ValueError("未设置 FIRECRAWL_API_KEY 环境变量")

app = FirecrawlApp(api_key=api_key)

# ✅ 日志中隐藏密钥
def mask_api_key(key: str) -> str:
    """隐藏 API 密钥"""
    return f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"

logger.info(f"使用 API 密钥: {mask_api_key(api_key)}")
```

---

## ⚡ 请求优化策略

### 1. 批量处理优化

```python
from typing import List, Dict
import asyncio
from firecrawl import FirecrawlApp

class FirecrawlOptimizer:
    """Firecrawl 请求优化器"""

    def __init__(self, api_key: str, batch_size: int = 10):
        self.app = FirecrawlApp(api_key=api_key)
        self.batch_size = batch_size

    def batch_scrape_optimized(
        self,
        urls: List[str],
        formats: List[str] = ['markdown'],
        **kwargs
    ) -> List[Dict]:
        """
        优化的批量爬取

        特性：
        1. 自动分批处理
        2. 并发控制
        3. 失败重试
        4. 进度追踪
        """
        results = []
        total_batches = (len(urls) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(urls), self.batch_size):
            batch = urls[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1

            print(f"处理批次 {batch_num}/{total_batches} ({len(batch)} 个 URL)")

            try:
                batch_results = self.app.batch_scrape(
                    urls=batch,
                    formats=formats,
                    **kwargs
                )
                results.extend(batch_results)

            except Exception as e:
                print(f"批次 {batch_num} 失败: {e}")
                # 失败重试（逐个处理）
                for url in batch:
                    try:
                        result = self.app.scrape(url, formats=formats, **kwargs)
                        results.append(result)
                    except Exception as url_error:
                        print(f"URL {url} 失败: {url_error}")
                        results.append({'url': url, 'error': str(url_error)})

        return results
```

### 2. 智能重试策略

```python
import time
from typing import Callable, Any
from functools import wraps

def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """
    指数退避重试装饰器

    参数：
        max_retries: 最大重试次数
        base_delay: 基础延迟（秒）
        max_delay: 最大延迟（秒）
        exponential_base: 指数基数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    retries += 1

                    if retries >= max_retries:
                        raise

                    # 计算延迟时间
                    delay = min(
                        base_delay * (exponential_base ** retries),
                        max_delay
                    )

                    print(f"请求失败，{delay:.1f}秒后重试 ({retries}/{max_retries}): {e}")
                    time.sleep(delay)

            raise Exception(f"超过最大重试次数 ({max_retries})")

        return wrapper
    return decorator

# 使用示例
@retry_with_exponential_backoff(max_retries=5)
def scrape_with_retry(url: str):
    """带重试的爬取"""
    return app.scrape(url, formats=['markdown'])
```

### 3. 并发控制

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

class ConcurrentScraper:
    """并发爬取管理器"""

    def __init__(
        self,
        api_key: str,
        max_workers: int = 5,
        rate_limit: int = 10  # 每秒最大请求数
    ):
        self.app = FirecrawlApp(api_key=api_key)
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(max_workers)

    async def scrape_url(self, url: str, **kwargs) -> Dict:
        """异步爬取单个 URL"""
        async with self.semaphore:
            try:
                # 速率限制
                await asyncio.sleep(1 / self.rate_limit)

                # 执行爬取
                result = await asyncio.to_thread(
                    self.app.scrape,
                    url,
                    **kwargs
                )
                return {'url': url, 'success': True, 'data': result}

            except Exception as e:
                return {'url': url, 'success': False, 'error': str(e)}

    async def scrape_all(self, urls: List[str], **kwargs) -> List[Dict]:
        """异步爬取所有 URL"""
        tasks = [self.scrape_url(url, **kwargs) for url in urls]
        return await asyncio.gather(*tasks)

# 使用示例
async def main():
    scraper = ConcurrentScraper(
        api_key=os.getenv('FIRECRAWL_API_KEY'),
        max_workers=5,
        rate_limit=10
    )

    urls = ["https://example.com/1", "https://example.com/2", ...]
    results = await scraper.scrape_all(urls, formats=['markdown'])

    print(f"成功: {sum(1 for r in results if r['success'])}/{len(results)}")

# asyncio.run(main())
```

---

## 💰 成本控制

### 1. 成本监控

```python
from datetime import datetime
from typing import Dict, List

class CostTracker:
    """API 成本追踪器"""

    # 定价（根据实际情况调整）
    PRICING = {
        'scrape': 0.005,      # 每页 $0.005
        'crawl': 0.004,       # 每页 $0.004（批量折扣）
        'search': 0.01,       # 每次搜索 $0.01
        'extract': 0.008,     # 每次提取 $0.008
    }

    def __init__(self):
        self.usage = {
            'scrape': 0,
            'crawl': 0,
            'search': 0,
            'extract': 0,
        }
        self.start_time = datetime.now()

    def track(self, operation: str, count: int = 1):
        """记录 API 使用"""
        if operation in self.usage:
            self.usage[operation] += count

    def get_cost(self) -> float:
        """计算总成本"""
        total = sum(
            self.usage[op] * self.PRICING[op]
            for op in self.usage
        )
        return round(total, 2)

    def get_report(self) -> Dict:
        """生成成本报告"""
        runtime = (datetime.now() - self.start_time).total_seconds()

        return {
            'total_cost': self.get_cost(),
            'usage': self.usage,
            'runtime_seconds': runtime,
            'cost_per_hour': round(self.get_cost() / (runtime / 3600), 2) if runtime > 0 else 0,
            'details': {
                op: {
                    'count': self.usage[op],
                    'cost': round(self.usage[op] * self.PRICING[op], 2)
                }
                for op in self.usage
            }
        }

# 全局成本追踪器
cost_tracker = CostTracker()

# 装饰器
def track_cost(operation: str):
    """成本追踪装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # 根据结果追踪成本
            if isinstance(result, list):
                cost_tracker.track(operation, len(result))
            else:
                cost_tracker.track(operation, 1)

            return result
        return wrapper
    return decorator

# 使用示例
@track_cost('scrape')
def scrape_urls(urls: List[str]):
    return app.batch_scrape(urls)

# 定期打印成本报告
import atexit

def print_cost_report():
    report = cost_tracker.get_report()
    print("\n" + "=" * 50)
    print("📊 Firecrawl API 成本报告")
    print("=" * 50)
    print(f"总成本: ${report['total_cost']}")
    print(f"运行时长: {report['runtime_seconds']:.0f} 秒")
    print(f"每小时成本: ${report['cost_per_hour']}")
    print("\n详细使用:")
    for op, details in report['details'].items():
        print(f"  {op}: {details['count']} 次 (${details['cost']})")
    print("=" * 50)

atexit.register(print_cost_report)
```

### 2. 预算限制

```python
class BudgetLimiter:
    """预算限制器"""

    def __init__(
        self,
        daily_budget: float = 10.0,   # 每日预算 $10
        monthly_budget: float = 200.0  # 每月预算 $200
    ):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.daily_spent = 0.0
        self.monthly_spent = 0.0
        self.last_reset = datetime.now()

    def check_budget(self, estimated_cost: float) -> bool:
        """检查是否超预算"""
        # 重置每日预算
        if (datetime.now() - self.last_reset).days >= 1:
            self.daily_spent = 0.0
            self.last_reset = datetime.now()

        # 检查预算
        if self.daily_spent + estimated_cost > self.daily_budget:
            raise BudgetExceededError(f"超过每日预算 (${self.daily_budget})")

        if self.monthly_spent + estimated_cost > self.monthly_budget:
            raise BudgetExceededError(f"超过每月预算 (${self.monthly_budget})")

        return True

    def record_cost(self, cost: float):
        """记录消费"""
        self.daily_spent += cost
        self.monthly_spent += cost

class BudgetExceededError(Exception):
    """预算超支异常"""
    pass

# 使用示例
budget = BudgetLimiter(daily_budget=10.0)

def scrape_with_budget(urls: List[str]):
    """带预算控制的爬取"""
    estimated_cost = len(urls) * 0.005

    # 检查预算
    budget.check_budget(estimated_cost)

    # 执行爬取
    results = app.batch_scrape(urls)

    # 记录成本
    budget.record_cost(estimated_cost)

    return results
```

### 3. 成本优化建议

#### **策略 1: 智能缓存**
```python
import hashlib
import json
from typing import Optional

class SmartCache:
    """智能缓存管理器"""

    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, url: str, params: dict) -> str:
        """生成缓存键"""
        data = f"{url}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()

    def get(self, url: str, params: dict, max_age: int = 3600) -> Optional[dict]:
        """获取缓存"""
        cache_key = self._get_cache_key(url, params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if not os.path.exists(cache_file):
            return None

        # 检查缓存是否过期
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime > max_age:
            os.remove(cache_file)
            return None

        with open(cache_file, 'r') as f:
            return json.load(f)

    def set(self, url: str, params: dict, data: dict):
        """设置缓存"""
        cache_key = self._get_cache_key(url, params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        with open(cache_file, 'w') as f:
            json.dump(data, f)

# 使用缓存
cache = SmartCache()

def scrape_with_cache(url: str, **params):
    """带缓存的爬取"""
    # 尝试从缓存获取
    cached = cache.get(url, params, max_age=3600)
    if cached:
        print(f"✅ 命中缓存: {url}")
        return cached

    # 缓存未命中，调用 API
    print(f"🔄 API 请求: {url}")
    result = app.scrape(url, **params)

    # 保存到缓存
    cache.set(url, params, result)

    return result
```

#### **策略 2: 内容去重**
```python
from typing import Set

class URLDeduplicator:
    """URL 去重器"""

    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_content_hashes: Set[str] = set()

    def is_duplicate_url(self, url: str) -> bool:
        """检查 URL 是否重复"""
        normalized_url = self._normalize_url(url)
        if normalized_url in self.seen_urls:
            return True
        self.seen_urls.add(normalized_url)
        return False

    def is_duplicate_content(self, content: str) -> bool:
        """检查内容是否重复"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        if content_hash in self.seen_content_hashes:
            return True
        self.seen_content_hashes.add(content_hash)
        return False

    @staticmethod
    def _normalize_url(url: str) -> str:
        """规范化 URL"""
        # 移除查询参数、锚点等
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

# 使用去重
deduplicator = URLDeduplicator()

def scrape_unique_urls(urls: List[str]):
    """只爬取不重复的 URL"""
    unique_urls = [
        url for url in urls
        if not deduplicator.is_duplicate_url(url)
    ]

    print(f"去重后: {len(unique_urls)}/{len(urls)} 个 URL")
    return app.batch_scrape(unique_urls)
```

---

## ❌ 错误处理

### 1. 完整的错误处理体系

```python
from enum import Enum
from typing import Optional, Dict, Any

class FirecrawlErrorType(Enum):
    """错误类型枚举"""
    AUTHENTICATION = "认证失败"
    RATE_LIMIT = "速率限制"
    TIMEOUT = "请求超时"
    INVALID_URL = "无效 URL"
    NETWORK = "网络错误"
    SERVER_ERROR = "服务器错误"
    UNKNOWN = "未知错误"

class FirecrawlError(Exception):
    """Firecrawl 自定义异常"""

    def __init__(
        self,
        error_type: FirecrawlErrorType,
        message: str,
        original_error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.error_type = error_type
        self.message = message
        self.original_error = original_error
        self.context = context or {}

        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_type.value}] {self.message}"

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'error_type': self.error_type.name,
            'message': self.message,
            'context': self.context,
            'original_error': str(self.original_error) if self.original_error else None
        }

class ErrorHandler:
    """统一错误处理器"""

    @staticmethod
    def handle_error(e: Exception, url: Optional[str] = None) -> FirecrawlError:
        """处理并分类错误"""
        error_msg = str(e).lower()
        context = {'url': url} if url else {}

        # 认证错误
        if 'unauthorized' in error_msg or 'api key' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.AUTHENTICATION,
                "API 密钥无效或已过期",
                e,
                context
            )

        # 速率限制
        if 'rate limit' in error_msg or '429' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.RATE_LIMIT,
                "超过 API 速率限制，请稍后重试",
                e,
                context
            )

        # 超时
        if 'timeout' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.TIMEOUT,
                "请求超时",
                e,
                context
            )

        # 无效 URL
        if 'invalid url' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.INVALID_URL,
                f"无效的 URL: {url}",
                e,
                context
            )

        # 网络错误
        if 'connection' in error_msg or 'network' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.NETWORK,
                "网络连接失败",
                e,
                context
            )

        # 服务器错误
        if '500' in error_msg or '502' in error_msg or '503' in error_msg:
            return FirecrawlError(
                FirecrawlErrorType.SERVER_ERROR,
                "Firecrawl 服务器错误",
                e,
                context
            )

        # 未知错误
        return FirecrawlError(
            FirecrawlErrorType.UNKNOWN,
            f"未知错误: {str(e)}",
            e,
            context
        )

# 使用示例
def safe_scrape(url: str, **kwargs) -> Dict:
    """安全的爬取（带错误处理）"""
    try:
        return app.scrape(url, **kwargs)

    except Exception as e:
        # 统一错误处理
        error = ErrorHandler.handle_error(e, url)

        # 记录错误日志
        logger.error(f"爬取失败: {error}", extra=error.to_dict())

        # 根据错误类型决定是否重试
        if error.error_type == FirecrawlErrorType.RATE_LIMIT:
            time.sleep(60)  # 等待 1 分钟后重试
            return safe_scrape(url, **kwargs)

        elif error.error_type == FirecrawlErrorType.TIMEOUT:
            # 增加超时时间重试
            kwargs['timeout'] = kwargs.get('timeout', 30) * 2
            return safe_scrape(url, **kwargs)

        # 其他错误直接抛出
        raise error
```

### 2. 错误日志记录

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
def setup_logging():
    """配置 Firecrawl 日志"""
    logger = logging.getLogger('firecrawl')
    logger.setLevel(logging.INFO)

    # 文件处理器（自动轮转）
    file_handler = RotatingFileHandler(
        'logs/firecrawl.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # 错误日志单独记录
    error_handler = RotatingFileHandler(
        'logs/firecrawl_errors.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)

    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger

logger = setup_logging()

# 使用日志
def logged_scrape(url: str, **kwargs):
    """带日志的爬取"""
    try:
        logger.info(f"开始爬取: {url}")
        result = app.scrape(url, **kwargs)
        logger.info(f"爬取成功: {url}")
        return result

    except Exception as e:
        logger.error(
            f"爬取失败: {url}",
            extra={
                'url': url,
                'error': str(e),
                'params': kwargs
            },
            exc_info=True
        )
        raise
```

---

## 🚀 性能优化

### 1. 连接池管理

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedFirecrawlApp:
    """优化的 Firecrawl 客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key

        # 配置连接池
        self.session = self._create_session()
        self.app = FirecrawlApp(api_key=api_key)

    def _create_session(self):
        """创建优化的 Session"""
        session = requests.Session()

        # 重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        # HTTP 适配器
        adapter = HTTPAdapter(
            pool_connections=100,    # 连接池大小
            pool_maxsize=100,
            max_retries=retry_strategy,
            pool_block=False
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session
```

### 2. 响应压缩

```python
# 启用 gzip 压缩
result = app.scrape(
    url="https://example.com",
    headers={
        'Accept-Encoding': 'gzip, deflate',
    }
)
```

### 3. 性能监控

```python
import time
from contextlib import contextmanager

class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
        }

    @contextmanager
    def track(self, operation: str):
        """追踪操作性能"""
        start_time = time.time()

        try:
            yield
        finally:
            elapsed = time.time() - start_time
            self._record(operation, elapsed)

    def _record(self, operation: str, elapsed: float):
        """记录性能数据"""
        self.metrics['total_requests'] += 1
        self.metrics['total_time'] += elapsed
        self.metrics['avg_time'] = self.metrics['total_time'] / self.metrics['total_requests']
        self.metrics['min_time'] = min(self.metrics['min_time'], elapsed)
        self.metrics['max_time'] = max(self.metrics['max_time'], elapsed)

        logger.info(
            f"[{operation}] 耗时: {elapsed:.2f}s "
            f"(平均: {self.metrics['avg_time']:.2f}s)"
        )

    def get_report(self) -> Dict:
        """生成性能报告"""
        return {
            'total_requests': self.metrics['total_requests'],
            'total_time': round(self.metrics['total_time'], 2),
            'avg_time': round(self.metrics['avg_time'], 2),
            'min_time': round(self.metrics['min_time'], 2),
            'max_time': round(self.metrics['max_time'], 2),
            'requests_per_second': round(
                self.metrics['total_requests'] / self.metrics['total_time'], 2
            ) if self.metrics['total_time'] > 0 else 0
        }

# 使用性能监控
monitor = PerformanceMonitor()

def monitored_scrape(url: str):
    """带性能监控的爬取"""
    with monitor.track('scrape'):
        return app.scrape(url)
```

---

## 🔒 安全规范

### 1. 请求头安全

```python
# 推荐的请求头配置
SECURE_HEADERS = {
    'User-Agent': 'HawaiiHub/1.0 (Firecrawl Bot)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',  # Do Not Track
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

result = app.scrape(
    url="https://example.com",
    headers=SECURE_HEADERS
)
```

### 2. URL 验证

```python
from urllib.parse import urlparse
import re

class URLValidator:
    """URL 验证器"""

    # 允许的协议
    ALLOWED_SCHEMES = ['http', 'https']

    # 禁止的域名（内网、敏感域名）
    BLOCKED_DOMAINS = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '::1',
        '192.168.',
        '10.',
        '172.16.',
    ]

    # 允许的域名白名单（可选）
    ALLOWED_DOMAINS = [
        'hawaiinewsnow.com',
        'staradvertiser.com',
        'civilbeat.org',
        # ... 其他可信域名
    ]

    @classmethod
    def validate(cls, url: str, strict: bool = False) -> bool:
        """
        验证 URL

        参数：
            url: 待验证的 URL
            strict: 严格模式（只允许白名单域名）
        """
        try:
            parsed = urlparse(url)

            # 检查协议
            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                raise ValueError(f"不允许的协议: {parsed.scheme}")

            # 检查域名
            hostname = parsed.hostname or ''

            # 禁止列表检查
            for blocked in cls.BLOCKED_DOMAINS:
                if hostname.startswith(blocked):
                    raise ValueError(f"禁止访问的域名: {hostname}")

            # 严格模式：白名单检查
            if strict and not any(
                hostname.endswith(domain)
                for domain in cls.ALLOWED_DOMAINS
            ):
                raise ValueError(f"域名不在白名单中: {hostname}")

            return True

        except Exception as e:
            logger.warning(f"URL 验证失败: {url} - {e}")
            return False

# 使用 URL 验证
def safe_scrape_validated(url: str, **kwargs):
    """验证 URL 后再爬取"""
    if not URLValidator.validate(url):
        raise ValueError(f"URL 验证失败: {url}")

    return app.scrape(url, **kwargs)
```

### 3. 数据脱敏

```python
import re

class DataSanitizer:
    """数据脱敏器"""

    # 敏感信息正则
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }

    @classmethod
    def sanitize(cls, text: str, keep_structure: bool = True) -> str:
        """
        脱敏文本中的敏感信息

        参数：
            text: 原始文本
            keep_structure: 是否保留结构（如 abc@example.com -> ***@***.com）
        """
        for pattern_type, pattern in cls.PATTERNS.items():
            if keep_structure and pattern_type == 'email':
                # 保留邮箱结构
                text = re.sub(
                    pattern,
                    lambda m: cls._mask_email(m.group(0)),
                    text
                )
            else:
                # 完全替换
                text = re.sub(pattern, f'[{pattern_type.upper()}_REDACTED]', text)

        return text

    @staticmethod
    def _mask_email(email: str) -> str:
        """脱敏邮箱地址"""
        parts = email.split('@')
        if len(parts) != 2:
            return '[EMAIL_REDACTED]'

        username, domain = parts
        masked_username = username[0] + '***' if username else '***'

        domain_parts = domain.split('.')
        masked_domain = '.'.join([
            '***' if i < len(domain_parts) - 1 else part
            for i, part in enumerate(domain_parts)
        ])

        return f"{masked_username}@{masked_domain}"

# 使用数据脱敏
def scrape_and_sanitize(url: str):
    """爬取并脱敏"""
    result = app.scrape(url, formats=['markdown'])
    result['markdown'] = DataSanitizer.sanitize(result['markdown'])
    return result
```

---

## 📊 监控与日志

### 1. 实时监控仪表板

```python
from collections import defaultdict
from datetime import datetime, timedelta

class DashboardMetrics:
    """仪表板指标"""

    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'success': 0,
            'failure': 0,
            'total_time': 0.0,
        })
        self.hourly_stats = defaultdict(int)

    def record(
        self,
        operation: str,
        success: bool,
        elapsed: float
    ):
        """记录操作指标"""
        m = self.metrics[operation]
        m['count'] += 1
        m['success' if success else 'failure'] += 1
        m['total_time'] += elapsed

        # 小时统计
        hour_key = datetime.now().strftime('%Y-%m-%d %H:00')
        self.hourly_stats[hour_key] += 1

    def get_dashboard(self) -> Dict:
        """获取仪表板数据"""
        dashboard = {}

        for operation, m in self.metrics.items():
            success_rate = (m['success'] / m['count'] * 100) if m['count'] > 0 else 0
            avg_time = m['total_time'] / m['count'] if m['count'] > 0 else 0

            dashboard[operation] = {
                '总请求': m['count'],
                '成功': m['success'],
                '失败': m['failure'],
                '成功率': f"{success_rate:.1f}%",
                '平均耗时': f"{avg_time:.2f}s",
            }

        return dashboard

    def print_dashboard(self):
        """打印仪表板"""
        print("\n" + "=" * 80)
        print("📊 Firecrawl API 实时监控仪表板")
        print("=" * 80)

        dashboard = self.get_dashboard()
        for operation, stats in dashboard.items():
            print(f"\n{operation.upper()}:")
            for key, value in stats.items():
                print(f"  {key}: {value}")

        # 小时趋势
        print("\n每小时请求趋势:")
        for hour in sorted(self.hourly_stats.keys())[-24:]:  # 最近 24 小时
            bar = '█' * (self.hourly_stats[hour] // 10)
            print(f"  {hour}: {bar} ({self.hourly_stats[hour]})")

        print("=" * 80)

# 全局仪表板
dashboard = DashboardMetrics()

# 定时打印（每 5 分钟）
import threading

def print_dashboard_periodically():
    """定时打印仪表板"""
    while True:
        time.sleep(300)  # 5 分钟
        dashboard.print_dashboard()

dashboard_thread = threading.Thread(target=print_dashboard_periodically, daemon=True)
dashboard_thread.start()
```

### 2. 告警系统

```python
from enum import Enum

class AlertLevel(Enum):
    """告警级别"""
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    CRITICAL = "严重"

class AlertSystem:
    """告警系统"""

    def __init__(
        self,
        webhook_url: Optional[str] = None,  # Slack/钉钉 Webhook
        email_config: Optional[Dict] = None
    ):
        self.webhook_url = webhook_url
        self.email_config = email_config
        self.alert_history = []

    def alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        context: Optional[Dict] = None
    ):
        """发送告警"""
        alert = {
            'level': level,
            'title': title,
            'message': message,
            'context': context or {},
            'timestamp': datetime.now()
        }

        self.alert_history.append(alert)

        # 根据级别决定是否发送通知
        if level in [AlertLevel.ERROR, AlertLevel.CRITICAL]:
            self._send_notification(alert)

        # 记录日志
        logger.log(
            logging.ERROR if level == AlertLevel.ERROR else logging.WARNING,
            f"[{level.value}] {title}: {message}",
            extra=context
        )

    def _send_notification(self, alert: Dict):
        """发送通知（Webhook/邮件）"""
        if self.webhook_url:
            try:
                import requests
                requests.post(self.webhook_url, json={
                    'text': f"[{alert['level'].value}] {alert['title']}\n{alert['message']}"
                })
            except Exception as e:
                logger.error(f"发送告警失败: {e}")

# 使用告警系统
alert_system = AlertSystem(
    webhook_url=os.getenv('ALERT_WEBHOOK_URL')
)

# 示例：成本告警
def check_cost_alert():
    """检查成本告警"""
    current_cost = cost_tracker.get_cost()

    if current_cost > 8.0:  # 接近每日预算 $10
        alert_system.alert(
            AlertLevel.WARNING,
            "API 成本告警",
            f"今日成本已达 ${current_cost:.2f}，接近预算上限",
            {'current_cost': current_cost, 'budget': 10.0}
        )

    if current_cost > 10.0:  # 超过预算
        alert_system.alert(
            AlertLevel.CRITICAL,
            "API 成本超支",
            f"今日成本 ${current_cost:.2f} 已超过预算 $10.00",
            {'current_cost': current_cost, 'budget': 10.0}
        )
```

---

## 📝 代码规范

### 1. 统一的 API 调用封装

```python
# utils/firecrawl_client.py
from typing import List, Dict, Optional, Union
from firecrawl import FirecrawlApp

class FirecrawlClient:
    """统一的 Firecrawl 客户端"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        self.app = FirecrawlApp(api_key=self.api_key)

        # 集成所有工具
        self.cache = SmartCache()
        self.cost_tracker = CostTracker()
        self.monitor = PerformanceMonitor()
        self.alert = AlertSystem()

    def scrape(
        self,
        url: str,
        formats: List[str] = ['markdown'],
        use_cache: bool = True,
        **kwargs
    ) -> Dict:
        """
        爬取单个 URL

        参数：
            url: 目标 URL
            formats: 返回格式
            use_cache: 是否使用缓存
            **kwargs: 其他参数

        返回：
            爬取结果字典
        """
        # URL 验证
        if not URLValidator.validate(url):
            raise ValueError(f"无效 URL: {url}")

        # 尝试缓存
        if use_cache:
            cached = self.cache.get(url, kwargs)
            if cached:
                return cached

        # 执行爬取（带监控）
        with self.monitor.track('scrape'):
            try:
                result = self.app.scrape(
                    url=url,
                    formats=formats,
                    **kwargs
                )

                # 记录成本
                self.cost_tracker.track('scrape', 1)

                # 保存缓存
                if use_cache:
                    self.cache.set(url, kwargs, result)

                return result

            except Exception as e:
                # 错误处理
                error = ErrorHandler.handle_error(e, url)
                self.alert.alert(
                    AlertLevel.ERROR,
                    f"爬取失败: {url}",
                    str(error)
                )
                raise error

    def batch_scrape(
        self,
        urls: List[str],
        formats: List[str] = ['markdown'],
        batch_size: int = 10,
        **kwargs
    ) -> List[Dict]:
        """
        批量爬取

        参数：
            urls: URL 列表
            formats: 返回格式
            batch_size: 批次大小
            **kwargs: 其他参数
        """
        # URL 去重
        deduplicator = URLDeduplicator()
        unique_urls = [
            url for url in urls
            if not deduplicator.is_duplicate_url(url)
        ]

        # 分批处理
        optimizer = FirecrawlOptimizer(self.api_key, batch_size)
        results = optimizer.batch_scrape_optimized(
            unique_urls,
            formats=formats,
            **kwargs
        )

        # 记录成本
        self.cost_tracker.track('scrape', len(results))

        return results

    def get_metrics(self) -> Dict:
        """获取所有指标"""
        return {
            'cost': self.cost_tracker.get_report(),
            'performance': self.monitor.get_report(),
            'cache_stats': {
                # TODO: 实现缓存统计
            }
        }

# 全局客户端实例
firecrawl_client = FirecrawlClient()

# 使用示例
def scrape_hawaii_news():
    """爬取夏威夷新闻"""
    urls = [
        "https://www.hawaiinewsnow.com/",
        "https://www.staradvertiser.com/",
    ]

    results = firecrawl_client.batch_scrape(urls)

    # 打印指标
    metrics = firecrawl_client.get_metrics()
    print(f"成本: ${metrics['cost']['total_cost']}")
    print(f"性能: {metrics['performance']['avg_time']:.2f}s")

    return results
```

### 2. 配置文件规范

```python
# config/firecrawl_config.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FirecrawlConfig:
    """Firecrawl 配置"""

    # API 配置
    api_key: str
    api_url: str = "https://api.firecrawl.dev"
    timeout: int = 60
    max_retries: int = 3

    # 功能开关
    enable_cache: bool = True
    enable_monitoring: bool = True
    enable_cost_tracking: bool = True

    # 缓存配置
    cache_ttl: int = 3600
    cache_dir: str = "./cache"

    # 成本限制
    daily_budget: float = 10.0
    monthly_budget: float = 200.0

    # 性能配置
    batch_size: int = 10
    max_workers: int = 5
    rate_limit: int = 10

    # 告警配置
    alert_webhook: Optional[str] = None
    alert_email: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'FirecrawlConfig':
        """从环境变量加载配置"""
        return cls(
            api_key=os.getenv('FIRECRAWL_API_KEY'),
            api_url=os.getenv('FIRECRAWL_API_URL', cls.api_url),
            timeout=int(os.getenv('FIRECRAWL_TIMEOUT', cls.timeout)),
            enable_cache=os.getenv('FIRECRAWL_ENABLE_CACHE', 'true').lower() == 'true',
            daily_budget=float(os.getenv('FIRECRAWL_DAILY_BUDGET', cls.daily_budget)),
            alert_webhook=os.getenv('FIRECRAWL_ALERT_WEBHOOK'),
        )

    def validate(self):
        """验证配置"""
        if not self.api_key:
            raise ValueError("未设置 FIRECRAWL_API_KEY")

        if self.daily_budget <= 0:
            raise ValueError("每日预算必须大于 0")

        if self.batch_size < 1:
            raise ValueError("批次大小必须至少为 1")

        return True

# 加载配置
config = FirecrawlConfig.from_env()
config.validate()
```

---

## 🚨 应急预案

### 1. API 故障应急

```python
class EmergencyFallback:
    """应急后备方案"""

    def __init__(self):
        # 备用 API 密钥
        self.backup_keys = [
            os.getenv('FIRECRAWL_API_KEY_BACKUP_1'),
            os.getenv('FIRECRAWL_API_KEY_BACKUP_2'),
        ]
        self.current_key_index = 0

        # 降级策略
        self.degraded_mode = False

    def switch_to_backup_key(self):
        """切换到备用密钥"""
        if self.current_key_index < len(self.backup_keys) - 1:
            self.current_key_index += 1
            new_key = self.backup_keys[self.current_key_index]
            print(f"⚠️ 切换到备用密钥 #{self.current_key_index + 1}")
            return FirecrawlApp(api_key=new_key)

        print("❌ 所有备用密钥已耗尽，启动降级模式")
        self.degraded_mode = True
        return None

    def scrape_with_fallback(self, url: str, **kwargs):
        """带降级的爬取"""
        if self.degraded_mode:
            # 降级模式：使用简单的 requests
            return self._simple_scrape(url)

        try:
            return app.scrape(url, **kwargs)

        except Exception as e:
            # API 故障，尝试切换密钥
            backup_app = self.switch_to_backup_key()

            if backup_app:
                return backup_app.scrape(url, **kwargs)
            else:
                # 降级到简单爬取
                return self._simple_scrape(url)

    @staticmethod
    def _simple_scrape(url: str) -> Dict:
        """简单爬取（降级方案）"""
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取主要内容
        main_content = soup.find('main') or soup.find('article') or soup.body
        text = main_content.get_text(strip=True) if main_content else ""

        return {
            'url': url,
            'markdown': text,
            'method': 'fallback',
            'warning': '使用降级方案，内容可能不完整'
        }

emergency = EmergencyFallback()
```

### 2. 速率限制应对

```python
class RateLimiter:
    """速率限制器"""

    def __init__(self, max_requests: int = 100, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def wait_if_needed(self):
        """如果需要，等待直到可以发送请求"""
        now = time.time()

        # 清理过期请求
        self.requests = [
            req_time for req_time in self.requests
            if now - req_time < self.time_window
        ]

        # 检查是否超限
        if len(self.requests) >= self.max_requests:
            # 计算需要等待的时间
            oldest_request = min(self.requests)
            wait_time = self.time_window - (now - oldest_request)

            if wait_time > 0:
                print(f"⏳ 达到速率限制，等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)

        # 记录本次请求
        self.requests.append(time.time())

rate_limiter = RateLimiter(max_requests=100, time_window=60)

def rate_limited_scrape(url: str, **kwargs):
    """速率限制的爬取"""
    rate_limiter.wait_if_needed()
    return app.scrape(url, **kwargs)
```

---

## 📌 快速参考

### 常用命令

```bash
# 安装依赖
pip install firecrawl-py requests python-dotenv

# 运行测试
python -m pytest tests/

# 查看成本报告
python -m scripts.cost_report

# 清理缓存
python -m scripts.clear_cache

# 导出日志
python -m scripts.export_logs --date 2025-10-27
```

### 环境变量清单

```bash
# 必需
FIRECRAWL_API_KEY=fc-xxx

# 可选
FIRECRAWL_API_URL=https://api.firecrawl.dev
FIRECRAWL_TIMEOUT=60
FIRECRAWL_MAX_RETRIES=3
FIRECRAWL_ENABLE_CACHE=true
FIRECRAWL_CACHE_TTL=3600
FIRECRAWL_DAILY_BUDGET=10.0
FIRECRAWL_MONTHLY_BUDGET=200.0
FIRECRAWL_ALERT_WEBHOOK=https://hooks.slack.com/xxx
```

### 性能基准

| 操作 | 单次耗时 | 批量 (10个) | 成本 |
|------|---------|------------|------|
| Scrape | 1-3s | 10-15s | $0.005/页 |
| Search | 2-5s | - | $0.01/次 |
| Crawl | 30-60s | - | $0.004/页 |

---

## ✅ 检查清单

### 上线前检查

- [ ] API 密钥已配置且有效
- [ ] 环境变量完整
- [ ] 错误处理已实现
- [ ] 日志系统已配置
- [ ] 成本监控已启用
- [ ] 缓存策略已配置
- [ ] 速率限制已设置
- [ ] 告警系统已测试
- [ ] 备用方案已准备
- [ ] 文档已更新

### 日常检查

- [ ] 检查 API 配额使用情况
- [ ] 查看错误日志
- [ ] 检查成本是否超标
- [ ] 清理过期缓存
- [ ] 更新监控数据
- [ ] 备份重要数据

---

## 📚 相关文档

- [Firecrawl 官方文档](https://docs.firecrawl.dev)
- [Firecrawl 生态系统指南](./FIRECRAWL_ECOSYSTEM_GUIDE.md)
- [HawaiiHub 技术规范](../AGENTS.md)

---

**🔥 遵守这些规范，让 Firecrawl 云 API 为 HawaiiHub 提供强大且稳定的数据采集能力！🌴**

---

_最后更新: 2025-10-27_
_维护者: HawaiiHub AI Team_
_版本: v1.0.0_
