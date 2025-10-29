#!/bin/bash
#
# HawaiiHub 新闻采集系统 - 定时采集脚本
#
# 用途: Cron 定时任务自动化采集新闻
#

set -e  # 遇到错误立即退出

# =============================================================================
# 配置
# =============================================================================

# 项目目录
PROJECT_DIR="/Users/zhiledeng/Downloads/FireShot/hawaiihub_news"

# Python 解释器
PYTHON="python3"

# 日志目录
LOG_DIR="${PROJECT_DIR}/logs"
SCHEDULE_LOG="${LOG_DIR}/schedule.log"

# 采集模式（可选值: all, p0, p1）
MODE="${1:-p0}"  # 默认 P0

# =============================================================================
# 函数
# =============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${SCHEDULE_LOG}"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "${SCHEDULE_LOG}" >&2
}

# =============================================================================
# 主程序
# =============================================================================

log "========================================"
log "HawaiiHub 新闻采集任务开始"
log "========================================"

# 切换到项目目录
cd "${PROJECT_DIR}" || {
    error "无法切换到项目目录: ${PROJECT_DIR}"
    exit 1
}

log "工作目录: $(pwd)"
log "采集模式: ${MODE}"

# 检查环境
if [ ! -f "../.env" ]; then
    error "未找到 .env 文件"
    exit 1
fi

log "环境配置: OK"

# 执行采集
log "开始采集..."

case "${MODE}" in
    all)
        log "采集所有新闻源"
        ${PYTHON} main.py --all 2>&1 | tee -a "${SCHEDULE_LOG}"
        ;;
    p0)
        log "采集 P0 优先级新闻源"
        ${PYTHON} main.py --priority P0 2>&1 | tee -a "${SCHEDULE_LOG}"
        ;;
    p1)
        log "采集 P1 优先级新闻源"
        ${PYTHON} main.py --priority P1 2>&1 | tee -a "${SCHEDULE_LOG}"
        ;;
    *)
        error "未知的采集模式: ${MODE}"
        error "可用模式: all, p0, p1"
        exit 1
        ;;
esac

# 检查退出状态
if [ $? -eq 0 ]; then
    log "采集成功完成"
else
    error "采集失败"
    exit 1
fi

log "========================================"
log "HawaiiHub 新闻采集任务完成"
log "========================================"

exit 0
