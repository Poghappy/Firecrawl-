# 测试模板

## 🎯 角色设定
你是QA工程师，具备丰富的测试设计和自动化测试经验。请生成可执行的测试用例和手工检查要点。

## 📥 输入格式

### 功能需求输入
```
[从实现模板生成的功能模块]
```

### 技术实现输入
```
[从实现模板生成的代码实现]
```

### 验收标准输入
```
[从用户故事和PRD中的验收标准]
```

## 📤 输出格式

### 1. 测试用例表格

| 用例ID | 场景            | 前置条件                   | 步骤                                          | 预期结果                        | 自动化(是/否) | 备注         |
| ------ | --------------- | -------------------------- | --------------------------------------------- | ------------------------------- | ------------- | ------------ |
| UT-001 | 成功采集单个URL | API密钥有效，目标URL可访问 | 1. 创建采集任务<br>2. 执行采集<br>3. 验证结果 | 返回结构化数据，状态为completed | 是            | 核心功能测试 |
| UT-002 | 采集不存在的URL | API密钥有效                | 1. 创建采集任务(无效URL)<br>2. 执行采集       | 返回错误信息，状态为failed      | 是            | 错误处理测试 |
| UT-003 | 批量采集多个URL | API密钥有效，多个URL可访问 | 1. 创建批量任务<br>2. 执行批量采集            | 所有任务完成，返回结果列表      | 是            | 批量处理测试 |

### 2. 测试分类详细说明

#### 单元测试 (Unit Tests)

##### 测试目标
- 验证单个函数或方法的行为
- 确保代码逻辑正确
- 覆盖边界条件和异常情况

##### 测试用例
```python
# tests/unit/test_collector.py
"""
数据采集器单元测试
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.core.collector import FirecrawlCollector, Job, JobStatus, CollectionError


class TestFirecrawlCollector:
    """Firecrawl采集器单元测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.collector = FirecrawlCollector("test-api-key")
        self.test_job = Job(
            id="test-job",
            url="https://example.com",
            status=JobStatus.PENDING
        )
    
    @pytest.mark.asyncio
    async def test_collect_url_success(self):
        """测试成功采集URL - UT-001"""
        # Given
        mock_result = {
            "title": "Test Title",
            "content": "Test Content",
            "metadata": {"author": "Test Author"}
        }
        
        with patch.object(self.collector, '_call_firecrawl_api', return_value=mock_result):
            # When
            result = await self.collector.collect_url(self.test_job)
            
            # Then
            assert result["job_id"] == "test-job"
            assert result["status"] == "success"
            assert result["data"]["title"] == "Test Title"
    
    @pytest.mark.asyncio
    async def test_collect_url_api_failure(self):
        """测试API调用失败 - UT-002"""
        # Given
        with patch.object(self.collector, '_call_firecrawl_api', side_effect=Exception("API Error")):
            # When & Then
            with pytest.raises(CollectionError, match="采集失败"):
                await self.collector.collect_url(self.test_job)
    
    @pytest.mark.asyncio
    async def test_collect_url_timeout(self):
        """测试采集超时 - UT-003"""
        # Given
        with patch.object(self.collector, '_call_firecrawl_api', side_effect=asyncio.TimeoutError):
            # When & Then
            with pytest.raises(CollectionError):
                await self.collector.collect_url(self.test_job)
    
    def test_process_result_with_empty_data(self):
        """测试处理空数据结果 - UT-004"""
        # Given
        raw_result = {}
        
        # When
        result = self.collector._process_result(raw_result, self.test_job)
        
        # Then
        assert result["status"] == "success"
        assert result["data"]["title"] == ""
        assert result["data"]["content"] == ""
    
    @pytest.mark.asyncio
    async def test_collect_with_custom_options(self):
        """测试自定义采集选项 - UT-005"""
        # Given
        job = Job(
            id="test-job",
            url="https://example.com",
            options=CollectionOptions(
                max_pages=5,
                timeout=60,
                retry_count=5
            )
        )
        
        with patch.object(self.collector, '_call_firecrawl_api') as mock_call:
            mock_call.return_value = {"title": "Test"}
            
            # When
            await self.collector.collect_url(job)
            
            # Then
            mock_call.assert_called_once()
            call_args = mock_call.call_args[1]
            assert call_args["options"]["maxPages"] == 5
            assert call_args["options"]["timeout"] == 60000
```

