# ✅ 项目优化任务清单

**创建时间**: 2025-01-29
**项目版本**: v2.1.0
**优化版本目标**: v2.2.0

---

## 🔴 P0 优先级 - 本周必须完成（5 项）

### [ ] P0-S1: 修复 API Key 泄露 ⚠️ 最紧急

**问题文件**: `honolulu_rentals/config.py` 行 20-25

**步骤**:

- [ ] 1. 登录 Firecrawl 控制台 <https://firecrawl.dev/app/settings>
- [ ] 2. 撤销这 4 个泄露的 API Key:
  - fc-31ebbe4647b84fdc975318d372eebea8
  - fc-00857d82ec534e8598df1bae9af9fb28
  - fc-9eb380b0dec74d6ebb6c756ee4de4c5a
  - fc-0a2c801f433d4718bcd8189f2742edf4
- [ ] 3. 生成 4 个新的 API Key
- [ ] 4. 添加到 .env 文件:

  ```bash
  FIRECRAWL_API_KEY_1=新Key1
  FIRECRAWL_API_KEY_2=新Key2
  FIRECRAWL_API_KEY_3=新Key3
  FIRECRAWL_API_KEY_4=新Key4
  ```

- [ ] 5. 修改 `honolulu_rentals/config.py`:

  ```python
  FIRECRAWL_API_KEYS = [
      os.getenv("FIRECRAWL_API_KEY_1"),
      os.getenv("FIRECRAWL_API_KEY_2"),
      os.getenv("FIRECRAWL_API_KEY_3"),
      os.getenv("FIRECRAWL_API_KEY_4"),
  ]
  FIRECRAWL_API_KEYS = [k for k in FIRECRAWL_API_KEYS if k]
  ```

- [ ] 6. 从 Git 历史中删除敏感信息
- [ ] 7. 强制推送清理后的历史

**预计时间**: 4 小时
**负责人**: DevOps + Dev
**风险**: 🔴 高（安全风险）

---

### [ ] P0-Q1: 移除所有硬编码配置

**需要检查的文件**:

- [ ] `honolulu_rentals/config.py`
- [ ] `news_collector/config.py`
- [ ] `src/firecrawl_config.py`
- [ ] `tests/*.py`

**检查命令**:

```bash
# 搜索所有可能的硬编码
grep -r "fc-[a-z0-9]" . --exclude-dir=归档 --exclude-dir=.git
grep -r "api_key.*=" . --include="*.py" --exclude-dir=归档
grep -r "password.*=" . --include="*.py" --exclude-dir=归档
```

**预计时间**: 2 小时
**负责人**: Dev

---

### [ ] P0-A1: 统一 BaseScraper 和 BaseAgent

**任务**:

- [ ] 1. 分析两个基类的功能差异
- [ ] 2. 设计统一的 BaseAgent 接口
- [ ] 3. 迁移 honolulu_rentals 使用新 BaseAgent
- [ ] 4. 更新所有业务场景继承新基类
- [ ] 5. 删除旧的 base_scraper.py
- [ ] 6. 更新文档

**参考设计**:

```python
# src/core/base_agent.py (统一版本)
class BaseAgent(ABC):
    """统一的智能体基类"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client: Optional[AsyncFirecrawl] = None
        self.semaphore = asyncio.Semaphore(config.max_concurrent)

    async def __aenter__(self):
        self.client = AsyncFirecrawl(api_key=self.config.api_key)
        await self.client.__aenter__()
        return self

    @abstractmethod
    async def collect(self, params: Dict[str, Any]) -> Any:
        """采集数据"""
        pass

    @abstractmethod
    async def parse(self, raw_data: Any) -> BaseModel:
        """解析数据"""
        pass

    async def execute(self, params: Dict[str, Any]) -> CollectionResult:
        """完整执行流程"""
        raw = await self.collect(params)
        parsed = await self.parse(raw)
        return CollectionResult(success=True, data=parsed)
```

**预计时间**: 8 小时
**负责人**: Dev
**影响范围**: 核心架构

---

### [ ] P0-P1: Firecrawl 成本优化

**优化点**:

#### [ ] 1. 启用长缓存

