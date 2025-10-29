#!/bin/bash
# 檀香山租房信息采集系统 - 定时任务设置脚本

echo "🏠 檀香山租房信息采集系统 - 定时任务设置"
echo "================================================"
echo ""

# 获取当前脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN=$(which python3)

echo "📁 项目目录: $SCRIPT_DIR"
echo "🐍 Python 路径: $PYTHON_BIN"
echo ""

# 生成 crontab 条目
CRON_JOB="0 8 * * * cd $SCRIPT_DIR && $PYTHON_BIN main.py >> logs/cron.log 2>&1"

echo "📋 将添加以下 crontab 条目:"
echo "================================================"
echo "$CRON_JOB"
echo "================================================"
echo ""
echo "⏰ 含义: 每天早上 8:00 (HST) 自动运行采集程序"
echo ""

# 询问用户是否确认
read -p "是否继续添加到 crontab？(y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    # 检查是否已存在相同的任务
    if crontab -l 2>/dev/null | grep -q "honolulu_rentals"; then
        echo "⚠️  检测到已存在的 honolulu_rentals 定时任务"
        read -p "是否替换？(y/n): " replace

        if [ "$replace" = "y" ] || [ "$replace" = "Y" ]; then
            # 删除旧任务
            crontab -l 2>/dev/null | grep -v "honolulu_rentals" | crontab -
            echo "✅ 已删除旧任务"
        else
            echo "❌ 取消操作"
            exit 0
        fi
    fi

    # 添加新任务
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

    echo ""
    echo "✅ 定时任务添加成功！"
    echo ""
    echo "📋 当前所有定时任务:"
    echo "================================================"
    crontab -l
    echo "================================================"
    echo ""
    echo "💡 提示:"
    echo "  - 查看定时任务: crontab -l"
    echo "  - 编辑定时任务: crontab -e"
    echo "  - 删除定时任务: crontab -r"
    echo "  - 查看运行日志: tail -f $SCRIPT_DIR/logs/cron.log"
    echo ""
    echo "🎉 设置完成！明天早上 8:00 将自动运行采集程序。"
else
    echo "❌ 操作已取消"
    echo ""
    echo "💡 您也可以手动添加定时任务:"
    echo "   1. 运行: crontab -e"
    echo "   2. 添加以下行:"
    echo "      $CRON_JOB"
fi
