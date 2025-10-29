#!/usr/bin/env python3
"""HawaiiHub 新闻采集系统 - 数据存储模块

实现数据保存、导出和管理功能
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from config import (
    DATA_PROCESSING,
    EXPORT_CONFIG,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)


logger = logging.getLogger(__name__)


class NewsStorage:
    """新闻数据存储管理器"""

    def __init__(
        self, raw_dir: str = RAW_DATA_DIR, processed_dir: str = PROCESSED_DATA_DIR
    ):
        """初始化存储管理器

        Args:
            raw_dir: 原始数据目录
            processed_dir: 处理后数据目录
        """
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)

        # 确保目录存在
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        logger.info("数据存储管理器已初始化")
        logger.info(f"  原始数据目录: {self.raw_dir}")
        logger.info(f"  处理数据目录: {self.processed_dir}")

    def save_raw_data(self, data: Dict | List, filename: str) -> Path:
        """保存原始数据（JSON格式）

        Args:
            data: 要保存的数据
            filename: 文件名

        Returns:
            保存的文件路径
        """
        filepath = self.raw_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=EXPORT_CONFIG["json_indent"])

        logger.info(f"✅ 原始数据已保存: {filepath}")
        return filepath

    def save_processed_data(self, data: Dict | List, filename: str) -> Path:
        """保存处理后的数据（JSON格式）

        Args:
            data: 要保存的数据
            filename: 文件名

        Returns:
            保存的文件路径
        """
        filepath = self.processed_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=EXPORT_CONFIG["json_indent"])

        logger.info(f"✅ 处理数据已保存: {filepath}")
        return filepath

    def export_to_json(self, data: List[Dict], filename: str) -> Path:
        """导出为 JSON 文件

        Args:
            data: 要导出的数据列表
            filename: 文件名

        Returns:
            导出的文件路径
        """
        filepath = self.processed_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=EXPORT_CONFIG["json_indent"])

        logger.info(f"📄 导出 JSON: {filepath} ({len(data)} 条记录)")
        return filepath

    def export_to_markdown(self, data: List[Dict], filename: str) -> Path:
        """导出为 Markdown 文件

        Args:
            data: 要导出的数据列表
            filename: 文件名

        Returns:
            导出的文件路径
        """
        filepath = self.processed_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            # 写入标题
            f.write("# HawaiiHub 新闻采集结果\n\n")
            f.write(f"> 导出时间: {datetime.now()}\n\n")
            f.write(f"> 文章数量: {len(data)}\n\n")
            f.write("---\n\n")

            # 写入每篇文章
            for i, article in enumerate(data, 1):
                f.write(f"## {i}. {article.get('title', 'Untitled')}\n\n")
                f.write(f"**来源**: {article.get('source_name', 'Unknown')}\n\n")
                f.write(f"**URL**: {article.get('url', 'N/A')}\n\n")
                f.write(f"**采集时间**: {article.get('scraped_at', 'N/A')}\n\n")

                # 文章内容
                content = article.get("content", "")
                if content:
                    f.write(f"{content}\n\n")

                f.write("---\n\n")

        logger.info(f"📝 导出 Markdown: {filepath} ({len(data)} 条记录)")
        return filepath

    def export_to_csv(self, data: List[Dict], filename: str) -> Path:
        """导出为 CSV 文件

        Args:
            data: 要导出的数据列表
            filename: 文件名

        Returns:
            导出的文件路径
        """
        if not data:
            logger.warning("没有数据可导出")
            return None

        filepath = self.processed_dir / filename

        # 提取所有字段
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())

        fieldnames = sorted(fieldnames)

        with open(
            filepath, "w", encoding=EXPORT_CONFIG["csv_encoding"], newline=""
        ) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"📊 导出 CSV: {filepath} ({len(data)} 条记录)")
        return filepath

    def export_news_results(self, results: List[Dict], prefix: str = "news") -> Dict:
        """导出新闻采集结果到多种格式

        Args:
            results: 采集结果列表
            prefix: 文件名前缀

        Returns:
            导出的文件路径字典
        """
        timestamp = datetime.now().strftime(EXPORT_CONFIG["timestamp_format"])

        # 处理数据：提取所有文章
        all_articles = []
        for result in results:
            source_name = result.get("source_name", "Unknown")
            source_id = result.get("source_id", "unknown")

            for article in result.get("articles", []):
                all_articles.append(
                    {
                        "source_id": source_id,
                        "source_name": source_name,
                        "url": article.get("url"),
                        "title": article.get("metadata", {}).get("title"),
                        "description": article.get("metadata", {}).get("description"),
                        "content": article.get("content", {}).get("markdown"),
                        "scraped_at": article.get("scraped_at"),
                    }
                )

        logger.info(f"准备导出 {len(all_articles)} 篇文章")

        exported_files = {}

        # 导出 JSON
        if "json" in EXPORT_CONFIG["formats"]:
            filename = f"{prefix}_{timestamp}.json"
            exported_files["json"] = self.export_to_json(all_articles, filename)

        # 导出 Markdown
        if "markdown" in EXPORT_CONFIG["formats"]:
            filename = f"{prefix}_{timestamp}.md"
            exported_files["markdown"] = self.export_to_markdown(all_articles, filename)

        # 导出 CSV
        if "csv" in EXPORT_CONFIG["formats"]:
            filename = f"{prefix}_{timestamp}.csv"
            exported_files["csv"] = self.export_to_csv(all_articles, filename)

        logger.info(f"✅ 导出完成: {len(exported_files)} 个文件")
        for format_name, filepath in exported_files.items():
            logger.info(f"   {format_name.upper()}: {filepath}")

        return exported_files

    def clean_old_files(self, days_to_keep: int = 30) -> int:
        """清理旧数据文件

        Args:
            days_to_keep: 保留天数

        Returns:
            删除的文件数量
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0

        for directory in [self.raw_dir, self.processed_dir]:
            for filepath in directory.rglob("*"):
                if filepath.is_file():
                    file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if file_time < cutoff_date:
                        filepath.unlink()
                        deleted_count += 1
                        logger.debug(f"删除旧文件: {filepath}")

        logger.info(f"🧹 清理完成: 删除 {deleted_count} 个旧文件")
        return deleted_count


def process_article_content(content: str) -> str:
    """处理文章内容（清洗、规范化）

    Args:
        content: 原始内容

    Returns:
        处理后的内容
    """
    import re

    if not content:
        return ""

    # 移除特定模式
    for pattern in DATA_PROCESSING["remove_patterns"]:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    # 规范化空白
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r" {2,}", " ", content)

    # 移除首尾空白
    content = content.strip()

    return content


def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """文章去重

    Args:
        articles: 文章列表

    Returns:
        去重后的文章列表
    """
    if not DATA_PROCESSING["enable_deduplication"]:
        return articles

    dedup_field = DATA_PROCESSING["dedup_field"]
    seen = set()
    unique_articles = []

    for article in articles:
        key = article.get(dedup_field)
        if key and key not in seen:
            seen.add(key)
            unique_articles.append(article)

    removed_count = len(articles) - len(unique_articles)
    if removed_count > 0:
        logger.info(f"🔄 去重: 移除 {removed_count} 篇重复文章")

    return unique_articles