```python
# config/agents/rental_agent.yaml
firecrawl:
  max_age: 86400000  # 改为 24 小时（当前 1 小时）

# config/agents/news_agent.yaml
firecrawl:
  max_age: 3600000  # 改为 1 小时（当前 10 分钟）
```

#### [ ] 2. 使用 Map + Batch 替代 Crawl

```python
# honolulu_rentals/scrapers/craigslist_scraper.py

# ❌ 当前（昂贵）
async def get_listing_urls(self):
    result = await self.app.crawl(
        self.base_url,
        limit=500
    )

# ✅ 优化（节省 50%）
async def get_listing_urls(self):
    # 步骤1: Map 发现所有URL (1 credit)
    map_result = await self.app.map(self.base_url)

    # 步骤2: 过滤需要的URL
    listing_urls = [
        url for url in map_result.links
        if '/apa/' in url  # 只要公寓房源
    ]

    return listing_urls[:100]  # 只采集前100个
```

#### [ ] 3. 智能去重

```python
# src/utils/deduplication.py
async def filter_new_urls(urls: List[str], db_session) -> List[str]:
    """过滤出未采集的URL"""
    # 查询最近24小时采集过的URL
    existing = await db_session.execute(
        select(ScrapedURL.url)
        .where(ScrapedURL.scraped_at > datetime.now() - timedelta(hours=24))
    )
    existing_urls = set(row.url for row in existing)

    # 只返回新URL
    return [url for url in urls if url not in existing_urls]

# 使用
new_urls = await filter_new_urls(all_urls, db)
# 只采集新URL，节省 30-50%
```

**预期成本节省**: **60%**

**预计时间**: 4 小时
**负责人**: Dev

---

### [ ] P0-T1: 添加核心功能测试

**任务**:

- [ ] 1. 创建测试目录结构

  ```
  tests/
  ├── unit/           # 单元测试
  ├── integration/    # 集成测试
  ├── e2e/           # 端到端测试
  ├── benchmark/     # 性能测试
  └── conftest.py    # 共享 fixtures
  ```

- [ ] 2. 添加核心单元测试:

  - [ ] `test_base_agent.py` - BaseAgent 测试
  - [ ] `test_agent_registry.py` - AgentRegistry 测试
  - [ ] `test_models.py` - 数据模型验证测试
  - [ ] `test_config.py` - 配置加载测试

- [ ] 3. 添加集成测试:

  - [ ] `test_news_collector.py` - 新闻采集完整流程
  - [ ] `test_rental_scraper.py` - 租房采集完整流程

- [ ] 4. 配置 pytest.ini:

  ```ini
  [pytest]
  asyncio_mode = auto
  testpaths = tests
  python_files = test_*.py
  python_classes = Test*
  python_functions = test_*
  addopts =
      -v
      --strict-markers
      --cov=src
      --cov-report=html
      --cov-report=term-missing
  markers =
      unit: 单元测试
      integration: 集成测试
      e2e: 端到端测试
      slow: 慢速测试
  ```

**预计时间**: 6 小时
**负责人**: QA + Dev

---

## 🟡 P1 优先级 - 本月完成（7 项）

### [ ] P1-A2: 实现 Agent 工厂模式

**创建文件**: `src/core/agent_factory.py`

**核心代码**:

```python
from typing import Dict, Optional
import yaml
from pathlib import Path

class AgentFactory:
    """智能体工厂"""

    @staticmethod
    async def create_from_config(
        agent_type: str,
        config_path: Optional[str] = None
    ) -> BaseAgent:
        """从配置文件创建 Agent"""

        # 加载配置
        if not config_path:
            config_path = f"config/agents/{agent_type}_agent.yaml"

        with open(config_path) as f:
            config_data = yaml.safe_load(f)

        # 构建 AgentConfig
        agent_config = AgentConfig(
            name=config_data['agent']['name'],
            type=agent_type,
            api_key=os.getenv('FIRECRAWL_API_KEY'),
            **config_data['api']
        )

        # 从注册表获取 Agent 类
        return get_agent(agent_type, agent_config)

    @staticmethod
    async def create_batch(
        agent_types: List[str]
    ) -> Dict[str, BaseAgent]:
        """批量创建 Agents"""
        agents = {}
        for agent_type in agent_types:
            agents[agent_type] = await AgentFactory.create_from_config(agent_type)
        return agents

# 使用示例
agent = await AgentFactory.create_from_config("news")
# 自动加载 config/agents/news_agent.yaml
```

