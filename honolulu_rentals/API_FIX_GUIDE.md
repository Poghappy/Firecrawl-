# 🔧 Firecrawl API 调用修复指南

## 当前状态

✅ **系统架构** - 完成
✅ **数据模型** - 完成
✅ **导出功能** - 完成
⚠️ **Firecrawl API 调用** - 需要修复

---

## 问题说明

当前 `craigslist_scraper.py` 中的 Firecrawl API 调用参数格式不正确。

**错误信息**：

```
FirecrawlClient.scrape() takes 2 positional arguments but 3 were given
```

---

## 解决方案

### 方法 1: 使用关键字参数（推荐）

```python
# ❌ 错误的调用方式
result = self.app.scrape(
    self.search_url,
    {
        "formats": ["links"],
        "onlyMainContent": False,
    }
)

# ✅ 正确的调用方式
result = self.app.scrape_url(
    url=self.search_url,
    params={
        "formats": ["links"],
        "onlyMainContent": False,
    }
)
```

### 方法 2: 查看 Firecrawl SDK 文档

请参考官方文档确认正确的 API 调用方式：

```bash
# 查看 SDK 版本
pip show firecrawl-py

# 查看 SDK 源码
python3 -c "import firecrawl; print(firecrawl.__file__)"
```

### 方法 3: 使用 MCP Firecrawl 工具（推荐）

如果直接 SDK 调用有问题，可以使用 MCP 工具：

```python
from mcp_client import firecrawl_scrape

result = firecrawl_scrape(
    url="https://honolulu.craigslist.org/search/apa",
    formats=["links"],
    maxAge=0
)
```

---

## 测试步骤

1. **查看 SDK 方法签名**：

   ```python
   from firecrawl import FirecrawlApp
   import inspect

   app = FirecrawlApp(api_key="test")
   print(inspect.signature(app.scrape))
   ```

2. **测试最简调用**：

   ```python
   from firecrawl import FirecrawlApp

   app = FirecrawlApp(api_key="fc-31ebbe4647b84fdc975318d372eebea8")
   result = app.scrape("https://firecrawl.dev")
   print(result)
   ```

3. **逐步添加参数**：

   ```python
   # 测试 1: 只传 URL
   result = app.scrape("https://firecrawl.dev")

   # 测试 2: 添加 formats
   result = app.scrape("https://firecrawl.dev", formats=["markdown"])

   # 测试 3: 添加更多参数
   result = app.scrape(
       "https://firecrawl.dev",
       formats=["markdown", "links"],
       onlyMainContent=True
   )
   ```

---

## 临时解决方案

在修复 API 调用之前，您可以：

1. **使用演示脚本**查看系统功能：

   ```bash
   python3 test_demo.py
   ```

2. **查看示例输出**：

   ```bash
   cat data/exports/rentals_demo_*.md
   ```

3. **验证数据模型和导出**功能正常。

---

## 正式版修复步骤

### Step 1: 确认 SDK 版本和方法

```bash
cd honolulu_rentals
python3 << 'EOF'
from firecrawl import FirecrawlApp
import inspect

app = FirecrawlApp(api_key="test")

print("=" * 60)
print("Firecrawl SDK Methods:")
print("=" * 60)
for method in dir(app):
    if not method.startswith('_'):
        print(f"- {method}")

print("\n" + "=" * 60)
print("scrape() signature:")
print("=" * 60)
print(inspect.signature(app.scrape))

if hasattr(app, 'scrape_url'):
    print("\n" + "=" * 60)
    print("scrape_url() signature:")
    print("=" * 60)
    print(inspect.signature(app.scrape_url))
EOF
```

### Step 2: 修改 `scrapers/craigslist_scraper.py`

根据 Step 1 的结果，修正 `get_listing_urls()` 方法中的 API 调用。

### Step 3: 测试修复

```bash
python3 main.py
```

---

## 常见问题

### Q1: 如何查看完整的 SDK 文档？

A: 访问 <https://docs.firecrawl.dev/sdks/python>

### Q2: 能否跳过 Firecrawl 直接爬取？

A: 可以，但会失去很多优势（反爬、JS 渲染、数据清洗等）。不推荐。

### Q3: MCP 工具的优势是什么？

A: MCP 工具封装了 Firecrawl API，提供更简洁的接口，且与 Cursor 深度集成。

---

## 联系支持

如果以上方法都无法解决问题：

1. 查看日志：`tail -100 logs/rentals.log`
2. 检查 API Key：确认 4 个 API Key 都有效
3. 访问 Firecrawl 官方文档
4. GitHub Issues: <https://github.com/mendableai/firecrawl/issues>

---

**最后更新**: 2025-10-29
