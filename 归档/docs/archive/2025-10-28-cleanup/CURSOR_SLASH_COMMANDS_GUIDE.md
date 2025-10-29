# Cursor Slash Commands 完整指南

> **学习时间**: 2025-10-27
> **项目**: FireShot（Firecrawl 专项）
> **参考文档**: https://cursor.com/cn/docs/cli/reference/slash-commands

---

## 📚 什么是 Slash Commands？

Slash Commands（斜杠命令）是 Cursor AI 编辑器中的快捷指令系统，通过输入 `/` 触发，可以快速执行常见编程任务。

**核心价值**：

- ⚡️ 减少重复性工作
- 🎯 精准的代码操作
- 🤖 AI 驱动的智能辅助
- 📝 标准化工作流

---

## 🎯 核心 Slash Commands

### 1. `/edit` - 智能代码编辑

**功能**: 使用自然语言描述修改代码

**使用场景**:

```python
# 示例 1: 添加类型注解
/edit 为这个函数添加完整的类型注解

# 示例 2: 重构代码
/edit 将这个函数重构为使用 Pydantic 模型

# 示例 3: 优化性能
/edit 优化这段代码的性能，使用缓存机制
```

**FireShot 项目应用**:

```python
# 当前代码
def scrape_news(url):
    return app.scrape(url)

# 使用 /edit 添加错误处理和类型注解
/edit 添加完整的错误处理、类型注解和中文 docstring

# AI 生成结果
def scrape_news(url: str, max_retries: int = 3) -> dict | None:
    """
    爬取新闻内容

    Args:
        url: 新闻 URL
        max_retries: 最大重试次数

    Returns:
        爬取结果，失败返回 None
    """
    for attempt in range(max_retries):
        try:
            return app.scrape(url, formats=["markdown"], only_main_content=True)
        except Exception as e:
            logging.error(f"爬取失败: {url} - {e}")
            if attempt == max_retries - 1:
                return None
```

---

### 2. `/fix` - 自动修复错误

**功能**: 修复代码中的 Bug、Linter 错误、类型错误

**使用场景**:

```python
# 示例 1: 修复 Linter 错误
/fix 修复所有 Ruff 检测到的错误

# 示例 2: 修复类型错误
/fix 修复 mypy 类型检查错误

# 示例 3: 修复运行时错误
/fix 修复 AttributeError: 'Document' object has no attribute 'get'
```

**FireShot 常见错误修复**:

```python
# 错误代码（SDK v1 风格）
result = app.scrape(url, onlyMainContent=True)
content = result.get("markdown")

# 使用 /fix 自动修复为 SDK v2
/fix 修复为 Firecrawl SDK v2 语法

# 修复后
result = app.scrape(url, only_main_content=True)
content = result.markdown
```

---

### 3. `/explain` - 代码解释

**功能**: 解释代码的工作原理

**使用场景**:

```python
# 示例 1: 解释复杂逻辑
/explain 这个密钥轮换机制是如何工作的？

# 示例 2: 解释设计模式
/explain 这里为什么使用 itertools.cycle？

# 示例 3: 解释配置
/explain .cursor/settings.json 中的自动批准规则
```

**实际应用**:

```python
# 选中以下代码后输入 /explain
class RotatingFirecrawlClient:
    def __init__(self, api_keys: List[str]):
        self.api_keys = itertools.cycle(api_keys)
        self.current_key = next(self.api_keys)

# AI 解释：
"""
这是一个 API 密钥轮换机制：
1. itertools.cycle() 将密钥列表转换为无限循环迭代器
2. 每次调用 next() 自动切换到下一个密钥
3. 用于突破单个密钥的速率限制
4. 当所有密钥用完后会自动回到第一个（循环）
"""
```

---

### 4. `/test` - 生成测试代码

**功能**: 为选中的代码生成单元测试

**使用场景**:

```python
# 示例 1: 生成基础测试
/test 为这个函数生成 pytest 测试

# 示例 2: 生成边界测试
/test 生成包含边界情况的测试

# 示例 3: 生成 Mock 测试
/test 生成使用 Mock 的测试（不实际调用 API）
```

**FireShot 测试生成**:

