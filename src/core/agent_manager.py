#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体管理器模块

提供智能体的生命周期管理、任务分配和监控功能。

作者: Firecrawl Team
创建时间: 2025-10-29
版本: v2.1.0
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

from .base_agent import BaseAgent, AgentConfig, CollectionTask, CollectionResult
from .agent_registry import AgentRegistry


logger = logging.getLogger(__name__)


@dataclass
class AgentStatus:
    """智能体状态"""
    agent_type: str
    name: str
    status: str  # idle, running, error
    created_at: datetime
    last_active: datetime
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_credits: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentManager:
    """
    智能体管理器

    负责智能体的创建、销毁、任务分配和监控。

    核心功能：
    - 智能体生命周期管理
    - 任务队列和分配
    - 负载均衡
    - 状态监控
    - 健康检查

    使用示例：
        manager = AgentManager(registry)

        # 创建智能体
        await manager.create_agent("news", config)

        # 提交任务
        task_id = await manager.submit_task("news", task)

        # 获取结果
        result = await manager.get_result(task_id)
    """

    def __init__(self, registry: Optional[AgentRegistry] = None):
        """
        初始化管理器

        Args:
            registry: 智能体注册表（可选，默认使用全局注册表）
        """
        self.registry = registry or AgentRegistry()
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_status: Dict[str, AgentStatus] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.results: Dict[str, CollectionResult] = {}
        self.logger = logging.getLogger(__name__)

        self._running = False
        self._worker_tasks: List[asyncio.Task] = []

    async def create_agent(
        self,
        agent_type: str,
        config: AgentConfig,
        replace: bool = False
    ) -> BaseAgent:
        """
        创建智能体实例

        Args:
            agent_type: 智能体类型
            config: 智能体配置
            replace: 是否替换已存在的智能体

        Returns:
            创建的智能体实例
        """
        if agent_type in self.agents and not replace:
            self.logger.warning(f"智能体 '{agent_type}' 已存在")
            return self.agents[agent_type]

        # 创建智能体
        agent = self.registry.get_agent(agent_type, config, singleton=False)
        self.agents[agent_type] = agent

        # 记录状态
        now = datetime.now()
        self.agent_status[agent_type] = AgentStatus(
            agent_type=agent_type,
            name=config.name,
            status="idle",
            created_at=now,
            last_active=now
        )

        self.logger.info(f"创建智能体: {agent_type} ({config.name})")
        return agent

    async def destroy_agent(self, agent_type: str) -> bool:
        """
        销毁智能体实例

        Args:
            agent_type: 智能体类型

        Returns:
            是否成功销毁
        """
        if agent_type not in self.agents:
            self.logger.warning(f"智能体 '{agent_type}' 不存在")
            return False

        # 清理资源
        del self.agents[agent_type]
        del self.agent_status[agent_type]

        self.logger.info(f"销毁智能体: {agent_type}")
        return True

    async def submit_task(
        self,
        agent_type: str,
        task: CollectionTask
    ) -> str:
        """
        提交采集任务

        Args:
            agent_type: 智能体类型
            task: 采集任务

        Returns:
            任务ID
        """
        if agent_type not in self.agents:
            raise ValueError(f"智能体 '{agent_type}' 不存在")

        # 添加任务到队列
        task.metadata["agent_type"] = agent_type
        await self.task_queue.put(task)

        self.logger.info(f"提交任务 [{task.task_id}] 到 {agent_type}")
        return task.task_id

    async def get_result(
        self,
        task_id: str,
        timeout: Optional[float] = None
    ) -> Optional[CollectionResult]:
        """
        获取任务结果

        Args:
            task_id: 任务ID
            timeout: 超时时间（秒）

        Returns:
            任务结果（如果未完成则返回 None）
        """
        if timeout:
            start_time = datetime.now()
            while task_id not in self.results:
                if (datetime.now() - start_time).total_seconds() > timeout:
                    return None
                await asyncio.sleep(0.1)

        return self.results.get(task_id)

    async def start(self, num_workers: int = 3):
        """
        启动管理器（开始处理任务队列）

        Args:
            num_workers: 工作线程数
        """
        if self._running:
            self.logger.warning("管理器已在运行")
            return

        self._running = True
        self.logger.info(f"启动管理器，工作线程数: {num_workers}")

        # 创建工作线程
        for i in range(num_workers):
            task = asyncio.create_task(self._worker(i))
            self._worker_tasks.append(task)

    async def stop(self):
        """停止管理器"""
        if not self._running:
            return

        self._running = False
        self.logger.info("停止管理器")

        # 等待所有工作线程完成
        for task in self._worker_tasks:
            task.cancel()

        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        self._worker_tasks.clear()

    async def _worker(self, worker_id: int):
        """
        工作线程

        Args:
            worker_id: 工作线程ID
        """
        self.logger.info(f"工作线程 {worker_id} 已启动")

        while self._running:
            try:
                # 获取任务（超时1秒）
                try:
                    task = await asyncio.wait_for(
                        self.task_queue.get(),
                        timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                # 执行任务
                agent_type = task.metadata.get("agent_type")
                if agent_type not in self.agents:
                    self.logger.error(f"未找到智能体: {agent_type}")
                    continue

                agent = self.agents[agent_type]

                # 更新状态
                self.agent_status[agent_type].status = "running"
                self.agent_status[agent_type].last_active = datetime.now()

                # 执行任务
                result = await agent.execute(task)

                # 保存结果
                self.results[task.task_id] = result

                # 更新统计
                status = self.agent_status[agent_type]
                if result.success:
                    status.tasks_completed += 1
                else:
                    status.tasks_failed += 1
                status.total_credits += result.credits_used
                status.status = "idle"

                self.logger.info(
                    f"任务完成 [{task.task_id}]: "
                    f"{'成功' if result.success else '失败'}"
                )

            except Exception as e:
                self.logger.error(f"工作线程 {worker_id} 错误: {e}")

        self.logger.info(f"工作线程 {worker_id} 已停止")

    def get_agent_status(self, agent_type: str) -> Optional[AgentStatus]:
        """获取智能体状态"""
        return self.agent_status.get(agent_type)

    def get_all_status(self) -> Dict[str, AgentStatus]:
        """获取所有智能体状态"""
        return self.agent_status.copy()

    def get_queue_size(self) -> int:
        """获取任务队列大小"""
        return self.task_queue.qsize()

    async def health_check(self) -> Dict[str, Any]:
        """
        健康检查

        Returns:
            健康状态信息
        """
        return {
            "status": "healthy" if self._running else "stopped",
            "agents_count": len(self.agents),
            "queue_size": self.task_queue.qsize(),
            "results_count": len(self.results),
            "workers_count": len(self._worker_tasks),
            "agents": {
                agent_type: {
                    "status": status.status,
                    "tasks_completed": status.tasks_completed,
                    "tasks_failed": status.tasks_failed,
                    "total_credits": status.total_credits,
                }
                for agent_type, status in self.agent_status.items()
            }
        }


# 使用示例
if __name__ == "__main__":
    async def main():
        from .agent_registry import AgentRegistry
        from .base_agent import BaseAgent

        # 创建示例智能体
        class ExampleAgent(BaseAgent):
            async def collect(self, params):
                await asyncio.sleep(1)  # 模拟采集
                return {"data": "example"}

            async def parse(self, raw_data):
                return raw_data

        # 注册智能体
        registry = AgentRegistry()
        registry.register("example", ExampleAgent)

        # 创建管理器
        manager = AgentManager(registry)

        # 创建智能体
        config = AgentConfig(
            name="示例智能体",
            type="example",
            api_key="fc-your-api-key"
        )
        await manager.create_agent("example", config)

        # 启动管理器
        await manager.start(num_workers=2)

        # 提交任务
        for i in range(5):
            task = CollectionTask(
                task_id=f"task-{i:03d}",
                params={"id": i}
            )
            await manager.submit_task("example", task)

        # 等待所有任务完成
        while manager.get_queue_size() > 0:
            await asyncio.sleep(0.5)

        # 健康检查
        health = await manager.health_check()
        print("\n健康状态:")
        print(f"  状态: {health['status']}")
        print(f"  智能体数量: {health['agents_count']}")
        print(f"  队列大小: {health['queue_size']}")

        # 停止管理器
        await manager.stop()

    # asyncio.run(main())
