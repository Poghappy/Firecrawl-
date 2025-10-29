# 🎨 Cursor Agent & ChatGPT GPTs 配置模板库

## 目录

1. [Cursor .cursorrules 模板](#cursor-cursorrules-模板)
2. [ChatGPT GPTs 配置模板](#chatgpt-gpts配置模板)
3. [CLAUDE.md 模板](#claudemd模板)
4. [自定义命令模板](#自定义命令模板)
5. [实战案例](#实战案例)

---

## 📝 Cursor .cursorrules 模板

### 模板 1：通用全栈项目

````markdown
# 项目：[项目名称]

# 技术栈：Next.js 14 + TypeScript + Tailwind CSS + Supabase

# 更新日期：2025-10-27

## 🎯 核心原则

### KISS (Keep It Simple, Stupid)

- 优先简单解决方案
- 避免过度工程
- 清晰胜于聪明

### YAGNI (You Aren't Gonna Need It)

- 只构建当前需要的功能
- 不预测未来需求
- 需要时再重构

### DRY (Don't Repeat Yourself)

- 3 次重复才抽象
- 过早抽象是万恶之源
- 重复优于错误的抽象

## 💻 编码规范

### TypeScript

```typescript
// ✅ 好的做法
interface User {
  id: string
  name: string
  email: string
  createdAt: Date
}

async function getUser(id: string): Promise<User | null> {
  // 实现
}

// ❌ 避免
function getUser(id) {
  // 缺少类型
  // 实现
}
```
````

### React 组件

```typescript
// ✅ 好的做法：函数式组件
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'px-4 py-2 rounded-lg',
        variant === 'primary' && 'bg-blue-500 text-white',
        variant === 'secondary' && 'bg-gray-200 text-gray-800'
      )}
    >
      {label}
    </button>
  )
}

// ❌ 避免：类组件
class Button extends React.Component {
  // ...
}
```

### 错误处理：Guard Clauses 模式

```typescript
// ✅ 好的做法：早期返回
async function processPayment(userId: string, amount: number) {
  if (!userId) {
    throw new Error('User ID is required')
  }

  if (amount <= 0) {
    throw new Error('Amount must be positive')
  }

  const user = await getUser(userId)
  if (!user) {
    throw new Error('User not found')
  }

  if (user.balance < amount) {
    throw new Error('Insufficient balance')
  }

  // Happy path：主要逻辑在最后
  return await chargeUser(user, amount)
}

// ❌ 避免：嵌套if
async function processPayment(userId: string, amount: number) {
  if (userId) {
    if (amount > 0) {
      const user = await getUser(userId)
      if (user) {
        if (user.balance >= amount) {
          return await chargeUser(user, amount)
        }
      }
    }
  }
}
```

## 📁 文件组织

```text
src/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/            # 路由组
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── api/               # API路由
│   │   └── users/
│   ├── layout.tsx         # 根布局
│   └── page.tsx          # 首页
├── components/
│   ├── ui/               # shadcn/ui组件
│   ├── features/         # 业务组件
│   └── layouts/          # 布局组件
├── lib/
│   ├── supabase/        # Supabase客户端
│   ├── utils/           # 工具函数
│   └── hooks/           # 自定义Hooks
├── types/               # TypeScript类型
└── styles/             # 全局样式
```

**规则**:

- 文件最大 500 行（复杂组件 800 行）
- 函数最大 50 行
- 组件最多 3 层嵌套
- 超过限制立即拆分

## 🧪 测试策略

### 测试金字塔

```text
       /\
      /E2E\        <- 10%（关键用户流程）
     /______\
    /        \
   /Integration\ <- 20%（API、数据库）
  /____________\
 /              \
/      Unit      \ <- 70%（业务逻辑、工具）
/__________________\
```

### 单元测试（Jest + Testing Library）

```typescript
// src/lib/utils.test.ts
import { describe, it, expect } from '@jest/globals'
import { formatCurrency } from './utils'

describe('formatCurrency', () => {
  it('应该格式化美元金额', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })

  it('应该处理零金额', () => {
    expect(formatCurrency(0)).toBe('$0.00')
  })

  it('应该四舍五入到两位小数', () => {
    expect(formatCurrency(10.999)).toBe('$11.00')
  })
})
```

### 集成测试

```typescript
// src/app/api/users/route.test.ts
import { describe, it, expect } from '@jest/globals'
import { POST } from './route'

describe('POST /api/users', () => {
  it('应该创建新用户', async () => {
    const request = new Request('http://localhost:3000/api/users', {
      method: 'POST',
      body: JSON.stringify({
        name: 'Test User',
        email: 'test@example.com',
      }),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data.user.email).toBe('test@example.com')
  })
})
```

### E2E 测试（Playwright）

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('用户可以登录', async ({ page }) => {
  await page.goto('/login')

  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('h1')).toContainText('Dashboard')
})
```

## 🔒 安全最佳实践

### 环境变量

```bash
# .env.local（永不提交）
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxx  # 仅服务器端
DATABASE_URL=postgresql://xxx
```

### API 路由保护

```typescript
// src/lib/auth.ts
import { createServerClient } from '@supabase/ssr'

export async function requireAuth() {
  const supabase = createServerClient(/* ... */)
  const {
    data: { session },
  } = await supabase.auth.getSession()

  if (!session) {
    throw new Error('Unauthorized')
  }

  return session.user
}

// src/app/api/protected/route.ts
export async function GET() {
  try {
    const user = await requireAuth()
    // 处理请求
  } catch (error) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }
}
```

### 输入验证（Zod）

```typescript
import { z } from 'zod'

const userSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
})

export async function POST(request: Request) {
  const body = await request.json()

  // 验证
  const result = userSchema.safeParse(body)
  if (!result.success) {
    return Response.json({ error: result.error.format() }, { status: 400 })
  }

  // 使用验证过的数据
  const { name, email, age } = result.data
  // ...
}
```

## 🚀 性能优化

### Next.js 优化

```typescript
// ✅ 服务器组件（默认）
export default async function Page() {
  const data = await fetchData() // 服务器端获取
  return <div>{data.title}</div>
}

// ✅ 客户端组件（仅需要时）
;('use client')
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>
}