```python
# 原始代码
def safe_scrape(url: str, max_retries: int = 3) -> dict | None:
    """安全爬取，带重试和日志"""
    for attempt in range(max_retries):
        try:
            result = app.scrape(url, formats=["markdown"], only_main_content=True)
            return result
        except RequestTimeoutError:
            if attempt == max_retries - 1:
                return None

# 使用 /test 生成测试
/test 生成完整的 pytest 测试，包含成功、超时、重试场景

# AI 生成（tests/test_scraper.py）
import pytest
from unittest.mock import Mock, patch
from firecrawl.exceptions import RequestTimeoutError

def test_safe_scrape_success():
    """测试：成功爬取"""
    mock_result = Mock()
    mock_result.markdown = "# 测试内容"

    with patch("firecrawl.FirecrawlApp.scrape", return_value=mock_result):
        result = safe_scrape("https://test.com")

    assert result is not None
    assert result.markdown == "# 测试内容"

def test_safe_scrape_timeout():
    """测试：超时重试机制"""
    with patch("firecrawl.FirecrawlApp.scrape", side_effect=RequestTimeoutError):
        result = safe_scrape("https://test.com", max_retries=2)

    assert result is None

def test_safe_scrape_retry_success():
    """测试：第2次重试成功"""
    mock_result = Mock()
    mock_result.markdown = "# 成功"

    with patch("firecrawl.FirecrawlApp.scrape", side_effect=[
        RequestTimeoutError,
        mock_result
    ]):
        result = safe_scrape("https://test.com", max_retries=3)

    assert result is not None
```

---

### 5. `/doc` - 生成文档

**功能**: 为代码生成文档字符串（Docstring）

**使用场景**:

```python
# 示例 1: 生成函数文档
/doc 生成中文 docstring（PEP 257 格式）

# 示例 2: 生成类文档
/doc 为这个类生成完整文档（包括属性和方法）

# 示例 3: 生成模块文档
/doc 为这个 Python 模块生成顶部文档
```

**FireShot 文档生成**:

```python
# 原始代码（无文档）
def batch_scrape(urls: List[str]) -> List[dict]:
    results = []
    for url in urls:
        result = app.scrape(url, formats=["markdown"])
        results.append(result)
    return results

# 使用 /doc 生成文档
/doc 生成完整的中文文档，包括参数、返回值、异常、示例

# AI 生成
def batch_scrape(urls: List[str]) -> List[dict]:
    """
    批量爬取网页内容

    Args:
        urls: 要爬取的 URL 列表

    Returns:
        爬取结果列表，每个元素为包含 markdown 内容的字典

    Raises:
        RequestTimeoutError: 请求超时
        RateLimitError: 超出速率限制

    Example:
        >>> urls = ["https://example.com", "https://test.com"]
        >>> results = batch_scrape(urls)
        >>> len(results)
        2

    Note:
        建议使用 Firecrawl 的 batch_scrape 方法以获得更好的性能
    """
    results = []
    for url in urls:
        result = app.scrape(url, formats=["markdown"])
        results.append(result)
    return results
```

---

### 6. `/commit` - 生成提交消息

**功能**: 根据代码更改生成符合规范的 Git commit 消息

**使用场景**:

```bash
# 示例 1: 生成标准 commit
/commit 生成 Conventional Commits 格式的消息

# 示例 2: 生成详细 commit
/commit 生成包含详细变更说明的 commit 消息

# 示例 3: 生成多语言 commit
/commit 生成中英文双语 commit 消息
```

**FireShot Commit 规范**:

```bash
# 当前更改：添加了缓存机制

# 使用 /commit 生成
/commit 生成符合项目规范的 commit 消息

# AI 生成
feat(scraper): 实现 Redis 缓存机制，节省 50% 成本

- 添加 cached_scrape 函数，使用 Redis 缓存
- 设置 1 小时缓存过期时间
- 添加缓存命中率统计
- 更新文档说明缓存使用方法

Closes #123

# 或者生成中英文双语
feat(scraper): 实现 Redis 缓存机制 / Implement Redis caching

- 添加缓存层，节省 50%+ API 调用成本
- Add Redis caching layer, saving 50%+ API costs
- 缓存有效期：1小时
- Cache TTL: 1 hour
```

---

### 7. `/review` - 代码审查

