# 实现模板

## 🎯 角色设定
你是资深开发工程师，具备丰富的代码实现经验。请基于任务分解和技术设计输出"最小可用"的代码实现。

## 📥 输入格式

### 任务输入
```
[从任务分解模板生成的具体任务]
```

### 技术设计输入
```
[从技术设计模板生成的技术方案]
```

### 代码规范
```
[从开发规范指南中的代码要求]
```

## 📤 输出格式

### 1. 目标文件路径与创建/修改说明

#### 文件变更计划
```
新增文件:
- src/core/collector.py (数据采集核心模块)
- src/models/job.py (任务数据模型)
- tests/unit/test_collector.py (采集器单元测试)

修改文件:
- src/api/routes.py (添加采集任务API端点)
- requirements.txt (添加新依赖)

删除文件:
- 无
```

#### 变更影响分析
- **核心功能**: 实现Firecrawl API集成和数据采集
- **API接口**: 新增任务创建和状态查询接口
- **数据模型**: 新增Job模型和相关字段
- **测试覆盖**: 新增单元测试和集成测试

### 2. 代码实现

#### 核心业务逻辑
```python
# src/core/collector.py
"""
数据采集核心模块

实现Firecrawl API集成，提供数据采集功能
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

import aiohttp
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobPriority(int, Enum):
    """任务优先级枚举"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class CollectionOptions:
    """采集选项配置"""
    max_pages: int = 10
    timeout: int = 30
    retry_count: int = 3
    include_metadata: bool = True
    extract_links: bool = False


class Job(BaseModel):
    """任务数据模型"""
    id: str = Field(..., description="任务ID")
    url: str = Field(..., description="目标URL")
    status: JobStatus = Field(default=JobStatus.PENDING, description="任务状态")
    priority: JobPriority = Field(default=JobPriority.NORMAL, description="任务优先级")
    options: CollectionOptions = Field(default_factory=CollectionOptions, description="采集选项")
    created_at: Optional[str] = Field(default=None, description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")
    result: Optional[Dict[str, Any]] = Field(default=None, description="采集结果")
    error_message: Optional[str] = Field(default=None, description="错误信息")


class FirecrawlCollector:
    """Firecrawl数据采集器"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev"):
        """
        初始化采集器
        
        Args:
            api_key: Firecrawl API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = FirecrawlApp(api_key=api_key)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def collect_url(self, job: Job) -> Dict[str, Any]:
        """
        采集单个URL
        
        Args:
            job: 采集任务
            
        Returns:
            采集结果字典
            
        Raises:
            CollectionError: 采集失败时抛出
        """
        self.logger.info(f"开始采集任务: {job.id}, URL: {job.url}")
        
        try:
            # 调用Firecrawl API进行采集
            result = await self._call_firecrawl_api(job)
            
            # 处理采集结果
            processed_result = self._process_result(result, job)
            
            self.logger.info(f"采集任务完成: {job.id}")
            return processed_result
            
        except Exception as e:
            self.logger.error(f"采集任务失败: {job.id}, 错误: {str(e)}")
            raise CollectionError(f"采集失败: {str(e)}") from e
    
    async def _call_firecrawl_api(self, job: Job) -> Dict[str, Any]:
        """
        调用Firecrawl API
        
        Args:
            job: 采集任务
            
        Returns:
            API返回结果
        """
        options = {
            "maxPages": job.options.max_pages,
            "timeout": job.options.timeout * 1000,  # 转换为毫秒
            "includeMetadata": job.options.include_metadata,
            "extractLinks": job.options.extract_links,
        }
        
        # 异步调用Firecrawl API
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.client.scrape_url(job.url, options)
        )
        
        return result
    
    def _process_result(self, raw_result: Dict[str, Any], job: Job) -> Dict[str, Any]:
        """
        处理采集结果
        
        Args:
            raw_result: 原始采集结果
            job: 采集任务
            
        Returns:
            处理后的结果
        """
        processed = {
            "job_id": job.id,
            "url": job.url,
            "status": "success",
            "data": {
                "title": raw_result.get("title", ""),
                "content": raw_result.get("content", ""),
                "metadata": raw_result.get("metadata", {}),
                "links": raw_result.get("links", []),
            },
            "timestamp": raw_result.get("timestamp"),
            "processing_time": raw_result.get("processingTime"),
        }
        
        return processed


class CollectionError(Exception):
    """采集异常"""
    pass


# 异步上下文管理器支持
class AsyncFirecrawlCollector:
    """异步Firecrawl采集器"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev"):
        self.api_key = api_key
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
    
    async def collect_batch(self, jobs: List[Job]) -> List[Dict[str, Any]]:
        """
        批量采集
        
        Args:
            jobs: 采集任务列表
            
        Returns:
            采集结果列表
        """
        tasks = [self._collect_single(job) for job in jobs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "job_id": jobs[i].id,
                    "status": "error",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _collect_single(self, job: Job) -> Dict[str, Any]:
        """采集单个任务"""
        collector = FirecrawlCollector(self.api_key, self.base_url)
        return await collector.collect_url(job)
```