#### 集成测试 (Integration Tests)

##### 测试目标
- 验证模块间的交互
- 确保API接口正常工作
- 测试数据库集成

##### 测试用例
```python
# tests/integration/test_api_integration.py
"""
API集成测试
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json

from src.api.main import app
from src.models.job import Job, JobStatus


class TestAPIIntegration:
    """API集成测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.client = TestClient(app)
        self.test_job_data = {
            "url": "https://example.com",
            "priority": 2,
            "max_pages": 10,
            "timeout": 30
        }
    
    def test_create_job_success(self):
        """测试成功创建任务 - IT-001"""
        # Given
        with patch('src.api.routes.get_job_repository') as mock_repo:
            mock_repo.return_value.create_job.return_value = None
            
            # When
            response = self.client.post("/api/v1/jobs", json=self.test_job_data)
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert "job_id" in data
            assert data["url"] == "https://example.com"
            assert data["status"] == "pending"
    
    def test_create_job_invalid_url(self):
        """测试无效URL创建任务 - IT-002"""
        # Given
        invalid_data = {"url": "invalid-url", "priority": 2}
        
        # When
        response = self.client.post("/api/v1/jobs", json=invalid_data)
        
        # Then
        assert response.status_code == 422  # Validation error
    
    def test_get_job_success(self):
        """测试成功获取任务状态 - IT-003"""
        # Given
        mock_job = Job(
            id="test-job-1",
            url="https://example.com",
            status=JobStatus.COMPLETED,
            result={"title": "Test Title"}
        )
        
        with patch('src.api.routes.get_job_repository') as mock_repo:
            mock_repo.return_value.get_job.return_value = mock_job
            
            # When
            response = self.client.get("/api/v1/jobs/test-job-1")
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "test-job-1"
            assert data["status"] == "completed"
            assert data["result"]["title"] == "Test Title"
    
    def test_get_job_not_found(self):
        """测试获取不存在的任务 - IT-004"""
        # Given
        with patch('src.api.routes.get_job_repository') as mock_repo:
            mock_repo.return_value.get_job.return_value = None
            
            # When
            response = self.client.get("/api/v1/jobs/non-existent-job")
            
            # Then
            assert response.status_code == 404
            assert "任务不存在" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_job_processing_workflow(self):
        """测试完整任务处理流程 - IT-005"""
        # Given
        with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
            mock_collector = mock_collector_class.return_value
            mock_collector.collect_url.return_value = {
                "job_id": "test-job",
                "status": "success",
                "data": {"title": "Test Title"}
            }
            
            # When
            response = self.client.post("/api/v1/jobs", json=self.test_job_data)
            
            # Then
            assert response.status_code == 200
            job_id = response.json()["job_id"]
            
            # 等待后台任务处理（模拟）
            import asyncio
            await asyncio.sleep(0.1)
            
            # 验证任务状态更新
            get_response = self.client.get(f"/api/v1/jobs/{job_id}")
            assert get_response.status_code == 200
```

#### 端到端测试 (End-to-End Tests)

##### 测试目标
- 验证完整的用户工作流
- 测试系统在真实环境中的行为
- 确保所有组件协同工作