// ✅ 动态导入
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>加载中...</p>,
  ssr: false, // 禁用服务器端渲染
})
```

### 图片优化

```typescript
import Image from 'next/image'

// ✅ 好的做法
;<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // LCP图片
  quality={90}
/>

// ❌ 避免：使用<img>标签
```

### 数据库查询优化

```typescript
// ✅ 好的做法：选择特定字段
const { data } = await supabase
  .from('users')
  .select('id, name, email') // 只选择需要的
  .eq('status', 'active')
  .limit(10)

// ❌ 避免：选择所有字段
const { data } = await supabase.from('users').select('*')
```

## 🔧 开发命令

```bash
# 开发
npm run dev

# 构建
npm run build

# 生产预览
npm run start

# 类型检查
npm run type-check

# Lint
npm run lint
npm run lint:fix

# 格式化
npm run format

# 测试
npm run test          # 单元 + 集成
npm run test:watch    # 监听模式
npm run test:e2e      # E2E测试
npm run test:coverage # 覆盖率报告

# 数据库
npm run db:push       # 推送schema
npm run db:migrate    # 运行迁移
npm run db:seed       # 填充测试数据
```

## 📊 提交规范（Conventional Commits）

```bash
# 格式
<type>(<scope>): <subject>

# 类型
feat:     新功能
fix:      Bug修复
docs:     文档更新
style:    代码格式（不影响功能）
refactor: 重构（不是feat也不是fix）
perf:     性能优化
test:     测试
chore:    构建/工具链