**功能**: AI 审查代码，发现潜在问题

**使用场景**:

```python
# 示例 1: 安全审查
/review 检查这段代码的安全问题

# 示例 2: 性能审查
/review 审查性能瓶颈

# 示例 3: 最佳实践审查
/review 检查是否符合 Python 最佳实践
```

**FireShot 代码审查示例**:

````python
# 提交以下代码进行审查
def scrape_all_news():
    urls = get_all_urls()  # 假设返回 1000 个 URL
    for url in urls:
        result = app.scrape(url)
        save_to_db(result)

# 使用 /review 审查
/review 审查这段代码的性能和成本问题

# AI 反馈
"""
⚠️ 发现的问题：

1. **性能问题**（严重）
   - 串行处理 1000 个 URL，预计耗时 >30 分钟
   - 建议：使用 batch_scrape 并发处理

2. **成本问题**（严重）
   - 1000 个请求约 $10，可能超出每日预算
   - 建议：添加预算检查和进度保存

3. **错误处理缺失**（中等）
   - 没有异常处理，一个失败会终止整个流程
   - 建议：添加 try-except 和重试逻辑

4. **缺少缓存**（中等）
   - 重复 URL 会浪费成本
   - 建议：添加缓存检查

建议修改：
```python
def scrape_all_news(batch_size: int = 50) -> None:
    \"\"\"批量爬取新闻（优化版）\"\"\"
    urls = get_all_urls()

    # 预算检查
    estimated_cost = len(urls) * 0.01
    if estimated_cost > DAILY_BUDGET:
        raise BudgetError(f"预计成本 ${estimated_cost} 超出预算")

    # 批量处理
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i+batch_size]

        try:
            results = app.batch_scrape(batch_urls, formats=["markdown"])
            for result in results:
                save_to_db(result)

            logging.info(f"已完成 {i+len(batch_urls)}/{len(urls)}")

        except Exception as e:
            logging.error(f"批次失败: {e}")
            continue
````

"""

````

---

## 🔥 FireShot 项目专用 Slash Commands

### `/firecrawl` - Firecrawl 专项命令

**自定义命令示例**（可配置到 .cursor/rules/）:

```python
# 在 .cursor/rules/firecrawl-commands.mdc 中定义

# /firecrawl scrape <url>
/firecrawl scrape https://example.com
# 自动使用项目规范：下划线命名、错误处理、类型注解、中文文档

# /firecrawl batch <file>
/firecrawl batch urls.txt
# 批量爬取，自动添加进度条、成本监控、结果保存

# /firecrawl analyze <file>
/firecrawl analyze data.json
# 生成数据分析报告（Markdown 格式）
````

---

## ⚙️ Cursor 配置优化

### 1. 自动批准配置

**当前项目配置**（`.cursor/settings.json`）:

```json
{
  "ai.autoApproveToolCalls": true,
  "ai.autoApproveReadOperations": true,
  "ai.autoApproveBrowserOperations": true,
  "ai.autoApproveFileOperations": true,
  "ai.autoApproveSearchOperations": true,
  "ai.toolCallApproval": {
    "browser_navigate": "auto",
    "browser_snapshot": "auto",
    "browser_click": "auto",
    "browser_type": "auto",
    "browser_screenshot": "auto",
    "read_file": "auto",
    "grep": "auto",
    "codebase_search": "auto",
    "list_dir": "auto",
    "glob_file_search": "auto"
  },
  "ai.dangerousOperationsRequireApproval": true,
  "ai.dangerousOperations": ["delete_file", "run_terminal_cmd", "search_replace", "write"]
}
```

**含义**：

- ✅ 自动批准：读取文件、搜索、浏览器操作
- ⚠️ 需要确认：删除文件、运行命令、修改代码

---

### 2. 规则优先级配置

**当前项目规则**（`.cursor/rules/`）:

```
00-hawaiihub-core.mdc       (priority: 1000) - 核心规范
01-code-standards.mdc       (priority: 900)  - 代码规范
99-deployment-safety.mdc    (priority: 100)  - 部署安全
```

**优先级说明**：

- 数字越大，优先级越高
- 冲突时高优先级规则覆盖低优先级
- 建议：核心规则 1000，专项规则 500-900，安全规则 100

---

## 🎓 最佳实践

### 1. Slash Command 组合技

**场景：重构旧代码为项目规范**

```python
# 步骤 1: 解释代码
/explain 这段代码的功能是什么？