**预计时间**: 6 小时
**依赖**: P0-A1

---

### [ ] P1-A3: 重构配置管理系统

**创建文件**: `src/core/config_manager.py`

**任务**:

- [ ] 1. 设计统一的配置接口
- [ ] 2. 实现多源配置加载（环境变量 > YAML > JSON > 默认）
- [ ] 3. 支持配置热重载
- [ ] 4. 添加配置验证
- [ ] 5. 迁移所有配置到统一管理

**核心代码**:

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class ConfigSource(ABC):
    """配置源基类"""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def reload(self):
        pass

class EnvironmentSource(ConfigSource):
    """环境变量配置源"""

    def get(self, key: str) -> Optional[Any]:
        return os.getenv(key)

    def reload(self):
        pass  # 环境变量不需要重载

class YAMLSource(ConfigSource):
    """YAML 文件配置源"""

    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self.configs = {}
        self.reload()

    def get(self, key: str) -> Optional[Any]:
        parts = key.split('.')
        config = self.configs
        for part in parts:
            if part in config:
                config = config[part]
            else:
                return None
        return config

    def reload(self):
        """重新加载所有 YAML 文件"""
        self.configs = {}
        for yaml_file in self.config_dir.glob("**/*.yaml"):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                # 使用文件名作为 key
                key = yaml_file.stem
                self.configs[key] = data