#### API接口实现
```python
# src/api/routes.py (新增部分)
"""
API路由模块 - 新增采集任务相关端点
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel

from ..core.collector import Job, JobStatus, FirecrawlCollector, CollectionError
from ..models.job import JobRepository

router = APIRouter(prefix="/api/v1", tags=["采集任务"])


class JobCreateRequest(BaseModel):
    """任务创建请求"""
    url: str
    priority: Optional[int] = 2
    max_pages: Optional[int] = 10
    timeout: Optional[int] = 30
    retry_count: Optional[int] = 3
    include_metadata: Optional[bool] = True
    extract_links: Optional[bool] = False


class JobResponse(BaseModel):
    """任务响应"""
    job_id: str
    url: str
    status: JobStatus
    priority: int
    created_at: str
    updated_at: Optional[str] = None
    result: Optional[dict] = None
    error_message: Optional[str] = None


@router.post("/jobs", response_model=JobResponse)
async def create_job(
    request: JobCreateRequest,
    background_tasks: BackgroundTasks,
    job_repo: JobRepository = Depends(get_job_repository)
):
    """
    创建采集任务
    
    Args:
        request: 任务创建请求
        background_tasks: 后台任务
        job_repo: 任务仓储
        
    Returns:
        创建的任务信息
    """
    try:
        # 创建任务
        job = Job(
            id=generate_job_id(),
            url=request.url,
            priority=JobPriority(request.priority),
            options=CollectionOptions(
                max_pages=request.max_pages,
                timeout=request.timeout,
                retry_count=request.retry_count,
                include_metadata=request.include_metadata,
                extract_links=request.extract_links,
            )
        )
        
        # 保存任务到数据库
        await job_repo.create_job(job)
        
        # 添加后台任务
        background_tasks.add_task(process_collection_job, job.id)
        
        return JobResponse(
            job_id=job.id,
            url=job.url,
            status=job.status,
            priority=job.priority.value,
            created_at=job.created_at or "",
            updated_at=job.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    job_repo: JobRepository = Depends(get_job_repository)
):
    """
    获取任务状态
    
    Args:
        job_id: 任务ID
        job_repo: 任务仓储
        
    Returns:
        任务信息
    """
    job = await job_repo.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return JobResponse(
        job_id=job.id,
        url=job.url,
        status=job.status,
        priority=job.priority.value,
        created_at=job.created_at or "",
        updated_at=job.updated_at,
        result=job.result,
        error_message=job.error_message
    )


async def process_collection_job(job_id: str):
    """处理采集任务（后台任务）"""
    try:
        # 获取任务信息
        job_repo = get_job_repository()
        job = await job_repo.get_job(job_id)
        if not job:
            return
        
        # 更新任务状态为运行中
        job.status = JobStatus.RUNNING
        await job_repo.update_job(job)
        
        # 执行采集
        collector = FirecrawlCollector(get_firecrawl_api_key())
        result = await collector.collect_url(job)
        
        # 更新任务结果
        job.status = JobStatus.COMPLETED
        job.result = result
        await job_repo.update_job(job)
        
    except Exception as e:
        # 更新任务状态为失败
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        await job_repo.update_job(job)
```

