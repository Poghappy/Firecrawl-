#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体基类模块

提供所有业务场景智能体的基础架构和通用功能。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

from firecrawl import AsyncFirecrawl
from pydantic import BaseModel


logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """智能体配置"""
    name: str
    type: str
    api_key: str
    max_concurrent: int = 10
    timeout: int = 120
    max_retries: int = 3
    retry_delay: float = 2.0
    enable_cache: bool = True
    max_age: int = 172800000  # 2 天缓存
    proxy: str = "basic"
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectionTask:
    """采集任务"""
    task_id: str
    params: Dict[str, Any]
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectionResult:
    """采集结果"""
    task_id: str
    success: bool
    data: Any
    error: Optional[str] = None
    credits_used: int = 0
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.now)


class BaseAgent(ABC):
    """
    智能体基类

    所有业务场景的智能体都应继承此类，实现具体的采集和解析逻辑。

    核心功能：
    - 异步采集（AsyncFirecrawl）
    - 并发控制（Semaphore）
    - 错误处理和重试
    - 数据验证（Pydantic）
    - 成本追踪

    使用示例：
        class NewsAgent(BaseAgent):
            async def collect(self, params: dict):
                # 实现新闻采集逻辑
                pass

            async def parse(self, raw_data):
                # 实现数据解析逻辑
                pass
    """

    def __init__(self, config: AgentConfig):
        """
        初始化智能体

        Args:
            config: 智能体配置
        """
        self.config = config
        self.client: Optional[AsyncFirecrawl] = None
        self.semaphore = asyncio.Semaphore(config.max_concurrent)
        self.logger = logging.getLogger(f"{__name__}.{config.name}")

        # 统计信息
        self.stats = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_credits": 0,
            "total_duration": 0.0,
        }

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.client = AsyncFirecrawl(api_key=self.config.api_key)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    @abstractmethod
    async def collect(self, params: Dict[str, Any]) -> Any:
        """
        执行数据采集（必须实现）

        Args:
            params: 采集参数

        Returns:
            采集的原始数据
        """
        pass

    @abstractmethod
    async def parse(self, raw_data: Any) -> Any:
        """
        解析原始数据为结构化格式（必须实现）

        Args:
            raw_data: 原始数据

        Returns:
            解析后的结构化数据
        """
        pass

    async def validate(self, data: Any, schema: type[BaseModel]) -> BaseModel:
        """
        验证数据格式

        Args:
            data: 待验证数据
            schema: Pydantic 模型

        Returns:
            验证后的数据模型实例
        """
        try:
            if isinstance(data, dict):
                return schema(**data)
            elif isinstance(data, list):
                return [schema(**item) for item in data]
            else:
                raise ValueError(f"不支持的数据类型: {type(data)}")
        except Exception as e:
            self.logger.error(f"数据验证失败: {e}")
            raise

    async def execute(self, task: CollectionTask) -> CollectionResult:
        """
        执行单个采集任务（统一入口）

        Args:
            task: 采集任务

        Returns:
            采集结果
        """
        start_time = datetime.now()

        async with self.semaphore:
            try:
                self.stats["total_tasks"] += 1

                # 执行采集
                raw_data = await self.collect(task.params)

                # 解析数据
                parsed_data = await self.parse(raw_data)

                # 记录成功
                self.stats["successful_tasks"] += 1
                duration = (datetime.now() - start_time).total_seconds()
                self.stats["total_duration"] += duration

                return CollectionResult(
                    task_id=task.task_id,
                    success=True,
                    data=parsed_data,
                    duration=duration,
                    metadata={
                        "agent": self.config.name,
                        "task_priority": task.priority,
                    }
                )

            except Exception as e:
                self.stats["failed_tasks"] += 1
                self.logger.error(f"任务执行失败 [{task.task_id}]: {e}")

                return CollectionResult(
                    task_id=task.task_id,
                    success=False,
                    data=None,
                    error=str(e),
                    metadata={
                        "agent": self.config.name,
                        "task_priority": task.priority,
                    }
                )

    async def execute_batch(
        self,
        tasks: List[CollectionTask],
        progress_callback: Optional[callable] = None
    ) -> List[CollectionResult]:
        """
        批量执行采集任务

        Args:
            tasks: 任务列表
            progress_callback: 进度回调函数

        Returns:
            结果列表
        """
        self.logger.info(f"开始批量执行 {len(tasks)} 个任务")

        async def execute_with_progress(task: CollectionTask, index: int):
            result = await self.execute(task)
            if progress_callback:
                await progress_callback(index + 1, len(tasks), result)
            return result

        results = await asyncio.gather(
            *[execute_with_progress(task, i) for i, task in enumerate(tasks)],
            return_exceptions=True
        )

        # 处理异常
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(CollectionResult(
                    task_id=tasks[i].task_id,
                    success=False,
                    data=None,
                    error=str(result)
                ))
            else:
                processed_results.append(result)

        self.logger.info(f"批量任务完成，成功: {sum(1 for r in processed_results if r.success)}/{len(tasks)}")
        return processed_results

    async def retry_with_backoff(
        self,
        func: callable,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None
    ) -> Any:
        """
        带指数退避的重试机制

        Args:
            func: 要重试的异步函数
            max_retries: 最大重试次数
            retry_delay: 基础重试延迟

        Returns:
            函数执行结果
        """
        max_retries = max_retries or self.config.max_retries
        retry_delay = retry_delay or self.config.retry_delay

        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

                wait_time = retry_delay * (2 ** attempt)
                self.logger.warning(
                    f"重试 {attempt + 1}/{max_retries}，等待 {wait_time}秒: {e}"
                )
                await asyncio.sleep(wait_time)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_tasks"] / self.stats["total_tasks"]
                if self.stats["total_tasks"] > 0 else 0
            ),
            "avg_duration": (
                self.stats["total_duration"] / self.stats["successful_tasks"]
                if self.stats["successful_tasks"] > 0 else 0
            ),
        }

    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_credits": 0,
            "total_duration": 0.0,
        }


# 使用示例
if __name__ == "__main__":
    # 这是一个示例实现
    class ExampleAgent(BaseAgent):
        async def collect(self, params: dict):
            # 使用 Firecrawl 采集数据
            result = await self.client.scrape(
                params["url"],
                formats=["markdown"]
            )
            return result

        async def parse(self, raw_data):
            # 解析数据
            return {
                "title": raw_data.get("metadata", {}).get("title", ""),
                "content": raw_data.get("markdown", ""),
            }

    async def main():
        config = AgentConfig(
            name="示例智能体",
            type="example",
            api_key="fc-your-api-key"
        )

        async with ExampleAgent(config) as agent:
            task = CollectionTask(
                task_id="task-001",
                params={"url": "https://firecrawl.dev"}
            )

            result = await agent.execute(task)
            print(f"任务完成: {result.success}")
            print(f"数据: {result.data}")
            print(f"统计: {agent.get_stats()}")

    # asyncio.run(main())
