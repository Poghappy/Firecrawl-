#!/bin/bash
set -e

BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/firecrawl_backup_$DATE.sql"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行数据库备份
pg_dump -h postgres -U firecrawl -d firecrawl > $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除7天前的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "备份完成: ${BACKUP_FILE}.gz"
