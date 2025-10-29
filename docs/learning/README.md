# 📚 Firecrawl 示例项目学习指南

> 本目录包含从官方 Firecrawl 示例项目中学习的笔记和分析

## 🎯 已克隆的示例项目

### 1. Fire Enrich - AI 数据丰富工具

**位置：** `docs/official-docs/05-应用案例/examples/fire-enrich/`
**GitHub：** <https://github.com/firecrawl/fire-enrich> (957 stars)
**技术栈：** Next.js + TypeScript + Tailwind CSS

**核心功能：**

- AI 驱动的数据提取和丰富
- 多 Agent 协作模式
- 公司信息、融资数据、技术栈提取

**关键文件：**

- `/app/api/enrich/route.ts` - 数据丰富核心 API
- `/app/api/scrape/route.ts` - Firecrawl 爬取 API 封装
- `/lib/strategies/agent-enrichment-strategy.ts` - Agent 策略模式实现
- `/lib/strategies/enrichment-strategy.ts` - 基础策略接口
- `/lib/config/enrichment.ts` - 配置管理

**适用场景：**

- ✅ Aloha 招聘网（公司信息丰富）
- ✅ 广告公司（线索收集）
- ✅ 所有需要数据丰富的业务场景

---

### 2. Open Agent Builder - 可视化工作流构建器

**位置：** `docs/official-docs/05-应用案例/examples/open-agent-builder/`
**GitHub：** <https://github.com/firecrawl/open-agent-builder> (1.7k stars)
**技术栈：** Next.js + TypeScript + Convex + LangGraph + Tailwind

**核心功能：**

- 拖拽式 AI Agent 工作流编排
- 实时执行监控
- MCP 工具集成
- 预定义工作流模板

**关键文件：**

- `/app/api/workflow/execute/route.ts` - 工作流执行 API
- `/lib/workflow/langgraph.ts` - LangGraph 工作流引擎
- `/lib/workflow/mcp-registry.ts` - MCP 工具注册表
- `/lib/workflow/templates.ts` - 预定义工作流模板
- `/components/workflow/WorkflowExecutionRenderer.tsx` - 工作流可视化组件
- `/convex/executions.ts` - 执行记录管理
- `/convex/schema.ts` - 数据模型定义

**适用场景：**

- ✅ 所有 8 个业务场景的 Agent 架构参考
- ✅ 学习工作流编排模式
- ✅ 学习 LangGraph 集成

---

### 3. Open Lovable - AI 网站克隆工具

**位置：** `docs/official-docs/05-应用案例/examples/open-lovable/`
**GitHub：** <https://github.com/firecrawl/open-lovable> (21.4k stars)
**技术栈：** Next.js + TypeScript + Tailwind + Bun

**核心功能：**

- 将任何网站转换为现代化 React 应用
- Firecrawl + LLM 结合使用
- 实时代码生成和预览

**关键文件：**

- `/app/page.tsx` - 主页面组件
- `/components/HeroInput.tsx` - 用户输入组件
- `/components/SandboxPreview.tsx` - 预览沙箱
- `/components/CodeApplicationProgress.tsx` - 代码生成进度展示
- `/lib/` - 核心逻辑库（Firecrawl 集成、AI 代码生成）

**适用场景：**

- ✅ 学习网（快速原型开发）
- ✅ 设计公司（网站重构）
- ✅ 学习 Firecrawl + LLM 集成模式

---

## 📖 学习笔记文件

### 1. fire-enrich-analysis.md

- Fire Enrich 项目深度分析
- 数据丰富 Agent 架构
- 策略模式实现细节
- Firecrawl Extract API 使用方法

### 2. agent-builder-patterns.md

- Open Agent Builder 架构分析
- 工作流编排模式
- LangGraph 集成方法
- Convex 后端设计

### 3. open-lovable-insights.md

- Open Lovable 核心逻辑
- Firecrawl + LLM 集成模式
- 代码生成流程分析

### 4. firecrawl-best-practices.md

- Firecrawl API 最佳实践
- 成本优化策略
- 错误处理和重试机制
- 适合我们项目的架构建议

---

## 🎓 学习路径建议

### 第一阶段：理解 API 使用模式（1-2 天）

