#!/bin/bash
# 矛盾调解受理服务API一键部署脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$ROOT_DIR"

# 显示欢迎信息
echo "===================================================="
echo "      矛盾调解受理服务API - 一键部署脚本"
echo "===================================================="
echo ""

# 检查环境变量文件
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo "未找到.env文件，正在从.env.example创建..."
    cp .env.example .env
    echo "已创建.env文件，请编辑此文件配置数据库连接信息"
    echo "命令: vi .env"
    exit 1
  else
    echo "错误: 未找到.env.example文件，无法创建配置"
    exit 1
  fi
fi

# 创建虚拟环境
if [ ! -d "mdtj_env" ]; then
  echo "正在创建Python虚拟环境..."
  python3 -m venv mdtj_env || {
    echo "创建虚拟环境失败，请确保已安装Python 3.8+"
    exit 1
  }
fi

# 激活虚拟环境
source mdtj_env/bin/activate || {
  echo "激活虚拟环境失败"
  exit 1
}
echo "已激活Python虚拟环境"

# 安装依赖
echo "正在安装项目依赖..."
pip install -r requirements.txt || {
  echo "安装依赖失败"
  exit 1
}
echo "依赖安装完成"

# 确保日志目录存在
mkdir -p logs

# 启动服务
echo "正在启动服务..."
./scripts/start.sh

echo ""
echo "===================================================="
echo "      部署完成！"
echo "===================================================="
echo "API文档地址: http://服务器IP:8701/api/docs/"
echo "如需重启服务，请运行: ./scripts/restart.sh"
echo "如需停止服务，请运行: pkill -f \"gunicorn.*run:app\""
echo "====================================================" 