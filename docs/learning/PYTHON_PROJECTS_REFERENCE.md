# 🐍 Python 项目参考指南 - 从 TypeScript 到 Python

**创建时间**: 2025-10-29
**目标**: 将 Firecrawl 官方示例的核心思想迁移到 Python 项目

---

## 📊 已下载的官方示例分析

### 1. ⭐ Fire Enrich - 数据丰富工具

**技术栈**: TypeScript + Next.js + Firecrawl + OpenAI
**GitHub**: <https://github.com/mendableai/fire-enrich>
**Stars**: 957+

**核心架构**:

```
多 Agent 系统 (Sequential Execution)
├─ Discovery Agent (Phase 1) - 发现公司基本信息
├─ Profile Agent (Phase 2) - 行业分类
├─ Funding Agent (Phase 3) - 融资信息
├─ Tech Stack Agent (Phase 4) - 技术栈
└─ General Purpose Agent (Phase 5) - 自定义字段
```

**可借鉴的核心思想** ✅:

1. **顺序执行 Agent**：每个 Agent 基于前一个的结果
2. **并行搜索**：每个 Agent 内部并行执行多个搜索
3. **数据合成**：最后用 LLM 合并所有结果
4. **类型安全**：使用 Zod Schema（Python 用 Pydantic）

**Python 实现建议**:

```python
# src/agents/enrichment_agent.py
from src.core import BaseAgent
from pydantic import BaseModel

class EnrichmentAgent(BaseAgent):
    """数据丰富智能体"""

    async def execute(self, email: str) -> dict:
        # Phase 1: Discovery
        discovery = await self.discovery_phase(email)

        # Phase 2: Profile
        profile = await self.profile_phase(discovery)

        # Phase 3: Funding
        funding = await self.funding_phase(profile)

        # Phase 4: Tech Stack
        tech = await self.tech_stack_phase(profile)

        # Final Synthesis
        return await self.synthesize(discovery, profile, funding, tech)

    async def discovery_phase(self, email: str):
        """并行搜索基本信息"""
        domain = email.split('@')[1]

        tasks = [
            self.client.search(f"{domain} company"),
            self.client.search(f"what is {domain}"),
            self.client.scrape(f"https://{domain}")
        ]

        results = await asyncio.gather(*tasks)
        return self.extract_discovery_data(results)
```

---

### 2. 🔧 Open Agent Builder - 工作流构建器

**技术栈**: TypeScript + Next.js + LangGraph + Convex + Clerk
**GitHub**: <https://github.com/firecrawl/open-agent-builder>
**Stars**: 1700+

**核心架构**:

```
Visual Workflow Builder
├─ Start Node - 输入
├─ Agent Node - LLM 推理
├─ MCP Tool Node - Firecrawl 调用
├─ Transform Node - 数据处理
├─ If/Else Node - 条件分支
├─ While Loop Node - 循环
├─ User Approval Node - 人工审核
└─ End Node - 输出
```

**可借鉴的核心思想** ✅:

1. **LangGraph 工作流引擎**：状态管理、条件路由
2. **MCP 工具集成**：标准化工具调用协议
3. **人工审核节点**：敏感操作需要确认
4. **实时流式更新**：WebSocket/SSE

**Python 实现建议**:

```python
# src/workflow/graph.py
from langgraph.graph import StateGraph
from typing import TypedDict

class WorkflowState(TypedDict):
    """工作流状态"""
    url: str
    content: str
    summary: str
    approved: bool

async def scrape_node(state: WorkflowState):
    """Firecrawl 抓取节点"""
    result = await firecrawl.scrape(state["url"])
    return {"content": result.markdown}

async def analyze_node(state: WorkflowState):
    """AI 分析节点"""
    summary = await llm.invoke(f"总结：{state['content']}")
    return {"summary": summary}

async def approval_node(state: WorkflowState):
    """人工审核节点"""
    # 等待用户确认
    approved = await wait_for_approval(state)
    return {"approved": approved}

# 构建工作流
workflow = StateGraph(WorkflowState)
workflow.add_node("scrape", scrape_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("approval", approval_node)
workflow.add_edge("scrape", "analyze")
workflow.add_edge("analyze", "approval")

# 执行
result = await workflow.invoke({"url": "https://example.com"})
```

---

### 3. 🚀 Open Lovable - 网站克隆工具

**技术栈**: TypeScript + Next.js + Firecrawl + Anthropic Claude
**GitHub**: <https://github.com/firecrawl/open-lovable>
**Stars**: 21400+

**核心架构**:

```
Website → AI React App
├─ Firecrawl 抓取网站内容
├─ Claude 分析页面结构
├─ 生成 React 组件代码
└─ Vercel Sandbox 预览
```

**可借鉴的核心思想** ✅:

1. **页面结构分析**：提取语义化结构
2. **代码生成**：模板化生成
3. **实时预览**：沙箱环境
4. **迭代优化**：用户反馈 → 重新生成

**Python 实现建议**:

