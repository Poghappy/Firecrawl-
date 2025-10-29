# 🚀 项目优化快速指南

**目标**: 在 1 周内完成最关键的优化，立即见效
**预期收益**: 成本降低 60%，安全风险解除，性能提升 3-5 倍

---

## ⏰ 今天（2 小时）- 紧急安全修复

### 🔴 修复 API Key 泄露（最高优先级）

**问题**: `honolulu_rentals/config.py` 硬编码了 4 个 Firecrawl API Key

**快速修复**（30 分钟）:

```bash
# 1. 运行自动修复脚本
chmod +x scripts/security/fix_api_key_leak.sh
./scripts/security/fix_api_key_leak.sh

# 2. 生成新的 API Key
# 访问: https://firecrawl.dev/app/settings
# 点击 "Generate New Key" 生成 4 个新 Key

# 3. 配置环境变量
cd honolulu_rentals
cp .env.example .env
# 编辑 .env，填入新生成的 Key

# 4. 测试配置
python test_demo.py
```

**撤销泄露的 Key**（必须！）:

1. 访问 <https://firecrawl.dev/app/settings>
2. 撤销这 4 个 Key:
   - fc-31ebbe4647b84fdc975318d372eebea8
   - fc-00857d82ec534e8598df1bae9af9fb28
   - fc-9eb380b0dec74d6ebb6c756ee4de4c5a
   - fc-0a2c801f433d4718bcd8189f2742edf4

---

## 📅 本周（剩余 22 小时）

### 第 1 天（8 小时）- 统一架构

#### ✅ 任务 1: 统一 BaseAgent（4 小时）

**目标**: 消除 BaseScraper 和 BaseAgent 的重复

**步骤**:

```bash
# 1. 查看统一后的示例
cat examples/optimization/01_unified_base_agent.py

# 2. 创建新的统一 BaseAgent
cp examples/optimization/01_unified_base_agent.py src/core/base_agent_v2.py

# 3. 更新 honolulu_rentals 使用新基类
# 修改 honolulu_rentals/scrapers/base_scraper.py

# 4. 测试
python -m pytest tests/ -v
```

**代码重点**:

```python
# src/core/base_agent_v2.py (已优化)
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseAgent(ABC, Generic[T]):
    """统一的智能体基类（支持泛型）"""

    @abstractmethod
    async def collect(self, params: Dict) -> List[dict]:
        """采集原始数据"""
        pass

    @abstractmethod
    async def parse(self, raw_data: List[dict]) -> List[T]:
        """解析为 Pydantic 模型"""
        pass
```

**收益**:

- 减少 200+ 行重复代码
- 统一错误处理
- 新建 Agent 时间减少 50%

---

#### ✅ 任务 2: 成本优化（4 小时）

**目标**: Firecrawl API 成本降低 60%

**步骤**:

```bash
# 1. 查看优化示例
cat examples/optimization/02_cost_optimization.py

# 2. 更新配置文件
# 修改 config/agents/rental_agent.yaml
# 修改 config/agents/news_agent.yaml

# 3. 更新采集代码
# 修改 honolulu_rentals/scrapers/craigslist_scraper.py

# 4. 对比测试
python examples/optimization/02_cost_optimization.py
```

**关键优化**:

1. **启用长缓存** (节省 30%):

   ```yaml
   # config/agents/rental_agent.yaml
   firecrawl:
     max_age: 86400000 # 改为 24 小时
   ```

2. **Map + Batch 替代 Crawl** (节省 50%):

   ```python
   # ❌ 昂贵
   result = await app.crawl(url, limit=500)

   # ✅ 优化
   urls = await app.map(url)
   result = await app.batch_scrape(urls[:100])
   ```

3. **智能去重** (节省 30%):

   ```python
   # 过滤最近 24h 采集过的 URL
   new_urls = filter_recent_urls(urls)
   result = await app.batch_scrape(new_urls)
   ```

**预期成本**:

- 优化前: ~$120/月
- 优化后: ~$48/月
- 节省: **$72/月 (-60%)**

---

### 第 2 天（8 小时）- 异步优化 + 测试

#### ✅ 任务 3: 异步代码统一（4 小时）

**目标**: 所有采集代码改为异步，性能提升 3-5 倍

**步骤**:

```bash
# 1. 查找所有同步代码
grep -r "from firecrawl import FirecrawlApp" honolulu_rentals/

# 2. 批量替换
# honolulu_rentals/scrapers/base_scraper.py
# honolulu_rentals/scrapers/craigslist_scraper.py
# honolulu_rentals/main.py

# 3. 更新导入
sed -i '' 's/from firecrawl import FirecrawlApp/from firecrawl import AsyncFirecrawl/g' honolulu_rentals/scrapers/*.py

# 4. 更新方法签名（手动）
# def scrape_all() -> 改为 async def scrape_all() ->
# self.app.scrape() 改为 await self.app.scrape()
```

**关键改动**:

