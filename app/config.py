"""
配置文件 - 存储数据库连接信息和API设置
"""
import os
import json
import logging
from dotenv import load_dotenv

# 配置日志记录
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 尝试加载.env文件，如果存在的话
load_dotenv()

# 获取当前环境
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
logger.info(f"当前运行环境: {FLASK_ENV}")

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '47.118.250.53'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'mt_zt'),
    'user': os.getenv('DB_USER', 'mt_zt'),
    'password': os.getenv('DB_PASSWORD', 'admin123456!'),
    'charset': 'utf8mb4'
}

# 打印数据库配置信息（不包含密码）
logger.info(f"数据库配置: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']} (用户: {DB_CONFIG['user']})")

# API配置
API_CONFIG = {
    'server_host': os.getenv('SERVER_HOST', '0.0.0.0'),
    'server_port': int(os.getenv('SERVER_PORT', 8701))
}

logger.info(f"API服务器配置: {API_CONFIG['server_host']}:{API_CONFIG['server_port']}")

# 从环境变量读取排除路径列表
def get_exclude_paths():
    """从环境变量获取排除路径列表"""
    paths = os.getenv('TOKEN_EXCLUDE_PATHS', '/api/health,/api/docs,/api/swagger.json,/api/auth/validate')
    return paths.split(',')

# API令牌配置
TOKEN_CONFIG = {
    'enabled': os.getenv('TOKEN_ENABLED', 'True').lower() in ('true', '1', 't'),            # 是否启用令牌验证
    'default_token': os.getenv('API_TOKEN', 'api_token_2025'),                              # 默认API令牌
    'token_header': os.getenv('TOKEN_HEADER', 'token'),                                     # 请求头中令牌的名称
    'token_query_param': os.getenv('TOKEN_QUERY_PARAM', 'token'),                           # URL参数中令牌的名称
    'token_lifetime': int(os.getenv('TOKEN_LIFETIME', 7776000)),                            # 令牌有效期（秒）- 3个月
    'exclude_paths': get_exclude_paths()                                                    # 不需要令牌的API路径
}

logger.info(f"令牌配置: 启用状态={TOKEN_CONFIG['enabled']}, 默认令牌={TOKEN_CONFIG['default_token'][:4]}***, 有效期={TOKEN_CONFIG['token_lifetime']/86400}天")

# 日志配置
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'file': os.getenv('LOG_FILE', 'logs/app.log')
}

# 调试模式（仅在开发环境下启用）
DEBUG = FLASK_ENV == 'development' and os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
logger.info(f"调试模式: {'启用' if DEBUG else '禁用'}")

# 环境相关配置
if FLASK_ENV == 'development':
    # 开发环境特定配置
    logger.info("使用开发环境配置")
else:
    # 生产环境特定配置
    logger.info("使用生产环境配置")
    # 在生产环境中禁用调试模式，不管环境变量如何设置
    DEBUG = False 