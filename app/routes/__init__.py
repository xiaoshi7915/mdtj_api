"""
路由模块初始化
"""
from flask import Blueprint

# 创建蓝图对象
identity_blueprint = Blueprint('identity', __name__, url_prefix='/api/identity')
appeals_blueprint = Blueprint('appeals', __name__, url_prefix='/api/appeals')
auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')
health_blueprint = Blueprint('health', __name__, url_prefix='/api')
user_blueprint = Blueprint('user', __name__, url_prefix='/api/users')

# 导入路由模块以注册路由
from app.routes import health_routes
from app.routes import identity_routes
from app.routes import appeals_routes
from app.routes import auth_routes
from app.routes import user_routes 