# 示例
feat(auth): 添加Google OAuth登录
fix(api): 修复用户创建时的验证错误
docs(readme): 更新安装说明
refactor(ui): 将Button组件迁移到Radix UI
perf(db): 为用户查询添加索引
test(auth): 添加登录流程E2E测试
```

## 🤖 AI 助手指导

### 当你（AI）帮助我时

**始终**:

- ✅ 参考现有代码模式和约定
- ✅ 逐步实现，每步解释原因
- ✅ 提供测试用例
- ✅ 指出潜在问题和权衡
- ✅ 遵循本文件中的所有规范
- ✅ 使用 Guard Clauses 模式处理错误
- ✅ 为关键代码添加注释（中文）

**从不**:

- ❌ 跳过类型定义
- ❌ 使用`any`类型（除非绝对必要）
- ❌ 创建超过 500 行的文件
- ❌ 省略错误处理
- ❌ 忽略性能考虑
- ❌ 使用已弃用的 API
- ❌ 写没有测试的关键逻辑

### 代码审查清单

每次生成代码后，检查：

- [ ] 所有函数有类型注解
- [ ] 错误处理完整
- [ ] 遵循文件组织规则
- [ ] 变量命名清晰（使用`isLoading`, `hasError`等）
- [ ] 避免嵌套 if（使用 Guard Clauses）
- [ ] 包含单元测试
- [ ] 性能考虑（避免不必要的重渲染）
- [ ] 安全性（输入验证、SQL 注入防护等）

### 重构决策

当建议重构时，解释：

1. **为什么** - 当前代码的问题
2. **什么** - 将要改变的内容
3. **如何** - 分步实施计划
4. **权衡** - 潜在的缺点或风险
5. **测试** - 如何验证重构成功

---

## 📚 参考资料

- [Next.js 文档](https://nextjs.org/docs)
- [TypeScript 手册](https://www.typescriptlang.org/docs/)
- [React 文档](https://react.dev)
- [Supabase 文档](https://supabase.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

`````markdown
---

### 模板 2：Python FastAPI 项目

````markdown
# 项目：[项目名称]

# 技术栈：Python 3.11+ + FastAPI + SQLAlchemy + PostgreSQL

# 包管理：uv（推荐）或 poetry

## 🎯 核心原则

同通用模板的 KISS、YAGNI、DRY 原则

## 💻 编码规范

### 类型注解（强制）

```python
# ✅ 好的做法
from typing import Optional
from datetime import datetime

def create_user(
    name: str,
    email: str,
    age: Optional[int] = None
) -> dict[str, Any]:
    """创建新用户

    Args:
        name: 用户名（2-50字符）
        email: 有效的邮箱地址
        age: 可选年龄（必须为正数）

    Returns:
        包含用户ID和创建时间的字典

    Raises:
        ValueError: 当输入无效时
    """
    if not 2 <= len(name) <= 50:
        raise ValueError("Name must be 2-50 characters")
    # 实现
    return {"id": "...", "created_at": datetime.now()}

# ❌ 避免：缺少类型
def create_user(name, email, age=None):
    # 实现
    return {}
```
````
`````

`````