### 3. 对应测试实现

#### 单元测试
```python
# tests/unit/test_collector.py
"""
数据采集器单元测试
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio

from src.core.collector import (
    FirecrawlCollector, 
    Job, 
    JobStatus, 
    JobPriority, 
    CollectionOptions,
    CollectionError
)


class TestFirecrawlCollector:
    """Firecrawl采集器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.api_key = "test-api-key"
        self.collector = FirecrawlCollector(self.api_key)
        self.test_job = Job(
            id="test-job-1",
            url="https://example.com",
            status=JobStatus.PENDING,
            priority=JobPriority.NORMAL,
            options=CollectionOptions()
        )
    
    @pytest.mark.asyncio
    async def test_collect_url_success(self):
        """测试成功采集URL"""
        # Given
        mock_result = {
            "title": "Test Title",
            "content": "Test Content",
            "metadata": {"author": "Test Author"},
            "links": ["https://example.com/link1"],
            "timestamp": "2024-01-01T00:00:00Z",
            "processingTime": 1500
        }
        
        with patch.object(self.collector, '_call_firecrawl_api', return_value=mock_result):
            # When
            result = await self.collector.collect_url(self.test_job)
            
            # Then
            assert result["job_id"] == "test-job-1"
            assert result["url"] == "https://example.com"
            assert result["status"] == "success"
            assert result["data"]["title"] == "Test Title"
            assert result["data"]["content"] == "Test Content"
    
    @pytest.mark.asyncio
    async def test_collect_url_failure(self):
        """测试采集URL失败"""
        # Given
        with patch.object(self.collector, '_call_firecrawl_api', side_effect=Exception("API Error")):
            # When & Then
            with pytest.raises(CollectionError):
                await self.collector.collect_url(self.test_job)
    
    @pytest.mark.asyncio
    async def test_call_firecrawl_api(self):
        """测试调用Firecrawl API"""
        # Given
        mock_client = Mock()
        mock_client.scrape_url.return_value = {"title": "Test"}
        self.collector.client = mock_client
        
        # When
        result = await self.collector._call_firecrawl_api(self.test_job)
        
        # Then
        assert result["title"] == "Test"
        mock_client.scrape_url.assert_called_once_with(
            "https://example.com",
            {
                "maxPages": 10,
                "timeout": 30000,
                "includeMetadata": True,
                "extractLinks": False,
            }
        )
    
    def test_process_result(self):
        """测试处理采集结果"""
        # Given
        raw_result = {
            "title": "Test Title",
            "content": "Test Content",
            "metadata": {"author": "Test Author"},
            "links": ["https://example.com/link1"],
            "timestamp": "2024-01-01T00:00:00Z",
            "processingTime": 1500
        }
        
        # When
        result = self.collector._process_result(raw_result, self.test_job)
        
        # Then
        assert result["job_id"] == "test-job-1"
        assert result["url"] == "https://example.com"
        assert result["status"] == "success"
        assert result["data"]["title"] == "Test Title"
        assert result["data"]["content"] == "Test Content"
        assert result["data"]["metadata"]["author"] == "Test Author"
        assert result["data"]["links"] == ["https://example.com/link1"]


class TestJob:
    """任务模型测试类"""
    
    def test_job_creation(self):
        """测试任务创建"""
        # Given & When
        job = Job(
            id="test-job",
            url="https://example.com",
            priority=JobPriority.HIGH
        )
        
        # Then
        assert job.id == "test-job"
        assert job.url == "https://example.com"
        assert job.status == JobStatus.PENDING
        assert job.priority == JobPriority.HIGH
        assert job.options.max_pages == 10
        assert job.options.timeout == 30
    
    def test_job_with_custom_options(self):
        """测试自定义选项的任务创建"""
        # Given & When
        options = CollectionOptions(
            max_pages=5,
            timeout=60,
            retry_count=5
        )
        job = Job(
            id="test-job",
            url="https://example.com",
            options=options
        )
        
        # Then
        assert job.options.max_pages == 5
        assert job.options.timeout == 60
        assert job.options.retry_count == 5


@pytest.mark.asyncio
class TestAsyncFirecrawlCollector:
    """异步Firecrawl采集器测试类"""
    
    async def test_collect_batch_success(self):
        """测试批量采集成功"""
        # Given
        jobs = [
            Job(id="job-1", url="https://example1.com"),
            Job(id="job-2", url="https://example2.com")
        ]
        
        with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
            mock_collector = mock_collector_class.return_value
            mock_collector.collect_url = AsyncMock(side_effect=[
                {"job_id": "job-1", "status": "success"},
                {"job_id": "job-2", "status": "success"}
            ])
            
            # When
            from src.core.collector import AsyncFirecrawlCollector
            async with AsyncFirecrawlCollector("test-key") as collector:
                results = await collector.collect_batch(jobs)
            
            # Then
            assert len(results) == 2
            assert results[0]["job_id"] == "job-1"
            assert results[1]["job_id"] == "job-2"
    
    async def test_collect_batch_with_errors(self):
        """测试批量采集包含错误"""
        # Given
        jobs = [
            Job(id="job-1", url="https://example1.com"),
            Job(id="job-2", url="https://example2.com")
        ]
        
        with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
            mock_collector = mock_collector_class.return_value
            mock_collector.collect_url = AsyncMock(side_effect=[
                {"job_id": "job-1", "status": "success"},
                Exception("Network error")
            ])
            
            # When
            from src.core.collector import AsyncFirecrawlCollector
            async with AsyncFirecrawlCollector("test-key") as collector:
                results = await collector.collect_batch(jobs)
            
            # Then
            assert len(results) == 2
            assert results[0]["job_id"] == "job-1"
            assert results[1]["job_id"] == "job-2"
            assert results[1]["status"] == "error"
            assert "Network error" in results[1]["error"]
```

