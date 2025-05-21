#!/bin/bash
# Docker一键部署脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$ROOT_DIR"

# 显示欢迎信息
echo "===================================================="
echo "      矛盾调解受理服务API - Docker一键部署"
echo "===================================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker，请先安装Docker"
    echo "安装命令: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未找到Docker Compose，请先安装"
    echo "安装命令: curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose"
    exit 1
fi

# 进入docker目录
cd "$ROOT_DIR/docker"

# 构建并启动容器
echo "正在构建并启动Docker容器..."
docker-compose up -d

# 检查容器状态
sleep 5
if docker ps | grep -q "mdtj_api"; then
    echo "Docker容器启动成功!"
    # 获取容器IP地址
    API_CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mdtj_api)
    DB_CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mdtj_mysql)
    
    # 获取主机IP
    HOST_IP=$(hostname -I | awk '{print $1}')
    
    echo ""
    echo "===================================================="
    echo "      部署完成！"
    echo "===================================================="
    echo "API文档地址: http://$HOST_IP:8701/api/docs/"
    echo "API容器IP: $API_CONTAINER_IP"
    echo "数据库容器IP: $DB_CONTAINER_IP"
    echo ""
    echo "管理命令:"
    echo "  查看日志: docker logs mdtj_api"
    echo "  重启容器: docker-compose restart"
    echo "  停止服务: docker-compose down"
    echo "===================================================="
else
    echo "错误: 容器启动失败，请检查日志"
    docker-compose logs
    exit 1
fi 