# 步骤 2: 审查问题
/review 检查是否符合 FireShot 项目规范

# 步骤 3: 修复问题
/fix 修复为 SDK v2 语法，添加类型注解和错误处理

# 步骤 4: 生成文档
/doc 生成完整的中文 docstring

# 步骤 5: 生成测试
/test 生成完整的 pytest 测试

# 步骤 6: 提交代码
/commit 生成 Conventional Commits 格式消息
```

---

### 2. 快捷键绑定

**在 Cursor 设置中自定义**:

```json
{
  "keybindings": [
    {
      "key": "cmd+shift+e",
      "command": "cursor.edit",
      "when": "editorTextFocus"
    },
    {
      "key": "cmd+shift+f",
      "command": "cursor.fix",
      "when": "editorTextFocus"
    },
    {
      "key": "cmd+shift+t",
      "command": "cursor.test",
      "when": "editorTextFocus"
    }
  ]
}
```

---

### 3. 批量操作

**使用 Slash Commands 批量处理文件**:

```bash
# 示例 1: 批量添加类型注解
# 选中 scripts/ 目录下所有 .py 文件
/edit 为所有函数添加完整的类型注解（List、Dict、Optional）

# 示例 2: 批量生成测试
# 选中 src/ 目录
/test 为每个 Python 文件生成对应的测试文件到 tests/

# 示例 3: 批量修复 Linter 错误
/fix 修复所有 Ruff 检测到的导入顺序问题
```

---

## 📊 项目配置检查清单

### ✅ 已完成配置

1. **核心规则文件**
   - ✅ `.cursorrules`（850 行，完整的 Firecrawl 规范）
   - ✅ `.cursor/rules/00-hawaiihub-core.mdc`（HawaiiHub 核心规范）
   - ✅ `.cursor/rules/01-code-standards.mdc`（代码质量规范）
   - ✅ `.cursor/rules/99-deployment-safety.mdc`（部署安全协议）

2. **自动批准设置**
   - ✅ `.cursor/settings.json`（已配置安全的自动批准规则）

3. **项目结构**
   - ✅ `docs/` - 文档目录
   - ✅ `scripts/` - 工具脚本
   - ✅ `src/` - 源代码
   - ✅ `tests/` - 测试代码

### ⚠️ 推荐优化

1. **添加自定义 Slash Commands**

   ```python
   # 创建 .cursor/rules/custom-commands.mdc
   # 定义 /firecrawl、/hawaiihub 等专项命令
   ```

2. **配置快捷键**

   ```json
   // .cursor/keybindings.json
   // 为常用 Slash Commands 绑定快捷键
   ```

3. **添加代码片段**
   ```json
   // .cursor/snippets/python.json
   // 定义常用的 Firecrawl 代码模板
   ```

---

## 🚀 快速启动

### 1. 打开 Cursor

```bash
cd /Users/zhiledeng/Downloads/FireShot
cursor .
```

### 2. 尝试 Slash Commands

```python
# 打开任意 Python 文件，输入：
/explain 这个文件的作用是什么？

# 选中一个函数，输入：
/doc 生成中文文档

# 修改代码后，输入：
/commit 生成 commit 消息
```

### 3. 查看 AI 响应

- Cursor 会自动分析代码
- 根据项目规则生成符合规范的输出
- 所有输出自动使用简体中文

---

## 📚 参考资源

### 官方文档

- Cursor 文档: https://cursor.com/cn/docs
- Slash Commands: https://cursor.com/cn/docs/cli/reference/slash-commands
- 规则配置: https://cursor.com/cn/docs/rules

### FireShot 项目文档

- `.cursorrules` - 完整项目规范
- `FIRECRAWL_CLOUD_SETUP_GUIDE.md` - Firecrawl 快速上手
- `SDK_CONFIGURATION_COMPLETE.md` - SDK 配置总结

---

**版本**: v1.0.0
**最后更新**: 2025-10-27
**维护者**: HawaiiHub AI Team
**适用项目**: FireShot + HawaiiHub
