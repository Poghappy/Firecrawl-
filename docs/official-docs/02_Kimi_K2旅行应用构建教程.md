# Building AI Applications with Kimi K2: A Complete Travel Deal Finder Tutorial

**作者**: Abid Ali Awan  
**发布时间**: Aug 15, 2025  
**原文链接**: https://www.firecrawl.dev/blog/building-ai-applications-with-kimi-k2-travel-deal-finder  
**分类**: AI Engineering, Travel Tech

## 摘要

本文提供了一个完整的教程，介绍如何使用 Kimi K2 AI 模型构建智能旅行优惠查找应用。教程涵盖了从环境设置到部署的完整流程，包括 API 集成、数据处理、用户界面设计和实时优惠监控功能。

## 主要内容

### Kimi K2 简介

Kimi K2 是 Moonshot AI 开发的先进语言模型，具有以下特点：

- **超长上下文**: 支持 200K+ token 的上下文长度
- **多模态能力**: 支持文本、图像和文档处理
- **实时推理**: 快速响应和高质量输出
- **中英双语**: 优秀的中英文理解和生成能力

### 环境设置

#### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv travel_finder_env
source travel_finder_env/bin/activate  # Linux/Mac
# travel_finder_env\Scripts\activate  # Windows

# 安装必要的包
pip install openai firecrawl-py gradio pandas numpy requests beautifulsoup4
```

#### 2. API 密钥配置

```python
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

### Groq Cloud 集成

#### Groq API 设置

```python
from groq import Groq

class GroqClient:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
    
    def generate_response(self, prompt, model="llama3-8b-8192"):
        """使用 Groq 生成响应"""
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model,
                temperature=0.3,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API 错误: {e}")
            return None
```

### Travel Deal Finder 应用构建

#### 1. 核心数据模型

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class TravelDeal:
    title: str
    destination: str
    price: float
    original_price: Optional[float]
    discount_percentage: Optional[float]
    departure_date: datetime
    return_date: Optional[datetime]
    airline: str
    source_url: str
    description: str
    deal_type: str  # flight, hotel, package
    rating: Optional[float]
    reviews_count: Optional[int]
    
@dataclass
class SearchCriteria:
    destination: str
    departure_city: str
    departure_date: datetime
    return_date: Optional[datetime]
    budget_max: Optional[float]
    travelers_count: int
    deal_types: List[str]
```

#### 2. 网页数据抓取器

```python
from firecrawl import FirecrawlApp
import re
from datetime import datetime, timedelta

class TravelDataScraper:
    def __init__(self, firecrawl_api_key):
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        self.travel_sites = [
            "expedia.com",
            "booking.com",
            "kayak.com",
            "skyscanner.com",
            "priceline.com"
        ]
    
    def search_travel_deals(self, criteria: SearchCriteria) -> List[dict]:
        """搜索旅行优惠"""
        all_deals = []
        
        for site in self.travel_sites:
            try:
                # 构建搜索查询
                query = self._build_search_query(criteria, site)
                
                # 使用 Firecrawl 搜索
                results = self.firecrawl.search(
                    query=query,
                    limit=10,
                    scrapeOptions={
                        "formats": ["markdown"],
                        "onlyMainContent": True,
                        "waitFor": 3000
                    }
                )
                
                # 处理搜索结果
                for result in results:
                    deal_data = self._extract_deal_info(result, site)
                    if deal_data:
                        all_deals.append(deal_data)
                        
            except Exception as e:
                print(f"抓取 {site} 时出错: {e}")
                continue
        
        return all_deals
    
    def _build_search_query(self, criteria: SearchCriteria, site: str) -> str:
        """构建搜索查询"""
        query_parts = [
            f"site:{site}",
            f"flights from {criteria.departure_city} to {criteria.destination}",
            f"departure {criteria.departure_date.strftime('%Y-%m-%d')}"
        ]
        
        if criteria.return_date:
            query_parts.append(f"return {criteria.return_date.strftime('%Y-%m-%d')}")
        
        if criteria.budget_max:
            query_parts.append(f"under ${criteria.budget_max}")
        
        return " ".join(query_parts)
    
    def _extract_deal_info(self, result: dict, site: str) -> Optional[dict]:
        """从搜索结果中提取优惠信息"""
        content = result.get('content', '')
        url = result.get('url', '')
        
        # 使用正则表达式提取价格信息
        price_pattern = r'\$([0-9,]+(?:\.[0-9]{2})?)'
        prices = re.findall(price_pattern, content)
        
        if not prices:
            return None
        
        # 提取其他信息
        title = self._extract_title(content)
        airline = self._extract_airline(content)
        
        return {
            'title': title,
            'price': float(prices[0].replace(',', '')),
            'airline': airline,
            'source_url': url,
            'site': site,
            'content': content[:500]  # 保留前500字符用于进一步分析
        }
    
    def _extract_title(self, content: str) -> str:
        """提取标题"""
        lines = content.split('\n')
        for line in lines[:5]:  # 检查前5行
            if len(line.strip()) > 10 and not line.startswith('#'):
                return line.strip()[:100]
        return "Travel Deal"
    
    def _extract_airline(self, content: str) -> str:
        """提取航空公司信息"""
        airlines = ['United', 'Delta', 'American', 'Southwest', 'JetBlue', 'Alaska']
        content_lower = content.lower()
        
        for airline in airlines:
            if airline.lower() in content_lower:
                return airline
        
        return "Unknown"