### 4. 更新文档

#### README更新
```markdown
# Firecrawl数据采集器

## 新增功能

### 数据采集核心模块
- 支持Firecrawl API集成
- 异步数据采集
- 批量任务处理
- 错误处理和重试机制

### API接口
- `POST /api/v1/jobs` - 创建采集任务
- `GET /api/v1/jobs/{job_id}` - 查询任务状态

## 使用示例

```python
from src.core.collector import FirecrawlCollector, Job, JobPriority

# 创建采集器
collector = FirecrawlCollector(api_key="your-api-key")

# 创建任务
job = Job(
    id="task-1",
    url="https://example.com",
    priority=JobPriority.HIGH
)

# 执行采集
result = await collector.collect_url(job)
print(result)
```

## 环境变量

```bash
FIRECRAWL_API_KEY=your-api-key
FIRECRAWL_BASE_URL=https://api.firecrawl.dev
```

## 测试

```bash
# 运行单元测试
make test-unit

# 运行特定测试
pytest tests/unit/test_collector.py -v
```
```

### 5. 提交建议

```bash
# 提交信息
feat(core): implement Firecrawl data collector with async support

- Add FirecrawlCollector class with URL collection functionality
- Implement Job model with status and priority management
- Add async batch processing capabilities
- Include comprehensive unit tests with 95% coverage
- Add API endpoints for job creation and status query
- Update documentation with usage examples

Closes #123
```

## 🔍 质量检查

### 实现质量检查
- [ ] 代码符合项目规范
- [ ] 包含完整的类型提示
- [ ] 错误处理完善
- [ ] 日志记录适当
- [ ] 测试覆盖率达标
- [ ] 文档已更新

### 功能验证
- [ ] 核心功能正常工作
- [ ] API接口响应正确
- [ ] 错误场景处理正确
- [ ] 性能指标达标

## 📝 输出位置
生成的代码应保存到对应的文件路径，并按照项目结构组织。
