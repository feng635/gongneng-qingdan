#!/bin/bash
# 快速查看最近错误日志
# 用法: bash scripts/check_logs.sh [行数]

LINES=${1:-20}
echo "=== 最近的错误日志（最近 $LINES 行）==="

# 尝试常见日志位置
for log in \
  /var/log/syslog \
  /var/log/messages \
  /var/log/nginx/error.log \
  /var/log/apache2/error.log \
  ./logs/error.log \
  ./log/*.log \
  ./**/logs/*.log; do
  if [ -f "$log" ]; then
    echo "--- $log ---"
    tail -$LINES "$log" 2>/dev/null | grep -i "error\|exception\|fail\|timeout" || echo "(无错误)"
    break
  fi
done
