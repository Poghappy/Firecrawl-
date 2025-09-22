#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Configuration Manager for 火鸟门户系统
基于 Open-WebUI-Pipelines 架构的配置管理系统

@version: 2.0.0
@author: 火鸟门户开发团队
@description: 统一的配置管理和验证系统
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
import secrets
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class CacheBackend(str, Enum):
    REDIS = "redis"
    MEMORY = "memory"
    FILE = "file"
    DISABLED = "disabled"

class DatabaseType(str, Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DINGTALK = "dingtalk"
    WECHAT = "wechat"

# 基础配置模型
class APIConfig(BaseModel):
    """API 配置"""
    firecrawl_api_key: str = Field(..., description="Firecrawl API 密钥")
    base_url: str = Field(default="https://api.firecrawl.dev/v1", description="API 基础URL")
    timeout: int = Field(default=30, ge=5, le=300, description="请求超时时间（秒）")
    max_retries: int = Field(default=3, ge=0, le=10, description="最大重试次数")
    retry_delay: float = Field(default=1.0, ge=0.1, le=60.0, description="重试延迟（秒）")
    rate_limit: int = Field(default=100, ge=1, le=1000, description="每分钟请求限制")
    
    @field_validator('firecrawl_api_key')
    @classmethod
    def validate_api_key(cls, v):
        if not v or len(v) < 10:
            raise ValueError('API key must be at least 10 characters long')
        return v
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Base URL must start with http:// or https://')
        return v.rstrip('/')

class CrawlConfig(BaseModel):
    """爬取配置"""
    default_max_depth: int = Field(default=3, ge=1, le=10, description="默认最大深度")
    default_limit: int = Field(default=100, ge=1, le=10000, description="默认页面限制")
    default_format: str = Field(default="markdown", description="默认输出格式")
    default_timeout: int = Field(default=30, ge=5, le=300, description="默认页面超时")
    
    # 高级选项
    ignore_sitemap: bool = Field(default=False, description="忽略站点地图")
    ignore_query_parameters: bool = Field(default=False, description="忽略查询参数")
    allow_backward_links: bool = Field(default=False, description="允许反向链接")
    allow_external_links: bool = Field(default=False, description="允许外部链接")
    
    # 内容提取选项
    include_html: bool = Field(default=True, description="包含HTML内容")
    include_raw_html: bool = Field(default=False, description="包含原始HTML")
    include_screenshot: bool = Field(default=False, description="包含截图")
    include_links: bool = Field(default=True, description="包含链接")
    
    # 过滤选项
    exclude_tags: List[str] = Field(default_factory=lambda: ['script', 'style', 'nav', 'footer'], description="排除的HTML标签")
    only_main_content: bool = Field(default=True, description="仅提取主要内容")
    
    @field_validator('default_format')
    @classmethod
    def validate_format(cls, v):
        allowed_formats = ['markdown', 'html', 'text', 'structured']
        if v not in allowed_formats:
            raise ValueError(f'Format must be one of: {allowed_formats}')
        return v

class TaskConfig(BaseModel):
    """任务配置"""
    max_concurrent_jobs: int = Field(default=5, ge=1, le=50, description="最大并发任务数")
    job_timeout: int = Field(default=3600, ge=60, le=86400, description="任务超时时间（秒）")
    retry_attempts: int = Field(default=3, ge=0, le=10, description="重试次数")
    retry_delay: float = Field(default=5.0, ge=1.0, le=300.0, description="重试延迟（秒）")
    
    # 队列配置
    queue_max_size: int = Field(default=1000, ge=10, le=10000, description="队列最大大小")
    worker_check_interval: int = Field(default=10, ge=1, le=300, description="工作线程检查间隔（秒）")
    status_check_interval: int = Field(default=30, ge=5, le=600, description="状态检查间隔（秒）")
    
    # 清理配置
    cleanup_completed_jobs: bool = Field(default=True, description="清理已完成任务")
    cleanup_after_days: int = Field(default=7, ge=1, le=365, description="清理天数")
    cleanup_failed_jobs: bool = Field(default=False, description="清理失败任务")

class CacheConfig(BaseModel):
    """缓存配置"""
    enabled: bool = Field(default=True, description="启用缓存")
    backend: CacheBackend = Field(default=CacheBackend.REDIS, description="缓存后端")
    ttl: int = Field(default=86400, ge=60, le=604800, description="缓存TTL（秒）")
    
    # Redis 配置
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis连接URL")
    redis_password: Optional[str] = Field(default=None, description="Redis密码")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis数据库")
    
    # 内存缓存配置
    memory_max_size: int = Field(default=1000, ge=10, le=100000, description="内存缓存最大条目数")
    
    # 文件缓存配置
    file_cache_dir: str = Field(default="./cache", description="文件缓存目录")
    file_max_size_mb: int = Field(default=1024, ge=10, le=10240, description="文件缓存最大大小（MB）")
    
    @field_validator('redis_url')
    @classmethod
    def validate_redis_url(cls, v):
        if not v.startswith('redis://'):
            raise ValueError('Redis URL must start with redis://')
        return v

class DatabaseConfig(BaseModel):
    """数据库配置"""
    type: DatabaseType = Field(default=DatabaseType.SQLITE, description="数据库类型")
    url: str = Field(default="sqlite:///firecrawl_jobs.db", description="数据库连接URL")
    
    # 连接池配置
    pool_size: int = Field(default=10, ge=1, le=100, description="连接池大小")
    max_overflow: int = Field(default=20, ge=0, le=100, description="最大溢出连接数")
    pool_timeout: int = Field(default=30, ge=5, le=300, description="连接池超时")
    pool_recycle: int = Field(default=3600, ge=300, le=86400, description="连接回收时间")
    
    # 备份配置
    backup_enabled: bool = Field(default=True, description="启用备份")
    backup_interval: int = Field(default=86400, ge=3600, le=604800, description="备份间隔（秒）")
    backup_keep_days: int = Field(default=30, ge=1, le=365, description="备份保留天数")
    backup_path: str = Field(default="./backups", description="备份路径")

class SecurityConfig(BaseModel):
    """安全配置"""
    # API 安全
    api_key_rotation_days: int = Field(default=90, ge=7, le=365, description="API密钥轮换天数")
    enable_request_signing: bool = Field(default=False, description="启用请求签名")
    signing_secret: Optional[str] = Field(default=None, description="签名密钥")
    
    # 访问控制
    allowed_domains: List[str] = Field(default_factory=list, description="允许的域名")
    blocked_domains: List[str] = Field(default_factory=list, description="阻止的域名")
    rate_limit_per_ip: int = Field(default=1000, ge=10, le=10000, description="每IP速率限制")
    
    # 数据安全
    encrypt_sensitive_data: bool = Field(default=True, description="加密敏感数据")
    encryption_key: Optional[str] = Field(default=None, description="加密密钥")
    
    # 审计
    enable_audit_log: bool = Field(default=True, description="启用审计日志")
    audit_log_retention_days: int = Field(default=90, ge=7, le=365, description="审计日志保留天数")
    
    @model_validator(mode='after')
    def validate_security_config(self):
        if self.enable_request_signing and not self.signing_secret:
            raise ValueError('Signing secret is required when request signing is enabled')
        
        if self.encrypt_sensitive_data and not self.encryption_key:
            # 自动生成加密密钥
            self.encryption_key = secrets.token_urlsafe(32)
        
        return self

class NotificationConfig(BaseModel):
    """通知配置"""
    enabled: bool = Field(default=True, description="启用通知")
    channels: List[NotificationChannel] = Field(default_factory=lambda: [NotificationChannel.WEBHOOK], description="通知渠道")
    
    # Webhook 配置
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL")
    webhook_secret: Optional[str] = Field(default=None, description="Webhook 密钥")
    webhook_timeout: int = Field(default=10, ge=1, le=60, description="Webhook 超时")
    
    # 邮件配置
    email_smtp_host: Optional[str] = Field(default=None, description="SMTP主机")
    email_smtp_port: int = Field(default=587, description="SMTP端口")
    email_username: Optional[str] = Field(default=None, description="邮箱用户名")
    email_password: Optional[str] = Field(default=None, description="邮箱密码")
    email_from: Optional[str] = Field(default=None, description="发件人邮箱")
    email_to: List[str] = Field(default_factory=list, description="收件人邮箱列表")
    
    # Slack 配置
    slack_webhook_url: Optional[str] = Field(default=None, description="Slack Webhook URL")
    slack_channel: Optional[str] = Field(default=None, description="Slack 频道")
    
    # 钉钉配置
    dingtalk_webhook_url: Optional[str] = Field(default=None, description="钉钉 Webhook URL")
    dingtalk_secret: Optional[str] = Field(default=None, description="钉钉密钥")
    
    # 通知规则
    notify_on_start: bool = Field(default=False, description="任务开始时通知")
    notify_on_complete: bool = Field(default=True, description="任务完成时通知")
    notify_on_error: bool = Field(default=True, description="任务错误时通知")
    notify_on_timeout: bool = Field(default=True, description="任务超时时通知")
    
    @model_validator(mode='after')
    def validate_notification_config(self):
        if self.enabled and not self.channels:
            raise ValueError('At least one notification channel must be specified when notifications are enabled')
        
        # 验证各渠道的必需配置
        if NotificationChannel.WEBHOOK in self.channels and not self.webhook_url:
            raise ValueError('Webhook URL is required when webhook notifications are enabled')
        
        if NotificationChannel.EMAIL in self.channels:
            required_fields = {
                'email_smtp_host': self.email_smtp_host,
                'email_username': self.email_username,
                'email_password': self.email_password,
                'email_from': self.email_from
            }
            for field_name, field_value in required_fields.items():
                if not field_value:
                    raise ValueError(f'{field_name} is required when email notifications are enabled')
        
        return self

class LoggingConfig(BaseModel):
    """日志配置"""
    level: LogLevel = Field(default=LogLevel.INFO, description="日志级别")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="日志格式")
    
    # 文件日志
    file_enabled: bool = Field(default=True, description="启用文件日志")
    file_path: str = Field(default="./logs/firecrawl.log", description="日志文件路径")
    file_max_size_mb: int = Field(default=100, ge=1, le=1000, description="日志文件最大大小（MB）")
    file_backup_count: int = Field(default=5, ge=1, le=50, description="日志文件备份数量")
    
    # 控制台日志
    console_enabled: bool = Field(default=True, description="启用控制台日志")
    console_level: LogLevel = Field(default=LogLevel.INFO, description="控制台日志级别")
    
    # 结构化日志
    structured_logging: bool = Field(default=False, description="启用结构化日志")
    json_format: bool = Field(default=False, description="使用JSON格式")
    
    # 远程日志
    remote_logging: bool = Field(default=False, description="启用远程日志")
    remote_url: Optional[str] = Field(default=None, description="远程日志URL")
    remote_api_key: Optional[str] = Field(default=None, description="远程日志API密钥")

