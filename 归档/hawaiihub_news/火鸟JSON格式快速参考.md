# 火鸟新闻 JSON 格式快速参考卡

> **快速查阅手册** - 5 秒找到你需要的格式

---

## 🎯 核心格式速查

### 1️⃣ 火鸟 API 发布格式（最常用）

```json
{
  "title": "新闻标题",
  "description": "摘要/导语",
  "body": "正文内容（Markdown 或 HTML）",
  "keywords": "关键词1,关键词2,关键词3",
  "source": "来源"
}
```

**API 地址**:
```
POST https://hawaiihub.net/api.php?service=article&action=add
```

**响应格式**:
```json
{
  "state": 100,    // 100=成功, 200=失败
  "info": "发布成功",
  "id": 12345      // 文章 ID
}
```

**文章 URL**:
```
https://hawaiihub.net/news/{id}
```

---

### 2️⃣ HawaiiHub 内部格式

```json
{
  "source_id": "hawaii-news-now",
  "source_name": "Hawaii News Now",
  "url": "https://hawaiinewsnow.com/article/123",
  "title": "文章标题",
  "description": "文章摘要",
  "content": "# Markdown 格式正文",
  "scraped_at": "2025-10-28T10:30:00.123Z"
}
```

---

### 3️⃣ NewsAPI 响应格式

```json
{
  "source": { "name": "Hawaii News Now" },
  "title": "文章标题",
  "description": "摘要",
  "url": "https://...",
  "publishedAt": "2025-10-28T09:00:00Z",
  "author": "作者",
  "urlToImage": "https://..."
}
```

---

### 4️⃣ Firecrawl 返回格式

```python
# Python SDK v2
result.url                    # URL
result.markdown               # Markdown 内容
result.html                   # HTML 内容
result.metadata.title         # 标题
result.metadata.description   # 摘要
result.metadata.status_code   # 状态码
```

---

## 📋 字段约束速查

| 字段 | 类型 | 必填 | 长度限制 | 说明 |
|------|------|------|----------|------|
| `title` | String | ✅ | 1-200 | 标题 |
| `description` | String | ⚠️ | 0-500 | 摘要 |
| `body` | String | ✅ | 100+ | 正文 |
| `keywords` | String | ⚠️ | 逗号分隔 | 关键词 |
| `source` | String | ⚠️ | 1-100 | 来源 |

**图例**:
- ✅ 必填
- ⚠️ 推荐填写

---

## 🔄 格式转换速查

### NewsAPI → HawaiiHub

```python
{
    "source_id": newsapi["source"]["name"].lower().replace(" ", "-"),
    "source_name": newsapi["source"]["name"],
    "url": newsapi["url"],
    "title": newsapi["title"],
    "description": newsapi["description"],
    "content": "",  # 需要 Firecrawl 补充
    "scraped_at": datetime.now().isoformat()
}
```

### HawaiiHub → 火鸟 API

```python
{
    "title": hawaiihub["title"],
    "description": hawaiihub["description"],
    "body": hawaiihub["content"],
    "keywords": extract_keywords(hawaiihub["title"], hawaiihub["content"]),
    "source": hawaiihub["source_name"]
}
```

### Firecrawl → HawaiiHub

```python
{
    "url": result.url,
    "title": result.metadata.title,
    "description": result.metadata.description,
    "content": result.markdown,
    "scraped_at": datetime.now().isoformat()
}
```

---

## 💡 常用代码片段

### 1. 火鸟 API 发布

```python
import requests

payload = {
    "title": "标题",
    "description": "摘要",
    "body": "正文",
    "keywords": "关键词1,关键词2",
    "source": "来源"
}

response = requests.post(
    "https://hawaiihub.net/api.php?service=article&action=add",
    json=payload
)

if response.json()["state"] == 100:
    print(f"✅ 发布成功: https://hawaiihub.net/news/{response.json()['id']}")
```

---

### 2. Firecrawl 采集

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-xxx")
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    only_main_content=True
)

print(result.markdown)
```

---

### 3. 数据验证

```python
from pydantic import BaseModel, Field

class FirebirdArticle(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=500)
    body: str = Field(..., min_length=100)
    keywords: str | None = None
    source: str | None = None

# 验证
try:
    article = FirebirdArticle(**data)
    print("✅ 验证通过")
