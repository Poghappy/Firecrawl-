#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体注册表模块

提供智能体的注册、管理和获取功能。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

import logging
from typing import Dict, Type, Optional
from .base_agent import BaseAgent, AgentConfig


logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    智能体注册表

    管理所有可用的智能体类型和实例。

    使用示例:
        # 注册智能体
        registry = AgentRegistry()
        registry.register("news", NewsAgent)

        # 获取智能体
        agent = registry.get_agent("news", config)
    """

    def __init__(self):
        """初始化注册表"""
        self._registry: Dict[str, Type[BaseAgent]] = {}
        self._instances: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger(__name__)

    def register(self, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """
        注册智能体类

        Args:
            agent_type: 智能体类型标识
            agent_class: 智能体类
        """
        if not issubclass(agent_class, BaseAgent):
            raise TypeError(f"{agent_class} 必须继承自 BaseAgent")

        if agent_type in self._registry:
            self.logger.warning(f"智能体类型 '{agent_type}' 已存在，将被覆盖")

        self._registry[agent_type] = agent_class
        self.logger.info(f"注册智能体: {agent_type} -> {agent_class.__name__}")

    def unregister(self, agent_type: str) -> None:
        """
        注销智能体类型

        Args:
            agent_type: 智能体类型标识
        """
        if agent_type in self._registry:
            del self._registry[agent_type]
            self.logger.info(f"注销智能体: {agent_type}")

        if agent_type in self._instances:
            del self._instances[agent_type]

    def get_agent(
        self,
        agent_type: str,
        config: AgentConfig,
        singleton: bool = True
    ) -> BaseAgent:
        """
        获取智能体实例

        Args:
            agent_type: 智能体类型标识
            config: 智能体配置
            singleton: 是否使用单例模式

        Returns:
            智能体实例

        Raises:
            ValueError: 未注册的智能体类型
        """
        if agent_type not in self._registry:
            raise ValueError(
                f"未注册的智能体类型: {agent_type}\n"
                f"可用类型: {list(self._registry.keys())}"
            )

        # 单例模式
        if singleton:
            if agent_type not in self._instances:
                agent_class = self._registry[agent_type]
                self._instances[agent_type] = agent_class(config)
                self.logger.info(f"创建智能体实例: {agent_type}")
            return self._instances[agent_type]

        # 每次创建新实例
        agent_class = self._registry[agent_type]
        return agent_class(config)

    def list_agents(self) -> Dict[str, str]:
        """
        列出所有已注册的智能体

        Returns:
            智能体类型到类名的映射
        """
        return {
            agent_type: agent_class.__name__
            for agent_type, agent_class in self._registry.items()
        }

    def is_registered(self, agent_type: str) -> bool:
        """
        检查智能体类型是否已注册

        Args:
            agent_type: 智能体类型标识

        Returns:
            是否已注册
        """
        return agent_type in self._registry

    def clear(self) -> None:
        """清空注册表"""
        self._registry.clear()
        self._instances.clear()
        self.logger.info("注册表已清空")


# 全局注册表实例
_global_registry = AgentRegistry()


def get_agent(
    agent_type: str,
    config: AgentConfig,
    singleton: bool = True
) -> BaseAgent:
    """
    从全局注册表获取智能体

    Args:
        agent_type: 智能体类型标识
        config: 智能体配置
        singleton: 是否使用单例模式

    Returns:
        智能体实例
    """
    return _global_registry.get_agent(agent_type, config, singleton)


def register_agent(agent_type: str, agent_class: Type[BaseAgent]) -> None:
    """
    注册智能体到全局注册表

    Args:
        agent_type: 智能体类型标识
        agent_class: 智能体类
    """
    _global_registry.register(agent_type, agent_class)


def list_registered_agents() -> Dict[str, str]:
    """
    列出全局注册表中的所有智能体

    Returns:
        智能体类型到类名的映射
    """
    return _global_registry.list_agents()


# 使用示例
if __name__ == "__main__":
    from .base_agent import BaseAgent

    # 创建示例智能体
    class NewsAgent(BaseAgent):
        async def collect(self, params):
            return {"news": "example"}

        async def parse(self, raw_data):
            return raw_data

    class EcommerceAgent(BaseAgent):
        async def collect(self, params):
            return {"product": "example"}

        async def parse(self, raw_data):
            return raw_data

    # 注册智能体
    registry = AgentRegistry()
    registry.register("news", NewsAgent)
    registry.register("ecommerce", EcommerceAgent)

    # 列出已注册的智能体
    print("已注册的智能体:")
    for agent_type, agent_name in registry.list_agents().items():
        print(f"  - {agent_type}: {agent_name}")

    # 获取智能体实例
    config = AgentConfig(
        name="新闻智能体",
        type="news",
        api_key="fc-your-api-key"
    )

    agent = registry.get_agent("news", config)
    print(f"\n获取智能体: {agent.__class__.__name__}")
    print(f"配置: {agent.config.name}")