class MonitoringConfig(BaseModel):
    """监控配置"""
    enabled: bool = Field(default=True, description="启用监控")
    
    # 性能监控
    performance_monitoring: bool = Field(default=True, description="启用性能监控")
    memory_threshold_mb: int = Field(default=1024, ge=100, le=10240, description="内存阈值（MB）")
    cpu_threshold_percent: int = Field(default=80, ge=10, le=100, description="CPU阈值（%）")
    
    # 健康检查
    health_check_enabled: bool = Field(default=True, description="启用健康检查")
    health_check_interval: int = Field(default=60, ge=10, le=600, description="健康检查间隔（秒）")
    health_check_timeout: int = Field(default=10, ge=1, le=60, description="健康检查超时（秒）")
    
    # 指标收集
    metrics_enabled: bool = Field(default=True, description="启用指标收集")
    metrics_port: int = Field(default=9090, ge=1024, le=65535, description="指标端口")
    metrics_path: str = Field(default="/metrics", description="指标路径")
    
    # 告警
    alerting_enabled: bool = Field(default=True, description="启用告警")
    alert_on_high_memory: bool = Field(default=True, description="高内存使用告警")
    alert_on_high_cpu: bool = Field(default=True, description="高CPU使用告警")
    alert_on_job_failure: bool = Field(default=True, description="任务失败告警")
    alert_on_queue_full: bool = Field(default=True, description="队列满告警")

