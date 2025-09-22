#!/usr/bin/env python3
"""
反馈收集系统
用于收集和分析AI Agent使用反馈，建立改进基线
"""

import json
import sqlite3
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class UserFeedback:
    """用户反馈数据"""
    feedback_id: str
    user_id: str
    session_id: str
    feedback_type: str  # usage, quality, performance, suggestion
    rating: int  # 1-5分
    category: str  # code_generation, problem_solving, documentation, etc.
    comment: str
    context: Dict[str, Any]
    timestamp: datetime
    priority: str = "medium"  # low, medium, high, critical

@dataclass
class SystemMetrics:
    """系统指标数据"""
    metric_id: str
    metric_name: str
    metric_value: float
    metric_unit: str
    timestamp: datetime
    context: Dict[str, Any]

@dataclass
class FeedbackAnalysis:
    """反馈分析结果"""
    analysis_id: str
    feedback_data: List[UserFeedback]
    system_metrics: List[SystemMetrics]
    insights: List[str]
    recommendations: List[str]
    action_items: List[str]
    confidence_score: float
    timestamp: datetime

class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self, db_path: str = "data/feedback.db"):
        """初始化反馈收集器"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建用户反馈表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_feedback (
                    feedback_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    session_id TEXT,
                    feedback_type TEXT NOT NULL,
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                    category TEXT,
                    comment TEXT,
                    context TEXT,
                    timestamp TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium'
                )
            ''')
            
            # 创建系统指标表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    metric_id TEXT PRIMARY KEY,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    timestamp TEXT NOT NULL,
                    context TEXT
                )
            ''')
            
            # 创建反馈分析表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback_analysis (
                    analysis_id TEXT PRIMARY KEY,
                    feedback_count INTEGER,
                    avg_rating REAL,
                    insights TEXT,
                    recommendations TEXT,
                    action_items TEXT,
                    confidence_score REAL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def collect_user_feedback(self, feedback: UserFeedback) -> bool:
        """收集用户反馈"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO user_feedback 
                    (feedback_id, user_id, session_id, feedback_type, rating, 
                     category, comment, context, timestamp, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    feedback.feedback_id,
                    feedback.user_id,
                    feedback.session_id,
                    feedback.feedback_type,
                    feedback.rating,
                    feedback.category,
                    feedback.comment,
                    json.dumps(feedback.context),
                    feedback.timestamp.isoformat(),
                    feedback.priority
                ))
                
                conn.commit()
                logger.info(f"用户反馈已收集: {feedback.feedback_id}")
                return True
                
        except Exception as e:
            logger.error(f"收集用户反馈失败: {e}")
            return False
    
    def collect_system_metrics(self, metrics: SystemMetrics) -> bool:
        """收集系统指标"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO system_metrics 
                    (metric_id, metric_name, metric_value, metric_unit, timestamp, context)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    metrics.metric_id,
                    metrics.metric_name,
                    metrics.metric_value,
                    metrics.metric_unit,
                    metrics.timestamp.isoformat(),
                    json.dumps(metrics.context)
                ))
                
                conn.commit()
                logger.info(f"系统指标已收集: {metrics.metric_name}")
                return True
                
        except Exception as e:
            logger.error(f"收集系统指标失败: {e}")
            return False
    
    def get_feedback_summary(self, days: int = 30) -> Dict[str, Any]:
        """获取反馈汇总"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取时间范围
                start_date = (datetime.now() - timedelta(days=days)).isoformat()
                
                # 统计反馈数据
                cursor.execute('''
                    SELECT 
                        feedback_type,
                        COUNT(*) as count,
                        AVG(rating) as avg_rating,
                        category,
                        priority
                    FROM user_feedback 
                    WHERE timestamp >= ?
                    GROUP BY feedback_type, category, priority
                    ORDER BY count DESC
                ''', (start_date,))
                
                feedback_stats = []
                for row in cursor.fetchall():
                    feedback_stats.append({
                        'type': row[0],
                        'count': row[1],
                        'avg_rating': round(row[2], 2) if row[2] else 0,
                        'category': row[3],
                        'priority': row[4]
                    })
                
                # 获取总体统计
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_feedback,
                        AVG(rating) as overall_rating,
                        COUNT(DISTINCT user_id) as unique_users
                    FROM user_feedback 
                    WHERE timestamp >= ?
                ''', (start_date,))
                
                overall_stats = cursor.fetchone()
                
                # 获取系统指标
                cursor.execute('''
                    SELECT 
                        metric_name,
                        AVG(metric_value) as avg_value,
                        MAX(metric_value) as max_value,
                        MIN(metric_value) as min_value
                    FROM system_metrics 
                    WHERE timestamp >= ?
                    GROUP BY metric_name
                ''', (start_date,))
                
                system_stats = []
                for row in cursor.fetchall():
                    system_stats.append({
                        'name': row[0],
                        'avg_value': round(row[1], 2),
                        'max_value': round(row[2], 2),
                        'min_value': round(row[3], 2)
                    })
                
                return {
                    'period_days': days,
                    'start_date': start_date,
                    'overall_stats': {
                        'total_feedback': overall_stats[0],
                        'overall_rating': round(overall_stats[1], 2) if overall_stats[1] else 0,
                        'unique_users': overall_stats[2]
                    },
                    'feedback_stats': feedback_stats,
                    'system_stats': system_stats,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"获取反馈汇总失败: {e}")
            return {}
    
    def analyze_feedback_trends(self, days: int = 7) -> Dict[str, Any]:
        """分析反馈趋势"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 获取每日反馈趋势
                cursor.execute('''
                    SELECT 
                        DATE(timestamp) as date,
                        COUNT(*) as feedback_count,
                        AVG(rating) as avg_rating
                    FROM user_feedback 
                    WHERE timestamp >= date('now', '-{} days')
                    GROUP BY DATE(timestamp)
                    ORDER BY date
                '''.format(days))
                
                daily_trends = []
                for row in cursor.fetchall():
                    daily_trends.append({
                        'date': row[0],
                        'feedback_count': row[1],
                        'avg_rating': round(row[2], 2) if row[2] else 0
                    })
                
                # 分析趋势
                if len(daily_trends) >= 2:
                    recent_trend = daily_trends[-1]['avg_rating'] - daily_trends[-2]['avg_rating']
                    trend_direction = "improving" if recent_trend > 0 else "declining" if recent_trend < 0 else "stable"
                else:
                    trend_direction = "insufficient_data"
                
                return {
                    'period_days': days,
                    'daily_trends': daily_trends,
                    'trend_direction': trend_direction,
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"分析反馈趋势失败: {e}")
            return {}
    
    def generate_insights(self, feedback_summary: Dict[str, Any]) -> List[str]:
        """生成洞察"""
        insights = []
        
        # 分析整体评分
        overall_rating = feedback_summary.get('overall_stats', {}).get('overall_rating', 0)
        if overall_rating >= 4.0:
            insights.append("✅ 用户满意度较高，AI Agent配置效果良好")
        elif overall_rating >= 3.0:
            insights.append("⚠️ 用户满意度中等，需要关注改进点")
        else:
            insights.append("❌ 用户满意度较低，需要重点改进")
        
        # 分析反馈类型分布
        feedback_stats = feedback_summary.get('feedback_stats', [])
        if feedback_stats:
            top_feedback_type = max(feedback_stats, key=lambda x: x['count'])
            insights.append(f"📊 主要反馈类型: {top_feedback_type['type']} ({top_feedback_type['count']}条)")
        
        # 分析高优先级问题
        high_priority_count = sum(1 for stat in feedback_stats if stat['priority'] == 'high')
        if high_priority_count > 0:
            insights.append(f"🚨 发现 {high_priority_count} 个高优先级问题需要处理")
        
        # 分析用户活跃度
        unique_users = feedback_summary.get('overall_stats', {}).get('unique_users', 0)
        if unique_users > 5:
            insights.append("👥 用户活跃度良好，团队广泛使用AI Agent")
        elif unique_users > 2:
            insights.append("👤 用户活跃度中等，建议推广使用")
        else:
            insights.append("⚠️ 用户活跃度较低，需要加强推广")
        
        return insights
    
    def generate_recommendations(self, insights: List[str], feedback_summary: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        overall_rating = feedback_summary.get('overall_stats', {}).get('overall_rating', 0)
        
        if overall_rating < 4.0:
            recommendations.append("🎯 提升用户满意度：分析低分反馈，优化AI Agent响应质量")
        
        if any("高优先级问题" in insight for insight in insights):
            recommendations.append("🔧 处理高优先级问题：优先解决影响用户体验的关键问题")
        
        if any("活跃度较低" in insight for insight in insights):
            recommendations.append("📢 提升用户活跃度：组织培训，推广AI Agent使用")
        
        # 基于反馈类型的建议
        feedback_stats = feedback_summary.get('feedback_stats', [])
        for stat in feedback_stats:
            if stat['type'] == 'performance' and stat['avg_rating'] < 4.0:
                recommendations.append("⚡ 性能优化：改进AI Agent响应速度和准确性")
            elif stat['type'] == 'quality' and stat['avg_rating'] < 4.0:
                recommendations.append("🎨 质量提升：改进代码生成质量和文档准确性")
            elif stat['type'] == 'usability' and stat['avg_rating'] < 4.0:
                recommendations.append("🔧 易用性改进：简化用户界面和交互流程")
        
        return recommendations
    
    def generate_feedback_report(self, days: int = 30) -> str:
        """生成反馈报告"""
        feedback_summary = self.get_feedback_summary(days)
        trends = self.analyze_feedback_trends(7)
        insights = self.generate_insights(feedback_summary)
        recommendations = self.generate_recommendations(insights, feedback_summary)
        
        report = []
        report.append("# AI Agent反馈收集报告")
        report.append("=" * 50)
        report.append("")
        report.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**统计周期**: 最近 {days} 天")
        report.append("")
        
        # 总体统计
        overall_stats = feedback_summary.get('overall_stats', {})
        report.append("## 📊 总体统计")
        report.append("")
        report.append(f"- **总反馈数**: {overall_stats.get('total_feedback', 0)}")
        report.append(f"- **平均评分**: {overall_stats.get('overall_rating', 0)}/5.0")
        report.append(f"- **活跃用户**: {overall_stats.get('unique_users', 0)}")
        report.append("")
        
        # 反馈分布
        if feedback_summary.get('feedback_stats'):
            report.append("## 📈 反馈分布")
            report.append("")
            for stat in feedback_summary['feedback_stats'][:5]:  # 显示前5个
                report.append(f"- **{stat['type']}** ({stat['category']}): {stat['count']}条, 平均{stat['avg_rating']}分")
            report.append("")
        
        # 趋势分析
        if trends.get('daily_trends'):
            report.append("## 📊 趋势分析")
            report.append("")
            report.append(f"- **趋势方向**: {trends['trend_direction']}")
            report.append(f"- **最近7天趋势**: {len(trends['daily_trends'])}天数据")
            report.append("")
        
        # 洞察
        if insights:
            report.append("## 💡 关键洞察")
            report.append("")
            for insight in insights:
                report.append(f"- {insight}")
            report.append("")
        
        # 改进建议
        if recommendations:
            report.append("## 🎯 改进建议")
            report.append("")
            for i, rec in enumerate(recommendations, 1):
                report.append(f"{i}. {rec}")
            report.append("")
        
        # 系统指标
        system_stats = feedback_summary.get('system_stats', [])
        if system_stats:
            report.append("## ⚙️ 系统指标")
            report.append("")
            for stat in system_stats:
                report.append(f"- **{stat['name']}**: 平均{stat['avg_value']} {stat.get('unit', '')}")
            report.append("")
        
        report.append("---")
        report.append("**报告说明**: 本报告基于用户反馈和系统指标自动生成，建议定期查看并根据建议进行改进。")
        
        return "\n".join(report)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI Agent反馈收集系统')
    parser.add_argument('--action', choices=['collect', 'analyze', 'report'], 
                       default='report', help='执行的操作')
    parser.add_argument('--days', type=int, default=30, help='统计天数')
    parser.add_argument('--db-path', default='data/feedback.db', help='数据库路径')
    
    args = parser.parse_args()
    
    collector = FeedbackCollector(args.db_path)
    
    if args.action == 'collect':
        print("📊 开始收集反馈数据...")
        # 这里可以添加实际的反馈收集逻辑
        print("✅ 反馈数据收集完成")
        
    elif args.action == 'analyze':
        print("🔍 开始分析反馈数据...")
        summary = collector.get_feedback_summary(args.days)
        trends = collector.analyze_feedback_trends(7)
        print(f"📈 分析完成: {summary.get('overall_stats', {}).get('total_feedback', 0)}条反馈")
        
    elif args.action == 'report':
        print("📄 生成反馈报告...")
        report = collector.generate_feedback_report(args.days)
        
        # 保存报告
        report_path = f"feedback-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 反馈报告已生成: {report_path}")
        print("\n" + "="*50)
        print(report)

if __name__ == "__main__":
    main()