```python
# ❌ Before (同步)
from firecrawl import FirecrawlApp

class CraigslistScraper:
    def __init__(self, api_key: str):
        self.app = FirecrawlApp(api_key=api_key)

    def scrape_all(self) -> List[RentalListing]:
        result = self.app.scrape(url)
        return self.parse(result)

# ✅ After (异步)
from firecrawl import AsyncFirecrawl

class CraigslistScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def scrape_all(self) -> List[RentalListing]:
        async with AsyncFirecrawl(api_key=self.api_key) as app:
            result = await app.scrape(url)
            return await self.parse(result)
```

**性能提升**: **3-5 倍**（并发请求）

---

#### ✅ 任务 4: 添加核心测试（4 小时）

**目标**: 测试覆盖率从 30% 提升到 60%

**步骤**:

```bash
# 1. 创建测试目录
mkdir -p tests/unit tests/integration

# 2. 添加核心测试
cat > tests/unit/test_base_agent.py << 'EOF'
import pytest
from src.core.base_agent import BaseAgent, AgentConfig

@pytest.mark.asyncio
async def test_agent_initialization():
    """测试 Agent 初始化"""
    config = AgentConfig(
        name="test",
        type="test",
        api_key="test-key"
    )

    # Mock Agent
    class MockAgent(BaseAgent):
        async def collect(self, params):
            return [{"title": "test"}]

        async def parse(self, raw_data):
            return raw_data

    agent = MockAgent(config)
    assert agent.config.name == "test"
    assert agent.config.max_concurrent == 10
EOF

# 3. 运行测试
pytest tests/unit/ -v

# 4. 查看覆盖率
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**最小测试集**:

- `test_base_agent.py` - BaseAgent 核心功能
- `test_models.py` - Pydantic 模型验证
- `test_config.py` - 配置加载
- `test_agent_factory.py` - Agent 工厂

---

### 第 3 天（6 小时）- 工厂模式 + 文档

#### ✅ 任务 5: 实现 Agent 工厂（4 小时）

**步骤**:

```bash
# 1. 复制示例代码
cp examples/optimization/03_agent_factory.py src/core/agent_factory.py

# 2. 集成到项目
# 更新 src/core/__init__.py

# 3. 更新使用代码
# 简化 Agent 创建流程
```

**使用对比**:

```python
# ❌ Before (12 行代码)
from honolulu_rentals.config import PLATFORMS
from honolulu_rentals.scrapers.craigslist_scraper import CraigslistScraper

platform_config = PLATFORMS["craigslist"]
api_key = platform_config["api_key"]
scraper = CraigslistScraper(api_key=api_key)
listings = scraper.scrape_all()

# ✅ After (2 行代码)
agent = await AgentFactory.create("rental")
result = await agent.execute({})

# 节省 10 行代码！
```

---

#### ✅ 任务 6: 更新文档（2 小时）

**步骤**:

```bash
# 1. 更新 README.md
# 添加优化后的快速开始示例

# 2. 更新 project_status.md
# 记录已完成的优化

# 3. 创建优化变更日志
cat >> CHANGELOG.md << 'EOF'
## [v2.2.0] - 2025-01-29

### 🔐 安全修复
- 修复 API Key 硬编码问题
- 添加 pre-commit 安全检查

### ⚡ 性能优化
- 统一异步代码，性能提升 3-5 倍
- Firecrawl 成本优化，节省 60%
- 实现智能缓存和去重

### 🏗️ 架构优化
- 统一 BaseAgent 和 BaseScraper
- 实现 Agent 工厂模式
- 重构配置管理系统

### ✅ 测试
- 测试覆盖率从 30% 提升到 60%
- 添加单元测试和集成测试
EOF
```

---

## 📊 预期成果

完成本周优化后，项目将获得以下提升：

### 安全性

- ✅ API Key 泄露风险解除
- ✅ 敏感信息从代码中移除
- ✅ Pre-commit 钩子防止再次泄露

### 性能

- ⚡ 异步性能提升：**3-5 倍**
- ⚡ API 成本降低：**60%**
- ⚡ 缓存命中率：**50-70%**

### 代码质量

- 📉 代码重复减少：**200+ 行**
- 📈 测试覆盖率：30% → 60%
- 📈 类型提示覆盖率：70% → 85%

### 开发效率

- 🚀 新建 Agent 时间：减少 **50%**
- 🚀 代码审查时间：减少 **30%**
- 🚀 Bug 修复时间：减少 **40%**

---

## 🛠️ 实用工具

### 1. 项目健康检查

```bash
# 运行健康检查
python scripts/project_health_check.py

# 查看报告
cat docs/reports/health_check_report.md
```

### 2. 安全扫描

```bash
# 扫描硬编码的密钥
grep -r "fc-[a-z0-9]" . --exclude-dir=归档 --exclude-dir=.git

# 扫描密码
grep -r "password.*=" . --include="*.py" --exclude-dir=归档
```

### 3. 成本分析

```bash
# 运行成本分析
python examples/optimization/02_cost_optimization.py

# 查看成本对比报告
```

### 4. 代码质量检查

```bash
# 运行所有检查
make check-all