1. **阅读官方文档**

   - `docs/official-docs/01-快速开始/`
   - `docs/official-docs/02-API参考/`

2. **研究 Fire Enrich 代码**

   ```bash
   cd docs/official-docs/05-应用案例/examples/fire-enrich
   # 重点查看：
   # - app/api/scrape/route.ts
   # - app/api/enrich/route.ts
   # - lib/strategies/
   ```

### 第二阶段：学习 Agent 编排（2-3 天）

3. **分析 Open Agent Builder**

   ```bash
   cd docs/official-docs/05-应用案例/examples/open-agent-builder
   # 重点查看：
   # - lib/workflow/langgraph.ts
   # - lib/workflow/templates.ts
   # - convex/schema.ts
   ```

### 第三阶段：实战开发（3-5 天）

4. **在项目中实现**
   - 基于示例项目架构
   - 创建 8 个业务场景的专用 Agent
   - 使用 AsyncFirecrawl SDK

---

## 🔑 关键技术要点

### 1. Firecrawl API 使用模式

```typescript
// Fire Enrich 示例
import Firecrawl from "@mendable/firecrawl-js";

const firecrawl = new Firecrawl({ apiKey: process.env.FIRECRAWL_API_KEY });

// Scrape + JSON Mode
const result = await firecrawl.scrape({
  url: companyUrl,
  formats: [
    {
      type: "json",
      schema: CompanySchema,
    },
  ],
});
```

### 2. Agent 策略模式

```typescript
// Fire Enrich 策略模式
interface EnrichmentStrategy {
  execute(data: InputData): Promise<EnrichedData>;
}

class AgentEnrichmentStrategy implements EnrichmentStrategy {
  async execute(data: InputData) {
    // 使用 Firecrawl + AI 提取
  }
}
```

### 3. 工作流编排

```typescript
// Open Agent Builder LangGraph 模式
import { StateGraph } from "@langchain/langgraph";

const workflow = new StateGraph({
  channels: {
    data: { value: [] },
    status: { value: "idle" },
  },
});

workflow
  .addNode("scrape", scrapeNode)
  .addNode("extract", extractNode)
  .addNode("enrich", enrichNode)
  .addEdge("scrape", "extract")
  .addEdge("extract", "enrich");
```

---

## 📊 项目对比分析

| 特性               | Fire Enrich        | Open Agent Builder | Open Lovable       |
| ------------------ | ------------------ | ------------------ | ------------------ |
| **主要功能**       | 数据丰富           | 工作流编排         | 网站克隆           |
| **后端架构**       | Next.js API Routes | Convex             | Next.js API Routes |
| **状态管理**       | React State        | Convex Real-time   | React State        |
| **AI 集成**        | OpenAI             | LangGraph + OpenAI | OpenAI             |
| **Firecrawl 使用** | Extract + Scrape   | MCP + Scrape       | Scrape             |
| **复杂度**         | ⭐⭐⭐ 中等        | ⭐⭐⭐⭐ 高        | ⭐⭐ 简单          |
| **学习价值**       | 数据丰富架构       | 工作流编排         | LLM 集成           |

---

## 🛠️ 下一步行动

1. **深度分析 Fire Enrich**

   - 阅读 `/app/api/enrich/route.ts`
   - 理解策略模式实现
   - 提取可复用的模块

2. **学习 Open Agent Builder**

   - 分析 LangGraph 工作流
   - 理解 MCP 工具集成
   - 学习 Convex 实时数据库

3. **应用到我们的项目**
   - 创建 BaseAgent 基类
   - 实现 8 个业务场景的 Agent
   - 集成 Firecrawl Cloud API

---

## 📝 更新日志

- **2025-10-29**：克隆 3 个核心示例项目
  - Fire Enrich (数据丰富)
  - Open Agent Builder (工作流编排)
  - Open Lovable (网站克隆)
- **下一步**：深度分析各项目架构，提取最佳实践

---

## 🔗 相关资源

- **Firecrawl 官网**：<https://firecrawl.dev>
- **官方文档**：<https://docs.firecrawl.dev>
- **API 参考**：<https://docs.firecrawl.dev/api-reference>
- **GitHub 组织**：<https://github.com/firecrawl>
- **Discord 社区**：<https://discord.gg/gSmWdAkdwd>