```python
# src/agents/website_cloner.py
class WebsiteCloner(BaseAgent):
    """网站克隆智能体"""

    async def clone(self, url: str) -> str:
        # 1. 抓取网站
        result = await self.client.scrape(
            url,
            formats=["markdown", "html", "screenshot"]
        )

        # 2. 分析结构
        structure = await self.analyze_structure(result)

        # 3. 生成代码
        code = await self.generate_code(structure)

        # 4. 保存文件
        return self.save_template(code)

    async def analyze_structure(self, result):
        """分析页面结构"""
        prompt = f"""
        分析以下网页结构，提取：
        - 导航栏
        - Hero 区域
        - 功能区块
        - Footer

        HTML: {result.html}
        """
        return await self.llm.invoke(prompt)
```

---

## 🎯 适合 Python 的 GitHub 项目推荐

### 官方推荐（Python 版本）

#### 1. ⭐ Firecrawl + LangChain 示例

**GitHub**: <https://github.com/langchain-ai/langchain/tree/master/cookbook>
**适用场景**: RAG 系统、Agent 架构

```python
from langchain.document_loaders import FirecrawlLoader

# 使用 Firecrawl 作为 LangChain 数据源
loader = FirecrawlLoader(
    url="https://example.com",
    mode="scrape",
    params={"formats": ["markdown"]}
)
docs = loader.load()
```

#### 2. 🔥 Firecrawl Python SDK 官方示例

**位置**: `firecrawl-py/examples/`
**内容**:

- `scrape_example.py` - 基础抓取
- `crawl_example.py` - 网站爬取
- `search_example.py` - 搜索示例
- `batch_scrape_example.py` - 批量抓取

#### 3. 📊 数据分析管道

**GitHub**: <https://github.com/mendableai/firecrawl-examples>
**示例**:

- 新闻聚合器
- 价格监控
- 竞品分析
- 数据丰富

---

## 🏗️ 我们项目的架构对标

### 对标 Fire Enrich（多 Agent 系统）

**我们的实现**:

```python
# src/agents/news_agent.py - 对标 Discovery Agent
class NewsAgent(BaseAgent):
    async def collect(self, params):
        # 并行搜索多个新闻源
        tasks = [
            self.search_source(source)
            for source in self.config.sources
        ]
        return await asyncio.gather(*tasks)

# src/agents/recruitment_agent.py - 对标 Profile Agent
class RecruitmentAgent(BaseAgent):
    async def enrich_job(self, job_url):
        # 抓取 + LLM 提取
        content = await self.client.scrape(job_url)
        return await self.extract_structured(content)
```

### 对标 Open Agent Builder（工作流系统）

**我们的实现**:

```python
# src/workflow/pipeline.py
class DataPipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, func):
        self.stages.append(func)

    async def execute(self, data):
        for stage in self.stages:
            data = await stage(data)
        return data

# 使用
pipeline = DataPipeline()
pipeline.add_stage(scrape_stage)
pipeline.add_stage(parse_stage)
pipeline.add_stage(validate_stage)
pipeline.add_stage(save_stage)

result = await pipeline.execute({"url": "https://example.com"})
```

---

## 🔍 从 TypeScript 迁移的核心概念

### 1. 类型系统对比

| TypeScript      | Python             | 说明     |
| --------------- | ------------------ | -------- |
| `interface`     | `class (Pydantic)` | 数据结构 |
| `Zod`           | `Pydantic`         | 数据验证 |
| `async/await`   | `async/await`      | 异步编程 |
| `Promise.all()` | `asyncio.gather()` | 并发执行 |
| `Map<K,V>`      | `Dict[K,V]`        | 映射     |

**TypeScript (Fire Enrich)**:

```typescript
const DiscoveryResult = z.object({
  companyName: z.string().optional(),
  website: z.string().optional(),
  domain: z.string(),
});
```

**Python (我们的项目)**:

```python
from pydantic import BaseModel

class CompanyInfo(BaseModel):
    company_name: Optional[str] = None
    website: Optional[str] = None
    domain: str
```

### 2. Agent 架构对比

**TypeScript (Fire Enrich)**:

```typescript
class DiscoveryAgent implements AgentBase {
  async execute(email: string): Promise<DiscoveryResult> {
    const searches = await Promise.all([firecrawl.search(`${domain} company`), firecrawl.search(`what is ${domain}`)]);
    return this.extract(searches);
  }
}
```

**Python (我们的项目)**:

```python
from src.core import BaseAgent

class DiscoveryAgent(BaseAgent):
    async def execute(self, email: str) -> CompanyInfo:
        domain = email.split('@')[1]

        searches = await asyncio.gather(
            self.client.search(f"{domain} company"),
            self.client.search(f"what is {domain}")
        )

        return await self.extract(searches)
```

### 3. 配置管理对比

**TypeScript (Open Agent Builder)**:

```typescript
// config/app.config.ts
export const config = {
  firecrawl: {
    apiKey: process.env.FIRECRAWL_API_KEY,
    maxConcurrent: 5,
  },
  llm: {
    provider: "anthropic",
    model: "claude-sonnet-4.5",
  },
};
```

**Python (我们的项目)**:

