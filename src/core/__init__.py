"""
Firecrawl 数据采集器核心模块

提供智能体架构的核心组件：
- BaseAgent: 智能体基类
- AgentRegistry: 智能体注册表
- AgentManager: 智能体管理器
"""

from .base_agent import BaseAgent
from .agent_registry import AgentRegistry, get_agent
from .agent_manager import AgentManager

__all__ = [
    "BaseAgent",
    "AgentRegistry",
    "get_agent",
    "AgentManager",
]
