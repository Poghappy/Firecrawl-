# Web Scraping APIs

> 自动化网页内容获取。关键概念：动态内容、反爬虫机制和数据检索。

**问题数量**: 19个（四个类别中最多）

## 常见问题列表

### 反爬机制与检测

1. [网站如何检测网络爬虫？](https://www.firecrawl.dev/glossary/web-scraping-apis/how-do-websites-detect-web-scrapers)

2. [什么是反爬虫机制？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-anti-scraping-mechanism)

3. [什么是浏览器指纹识别规避？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-browser-fingerprinting-evasion-web-scraping)

4. [什么是自动验证码破解？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-automatic-captcha-solving-web-scraping)

### HTTP 状态码

5. [网络爬取中的 HTTP 状态码有哪些？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-are-http-status-codes-web-scraping)

6. [什么是 200 状态码？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-200-status-code)

7. [什么是 402 错误？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-402-error-web-scraping)

8. [什么是 403 错误？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-403-error-web-scraping)

9. [什么是 404 错误？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-404-error-web-scraping)

10. [什么是 429 错误？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-429-error-web-scraping)

### 数据提取技术

11. [什么是 CSS 选择器？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-css-selector-web-scraping)

12. [什么是 XPath 选择器？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-xpath-selector-in-web-scraping)

13. [什么是正则表达式（regex）？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-are-regular-expressions-regex-web-scraping)

14. [什么是 JavaScript 渲染？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-javascript-rendering-web-scraping)

15. [什么是 OCR（光学字符识别）？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-ocr-in-web-scraping)

### 代理与网络

16. [什么是爬取中的代理？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-proxy-web-scraping)

17. [住宅代理 vs. 数据中心代理有什么区别？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-residential-proxy-vs-datacenter-proxy)

### 核心概念

18. [什么是网络爬取 API？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-web-scraping-api)

19. [网络爬取 API 与传统爬取有什么区别？](https://www.firecrawl.dev/glossary/web-scraping-apis/what-is-difference-between-web-scraping-api-and-traditional-scraping)

---

## 元数据

- **来源URL**: https://www.firecrawl.dev/glossary/web-scraping-apis
- **爬取时间**: 2025-10-27T07:13:59.004Z
- **状态码**: 200
- **缓存状态**: 命中
- **消耗积分**: 1
- **页面标题**: Web Scraping APIs Glossary | Firecrawl
- **描述**: Automated web content fetching. Key concepts: dynamic content, anti-bot mechanisms, and data retrieval. Browse definitions, explanations, and answers to common questions about web scraping apis.

## 核心概念

### 动态内容 (Dynamic Content)

通过 JavaScript 加载的网页内容，需要浏览器渲染才能获取

### 反爬虫机制 (Anti-bot Mechanisms)

网站用来检测和阻止自动化爬虫的技术（如 CAPTCHA、速率限制、指纹识别）

### 数据检索 (Data Retrieval)

从网页中提取和获取所需信息的过程

## 重要技术说明

### 常见 HTTP 状态码

- **200**: 成功响应
- **402**: 需要付费（Payment Required）
- **403**: 禁止访问（Forbidden）
- **404**: 页面未找到（Not Found）
- **429**: 请求过多（Too Many Requests）

### 选择器类型

- **CSS 选择器**: 使用 CSS 语法定位 HTML 元素（如 `.class`, `#id`, `div > p`）
- **XPath 选择器**: 使用路径表达式定位 XML/HTML 节点（如 `//div[@class='content']`）

### 代理类型

- **住宅代理**: 使用真实 IP 地址，更难被检测，但成本较高
- **数据中心代理**: 来自数据中心的 IP，速度快成本低，但容易被识别

---

**返回**: [术语表主页](https://www.firecrawl.dev/glossary)

**Firecrawl 最新动态**: 刚完成 A 轮融资并发布 Firecrawl /v2 🎉