# 查看详细报告
make lint        # 代码风格
make test        # 运行测试
make cov         # 查看覆盖率
make security    # 安全检查
```

---

## 📝 检查清单

### Day 1 - 安全和架构

- [ ] ✅ 修复 API Key 泄露
- [ ] ✅ 撤销泄露的 Key
- [ ] ✅ 配置新的环境变量
- [ ] ✅ 统一 BaseAgent 架构
- [ ] ✅ 运行测试验证

### Day 2 - 成本和性能

- [ ] ✅ 启用长缓存（24h）
- [ ] ✅ 实现 Map + Batch 策略
- [ ] ✅ 添加智能去重
- [ ] ✅ 实现成本监控
- [ ] ✅ 对比测试

### Day 3 - 异步和测试

- [ ] ✅ 所有代码改为异步
- [ ] ✅ 更新 honolulu_rentals
- [ ] ✅ 添加单元测试
- [ ] ✅ 添加集成测试
- [ ] ✅ 覆盖率 >60%

### Day 4 - 工厂模式

- [ ] ✅ 实现 Agent 工厂
- [ ] ✅ 简化创建流程
- [ ] ✅ 批量创建支持
- [ ] ✅ 更新文档

### Day 5 - 验证和部署

- [ ] ✅ 完整回归测试
- [ ] ✅ 性能基准测试
- [ ] ✅ 更新 CHANGELOG
- [ ] ✅ 发布 v2.2.0

---

## 💡 关键技巧

### 1. 使用 Agent 工厂简化代码

```python
# ❌ 优化前（繁琐）
from honolulu_rentals.config import PLATFORMS
from honolulu_rentals.scrapers.craigslist_scraper import CraigslistScraper

config = PLATFORMS["craigslist"]
scraper = CraigslistScraper(api_key=config["api_key"])
listings = scraper.scrape_all()

# ✅ 优化后（简洁）
agent = await AgentFactory.create("rental")
result = await agent.execute({})
```

### 2. 成本优化三板斧

```python
# 1. 启用缓存
maxAge=86400000  # 24 小时

# 2. Map + Batch
urls = await app.map(base_url)
result = await app.batch_scrape(urls[:100])

# 3. 智能去重
new_urls = filter_recent_urls(urls)
```

### 3. 异步并发

```python
# ❌ 同步（慢）
for url in urls:
    result = app.scrape(url)  # 串行

# ✅ 异步（快 5 倍）
async with AsyncFirecrawl(api_key=key) as app:
    tasks = [app.scrape(url) for url in urls]
    results = await asyncio.gather(*tasks)  # 并行
```

---

## 📈 进度追踪

### 每日进度

| 日期  | 完成任务            | 时间 | 状态      |
| ----- | ------------------- | ---- | --------- |
| Day 1 | 安全修复 + 统一架构 | 8h   | ⏳ 待开始 |
| Day 2 | 成本优化            | 8h   | ⏳ 待开始 |
| Day 3 | 异步优化 + 测试     | 8h   | ⏳ 待开始 |
| Day 4 | 工厂模式            | 6h   | ⏳ 待开始 |
| Day 5 | 验证和发布          | 6h   | ⏳ 待开始 |

### 关键指标

| 指标        | 当前   | 目标    | Week 1 | 状态 |
| ----------- | ------ | ------- | ------ | ---- |
| 测试覆盖率  | 30%    | 60%     | -      | ⏳   |
| API 成本/月 | $120   | $48     | -      | ⏳   |
| 异步代码率  | 50%    | 100%    | -      | ⏳   |
| 安全得分    | 50/100 | 100/100 | -      | ⏳   |
| 代码重复行  | 200+   | <50     | -      | ⏳   |

---

## 🎯 成功标准

完成本周优化后，应达到：

### 必须达标（P0）

- ✅ 所有硬编码 API Key 已移除
- ✅ 泄露的 Key 已撤销
- ✅ BaseAgent 已统一
- ✅ 核心功能有测试覆盖

### 应当达标（P1）

- ✅ Firecrawl 成本降低 >50%
- ✅ 异步代码覆盖率 >90%
- ✅ 测试覆盖率 >50%
- ✅ Agent 工厂已实现

### 最好达标（P2）

- ✅ 文档已更新
- ✅ CHANGELOG 已更新
- ✅ 性能基准测试已添加

---

## 🚀 立即开始

```bash
# 1. 克隆当前分支
git checkout -b feature/week1-optimization

# 2. 运行健康检查
python scripts/project_health_check.py

# 3. 修复 API Key 泄露
./scripts/security/fix_api_key_leak.sh

# 4. 开始优化
# 按照上述计划逐项完成

# 5. 每天提交
git add .
git commit -m "feat: day1 optimization - security and architecture"
git push origin feature/week1-optimization
```

---

## 📞 需要帮助？

如果遇到问题，请：

1. 查看完整报告: [PROJECT_OPTIMIZATION_REPORT.md](./PROJECT_OPTIMIZATION_REPORT.md)
2. 查看任务清单: [OPTIMIZATION_CHECKLIST.md](./OPTIMIZATION_CHECKLIST.md)
3. 查看代码示例: `examples/optimization/`
4. 运行健康检查: `python scripts/project_health_check.py`

---

**创建时间**: 2025-01-29
**维护者**: AI Assistant
**下次审查**: 每周五