##### 测试用例
```python
# tests/e2e/test_e2e_workflow.py
"""
端到端测试
"""

import pytest
import asyncio
from unittest.mock import patch
import time

from src.core.collector import AsyncFirecrawlCollector, Job, JobPriority
from src.api.main import app
from fastapi.testclient import TestClient


class TestE2EWorkflow:
    """端到端测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.client = TestClient(app)
    
    @pytest.mark.asyncio
    async def test_complete_collection_workflow(self):
        """测试完整采集工作流 - E2E-001"""
        # Given
        test_url = "https://example.com"
        
        # When - 创建任务
        response = self.client.post("/api/v1/jobs", json={
            "url": test_url,
            "priority": JobPriority.HIGH.value,
            "max_pages": 1,
            "timeout": 30
        })
        
        # Then - 验证任务创建
        assert response.status_code == 200
        job_data = response.json()
        job_id = job_data["job_id"]
        assert job_data["status"] == "pending"
        assert job_data["url"] == test_url
        
        # 等待任务处理完成（实际环境中可能需要更长时间）
        max_wait_time = 60  # 60秒超时
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status_response = self.client.get(f"/api/v1/jobs/{job_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            if status_data["status"] in ["completed", "failed"]:
                break
            
            await asyncio.sleep(1)
        
        # 验证最终状态
        final_response = self.client.get(f"/api/v1/jobs/{job_id}")
        assert final_response.status_code == 200
        
        final_data = final_response.json()
        assert final_data["status"] in ["completed", "failed"]
        
        if final_data["status"] == "completed":
            assert final_data["result"] is not None
            assert "data" in final_data["result"]
    
    @pytest.mark.asyncio
    async def test_batch_collection_workflow(self):
        """测试批量采集工作流 - E2E-002"""
        # Given
        test_urls = [
            "https://example.com",
            "https://httpbin.org/html",
            "https://httpbin.org/json"
        ]
        
        # When - 创建多个任务
        job_ids = []
        for url in test_urls:
            response = self.client.post("/api/v1/jobs", json={
                "url": url,
                "priority": JobPriority.NORMAL.value
            })
            assert response.status_code == 200
            job_ids.append(response.json()["job_id"])
        
        # Then - 等待所有任务完成
        max_wait_time = 120  # 2分钟超时
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            all_completed = True
            for job_id in job_ids:
                status_response = self.client.get(f"/api/v1/jobs/{job_id}")
                assert status_response.status_code == 200
                
                status = status_response.json()["status"]
                if status not in ["completed", "failed"]:
                    all_completed = False
                    break
            
            if all_completed:
                break
            
            await asyncio.sleep(2)
        
        # 验证所有任务状态
        for job_id in job_ids:
            final_response = self.client.get(f"/api/v1/jobs/{job_id}")
            assert final_response.status_code == 200
            
            final_data = final_response.json()
            assert final_data["status"] in ["completed", "failed"]
    
    @pytest.mark.asyncio
    async def test_error_handling_workflow(self):
        """测试错误处理工作流 - E2E-003"""
        # Given - 使用无效URL
        invalid_url = "https://non-existent-domain-12345.com"
        
        # When - 创建任务
        response = self.client.post("/api/v1/jobs", json={
            "url": invalid_url,
            "timeout": 5  # 短超时时间
        })
        
        # Then - 验证任务创建
        assert response.status_code == 200
        job_id = response.json()["job_id"]
        
        # 等待任务失败
        max_wait_time = 30
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status_response = self.client.get(f"/api/v1/jobs/{job_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            if status_data["status"] == "failed":
                assert status_data["error_message"] is not None
                break
            
            await asyncio.sleep(1)
        
        # 验证最终失败状态
        final_response = self.client.get(f"/api/v1/jobs/{job_id}")
        assert final_response.status_code == 200
        
        final_data = final_response.json()
        assert final_data["status"] == "failed"
        assert final_data["error_message"] is not None
```

### 3. 性能测试

