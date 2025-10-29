#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 工厂模式示例

这是 P1-A2 优化任务的参考实现。
简化 Agent 创建流程，支持从配置文件自动创建。

作者: AI Assistant
创建时间: 2025-01-29
优化版本: v2.2.0
"""

import os
import yaml
from typing import Dict, Optional, List, Type
from pathlib import Path
from dataclasses import dataclass

# 假设已有的导入
# from src.core.base_agent import BaseAgent, AgentConfig
# from src.core.agent_registry import AgentRegistry


@dataclass
class AgentConfig:
    """智能体配置（简化版）"""
    name: str
    type: str
    api_key: str
    timeout: int = 120
    max_concurrent: int = 10


class AgentFactory:
    """
    智能体工厂

    职责:
    - 从配置文件创建 Agent
    - 自动加载 API Key
    - 批量创建 Agents
    - 管理 Agent 生命周期

    使用示例:
        # 方式1: 从配置文件创建
        agent = await AgentFactory.create("news")

        # 方式2: 批量创建
        agents = await AgentFactory.create_batch(["news", "rental", "recruitment"])

        # 方式3: 自定义配置
        agent = await AgentFactory.create("news", api_key="custom-key")
    """

    # 配置文件目录
    CONFIG_DIR = Path("config/agents")

    # Agent 类型到配置文件的映射
    CONFIG_FILE_MAPPING = {
        "news": "news_agent.yaml",
        "rental": "rental_agent.yaml",
        "recruitment": "recruitment_agent.yaml",
        "ecommerce": "ecommerce_agent.yaml",
        "learning": "learning_agent.yaml"
    }

    @classmethod
    async def create(
        cls,
        agent_type: str,
        api_key: Optional[str] = None,
        config_path: Optional[str] = None,
        **override_params
    ):
        """
        创建智能体实例

        Args:
            agent_type: 智能体类型 (news, rental, recruitment 等)
            api_key: API Key（可选，默认从环境变量读取）
            config_path: 配置文件路径（可选）
            **override_params: 覆盖配置的参数

        Returns:
            智能体实例

        Example:
            # 使用默认配置
            agent = await AgentFactory.create("news")

            # 自定义 API Key
            agent = await AgentFactory.create("news", api_key="custom-key")

            # 覆盖配置参数
            agent = await AgentFactory.create("news", max_concurrent=20)
        """
        # 加载配置
        config_data = await cls._load_config(agent_type, config_path)

        # 构建 AgentConfig
        agent_config = cls._build_agent_config(
            agent_type,
            config_data,
            api_key,
            override_params
        )

        # 从注册表获取 Agent 类
        from src.core.agent_registry import get_agent
        return get_agent(agent_type, agent_config, singleton=False)

    @classmethod
    async def create_batch(
        cls,
        agent_types: List[str],
        api_keys: Optional[Dict[str, str]] = None
    ) -> Dict[str, 'BaseAgent']:
        """
        批量创建智能体

        Args:
            agent_types: 智能体类型列表
            api_keys: 为每个类型指定 API Key（可选）

        Returns:
            智能体字典 {agent_type: agent_instance}

        Example:
            agents = await AgentFactory.create_batch([
                "news",
                "rental",
                "recruitment"
            ])

            # 使用不同的 API Key
            agents = await AgentFactory.create_batch(
                ["news", "rental"],
                api_keys={
                    "news": "key-1",
                    "rental": "key-2"
                }
            )
        """
        agents = {}
        api_keys = api_keys or {}

        for agent_type in agent_types:
            api_key = api_keys.get(agent_type)
            agents[agent_type] = await cls.create(agent_type, api_key=api_key)

        return agents

    @classmethod
    async def _load_config(
        cls,
        agent_type: str,
        config_path: Optional[str] = None
    ) -> Dict:
        """加载配置文件"""
        # 确定配置文件路径
        if config_path:
            path = Path(config_path)
        else:
            filename = cls.CONFIG_FILE_MAPPING.get(agent_type)
            if not filename:
                raise ValueError(f"未知的智能体类型: {agent_type}")
            path = cls.CONFIG_DIR / filename

        # 检查文件是否存在
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {path}")

        # 加载 YAML
        with open(path) as f:
            return yaml.safe_load(f)

    @classmethod
    def _build_agent_config(
        cls,
        agent_type: str,
        config_data: Dict,
        api_key: Optional[str],
        override_params: Dict
    ) -> AgentConfig:
        """构建 AgentConfig 对象"""
        # API Key 优先级: 参数 > 环境变量 > 配置文件
        final_api_key = (
            api_key or
            os.getenv("FIRECRAWL_API_KEY") or
            config_data.get("api", {}).get("api_key")
        )

        if not final_api_key:
            raise ValueError("未提供 API Key")

        # 合并配置
        agent_data = config_data.get("agent", {})
        api_data = config_data.get("api", {})

        # 构建配置对象
        return AgentConfig(
            name=agent_data.get("name", f"{agent_type} Agent"),
            type=agent_type,
            api_key=final_api_key,
            timeout=api_data.get("timeout", 120),
            max_concurrent=config_data.get("concurrency", {}).get("max_concurrent", 10),
            **override_params  # 覆盖参数
        )

    @classmethod
    def list_available_types(cls) -> List[str]:
        """列出所有可用的智能体类型"""
        return list(cls.CONFIG_FILE_MAPPING.keys())

    @classmethod
    def get_config_path(cls, agent_type: str) -> Path:
        """获取配置文件路径"""
        filename = cls.CONFIG_FILE_MAPPING.get(agent_type)
        if not filename:
            raise ValueError(f"未知的智能体类型: {agent_type}")
        return cls.CONFIG_DIR / filename


# ============================================================
# 使用示例
# ============================================================

async def example_basic_usage():
    """基础使用示例"""
    print("=" * 60)
    print("示例 1: 基础使用")
    print("=" * 60)

    # 创建新闻智能体
    agent = await AgentFactory.create("news")

    print(f"✅ 创建成功: {agent.config.name}")
    print(f"   类型: {agent.config.type}")
    print(f"   超时: {agent.config.timeout}s")
    print(f"   并发: {agent.config.max_concurrent}")


async def example_batch_creation():
    """批量创建示例"""
    print("\n" + "=" * 60)
    print("示例 2: 批量创建")
    print("=" * 60)

    # 批量创建多个智能体
    agents = await AgentFactory.create_batch([
        "news",
        "rental",
        "recruitment"
    ])

    print(f"✅ 创建了 {len(agents)} 个智能体:")
    for agent_type, agent in agents.items():
        print(f"   - {agent_type}: {agent.config.name}")


async def example_custom_config():
    """自定义配置示例"""
    print("\n" + "=" * 60)
    print("示例 3: 自定义配置")
    print("=" * 60)

    # 覆盖默认配置
    agent = await AgentFactory.create(
        "news",
        max_concurrent=20,  # 增加并发
        timeout=180  # 增加超时
    )

    print(f"✅ 自定义配置创建成功")
    print(f"   并发: {agent.config.max_concurrent}")
    print(f"   超时: {agent.config.timeout}s")


def example_list_types():
    """列出可用类型示例"""
    print("\n" + "=" * 60)
    print("示例 4: 列出可用类型")
    print("=" * 60)

    types = AgentFactory.list_available_types()

    print(f"✅ 可用的智能体类型:")
    for agent_type in types:
        config_path = AgentFactory.get_config_path(agent_type)
        print(f"   - {agent_type}: {config_path}")


# ============================================================
# 对比：优化前 vs 优化后
# ============================================================

def comparison_before_after():
    """对比优化前后的代码"""
    print("\n" + "=" * 60)
    print("📊 代码对比")
    print("=" * 60)

    print("\n❌ 优化前（繁琐）:")
    print("""
    from honolulu_rentals.config import PLATFORMS
    from honolulu_rentals.scrapers.craigslist_scraper import CraigslistScraper

    # 需要手动加载配置
    platform_config = PLATFORMS["craigslist"]
    api_key = platform_config["api_key"]

    # 需要手动创建
    scraper = CraigslistScraper(api_key=api_key)

    # 需要手动调用
    listings = scraper.scrape_all()

    # 12 行代码
    """)

    print("\n✅ 优化后（简洁）:")
    print("""
    # 一行代码创建
    agent = await AgentFactory.create("rental")

    # 一行代码执行
    result = await agent.execute({})

    # 2 行代码，节省 10 行！
    """)


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()

    # 运行所有示例
    asyncio.run(example_basic_usage())
    asyncio.run(example_batch_creation())
    asyncio.run(example_custom_config())
    example_list_types()
    comparison_before_after()

    print("\n✅ 所有示例运行完成")