class UnifiedConfigManager:
    """统一配置管理器"""

    def __init__(self):
        # 优先级：环境变量 > YAML > JSON > 默认值
        self.sources = [
            EnvironmentSource(),
            YAMLSource("config/agents/"),
            DefaultSource()
        ]

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（按优先级）"""
        for source in self.sources:
            value = source.get(key)
            if value is not None:
                return value
        return default

    def reload(self):
        """热重载所有配置"""
        for source in self.sources:
            source.reload()

# 全局配置管理器
config_manager = UnifiedConfigManager()
```

**预计时间**: 12 小时
**负责人**: Dev

---

### [ ] P1-A4: 实现统一的错误处理中间件

**创建文件**: `src/middleware/error_handler.py`

**任务**:

- [ ] 1. 定义自定义异常类
- [ ] 2. 创建错误处理中间件
- [ ] 3. 集成到 FastAPI
- [ ] 4. 添加错误追踪（Sentry）
- [ ] 5. 统一错误响应格式

**核心代码**:

```python
# src/exceptions.py
class FirecrawlCollectorException(Exception):
    """基础异常"""
    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(message)

class APIKeyError(FirecrawlCollectorException):
    """API Key 错误"""
    def __init__(self, message: str = "API Key 无效或已过期"):
        super().__init__(message, code="API_KEY_ERROR")

class RateLimitError(FirecrawlCollectorException):
    """速率限制错误"""
    def __init__(self, message: str = "超出 API 速率限制"):
        super().__init__(message, code="RATE_LIMIT")

# src/middleware/error_handler.py
from fastapi import Request, status
from fastapi.responses import JSONResponse

class ErrorHandlerMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.exception_handler(APIKeyError)
        async def api_key_error_handler(request: Request, exc: APIKeyError):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "success": False,
                    "error": {
                        "code": exc.code,
                        "message": exc.message,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        @self.app.exception_handler(RateLimitError)
        async def rate_limit_error_handler(request: Request, exc: RateLimitError):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "error": {
                        "code": exc.code,
                        "message": exc.message,
                        "retry_after": 60
                    }
                },
                headers={"Retry-After": "60"}
            )

# 使用
app = FastAPI()
ErrorHandlerMiddleware(app)
```

**预计时间**: 8 小时
**负责人**: Dev

---

### [ ] P1-Q3: 完善类型提示

**当前覆盖率**: ~70%
**目标覆盖率**: 95%

**任务**:

- [ ] 1. 使用 mypy 检查类型

  ```bash
  mypy src/ --strict --show-error-codes
  ```

- [ ] 2. 修复所有类型错误
- [ ] 3. 添加缺失的类型提示
- [ ] 4. 更新 pyproject.toml 配置

  ```toml
  [tool.mypy]
  python_version = "3.11"
  strict = true
  warn_return_any = true
  warn_unused_configs = true
  disallow_untyped_defs = true
  ```

**需要处理的文件**（按优先级）:

1. [ ] `src/core/base_agent.py`
2. [ ] `src/core/agent_registry.py`
3. [ ] `src/core/agent_manager.py`
4. [ ] `src/firecrawl_collector.py`
5. [ ] `src/task_scheduler.py`
6. [ ] `src/api_server.py`

**预计时间**: 16 小时
**负责人**: Dev

---

### [ ] P1-Q4: 异步代码一致性

**任务**:

- [ ] 1. 审计所有同步代码

  ```bash
  # 查找同步的 Firecrawl 调用
  grep -r "FirecrawlApp(" . --include="*.py"
  grep -r "\.scrape(" . --include="*.py" | grep -v "async"
  ```

- [ ] 2. 迁移到异步版本:

  - [ ] `honolulu_rentals/scrapers/base_scraper.py`
  - [ ] `honolulu_rentals/scrapers/craigslist_scraper.py`
  - [ ] `honolulu_rentals/main.py`

- [ ] 3. 更新导入:

  ```python
  # ❌ Before
  from firecrawl import FirecrawlApp

  # ✅ After
  from firecrawl import AsyncFirecrawl
  ```

- [ ] 4. 更新方法签名:

  ```python
  # ❌ Before
  def scrape_all(self) -> List[RentalListing]:
      result = self.app.scrape(url)

  # ✅ After
  async def scrape_all(self) -> List[RentalListing]:
      async with AsyncFirecrawl(api_key=self.api_key) as app:
          result = await app.scrape(url)
  ```

- [ ] 5. 更新所有调用点

**预计时间**: 12 小时
**负责人**: Dev
**性能提升**: **3-5 倍**

---

### [ ] P1-S2: 实施 API 认证

**创建文件**: `src/middleware/auth.py`

**任务**:

- [ ] 1. 实现 JWT 认证
- [ ] 2. 创建用户管理
- [ ] 3. 添加 API Key 认证（备选）
- [ ] 4. 更新所有 API 端点
- [ ] 5. 添加认证测试

**核心代码**:

```python
# src/middleware/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建 JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """验证 Token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return payload
    except JWTError:
        raise HTTPException(status_code=401)

# 使用
@app.post("/api/crawl")
async def create_crawl(
    request: CrawlRequest,
    user: dict = Depends(verify_token)  # 要求认证
):
    pass