#### 性能基准测试
```python
# tests/benchmark/test_performance.py
"""
性能基准测试
"""

import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.core.collector import AsyncFirecrawlCollector, Job, JobPriority


class TestPerformance:
    """性能测试类"""
    
    @pytest.mark.asyncio
    async def test_single_job_performance(self):
        """测试单个任务性能 - PT-001"""
        # Given
        job = Job(
            id="perf-test-1",
            url="https://example.com",
            priority=JobPriority.HIGH
        )
        
        # When
        start_time = time.time()
        
        with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
            mock_collector = mock_collector_class.return_value
            mock_collector.collect_url.return_value = {"status": "success"}
            
            async with AsyncFirecrawlCollector("test-key") as collector:
                result = await collector._collect_single(job)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Then
        assert duration < 5.0  # 单个任务应在5秒内完成
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_batch_job_performance(self):
        """测试批量任务性能 - PT-002"""
        # Given
        jobs = [
            Job(id=f"batch-test-{i}", url=f"https://example{i}.com")
            for i in range(10)
        ]
        
        # When
        start_time = time.time()
        
        with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
            mock_collector = mock_collector_class.return_value
            mock_collector.collect_url.return_value = {"status": "success"}
            
            async with AsyncFirecrawlCollector("test-key") as collector:
                results = await collector.collect_batch(jobs)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Then
        assert len(results) == 10
        assert duration < 30.0  # 10个任务应在30秒内完成
        assert all(r["status"] == "success" for r in results)
    
    @pytest.mark.asyncio
    async def test_concurrent_job_performance(self):
        """测试并发任务性能 - PT-003"""
        # Given
        async def create_and_process_job(job_id: int):
            job = Job(
                id=f"concurrent-test-{job_id}",
                url=f"https://example{job_id}.com"
            )
            
            with patch('src.core.collector.FirecrawlCollector') as mock_collector_class:
                mock_collector = mock_collector_class.return_value
                mock_collector.collect_url.return_value = {"status": "success"}
                
                async with AsyncFirecrawlCollector("test-key") as collector:
                    return await collector._collect_single(job)
        
        # When
        start_time = time.time()
        
        tasks = [create_and_process_job(i) for i in range(20)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Then
        assert len(results) == 20
        assert duration < 60.0  # 20个并发任务应在60秒内完成
        assert all(r["status"] == "success" for r in results)
```

### 4. 手工检查要点

#### 功能检查清单
- [ ] **API接口检查**
  - [ ] 任务创建接口响应正常
  - [ ] 任务状态查询接口正常
  - [ ] 错误响应格式正确
  - [ ] 请求参数验证正常

- [ ] **数据采集检查**
  - [ ] 正常URL采集成功
  - [ ] 无效URL处理正确
  - [ ] 超时处理正常
  - [ ] 重试机制有效

- [ ] **数据处理检查**
  - [ ] 数据清洗逻辑正确
  - [ ] 结构化数据格式正确
  - [ ] 元数据提取完整
  - [ ] 链接提取正常

#### 性能检查清单
- [ ] **响应时间检查**
  - [ ] 单个任务处理时间 ≤ 30秒
  - [ ] API响应时间 ≤ 2秒
  - [ ] 批量任务处理效率正常

- [ ] **并发能力检查**
  - [ ] 支持100个并发任务
  - [ ] 系统资源使用正常
  - [ ] 无内存泄漏问题

#### 安全检查清单
- [ ] **输入验证检查**
  - [ ] URL格式验证
  - [ ] 参数范围检查
  - [ ] 恶意输入防护

- [ ] **权限检查**
  - [ ] API访问控制
  - [ ] 数据访问权限
  - [ ] 敏感信息保护

### 5. 测试执行命令

#### 运行所有测试
```bash
# 运行所有测试
make test

# 运行单元测试
make test-unit

# 运行集成测试
make test-integration

# 运行端到端测试
make test-e2e

# 运行性能测试
make benchmark
```

#### 生成测试报告
```bash
# 生成覆盖率报告
make cov

# 生成HTML测试报告
pytest --html=report.html --self-contained-html

# 生成JUnit XML报告
pytest --junitxml=test-results.xml
```

### 6. 成功/失败判定标准

#### 测试通过标准
- [ ] 所有单元测试通过
- [ ] 所有集成测试通过
- [ ] 所有端到端测试通过
- [ ] 代码覆盖率 ≥ 80%
- [ ] 性能指标达标
- [ ] 安全检查通过

#### 测试失败处理
1. **分析失败原因**
   - 检查测试日志
   - 分析错误堆栈
   - 确认环境配置

2. **修复问题**
   - 修复代码缺陷
   - 更新测试用例
   - 调整测试环境

3. **重新验证**
   - 重新运行失败测试
   - 验证修复效果
   - 确保无回归问题

## 🔍 质量检查

### 测试用例质量检查
- [ ] 测试用例覆盖正常和异常场景
- [ ] 测试数据准备充分
- [ ] 断言检查点明确
- [ ] 测试独立性保证

### 测试执行质量检查
- [ ] 测试环境配置正确
- [ ] 测试数据隔离
- [ ] 测试结果可重现
- [ ] 测试报告完整

## 📝 输出位置
生成的测试用例应保存到 `docs/TEST_PLAN.md` 文件中，测试代码保存到对应的测试目录。
