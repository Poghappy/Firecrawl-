# 项目健康检查报告

**生成时间**: 2025-10-29T03:50:02.502335
**项目版本**: v2.1.0
**整体得分**: 68/100
**健康状况**: GOOD

---

## ❌ 安全检查 (0/100)

**问题**:
- 发现硬编码 API Key: /Users/zhiledeng/Movies/Firecrawl数据采集器/tests/quick_test.py
- 发现硬编码 API Key: /Users/zhiledeng/Movies/Firecrawl数据采集器/honolulu_rentals/config.py
- 发现硬编码 API Key: /Users/zhiledeng/Movies/Firecrawl数据采集器/scripts/test-firecrawl-api.py
- 发现硬编码 API Key: /Users/zhiledeng/Movies/Firecrawl数据采集器/scripts/github-actions/verify-github-secrets.py

**建议**:
- 使用环境变量存储敏感信息
- 添加 pre-commit 钩子检测泄露
- 定期审计代码

## ✅ 代码质量 (100/100)

**统计**:
- total_files: 23
- total_lines: 9277
- type_hint_coverage: 91.3%
- docstring_coverage: 100.0%

## ❌ 测试覆盖率 (30/100)

**统计**:
- test_files: 2
- source_files: 23
- estimated_coverage: ~17%

**问题**:
- 测试覆盖率过低: ~17%

**建议**:
- 目标覆盖率: >80%
- 添加单元测试
- 添加集成测试

## ✅ 依赖检查 (100/100)

**统计**:
- total_dependencies: 56
- pinned_versions: 100%

## ✅ 配置完整性 (100/100)

## ✅ 文档完整性 (100/100)

## ✅ 代码规范 (70/100)

**问题**:
- 缺少代码格式化配置

## ❌ 性能指标 (50/100)

**统计**:
- async_usage: 39%

**问题**:
- 异步代码使用率低: 39%

---

## 总结

项目整体健康状况: **GOOD**

⚠️ 项目状态良好，建议处理上述问题。