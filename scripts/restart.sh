#!/bin/bash

# 重启矛盾调解受理服务API

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$ROOT_DIR"

# 停止已运行的服务
echo "停止已运行的服务..."
pkill -f "gunicorn.*app:app" || true
sleep 1

# 重新启动服务
echo "重新启动服务..."
./scripts/start.sh

# 检查服务是否成功启动
sleep 2
if pgrep -f "gunicorn.*run:app" > /dev/null; then
  echo "服务已成功重启，运行在 ${SERVER_HOST:-0.0.0.0}:${SERVER_PORT:-8701}"
else
  echo "错误: 服务启动失败，请检查日志文件了解详情"
  exit 1
fi 