```

#### 3. AI 分析引擎

```python
class TravelDealAnalyzer:
    def __init__(self, kimi_api_key, groq_client):
        self.kimi_client = self._setup_kimi_client(kimi_api_key)
        self.groq_client = groq_client
    
    def _setup_kimi_client(self, api_key):
        """设置 Kimi API 客户端"""
        from openai import OpenAI
        
        return OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )
    
    def analyze_deals(self, raw_deals: List[dict], criteria: SearchCriteria) -> List[TravelDeal]:
        """分析和结构化旅行优惠数据"""
        analyzed_deals = []
        
        for deal_data in raw_deals:
            try:
                # 使用 Kimi K2 分析优惠详情
                analysis = self._analyze_single_deal(deal_data, criteria)
                
                if analysis:
                    travel_deal = self._create_travel_deal(analysis, deal_data)
                    analyzed_deals.append(travel_deal)
                    
            except Exception as e:
                print(f"分析优惠时出错: {e}")
                continue
        
        return analyzed_deals
    
    def _analyze_single_deal(self, deal_data: dict, criteria: SearchCriteria) -> Optional[dict]:
        """使用 Kimi K2 分析单个优惠"""
        prompt = f"""
        请分析以下旅行优惠信息，并提取结构化数据：
        
        搜索条件：
        - 目的地：{criteria.destination}
        - 出发城市：{criteria.departure_city}
        - 出发日期：{criteria.departure_date}
        - 预算上限：{criteria.budget_max or '无限制'}
        
        优惠信息：
        标题：{deal_data.get('title', '')}
        价格：${deal_data.get('price', 0)}
        航空公司：{deal_data.get('airline', '')}
        来源：{deal_data.get('site', '')}
        内容：{deal_data.get('content', '')}
        
        请提取并返回以下信息（JSON格式）：
        {{
            "destination": "目的地",
            "price": 价格数字,
            "original_price": 原价（如果有折扣）,
            "discount_percentage": 折扣百分比,
            "airline": "航空公司",
            "deal_type": "flight/hotel/package",
            "description": "优惠描述",
            "rating": 评分（1-5）,
            "is_good_deal": true/false
        }}
        """
        
        try:
            response = self.kimi_client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            
            # 尝试解析 JSON 响应
            import json
            return json.loads(result)
            
        except Exception as e:
            print(f"Kimi API 分析错误: {e}")
            return None
    
    def _create_travel_deal(self, analysis: dict, raw_data: dict) -> TravelDeal:
        """创建 TravelDeal 对象"""
        return TravelDeal(
            title=analysis.get('title', raw_data.get('title', '')),
            destination=analysis.get('destination', ''),
            price=analysis.get('price', raw_data.get('price', 0)),
            original_price=analysis.get('original_price'),
            discount_percentage=analysis.get('discount_percentage'),
            departure_date=datetime.now() + timedelta(days=30),  # 默认30天后
            return_date=None,
            airline=analysis.get('airline', raw_data.get('airline', '')),
            source_url=raw_data.get('source_url', ''),
            description=analysis.get('description', ''),
            deal_type=analysis.get('deal_type', 'flight'),
            rating=analysis.get('rating'),
            reviews_count=None
        )
    
    def rank_deals(self, deals: List[TravelDeal], criteria: SearchCriteria) -> List[TravelDeal]:
        """使用 AI 对优惠进行排名"""
        if not deals:
            return []
        
        # 构建排名提示
        deals_summary = "\n".join([
            f"{i+1}. {deal.title} - ${deal.price} - {deal.airline}"
            for i, deal in enumerate(deals)
        ])
        
        prompt = f"""
        请根据以下条件对旅行优惠进行排名：
        
        用户偏好：
        - 目的地：{criteria.destination}
        - 预算：{criteria.budget_max or '灵活'}
        - 旅行者数量：{criteria.travelers_count}
        
        优惠列表：
        {deals_summary}
        
        请返回排名后的优惠编号列表（用逗号分隔），考虑因素：
        1. 价格性价比
        2. 航空公司声誉
        3. 折扣幅度
        4. 用户预算匹配度
        
        示例：3,1,5,2,4
        """
        
        try:
            ranking_result = self.groq_client.generate_response(prompt)
            
            if ranking_result:
                # 解析排名结果
                ranking_indices = [int(x.strip()) - 1 for x in ranking_result.split(',')]
                return [deals[i] for i in ranking_indices if 0 <= i < len(deals)]
        
        except Exception as e:
            print(f"排名错误: {e}")
        
        # 如果 AI 排名失败，按价格排序
        return sorted(deals, key=lambda x: x.price)
