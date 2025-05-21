#!/bin/bash

# 启动矛盾调解受理服务API

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$ROOT_DIR"

# 加载环境变量
if [ -f ".env" ]; then
  export $(cat .env | grep -v '#' | sed 's/\r$//' | xargs)
fi

# 设置开发环境
export FLASK_ENV=${FLASK_ENV:-development}
export DEBUG=${DEBUG:-True}

# 检查端口是否被占用
PORT=${SERVER_PORT:-8701}
if lsof -i:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "警告: 端口 $PORT 已被占用，尝试停止相关进程..."
  # 尝试停止之前的进程
  pkill -f "gunicorn.*run:app" || true
  sleep 1
fi

# 确保日志目录存在
mkdir -p "$ROOT_DIR/logs"

# 检查并激活虚拟环境
if [ -d "$ROOT_DIR/mdtj_env" ]; then
  source "$ROOT_DIR/mdtj_env/bin/activate"
  echo "已激活Python虚拟环境"
fi

# 启动API服务
echo "启动矛盾调解受理服务API..."

# 根据环境选择启动方式
if [ "$FLASK_ENV" = "production" ]; then
  # 生产环境：使用Gunicorn
  gunicorn -w 4 -b ${SERVER_HOST:-0.0.0.0}:${SERVER_PORT:-8701} run:app \
           --timeout 120 --access-logfile "$ROOT_DIR/logs/access.log" \
           --error-logfile "$ROOT_DIR/logs/error.log" --daemon
else
  # 开发环境：使用Gunicorn但启用自动重载
  gunicorn -w 2 -b ${SERVER_HOST:-0.0.0.0}:${SERVER_PORT:-8701} run:app \
           --timeout 120 --reload --access-logfile "$ROOT_DIR/logs/access.log" \
           --error-logfile "$ROOT_DIR/logs/error.log" --daemon
fi

# 检查是否成功启动
sleep 2
if lsof -i:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "服务已启动，运行在 ${SERVER_HOST:-0.0.0.0}:${SERVER_PORT:-8701}"
  echo "API文档地址: http://${SERVER_HOST:-0.0.0.0}:${SERVER_PORT:-8701}/api/docs/"
else
  echo "服务启动失败，请检查日志文件了解详情"
fi 