except ValidationError as e:
    print(f"❌ 验证失败: {e}")
```

---

### 4. 关键词提取

```python
import re
from collections import Counter

def extract_keywords(title: str, content: str, max_n: int = 5) -> str:
    text = f"{title} {content}"
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
    stopwords = {'的', '了', '在', '是', 'the', 'a', 'an'}
    words = [w for w in words if w not in stopwords and len(w) > 1]
    counter = Counter(words)
    top = [word for word, _ in counter.most_common(max_n)]
    return ','.join(top)
```

---

### 5. 内容清洗

```python
import re

def clean_content(content: str) -> str:
    # 移除广告
    patterns = [
        r'Subscribe to.*newsletter',
        r'Advertisement',
        r'Related Articles'
    ]
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # 规范化空白
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)

    return content.strip()
```

---

## 🎯 完整工作流（复制即用）

```python
from firecrawl import FirecrawlApp
import requests
from datetime import datetime

# 1. 初始化
app = FirecrawlApp(api_key="fc-xxx")

# 2. 采集新闻
url = "https://civilbeat.org/article/456"
result = app.scrape(url, formats=["markdown"], only_main_content=True)

# 3. 准备数据
payload = {
    "title": result.metadata.title,
    "description": result.metadata.description,
    "body": result.markdown,
    "keywords": "夏威夷,新闻",  # 或使用 extract_keywords()
    "source": "Civil Beat"
}

# 4. 发布
response = requests.post(
    "https://hawaiihub.net/api.php?service=article&action=add",
    json=payload
)

# 5. 处理结果
if response.json()["state"] == 100:
    article_id = response.json()["id"]
    print(f"✅ 发布成功: https://hawaiihub.net/news/{article_id}")
else:
    print(f"❌ 发布失败: {response.json()['info']}")
```

---

## 📊 数据流向图

```
NewsAPI
  ↓ (发现 URLs)
Firecrawl 采集
  ↓ (完整内容 + Markdown)
HawaiiHub 处理
  ↓ (标准化 + 清洗)
火鸟 API 发布
  ↓ (JSON 格式)
发布成功 ✅
```

---

## ⚡ 快速决策

### 我应该用什么格式？

| 场景 | 使用格式 |
|------|----------|
| **发布到火鸟系统** | 火鸟 API 格式 |
| **从 NewsAPI 获取** | NewsAPI 格式 → 转换 |
| **内部数据处理** | HawaiiHub 格式 |
| **采集网页内容** | Firecrawl 格式 → 转换 |

---

## 🔍 常见问题速查

### Q: 正文用 Markdown 还是 HTML？

**A**: 推荐 **Markdown**，更简洁易维护。需要时可转换为 HTML。

---

### Q: 关键词怎么填？

**A**: 3-8 个关键词，逗号分隔。格式：`地域,主题,扩展`

示例: `夏威夷,租房,房价,住房危机`

---

### Q: 如何判断发布是否成功？

**A**: 检查响应的 `state` 字段：
- `100` = 成功
- `200` = 失败

---

### Q: 文章链接在哪？

**A**: `https://hawaiihub.net/news/{id}`

其中 `{id}` 是 API 响应中的 `id` 字段。

---

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| [火鸟JSON格式规范](./火鸟新闻JSON格式规范.md) | 完整规范（30 页） |
| [代码示例](./firebird_json_examples.py) | 可运行示例 |
| [HawaiiHub README](./README.md) | 项目说明 |
| [快速开始](./QUICK_START.md) | 5 分钟上手 |

---

## 🚀 立即开始

### 方法 1: 运行示例代码

```bash
cd /Users/zhiledeng/Downloads/FireShot/hawaiihub_news
python3 firebird_json_examples.py
```

### 方法 2: 查看完整文档

```bash
# 在 Cursor 中打开
cursor 火鸟新闻JSON格式规范.md
```

### 方法 3: 直接复制模板

```json
{
  "title": "你的标题",
  "description": "你的摘要",
  "body": "# 你的正文\n\n详细内容...",
  "keywords": "关键词1,关键词2,关键词3",
  "source": "你的来源"
}
```

---

**快速参考卡版本**: v1.0
**更新时间**: 2025-10-28
**维护者**: HawaiiHub AI Team

**打印提示**: 建议打印此文档贴在显示器旁边，随时查阅 📄✨