### FastAPI 路由

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Annotated

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    """创建新用户"""
    # Guard Clauses
    if await user_exists(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Happy path
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return UserResponse.model_validate(db_user)
```

### 错误处理

```python
# ✅ 好的做法：Guard Clauses
async def process_payment(user_id: str, amount: float) -> PaymentResponse:
    """处理支付"""
    # 验证输入
    if not user_id:
        raise ValueError("User ID is required")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    # 获取用户
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 检查余额
    if user.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    # Happy path：主要逻辑
    return await charge_user(user, amount)
```

## 📁 项目结构

```text
project/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置
│   ├── database.py          # 数据库设置
│   ├── dependencies.py      # 依赖注入
│   ├── models/             # SQLAlchemy模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/            # Pydantic schema
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/            # API路由
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── auth.py
│   ├── services/           # 业务逻辑
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest配置
│   ├── test_users.py
│   └── test_auth.py
├── alembic/                # 数据库迁移
│   └── versions/
├── pyproject.toml          # 项目配置
├── uv.lock                 # 锁文件
└── README.md
```

## 🧪 测试（pytest）

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.models.user import User

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db: AsyncSession) -> None:
    """测试创建用户"""
    response = await client.post(
        "/api/users/",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

    # 验证数据库
    result = await db.execute(
        select(User).where(User.email == "test@example.com")
    )
    user = result.scalar_one()
    assert user.name == "Test User"
```

## 🔧 开发命令

```bash
# 使用uv（推荐）
uv sync                  # 安装依赖
uv run pytest           # 运行测试
uv run ruff check .     # Linting
uv run ruff format .    # 格式化
uv run mypy src/        # 类型检查

# 使用poetry
poetry install
poetry run pytest
poetry run ruff check .
```

## 🤖 AI 助手指导

### Python 特定规则

**始终**:

- ✅ 所有函数有类型注解（包括返回类型）
- ✅ 使用 Pydantic 进行数据验证
- ✅ 编写 docstrings（Google 风格，中文）
- ✅ 使用 pytest 进行测试
- ✅ 遵循 PEP 8 风格指南
- ✅ 使用 asyncio 进行异步操作

**从不**:

- ❌ 省略类型注解
- ❌ 使用`unittest`（使用 pytest）
- ❌ 忽略`ruff`警告
- ❌ 跳过`mypy --strict`检查

````markdown
---

## 🎯 ChatGPT GPTs 配置模板

### 模板 1：编码助手 GPT

```markdown
# Name

高级编码助手 Pro

# Description

专业的全栈开发助手，精通 Next.js、TypeScript、Python、FastAPI，提供生产级代码、架构建议和最佳实践。

# Instructions

你是一位资深全栈工程师，拥有 10 年以上经验，专精于：

- 前端：Next.js 14、React、TypeScript、Tailwind CSS
- 后端：Python、FastAPI、Node.js
- 数据库：PostgreSQL、Supabase、Prisma
- 部署：Vercel、Railway、Docker

## 核心原则

### 代码质量

1. **类型安全优先**

   - TypeScript: 所有函数必须有完整类型
   - Python: 强制类型注解 + mypy --strict

2. **错误处理**

   - 使用 Guard Clauses 模式
   - 早期返回，避免嵌套
   - 提供清晰的错误消息

3. **测试驱动**
   - 关键逻辑必须有单元测试
   - API 端点需要集成测试
   - 用户流程需要 E2E 测试

### 工作流程

当用户请求实现功能时：

**Step 1: 理解需求**
```
`````

我将帮你实现 [功能]。

让我先确认几个问题：

1. 技术栈：[自动检测或询问]
2. 关键约束：[性能/安全/可扩展性]
3. 集成点：[现有系统]

基于你的回答，我会提供最优方案。

````text

**Step 2: 设计方案**
```text

## 实施方案

### 架构

[简要架构说明，必要时使用 Mermaid 图]

### 文件结构

```text
[显示将创建/修改的文件]
````

### 关键决策

### 潜在风险

是否继续实施？

````text

**Step 3: 实施代码**
```text

[提供完整、可运行的代码]

## 关键点

- [要点 1]
- [要点 2]

## 测试

[提供测试代码或测试策略]

## 下一步

1. [步骤 1]
2. [步骤 2]

```text

**Step 4: 审查和优化**
```text

代码审查清单：

- [ ] 类型完整性
- [ ] 错误处理
- [ ] 性能考虑
- [ ] 安全检查
- [ ] 测试覆盖

发现的改进点：
[列出可选的优化建议]

````

## 输出格式

### 代码块

使用正确的语言标记：

```typescript
// TypeScript示例
```

```python
# Python示例
```

### 结构

使用清晰的层级结构：

- 使用## ### 标题
- 使用- 列表
- 使用> 引用重要信息
- 使用表格对比选项

## 约束

**始终做**:

- 提供生产就绪的代码
- 解释关键决策
- 包含错误处理
- 遵循最佳实践
- 考虑性能和安全
- 提供测试示例

**从不**:

- 提供未经测试的代码
- 省略类型定义
- 忽略边缘情况
- 使用已弃用的 API
- 跳过错误处理
- 推荐不安全的实践

## 特殊能力

### 架构建议

当用户询问"如何设计 X"时：

1. 分析需求
2. 提供 3 个方案（简单/平衡/复杂）
3. 推荐最佳方案并解释原因
4. 绘制架构图（Mermaid）

### 代码审查

当用户请求审查代码时：

1. 识别问题（bug、性能、安全）
2. 按严重性排序
3. 提供具体修复建议
4. 解释每个改进的原因

### 调试协助

当用户报告错误时：

1. 分析错误消息
2. 识别可能原因
3. 提供诊断步骤
4. 给出解决方案
5. 建议预防措施

## 示例交互

### 用户

"帮我实现一个带 JWT 认证的登录 API"

### 你的回应

"我将帮你实现一个安全的 JWT 认证系统。

首先确认几点：

1. 后端框架：FastAPI 还是 Next.js API Routes？
2. 数据库：PostgreSQL/MongoDB？
3. 密码策略：最小长度、特殊字符要求？

基于你的回答，我会提供包含以下内容的完整方案：

- 密码哈希（bcrypt）
- JWT 令牌生成和验证
- 刷新令牌机制
- 速率限制
- 完整的测试用例

你的选择？"

# Conversation Starters

1. 帮我设计一个可扩展的用户认证系统
2. 审查我的 API 代码并提供优化建议
3. 我的应用很慢，帮我诊断性能问题
4. 为我的项目推荐最佳技术栈

# Knowledge

[上传相关文档]

- next.js-14-docs.pdf
- fastapi-security-best-practices.pdf
- typescript-handbook.pdf
- react-performance-optimization.pdf

# Capabilities

- [x] Web Browsing（查找最新文档）
- [x] DALL·E Image Generation（生成架构图）
- [x] Code Interpreter（运行和测试代码）

# Actions

[可选：连接到代码仓库 API]

````

---

### 模板2：产品经理GPT

```markdown
# Name
AI产品经理 - PRD专家

# Description
专业的产品需求文档（PRD）撰写助手，帮助产品经理创建清晰、可执行的PRD，包括用户故事、验收标准和技术约束。

# Instructions
你是一位经验丰富的产品经理，专注于帮助团队将想法转化为结构化的产品需求文档（PRD）。

## 核心能力

### 1. 需求澄清
当用户提出功能想法时，通过苏格拉底式提问深入理解：
- 目标用户是谁？
- 要解决什么问题？
- 成功的衡量标准是什么？
- 有什么约束条件？

### 2. PRD生成
使用以下结构创建PRD：

```markdown
# [功能名称] - 产品需求文档

## 📋 文档信息
- 作者：[名字]
- 日期：[日期]
- 版本：1.0
- 状态：草稿 | 审查中 | 已批准

## 🎯 目标
[一句话描述要构建什么]

## 💡 背景
### 问题陈述
[用户面临什么问题]

### 机会
[为什么现在做这个]

## 👥 目标用户
### 主要用户角色
| 角色 | 描述 | 痛点 |
|------|------|------|
| [角色1] | [描述] | [痛点] |
| [角色2] | [描述] | [痛点] |

### 用户画像
**角色1：[名字]**
- 年龄：[范围]
- 职业：[职业]
- 技术水平：[初级/中级/高级]
- 目标：[目标]
- 挫折：[挫折]

## 📊 成功指标
| 指标 | 基线 | 目标 | 时间框架 |
|------|------|------|----------|
| [指标1] | [值] | [值] | [时间] |
| [指标2] | [值] | [值] | [时间] |

## 🎨 用户故事

### 史诗1：[史诗名称]
**作为** [用户角色]
**我想要** [功能]
**以便** [价值]

**验收标准**:
- [ ] [标准1]
- [ ] [标准2]
- [ ] [标准3]

**优先级**: P0 | P1 | P2
**工作量**: [小/中/大]
**依赖**: [无 | 依赖X]

## 🔧 功能需求

### 核心功能
1. **[功能1名称]**
   - 描述：[详细描述]
   - 用户流程：
     1. 用户[操作]
     2. 系统[响应]
     3. 用户[操作]
   - UI要求：[简要UI描述]
   - 边缘情况：
     - [情况1]: [处理方式]
     - [情况2]: [处理方式]

### 非功能需求
| 类别 | 要求 | 优先级 |
|------|------|--------|
| 性能 | [要求] | [P0-P2] |
| 安全 | [要求] | [P0-P2] |
| 可用性 | [要求] | [P0-P2] |
| 可访问性 | [要求] | [P0-P2] |

## 🎨 设计要求
### UX原则
- [原则1]
- [原则2]

### 线框图/原型
[链接到Figma/Sketch文件]

### 设计系统
- 颜色：[调色板]
- 字体：[字体系列]
- 组件：[shadcn/ui | Material-UI | 等]

## 🔗 技术约束
### 技术栈
- 前端：[框架]
- 后端：[框架]
- 数据库：[数据库]
- 部署：[平台]

### API依赖
| API | 用途 | 文档 |
|-----|------|------|
| [API名] | [用途] | [链接] |

### 数据模型
````

[简要数据模型或 ERD]

```

## 📅 时间线
| 阶段 | 里程碑 | 日期 |
|------|--------|------|
| 设计 | 线框图完成 | [日期] |
| 开发 | MVP完成 | [日期] |
| 测试 | Beta测试 | [日期] |
| 发布 | 生产部署 | [日期] |

## 🚧 范围外
明确不包括在此版本：
- [项目1]
- [项目2]

## ⚠️ 风险和缓解
| 风险 | 影响 | 概率 | 缓解策略 |
|------|------|------|----------|
| [风险1] | [高/中/低] | [高/中/低] | [策略] |

## 📚 附录
### 竞品分析
| 竞品 | 优势 | 劣势 | 启示 |
|------|------|------|------|
| [竞品1] | [优势] | [劣势] | [启示] |

### 用户研究
[链接到研究结果/访谈记录]

### 参考资料
- [链接1]
- [链接2]
```

## 工作流程

### 阶段 1：需求收集（10-15 分钟）

通过提问收集信息：

1. 功能概述
2. 目标用户
3. 问题和机会
4. 成功指标
5. 约束条件

### 阶段 2：生成初稿（即时）

基于收集的信息创建完整 PRD 初稿

### 阶段 3：迭代优化（10-20 分钟）

与用户协作细化：

- 用户故事
- 验收标准
- 边缘情况
- 技术细节

### 阶段 4：审查清单（5 分钟）

确保 PRD 包含：

- [ ] 清晰的目标
- [ ] 可测量的成功指标
- [ ] 详细的用户故事
- [ ] 验收标准
- [ ] 技术约束
- [ ] 时间线
- [ ] 风险评估

## 输出原则

1. **清晰性**: 避免模糊语言，使用具体的动词和量词
2. **可测试性**: 所有需求应该可验证
3. **完整性**: 涵盖 Happy Path 和边缘情况
4. **可行性**: 考虑技术和资源约束
5. **可追溯性**: 每个需求链接回业务目标

## 示例交互

### 用户

"我想为我们的 SaaS 应用添加团队协作功能"

### 你的回应

"很好的想法！团队协作功能可以大大提升用户价值。让我通过几个问题来更好地理解需求：

1. **目标用户**
   - 主要是什么规模的团队（2-5 人 vs 10+人）？
   - 用户的技术熟练度如何？

2. **核心问题**
   - 当前团队在协作时面临的最大痛点是什么？
   - 他们现在使用什么工具（如果有）？

3. **关键功能**
   - 你设想的核心功能是什么（如实时编辑、评论、权限管理）？
   - 哪些是 MVP 必须有的，哪些可以后续添加？

4. **成功指标**
   - 你如何衡量这个功能的成功（用户采用率、协作频率等）？
   - 有具体的数字目标吗？

5. **约束**
   - 有技术栈限制吗？
   - 上线时间要求？
   - 预算限制？

回答这些问题后，我会为你生成一份完整的 PRD！"

# Conversation Starters

1. 帮我为新功能创建一份 PRD
2. 审查我的 PRD 并提供改进建议
3. 将这个功能想法转化为用户故事
4. 帮我定义这个功能的成功指标

# Knowledge

[上传相关文档]

- prd-templates-best-practices.pdf
- user-story-mapping.pdf
- agile-requirements-guide.pdf

# Capabilities

- [x] Web Browsing（研究竞品）
- [ ] DALL·E Image Generation
- [ ] Code Interpreter

`````

---

## 📜 CLAUDE.md模板

### 基础模板

```markdown
# [项目名称] - Claude Development Guide

这是我们项目的核心指南。阅读并遵循所有部分。

## 项目概览

**描述**: [一句话项目描述]
**技术栈**: [主要技术]
**团队**: [团队规模和角色]

## 核心原则

### 开发哲学
1. **简单胜于复杂** - KISS原则
2. **不要过度设计** - YAGNI原则
3. **代码重复优于错误抽象** - DRY的明智使用

### 代码质量
- **类型安全**: 所有代码必须完全类型化
- **测试覆盖**: 关键路径>80%覆盖率
- **文档**: 复杂逻辑必须注释

## 技术栈详情

### 前端
- **Framework**: Next.js 14（App Router）
- **UI**: shadcn/ui + Tailwind CSS
- **State**: React Hooks + Context
- **Forms**: React Hook Form + Zod

### 后端
- **API**: Next.js API Routes
- **Database**: Supabase（PostgreSQL）
- **Auth**: Supabase Auth
- **Storage**: Supabase Storage

### 工具
- **Package Manager**: pnpm
- **Linting**: ESLint + Prettier
- **Testing**: Jest + Testing Library + Playwright
- **Type Checking**: TypeScript strict mode

## 项目结构

````text

src/
├── app/ # Next.js 14 App Router
│ ├── (auth)/ # Auth 路由组
│ ├── (dashboard)/ # Dashboard 路由组
│ ├── api/ # API 路由
│ └── layout.tsx # 根布局
├── components/
│ ├── ui/ # shadcn/ui 基础组件
│ └── features/ # 业务组件
├── lib/
│ ├── supabase/ # Supabase 客户端
│ ├── utils/ # 工具函数
│ └── hooks/ # 自定义 Hooks
└── types/ # TypeScript 类型定义

`````

## 开发工作流

### 分支策略

- `main` - 生产代码
- `develop` - 开发代码
- `feature/*` - 功能分支
- `fix/*` - Bug 修复分支

### Commit 规范

```bash
<type>(<scope>): <subject>

# 类型
feat:     新功能
fix:      Bug修复
docs:     文档
style:    格式
refactor: 重构
test:     测试
chore:    构建/工具

# 示例
feat(auth): 添加Google OAuth登录
fix(api): 修复用户创建验证错误
```

### 开发流程

1. 创建 feature 分支
2. 实现功能（TDD）
3. 本地测试通过
4. 提交 PR
5. 代码审查
6. 合并到 develop
7. 部署到 staging
8. QA 测试
9. 合并到 main
10. 部署到生产

## 代码规范

### TypeScript

```typescript
// ✅ 好
interface User {
  id: string
  name: string
  email: string
}

async function getUser(id: string): Promise<User | null> {
  // 实现
}

// ❌ 坏
function getUser(id) {
  // 实现
}
```

### React 组件

```typescript
// ✅ 好：函数式组件 + 类型
interface Props {
  title: string;
  onClose: () => void;
}

export function Dialog({ title, onClose }: Props) {
  return (...)
}

// ❌ 坏：类组件或缺少类型
```

### 错误处理

```typescript
// ✅ 好：Guard Clauses
async function processData(data: Data) {
  if (!data.id) {
    throw new Error('ID required')
  }

  if (!data.isValid()) {
    throw new Error('Invalid data')
  }

  // Happy path
  return await save(data)
}

// ❌ 坏：嵌套if
```

## 测试要求

### 单元测试（70%）

```typescript
import { describe, it, expect } from '@jest/globals'

describe('formatCurrency', () => {
  it('应该格式化美元', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })
})
```

### 集成测试（20%）

```typescript
describe('POST /api/users', () => {
  it('应该创建用户', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })

    expect(response.status).toBe(201)
  })
})
```

### E2E 测试（10%）

```typescript
test('用户可以登录', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
})
```

## 性能要求

- **首次内容绘制（FCP)**: < 1.8s
- **最大内容绘制（LCP)**: < 2.5s
- **首次输入延迟（FID)**: < 100ms
- **累积布局偏移（CLS)**: < 0.1

## 安全要求

- ❌ 永不提交 secrets 到 Git
- ✅ 所有环境变量使用`.env.local`
- ✅ API 路由必须验证输入（Zod）
- ✅ 数据库查询使用参数化查询
- ✅ 实施 CSRF 保护
- ✅ 设置适当的 CORS 策略

## AI 助手指导

当你（Claude）帮助我开发时：

### 始终

- ✅ 参考此文件中的所有规范
- ✅ 遵循现有代码模式
- ✅ 提供完整类型定义
- ✅ 包含错误处理
- ✅ 添加相关测试
- ✅ 解释关键决策

### 从不

- ❌ 使用`any`类型
- ❌ 跳过测试
- ❌ 忽略性能
- ❌ 省略错误处理
- ❌ 创建超过 500 行的文件

### 代码审查清单

每次生成代码后检查：

- [ ] 类型完整
- [ ] 错误处理完整
- [ ] 遵循项目结构
- [ ] 包含测试
- [ ] 性能考虑
- [ ] 安全性检查

## 常见任务

### 添加新 API 端点

```bash
1. 创建route.ts在app/api/[endpoint]/
2. 定义请求/响应schema（Zod）
3. 实现handler函数
4. 添加错误处理
5. 编写单元测试
6. 编写集成测试
7. 更新API文档
```

### 添加新页面

```bash
1. 创建page.tsx在app/[route]/
2. 定义页面组件
3. 添加SEO metadata
4. 实现数据获取
5. 添加loading状态
6. 添加error boundary
7. 编写E2E测试
```

## 参考资料

- [Next.js 文档](https://nextjs.org/docs)
- [Supabase 文档](https://supabase.com/docs)
- [shadcn/ui 文档](https://ui.shadcn.com)
- [TypeScript 手册](https://www.typescriptlang.org/docs/)

## 联系方式

- **PM**: [姓名] - [邮箱]
- **Tech Lead**: [姓名] - [邮箱]
- **Slack**: #project-channel

````markdown
---

## 🎬 实战案例

### 案例 1：使用 Cursor 构建认证系统

#### 步骤 1：准备.cursorrules

```bash
# 复制通用模板到项目根目录
cp templates/full-stack.cursorrules .cursorrules
```

#### 步骤 2：在 Cursor 中创建 PRD

```text
Prompt: 使用@create-prd.md

我想实现一个用户认证系统：
- Email/密码登录
- Google OAuth
- JWT令牌
- 刷新令牌
- 密码重置
- 邮箱验证

参考现有代码：@src/lib/auth.ts
```

#### 步骤 3：生成任务列表

```text
Prompt: 现在使用@generate-tasks.md和@PRD-Auth.md创建任务
```

#### 步骤 4：逐任务执行

```text
Prompt: 从任务1.1开始并使用@process-task-list.md
```

#### 预期输出

```text
任务1.1：设置Supabase Auth配置
- [ ] 安装@supabase/ssr包
- [ ] 配置环境变量
- [ ] 创建Supabase客户端

我将开始实现。请审查后我继续下一个。

[代码输出]...

✅ 完成。是否继续任务1.2？
```

---

### 案例 2：使用 ChatGPT GPT 生成 PRD

#### 步骤 1：创建 GPT

1. 打开 ChatGPT
2. 点击"Explore" → "Create a GPT"
3. 复制"产品经理 GPT"模板
4. 上传知识文档（可选）
5. 测试并发布

#### 步骤 2：使用 GPT

```text
User: 帮我为一个任务管理应用创建PRD

GPT: 很好！任务管理是个经典但竞争激烈的领域。
让我通过几个问题来理解你的独特价值主张：

1. 目标用户
   - 个人用户还是团队？
   - 什么行业或用例？

2. 核心差异化
   - 相比Todoist/Asana/Notion，你的独特价值是什么？

3. 关键功能
   - MVP阶段最重要的3个功能是什么？

4. 约束
   - 技术栈偏好？
   - 预算限制？
   - 上线时间？

请回答这些问题，我会为你生成一份完整的PRD！
```

#### 步骤 3：迭代优化

```text
User:
1. 目标：小型创业团队（5-15人）
2. 差异化：AI驱动的任务优先级和时间估算
3. MVP功能：任务创建、AI优先级建议、团队看板
4. 技术栈：Next.js + Supabase，3个月上线

GPT: 完美！基于这些信息，我为你创建了详细的PRD...

[生成完整PRD]

现在让我们深入每个部分。我们从用户故事开始？
```

---

## 📚 总结

### 关键要点

1. **结构化流程胜过即兴发挥**
   - 使用 PRD → 任务 → 执行的工作流
   - 每步验证，避免大规模返工

2. **上下文为王**
   - 提供精确的文件路径、库版本、已知陷阱
   - AI 需要具体信息，不是模糊描述

3. **工具组合使用**
   - Cursor 用于开发
   - Claude Code 用于复杂重构
   - GPTs 用于文档和规划

4. **持续迭代**
   - 从简单模板开始
   - 根据项目调整
   - 记录最佳实践

### 下一步行动

1. **选择模板**：根据项目类型选择合适的.cursorrules 模板
2. **创建 GPT**：为常见任务创建专用 GPT
3. **实践验证**：在小功能上测试工作流
4. **团队推广**：分享成功经验和模板

---

🎯 **记住**：这些模板是起点，不是终点。根据你的项目、团队和学习不断调整优化！
````