```python
# src/firecrawl_config.py
from dataclasses import dataclass
import os

@dataclass
class FirecrawlConfig:
    api_key: str = os.getenv('FIRECRAWL_API_KEY')
    max_concurrent: int = 5

@dataclass
class LLMConfig:
    provider: str = 'anthropic'
    model: str = 'claude-sonnet-4.5'
```

---

## 💡 实战迁移指南

### 步骤 1: 分析 TypeScript 项目核心逻辑

```bash
# 查看 Fire Enrich 的 Agent 架构
cd docs/official-docs/05-应用案例/examples/fire-enrich
code lib/agent-architecture/agents/
```

**关键文件**:

- `discovery-agent.ts` - 发现逻辑
- `profile-agent.ts` - 提取逻辑
- `orchestrator.ts` - 编排逻辑

### 步骤 2: 提取核心算法

从 TypeScript 中提取：

1. 搜索策略（search queries）
2. 数据提取逻辑（extraction patterns）
3. LLM Prompts
4. 错误处理

### 步骤 3: 用 Python 重写

**示例：从 Fire Enrich 提取公司信息**

**TypeScript 原版**:

```typescript
async function searchCompanyInfo(domain: string) {
  const queries = [`${domain} company about`, `${domain} official website`, `what is ${domain} company`];

  const results = await Promise.all(queries.map((q) => firecrawl.search({ query: q, limit: 3 })));

  return extractCompanyName(results);
}
```

**Python 迁移版**:

```python
async def search_company_info(domain: str) -> CompanyInfo:
    queries = [
        f"{domain} company about",
        f"{domain} official website",
        f"what is {domain} company"
    ]

    async with AsyncFirecrawl() as client:
        tasks = [
            client.search(query=q, limit=3)
            for q in queries
        ]
        results = await asyncio.gather(*tasks)

    return extract_company_name(results)
```

---

## 🎓 学习路径建议

### Week 1: 阅读和分析

- [ ] Day 1-2: 阅读 Fire Enrich README 和核心代码
- [ ] Day 3-4: 阅读 Open Agent Builder 工作流逻辑
- [ ] Day 5: 提取可复用的算法和 Prompts

### Week 2: 迁移到 Python

- [ ] Day 1-2: 实现第一个 Agent（NewsAgent）
- [ ] Day 3: 添加多 Agent 编排
- [ ] Day 4: 实现工作流管道
- [ ] Day 5: 测试和优化

### Week 3: 扩展和优化

- [ ] Day 1: 添加更多业务 Agent
- [ ] Day 2: 优化并发和缓存
- [ ] Day 3-5: 添加 UI 和监控

---

## 📦 可直接复用的组件

### 1. LLM Prompts（通用）

**从 Fire Enrich 复用**:

```python
# 提取公司信息的 Prompt（可直接用）
EXTRACT_COMPANY_PROMPT = """
从以下内容中提取公司信息：

{content}

提取：
- 公司名称
- 官方网站
- 行业分类
- 成立年份
- 总部位置
"""
```

### 2. 数据验证逻辑

**从 Open Agent Builder 复用**:

```python
from pydantic import BaseModel, validator

class JobPosting(BaseModel):
    title: str
    salary: Optional[str]

    @validator('salary')
    def validate_salary(cls, v):
        if v and not any(char.isdigit() for char in v):
            raise ValueError("Salary must contain numbers")
        return v
```

### 3. 错误重试机制

**从所有项目复用**:

```python
async def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
```

---

## 🔗 相关资源

### 官方文档

- ✅ Firecrawl Python SDK: <https://docs.firecrawl.dev/sdks/python>
- ✅ LangChain 集成: <https://python.langchain.com/docs/integrations/document_loaders/firecrawl>
- ✅ Pydantic 文档: <https://docs.pydantic.dev/>

### 示例代码

- ✅ 本地已下载: `docs/official-docs/05-应用案例/examples/`
- ✅ HawaiiHub 示例: `honolulu_rentals/`
- ✅ 归档示例: `归档/examples/`

### 社区资源

- GitHub Firecrawl Tag: <https://github.com/topics/firecrawl>
- Python + Firecrawl 搜索: <https://github.com/search?q=firecrawl+python>
- LangChain Cookbook: <https://github.com/langchain-ai/langchain/tree/master/cookbook>

---

## 🎯 行动计划

### 立即行动（今天）

1. ✅ 查看 Fire Enrich 的 Agent 实现
2. ✅ 提取 3-5 个可复用的 Prompts
3. ✅ 创建第一个 NewsAgent

### 本周任务

1. 实现 5 个业务 Agent
2. 添加多 Agent 编排
3. 测试完整流程

### 下周目标

1. 优化性能和成本
2. 添加监控和日志
3. 编写文档

---

**总结**: 虽然官方示例是 TypeScript，但核心思想（Agent 架构、工作流编排、数据提取策略）完全可以迁移到 Python。我们已经有了基础架构，现在需要填充业务逻辑！

---

_创建时间: 2025-10-29_
_适用版本: Firecrawl v4.5.0 + Python 3.14_