```

**预计时间**: 8 小时
**负责人**: Dev

---

### [ ] P1-O1: 优化 Docker 镜像

**任务**:

- [ ] 1. 使用多阶段构建
- [ ] 2. 使用 Alpine 基础镜像
- [ ] 3. 清理构建缓存
- [ ] 4. 使用非 root 用户
- [ ] 5. 优化层缓存

**完整 Dockerfile**: 见 [PROJECT_OPTIMIZATION_REPORT.md](./PROJECT_OPTIMIZATION_REPORT.md) 第 8 节

**预计时间**: 6 小时
**负责人**: DevOps
**收益**: 镜像大小 -72% (900MB → 250MB)

---

## 🟢 P2 优先级 - 两个月完成（11 项）

### 性能优化（4 项）

- [ ] P2-P1: 迁移到 PostgreSQL
- [ ] P2-P2: 添加数据库索引
- [ ] P2-P3: 实现自适应并发控制
- [ ] P2-P4: 实现 Redis 缓存层

**预计时间**: 32 小时

---

### 测试完善（4 项）

- [ ] P2-T2: 添加性能基准测试
- [ ] P2-T3: 实现自动化回归测试
- [ ] P2-T4: 实现模糊测试
- [ ] P2-T5: 集成测试覆盖率 >60%

**预计时间**: 40 小时

---

### 文档优化（4 项）

- [ ] P2-D1: 重组文档结构
- [ ] P2-D2: 添加 ADR（架构决策记录）
- [ ] P2-D3: 生成自动化变更日志
- [ ] P2-D4: 完善贡献指南

**预计时间**: 24 小时

---

### DevOps 优化（3 项）

- [ ] P2-O2: 实现完整 CI/CD 流水线
- [ ] P2-O3: 添加完整健康检查
- [ ] P2-O4: 实施自动化部署

**预计时间**: 16 小时

---

## 📅 时间线

### 第 1 周（本周）

- **周一-周二**: P0-S1 (API Key 安全)
- **周三-周四**: P0-A1 (统一 BaseAgent)
- **周五**: P0-P1 (成本优化) + P0-Q1 (移除硬编码)

### 第 2 周

- **周一-周二**: P0-T1 (核心测试)
- **周三-周五**: P1-A2 (Agent 工厂)

### 第 3-4 周

- P1-A3: 配置管理重构
- P1-Q3: 类型提示完善
- P1-Q4: 异步代码统一

### 第 5-6 周

- P1-S2: API 认证
- P1-O1: Docker 优化
- P1 其他任务

### 第 7-12 周

- P2 所有任务（根据优先级）

---

## 📊 进度追踪

### 整体进度

| 优先级   | 总任务 | 已完成 | 进行中 | 待开始 | 完成率 |
| -------- | ------ | ------ | ------ | ------ | ------ |
| P0       | 5      | 0      | 0      | 5      | 0%     |
| P1       | 7      | 0      | 0      | 7      | 0%     |
| P2       | 11     | 0      | 0      | 11     | 0%     |
| **总计** | **23** | **0**  | **0**  | **23** | **0%** |

### 每周目标

- **Week 1**: 完成 5 个 P0 任务（100%）
- **Week 2-3**: 完成 4 个 P1 任务（57%）
- **Week 4**: 完成 3 个 P1 任务（100%）
- **Week 5-12**: 完成 11 个 P2 任务（100%）

---

## 🎯 成功指标

### 代码质量

- [ ] 测试覆盖率 >80%
- [ ] 类型提示覆盖率 >95%
- [ ] 代码重复率 <5%
- [ ] 圈复杂度 <10
- [ ] 技术债务 <20%

### 性能指标

- [ ] API 响应时间 P95 <500ms
- [ ] 并发处理能力 >50 req/s
- [ ] 数据库查询 P95 <100ms
- [ ] 缓存命中率 >70%

### 成本指标

- [ ] Firecrawl API 成本 <$50/月
- [ ] 基础设施成本 <$30/月
- [ ] 总运营成本 <$100/月

### 稳定性指标

- [ ] 系统可用性 >99.5%
- [ ] 错误率 <0.1%
- [ ] MTTR (平均恢复时间) <15 分钟
- [ ] MTTF (平均故障间隔) >30 天

---

## 📝 使用说明

### 更新进度

完成一项任务后，在对应的 `[ ]` 中打勾：`[x]`

```markdown
- [x] P0-S1: 修复 API Key 泄露 ✅ 已完成
```

### 添加备注

在任务下方添加完成时间和备注：

```markdown
- [x] P0-S1: 修复 API Key 泄露
      **完成时间**: 2025-01-29 14:30
      **备注**: 已撤销旧 Key，生成新 Key，更新 .env
```

### 标记阻塞

如果任务被阻塞，添加说明：

```markdown
- [ ] P1-A3: 重构配置管理系统
      **状态**: ⏸️ 阻塞
      **原因**: 等待 P0-A1 完成
      **预计恢复**: 2025-02-05
```

---

## 🔗 相关文档

- [完整优化报告](./PROJECT_OPTIMIZATION_REPORT.md)
- [优化摘要](./OPTIMIZATION_SUMMARY.md)
- [项目状态](./project_status.md)
- [变更日志](./CHANGELOG.md)

---

**创建时间**: 2025-01-29
**最后更新**: 2025-01-29
**维护者**: AI Assistant
