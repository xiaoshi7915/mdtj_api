#!/usr/bin/env python
"""
矛盾调解受理服务 API - 应用入口文件
支持直接启动和WSGI服务器部署
"""
import os
import sys
import logging
from app.main import run_app, create_app

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log', encoding='utf-8', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# 创建Flask应用实例（用于WSGI服务器如Gunicorn）
app = create_app()

def main():
    """直接启动应用的入口函数"""
    try:
        # 确保日志目录存在
        os.makedirs('logs', exist_ok=True)
        
        # 获取环境变量，默认为开发环境
        env = os.environ.get('FLASK_ENV', 'development')
        logger.info(f"应用启动中，环境: {env}")
        
        # 运行应用
        run_app()
    except Exception as e:
        logger.exception(f"应用启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 