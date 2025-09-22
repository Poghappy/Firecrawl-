#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火鸟门户系统 - Firecrawl Observer 数据采集器
基于 Firecrawl Observer 架构优化的智能内容监控系统

功能特性:
- 智能变化检测
- AI内容过滤
- 实时通知系统
- Web监控面板
- 火鸟门户API集成

@version: 2.0.0
@author: 火鸟门户开发团队
@link: https://hawaiihub.net
"""

import json
import asyncio
import hashlib
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

import aiohttp
import schedule
from firecrawl import FirecrawlApp
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

class FirecrawlObserver:
    """火鸟门户 Firecrawl Observer 主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.firecrawl = FirecrawlApp(api_key=self.config['firecrawl']['api_key'])
        self.content_hashes = {}
        self.change_history = []
        self.app = FastAPI(title="Firecrawl Observer Dashboard")
        self.security = HTTPBasic()
        
        # 设置日志
        self._setup_logging()
        
        # 初始化监控面板
        if self.config['notifications']['enable_dashboard']:
            self._setup_dashboard()
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"配置文件加载失败: {e}")
    
    def _setup_logging(self):
        """设置日志系统"""
        log_config = self.config['logging']
        
        # 创建日志目录
        log_path = Path(log_config['file_path'])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 配置日志格式
        logging.basicConfig(
            level=getattr(logging, log_config['level']),
            format=log_config['format'],
            handlers=[
                logging.FileHandler(log_config['file_path'], encoding='utf-8'),
                logging.StreamHandler() if log_config['enable_console'] else logging.NullHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Firecrawl Observer 启动")
    
    def _setup_dashboard(self):
        """设置监控面板"""
        
        def verify_credentials(credentials: HTTPBasicCredentials = Depends(self.security)):
            """验证用户凭据"""
            dashboard_config = self.config['notifications']['dashboard_config']
            correct_username = dashboard_config['username']
            correct_password = dashboard_config['password']
            
            if credentials.username != correct_username or credentials.password != correct_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Basic"},
                )
            return credentials.username
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(username: str = Depends(verify_credentials)):
            """监控面板主页"""
            return self._generate_dashboard_html()
        
        @self.app.get("/api/status")
        async def get_status(username: str = Depends(verify_credentials)):
            """获取系统状态"""
            return {
                "status": "running",
                "sources_count": len([s for s in self.config['sources'] if s['enabled']]),
                "last_check": datetime.now().isoformat(),
                "changes_today": len([c for c in self.change_history 
                                    if c['timestamp'] > (datetime.now() - timedelta(days=1)).isoformat()])
            }
        
        @self.app.get("/api/changes")
        async def get_changes(username: str = Depends(verify_credentials)):
            """获取变化历史"""
            return {"changes": self.change_history[-50:]}  # 返回最近50条变化
    
    def _generate_dashboard_html(self) -> str:
        """生成监控面板HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Firecrawl Observer - 火鸟门户监控面板</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
                .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
                .stat-card {{ background: white; padding: 20px; border-radius: 8px; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .changes {{ background: white; padding: 20px; border-radius: 8px; margin-top: 20px; }}
                .change-item {{ border-bottom: 1px solid #eee; padding: 10px 0; }}
                .timestamp {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔥 Firecrawl Observer</h1>
                <p>火鸟门户系统 - 智能内容监控面板</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>监控源</h3>
                    <p>{len([s for s in self.config['sources'] if s['enabled']])} 个活跃</p>
                </div>
                <div class="stat-card">
                    <h3>今日变化</h3>
                    <p>{len([c for c in self.change_history if c['timestamp'] > (datetime.now() - timedelta(days=1)).isoformat()])} 次</p>
                </div>
                <div class="stat-card">
                    <h3>系统状态</h3>
                    <p style="color: green;">✅ 正常运行</p>
                </div>
            </div>
            
            <div class="changes">
                <h3>最近变化</h3>
                <div id="changes-list">
                    {''.join([f'<div class="change-item"><strong>{c["source"]}</strong><br><span class="timestamp">{c["timestamp"]}</span></div>' for c in self.change_history[-10:]])}
                </div>
            </div>
            
            <script>
                // 每30秒刷新一次数据
                setInterval(() => location.reload(), 30000);
            </script>
        </body>
        </html>
        """
    
    async def check_content_changes(self, source: Dict) -> Optional[Dict]:
        """检查内容变化"""
        try:
            self.logger.info(f"检查源: {source['name']}")
            
            # 根据类型选择抓取方法
            if source['type'] == 'single':
                result = self.firecrawl.scrape_url(source['url'])
                content = result.get('content', '')
            else:
                result = self.firecrawl.crawl_url(
                    source['url'], 
                    params=source.get('crawl_options', {})
                )
                content = '\n'.join([page.get('content', '') for page in result.get('data', [])])
            
            # 计算内容哈希
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # 检查是否有变化
            if source['name'] in self.content_hashes:
                if self.content_hashes[source['name']] != content_hash:
                    change_data = {
                        'source': source['name'],
                        'url': source['url'],
                        'timestamp': datetime.now().isoformat(),
                        'old_hash': self.content_hashes[source['name']],
                        'new_hash': content_hash,
                        'content': content[:1000] + '...' if len(content) > 1000 else content
                    }
                    
                    # AI内容过滤
                    if self.config['monitoring']['change_detection']['ai_filtering']['enabled']:
                        ai_analysis = await self._ai_content_analysis(content, source)
                        change_data['ai_analysis'] = ai_analysis
                        
                        # 根据AI分析结果决定是否通知
                        if ai_analysis['importance_score'] < self.config['monitoring']['change_detection']['ai_filtering']['threshold']:
                            self.logger.info(f"AI过滤: {source['name']} 变化重要性较低，跳过通知")
                            self.content_hashes[source['name']] = content_hash
                            return None
                    
                    self.content_hashes[source['name']] = content_hash
                    self.change_history.append(change_data)
                    
                    # 发送通知
                    await self._send_notifications(change_data)
                    
                    # 推送到火鸟门户
                    await self._push_to_huoniao(change_data, source)
                    
                    return change_data
            else:
                # 首次检查，记录哈希值
                self.content_hashes[source['name']] = content_hash
                self.logger.info(f"首次检查 {source['name']}，记录基准哈希")
            
            return None
            
        except Exception as e:
            self.logger.error(f"检查 {source['name']} 时出错: {e}")
            return None
    
    async def _ai_content_analysis(self, content: str, source: Dict) -> Dict:
        """AI内容分析"""
        ai_config = self.config['monitoring']['change_detection']['ai_filtering']
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {ai_config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                
                prompt = f"""
                请分析以下内容的重要性和新闻价值，返回JSON格式:
                {{
                    "importance_score": 0-100的重要性评分,
                    "category": "新闻分类",
                    "summary": "内容摘要",
                    "keywords": ["关键词列表"]
                }}
                
                内容:
                {content[:2000]}
                """
                
                data = {
                    'model': ai_config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': ai_config['max_tokens']
                }
                
                async with session.post('https://api.openai.com/v1/chat/completions', 
                                       headers=headers, json=data) as resp:
                    result = await resp.json()
                    ai_response = result['choices'][0]['message']['content']
                    
                    # 尝试解析JSON响应
                    try:
                        return json.loads(ai_response)
                    except:
                        return {
                            'importance_score': 50,
                            'category': '未分类',
                            'summary': ai_response[:200],
                            'keywords': []
                        }
        except Exception as e:
            self.logger.error(f"AI分析失败: {e}")
            return {
                'importance_score': 50,
                'category': '未分类',
                'summary': '分析失败',
                'keywords': []
            }
    
    async def _send_notifications(self, change_data: Dict):
        """发送通知"""
        # 邮件通知
        if self.config['notifications']['enable_email']:
            await self._send_email_notification(change_data)
        
        # Webhook通知
        if self.config['notifications']['enable_webhook']:
            await self._send_webhook_notification(change_data)
    
    async def _send_email_notification(self, change_data: Dict):
        """发送邮件通知"""
        # 这里实现邮件发送逻辑
        self.logger.info(f"发送邮件通知: {change_data['source']}")
    
    async def _send_webhook_notification(self, change_data: Dict):
        """发送Webhook通知"""
        webhook_config = self.config['notifications']['webhook_config']
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Content-Type': 'application/json',
                    'X-Webhook-Secret': webhook_config['secret']
                }
                
                async with session.post(
                    webhook_config['url'],
                    json=change_data,
                    headers=headers,
                    timeout=webhook_config['timeout']
                ) as resp:
                    if resp.status == 200:
                        self.logger.info(f"Webhook通知发送成功: {change_data['source']}")
                    else:
                        self.logger.error(f"Webhook通知发送失败: {resp.status}")
        except Exception as e:
            self.logger.error(f"Webhook通知发送异常: {e}")
    
    async def _push_to_huoniao(self, change_data: Dict, source: Dict):
        """推送到火鸟门户"""
        api_config = self.config['api_integration']
        
        try:
            # 构建文章数据
            article_data = {
                'title': f"[{source['name']}] 内容更新",
                'content': change_data['content'],
                'category_id': source.get('processing_options', {}).get('category_override', api_config['default_category_id']),
                'author_id': api_config['default_author_id'],
                'source_url': change_data['url'],
                'auto_publish': source.get('processing_options', {}).get('auto_publish', api_config['auto_publish'])
            }
            
            # 添加AI分析结果
            if 'ai_analysis' in change_data:
                article_data['ai_summary'] = change_data['ai_analysis']['summary']
                article_data['keywords'] = ','.join(change_data['ai_analysis']['keywords'])
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {api_config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                
                async with session.post(
                    f"{api_config['base_url']}articles",
                    json=article_data,
                    headers=headers,
                    timeout=api_config['timeout']
                ) as resp:
                    if resp.status == 201:
                        self.logger.info(f"成功推送到火鸟门户: {change_data['source']}")
                    else:
                        self.logger.error(f"推送到火鸟门户失败: {resp.status}")
        except Exception as e:
            self.logger.error(f"推送到火鸟门户异常: {e}")
    
    def start_monitoring(self):
        """启动监控"""
        self.logger.info("开始设置监控任务")
        
        # 为每个启用的源设置定时任务
        for source in self.config['sources']:
            if source['enabled']:
                schedule.every(self.config['monitoring']['change_detection']['check_interval']).seconds.do(
                    lambda s=source: asyncio.create_task(self.check_content_changes(s))
                )
                self.logger.info(f"已设置监控任务: {source['name']}")
        
        # 启动监控面板
        if self.config['notifications']['enable_dashboard']:
            dashboard_config = self.config['notifications']['dashboard_config']
            self.logger.info(f"启动监控面板: http://localhost:{dashboard_config['port']}")
            
            # 在后台运行FastAPI应用
            import threading
            def run_dashboard():
                uvicorn.run(self.app, host="0.0.0.0", port=dashboard_config['port'], log_level="warning")
            
            dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            dashboard_thread.start()
        
        # 主监控循环
        self.logger.info("监控系统已启动")
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    """主函数"""
    try:
        observer = FirecrawlObserver()
        observer.start_monitoring()
    except KeyboardInterrupt:
        print("\n监控系统已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()