class PipelineConfig(BaseModel):
    """主配置类"""
    # 基础信息
    name: str = Field(default="Firecrawl Pipeline", description="Pipeline名称")
    version: str = Field(default="2.0.0", description="版本号")
    description: str = Field(default="火鸟门户系统 Firecrawl 数据采集器", description="描述")
    
    # 各模块配置
    api: APIConfig = Field(default_factory=APIConfig, description="API配置")
    crawl: CrawlConfig = Field(default_factory=CrawlConfig, description="爬取配置")
    task: TaskConfig = Field(default_factory=TaskConfig, description="任务配置")
    cache: CacheConfig = Field(default_factory=CacheConfig, description="缓存配置")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig, description="数据库配置")
    security: SecurityConfig = Field(default_factory=SecurityConfig, description="安全配置")
    notification: NotificationConfig = Field(default_factory=NotificationConfig, description="通知配置")
    logging: LoggingConfig = Field(default_factory=LoggingConfig, description="日志配置")
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig, description="监控配置")
    
    # 环境配置
    environment: str = Field(default="production", description="运行环境")
    debug: bool = Field(default=False, description="调试模式")
    
    # 自定义配置
    custom: Dict[str, Any] = Field(default_factory=dict, description="自定义配置")
    
    class Config:
        extra = "allow"
        validate_assignment = True
    
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        allowed_envs = ['development', 'testing', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'Environment must be one of: {allowed_envs}')
        return v
    
    @model_validator(mode='after')
    def validate_config(self):
        # 环境特定验证
        if self.environment == 'production' and self.debug:
            logger.warning('Debug mode is enabled in production environment')
        
        return self

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config: Optional[PipelineConfig] = None
        self._config_hash: Optional[str] = None
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        # 按优先级查找配置文件
        possible_paths = [
            os.getenv('FIRECRAWL_CONFIG_PATH'),
            './config/pipeline.yaml',
            './config/pipeline.yml',
            './config/pipeline.json',
            './pipeline.yaml',
            './pipeline.yml',
            './pipeline.json'
        ]
        
        for path in possible_paths:
            if path and Path(path).exists():
                return path
        
        # 如果没有找到配置文件，返回默认路径
        return './config/pipeline.yaml'
    
    def load_config(self, config_path: Optional[str] = None) -> PipelineConfig:
        """加载配置"""
        if config_path:
            self.config_path = config_path
        
        try:
            if Path(self.config_path).exists():
                config_data = self._load_config_file(self.config_path)
                self.config = PipelineConfig(**config_data)
            else:
                logger.warning(f"Config file not found: {self.config_path}, using default config")
                self.config = self._create_default_config()
            
            # 应用环境变量覆盖
            self._apply_env_overrides()
            
            # 计算配置哈希
            self._config_hash = self._calculate_config_hash()
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
            
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise
    
    def _load_config_file(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        path = Path(config_path)
        
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(f) or {}
            elif path.suffix.lower() == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
    
    def _create_default_config(self) -> PipelineConfig:
        """创建默认配置"""
        return PipelineConfig(
            api=APIConfig(
                firecrawl_api_key=os.getenv('FIRECRAWL_API_KEY', '')
            ),
            database=DatabaseConfig(
                url=os.getenv('DATABASE_URL', 'sqlite:///firecrawl_jobs.db')
            ),
            cache=CacheConfig(
                redis_url=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            ),
            notification=NotificationConfig(
                enabled=False,
                webhook_url="https://example.com/webhook"
            )
        )
    
    def _apply_env_overrides(self):
        """应用环境变量覆盖"""
        if not self.config:
            return
        
        # API 配置覆盖
        if os.getenv('FIRECRAWL_API_KEY'):
            self.config.api.firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        
        if os.getenv('FIRECRAWL_BASE_URL'):
            self.config.api.base_url = os.getenv('FIRECRAWL_BASE_URL')
        
        # 数据库配置覆盖
        if os.getenv('DATABASE_URL'):
            self.config.database.url = os.getenv('DATABASE_URL')
        
        # Redis 配置覆盖
        if os.getenv('REDIS_URL'):
            self.config.cache.redis_url = os.getenv('REDIS_URL')
        
        # 日志级别覆盖
        if os.getenv('LOG_LEVEL'):
            try:
                self.config.logging.level = LogLevel(os.getenv('LOG_LEVEL').upper())
            except ValueError:
                logger.warning(f"Invalid log level: {os.getenv('LOG_LEVEL')}")
        
        # 调试模式覆盖
        if os.getenv('DEBUG'):
            self.config.debug = os.getenv('DEBUG').lower() in ['true', '1', 'yes']
        
        # 环境覆盖
        if os.getenv('ENVIRONMENT'):
            self.config.environment = os.getenv('ENVIRONMENT')
    
    def save_config(self, config_path: Optional[str] = None) -> None:
        """保存配置"""
        if not self.config:
            raise ValueError("No config to save")
        
        save_path = config_path or self.config_path
        path = Path(save_path)
        
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 导出配置数据
        config_data = self.config.dict()
        
        # 保存文件
        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            elif path.suffix.lower() == '.json':
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
        
        logger.info(f"Configuration saved to {save_path}")
    
    def reload_config(self) -> bool:
        """重新加载配置"""
        try:
            old_hash = self._config_hash
            self.load_config()
            
            # 检查配置是否有变化
            if old_hash != self._config_hash:
                logger.info("Configuration reloaded with changes")
                return True
            else:
                logger.debug("Configuration reloaded, no changes detected")
                return False
                
        except Exception as e:
            logger.error(f"Error reloading config: {str(e)}")
            return False
    
    def _calculate_config_hash(self) -> str:
        """计算配置哈希"""
        if not self.config:
            return ""
        
        config_str = json.dumps(self.config.dict(), sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()
    
    def validate_config(self) -> List[str]:
        """验证配置"""
        errors = []
        
        if not self.config:
            errors.append("No configuration loaded")
            return errors
        
        try:
            # 重新验证配置
            PipelineConfig(**self.config.dict())
        except Exception as e:
            errors.append(f"Configuration validation error: {str(e)}")
        
        # 自定义验证规则
        if not self.config.api.firecrawl_api_key:
            errors.append("Firecrawl API key is required")
        
        if self.config.cache.enabled and self.config.cache.backend == CacheBackend.REDIS:
            if not self.config.cache.redis_url:
                errors.append("Redis URL is required when Redis cache is enabled")
        
        if self.config.notification.enabled:
            if not self.config.notification.channels:
                errors.append("At least one notification channel must be configured")
        
        return errors
    
    def get_config(self) -> PipelineConfig:
        """获取配置"""
        if not self.config:
            self.load_config()
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """更新配置"""
        if not self.config:
            self.load_config()
        
        # 深度更新配置
        config_dict = self.config.dict()
        self._deep_update(config_dict, updates)
        
        # 重新创建配置对象
        self.config = PipelineConfig(**config_dict)
        
        # 重新计算哈希
        self._config_hash = self._calculate_config_hash()
        
        logger.info("Configuration updated")
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> None:
        """深度更新字典"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def export_config_template(self, output_path: str) -> None:
        """导出配置模板"""
        template_config = PipelineConfig()
        
        # 添加注释和示例
        config_dict = template_config.dict()
        
        # 保存模板
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix.lower() in ['.yaml', '.yml']:
                # 添加 YAML 注释
                f.write("# 火鸟门户系统 Firecrawl Pipeline 配置文件\n")
                f.write(f"# 生成时间: {datetime.now().isoformat()}\n")
                f.write("# 请根据实际需求修改配置项\n\n")
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            elif path.suffix.lower() == '.json':
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Configuration template exported to {output_path}")

# 全局配置管理器实例
config_manager = ConfigManager()

# 便捷函数
def get_config() -> PipelineConfig:
    """获取全局配置"""
    return config_manager.get_config()

def load_config(config_path: Optional[str] = None) -> PipelineConfig:
    """加载配置"""
    return config_manager.load_config(config_path)

def reload_config() -> bool:
    """重新加载配置"""
    return config_manager.reload_config()

def validate_config() -> List[str]:
    """验证配置"""
    return config_manager.validate_config()

# 使用示例
if __name__ == "__main__":
    # 创建配置管理器
    manager = ConfigManager()
    
    # 加载配置
    config = manager.load_config()
    print(f"Loaded config: {config.name} v{config.version}")
    
    # 验证配置
    errors = manager.validate_config()
    if errors:
        print(f"Configuration errors: {errors}")
    else:
        print("Configuration is valid")
    
    # 导出配置模板
    manager.export_config_template('./config/pipeline_template.yaml')
    print("Configuration template exported")