```

#### 4. Gradio 用户界面

```python
import gradio as gr
from datetime import datetime, timedelta

class TravelFinderUI:
    def __init__(self, scraper, analyzer):
        self.scraper = scraper
        self.analyzer = analyzer
    
    def create_interface(self):
        """创建 Gradio 界面"""
        with gr.Blocks(title="AI Travel Deal Finder", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🌍 AI Travel Deal Finder")
            gr.Markdown("使用 Kimi K2 和 Firecrawl 找到最佳旅行优惠")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # 搜索参数
                    departure_city = gr.Textbox(
                        label="出发城市",
                        placeholder="例如：New York",
                        value="New York"
                    )
                    
                    destination = gr.Textbox(
                        label="目的地",
                        placeholder="例如：Paris",
                        value="Paris"
                    )
                    
                    departure_date = gr.Date(
                        label="出发日期",
                        value=datetime.now() + timedelta(days=30)
                    )
                    
                    return_date = gr.Date(
                        label="返回日期（可选）",
                        value=datetime.now() + timedelta(days=37)
                    )
                    
                    budget_max = gr.Number(
                        label="最大预算 ($)",
                        value=1000,
                        minimum=0
                    )
                    
                    travelers_count = gr.Number(
                        label="旅行者数量",
                        value=1,
                        minimum=1,
                        maximum=10
                    )
                    
                    deal_types = gr.CheckboxGroup(
                        label="优惠类型",
                        choices=["flight", "hotel", "package"],
                        value=["flight"]
                    )
                    
                    search_btn = gr.Button("🔍 搜索优惠", variant="primary")
                
                with gr.Column(scale=2):
                    # 结果显示
                    results_display = gr.HTML(label="搜索结果")
                    
                    # 详细信息
                    with gr.Accordion("优惠详情", open=False):
                        deal_details = gr.JSON(label="详细数据")
            
            # 搜索事件处理
            search_btn.click(
                fn=self.search_deals,
                inputs=[
                    departure_city,
                    destination,
                    departure_date,
                    return_date,
                    budget_max,
                    travelers_count,
                    deal_types
                ],
                outputs=[results_display, deal_details]
            )
            
            # 示例
            gr.Examples(
                examples=[
                    ["New York", "London", "2024-06-01", "2024-06-08", 800, 2, ["flight"]],
                    ["Los Angeles", "Tokyo", "2024-07-15", "2024-07-25", 1200, 1, ["flight", "hotel"]],
                    ["Chicago", "Barcelona", "2024-08-10", "2024-08-20", 1000, 4, ["package"]]
                ],
                inputs=[
                    departure_city,
                    destination,
                    departure_date,
                    return_date,
                    budget_max,
                    travelers_count,
                    deal_types
                ]
            )
        
        return interface
    
    def search_deals(self, departure_city, destination, departure_date, 
                    return_date, budget_max, travelers_count, deal_types):
        """搜索旅行优惠"""
        try:
            # 创建搜索条件
            criteria = SearchCriteria(
                destination=destination,
                departure_city=departure_city,
                departure_date=datetime.strptime(departure_date, "%Y-%m-%d"),
                return_date=datetime.strptime(return_date, "%Y-%m-%d") if return_date else None,
                budget_max=budget_max if budget_max > 0 else None,
                travelers_count=int(travelers_count),
                deal_types=deal_types
            )
            
            # 搜索原始数据
            raw_deals = self.scraper.search_travel_deals(criteria)
            
            if not raw_deals:
                return "<p>未找到符合条件的优惠，请尝试调整搜索条件。</p>", {}
            
            # AI 分析
            analyzed_deals = self.analyzer.analyze_deals(raw_deals, criteria)
            
            # AI 排名
            ranked_deals = self.analyzer.rank_deals(analyzed_deals, criteria)
            
            # 生成 HTML 结果
            html_results = self._generate_results_html(ranked_deals)
            
            # 生成详细 JSON
            details_json = {
                "search_criteria": {
                    "departure_city": departure_city,
                    "destination": destination,
                    "departure_date": departure_date,
                    "budget_max": budget_max,
                    "travelers_count": travelers_count
                },
                "deals_found": len(ranked_deals),
                "deals": [self._deal_to_dict(deal) for deal in ranked_deals[:5]]
            }
            
            return html_results, details_json
            
        except Exception as e:
            error_msg = f"<p style='color: red;'>搜索出错: {str(e)}</p>"
            return error_msg, {"error": str(e)}
    
    def _generate_results_html(self, deals: List[TravelDeal]) -> str:
        """生成结果 HTML"""
        if not deals:
            return "<p>未找到优惠</p>"
        
        html = "<div style='max-height: 600px; overflow-y: auto;'>"
        
        for i, deal in enumerate(deals[:10]):  # 显示前10个结果
            discount_badge = ""
            if deal.discount_percentage:
                discount_badge = f"<span style='background: #ff4444; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px;'>-{deal.discount_percentage}%</span>"
            
            rating_stars = "⭐" * int(deal.rating or 0)
            
            html += f"""
            <div style='border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; background: white;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='margin: 0; color: #333;'>{deal.title}</h3>
                    {discount_badge}
                </div>
                
                <div style='margin: 10px 0;'>
                    <strong style='font-size: 24px; color: #2196F3;'>${deal.price:.2f}</strong>
                    {f'<span style="text-decoration: line-through; color: #999; margin-left: 10px;">${deal.original_price:.2f}</span>' if deal.original_price else ''}
                </div>
                
                <div style='margin: 5px 0;'>
                    <span style='color: #666;'>🛫 {deal.airline}</span>
                    <span style='margin-left: 20px; color: #666;'>📍 {deal.destination}</span>
                    {f'<span style="margin-left: 20px;">{rating_stars}</span>' if deal.rating else ''}
                </div>
                
                <p style='color: #555; margin: 10px 0;'>{deal.description[:200]}...</p>
                
                <a href='{deal.source_url}' target='_blank' style='color: #2196F3; text-decoration: none;'>查看详情 →</a>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _deal_to_dict(self, deal: TravelDeal) -> dict:
        """将 TravelDeal 转换为字典"""
        return {
            "title": deal.title,
            "destination": deal.destination,
            "price": deal.price,
            "original_price": deal.original_price,
            "discount_percentage": deal.discount_percentage,
            "airline": deal.airline,
            "deal_type": deal.deal_type,
            "rating": deal.rating,
            "source_url": deal.source_url
        }
```

### 主应用程序

```python
def main():
    """主应用程序"""
    print("🌍 启动 AI Travel Deal Finder...")
    
    # 初始化组件
    scraper = TravelDataScraper(FIRECRAWL_API_KEY)
    groq_client = GroqClient(GROQ_API_KEY)
    analyzer = TravelDealAnalyzer(KIMI_API_KEY, groq_client)
    ui = TravelFinderUI(scraper, analyzer)
    
    # 创建并启动界面
    interface = ui.create_interface()
    
    print("✅ 应用程序已启动！")
    print("🌐 访问 http://localhost:7860 使用应用")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

if __name__ == "__main__":
    main()
```

## 技术亮点

### 1. 多模型协作

- **Kimi K2**: 负责复杂的旅行数据分析和结构化
- **Groq**: 提供快速的排名和推荐算法
- **Firecrawl**: 处理大规模网页数据抓取

### 2. 智能数据处理

- **实时抓取**: 从多个旅行网站获取最新优惠
- **AI 分析**: 使用 AI 提取和验证优惠信息
- **智能排名**: 基于用户偏好进行个性化排序

### 3. 用户体验优化

- **直观界面**: 简洁的 Gradio 界面设计
- **实时反馈**: 搜索过程中的状态更新
- **详细信息**: 提供完整的优惠分析数据

## 部署和扩展

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

### 云平台部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  travel-finder:
    build: .
    ports:
      - "7860:7860"
    environment:
      - KIMI_API_KEY=${KIMI_API_KEY}
      - FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./data:/app/data
```

## 最佳实践

### 1. 性能优化

- **缓存机制**: 缓存搜索结果减少 API 调用
- **并行处理**: 同时处理多个旅行网站
- **请求限制**: 遵守网站的爬虫协议

### 2. 错误处理

- **重试机制**: 网络请求失败时自动重试
- **降级策略**: API 不可用时的备选方案
- **用户反馈**: 清晰的错误信息提示

### 3. 数据质量

- **验证机制**: 验证抓取数据的准确性
- **去重处理**: 避免重复的优惠信息
- **实时更新**: 定期更新优惠状态

## 结论

通过结合 Kimi K2 的强大 AI 能力和 Firecrawl 的高效数据抓取功能，我们成功构建了一个智能的旅行优惠查找应用。该应用不仅能够自动发现和分析旅行优惠，还能根据用户偏好提供个性化推荐。

这个项目展示了如何将多个 AI 服务有效整合，创建实用的消费者应用。通过遵循本教程的最佳实践，您可以构建出更加强大和可靠的 AI 驱动应用程序。