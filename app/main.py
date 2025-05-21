"""
矛盾调解受理服务 API - Flask应用主程序
"""
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

# 导入配置和各个模块
from app.config import API_CONFIG, DEBUG
from app.routes import (
    identity_blueprint, 
    appeals_blueprint, 
    auth_blueprint, 
    health_blueprint,
    user_blueprint
)
from app.utils.cors_handler import register_cors_handler

def create_app():
    """
    创建并配置Flask应用
    
    Returns:
        app: 配置好的Flask应用实例
    """
    # 初始化 Flask 应用
    app = Flask(__name__)
    
    # 启用强化版跨域支持
    CORS(app, 
         resources={r"/*": {"origins": "*", "supports_credentials": True}},
         allow_headers=["Content-Type", "Authorization", "token", "Access-Control-Allow-Credentials"],
         expose_headers=["Content-Length", "X-Total-Count"],
         max_age=86400)
    
    # 注册通用跨域处理
    register_cors_handler(app)

    # 注册蓝图
    app.register_blueprint(identity_blueprint)
    app.register_blueprint(appeals_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(health_blueprint)
    app.register_blueprint(user_blueprint)

    # 配置Swagger UI
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
    API_URL = '/api/swagger.json'  # Our API url (can be a local file)

    # 读取swagger.json文件路径
    swagger_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

    # 如果swagger.json文件不存在，创建一个简单的文档
    if not os.path.exists(swagger_path):
        swagger_data = {
            "swagger": "2.0",
            "info": {
                "title": "矛盾调解受理服务 API",
                "description": "提供身份验证和矛盾调解受理单管理的API",
                "version": "1.0.0"
            },
            "basePath": "/api",
            "schemes": ["http"],
            "paths": {
                "/health": {
                    "get": {
                        "summary": "健康检查",
                        "description": "检查API服务是否正常运行",
                        "responses": {
                            "200": {
                                "description": "服务正常运行"
                            }
                        }
                    }
                }
            }
        }
        # 保存临时swagger.json文件
        with open(swagger_path, 'w', encoding='utf-8') as f:
            json.dump(swagger_data, f, ensure_ascii=False, indent=2)
    else:
        # 读取swagger.json文件
        with open(swagger_path, 'r', encoding='utf-8') as swagger_file:
            swagger_data = json.load(swagger_file)

    # 创建Swagger UI蓝图
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "矛盾调解受理服务 API 文档",
            'dom_id': '#swagger-ui',
            'deepLinking': True,
            'layout': 'StandaloneLayout',
            'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
            'validatorUrl': None
        }
    )

    # 注册Swagger UI蓝图
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # 提供swagger.json
    @app.route('/api/swagger.json')
    def get_swagger():
        """提供Swagger API文档"""
        response = jsonify(swagger_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # 默认路由重定向到API文档
    @app.route('/')
    def index():
        """将根路径访问重定向到API文档"""
        return redirect('/api/docs')
    
    # 创建数据表和测试数据
    @app.before_first_request
    def initialize_database():
        """初始化数据库表和测试数据"""
        try:
            from app.models import database
            database.create_tables_if_not_exist()
            database.insert_test_data()
        except Exception as e:
            app.logger.error(f"数据库初始化失败: {e}")
    
    return app

def run_app():
    """运行Flask应用"""
    app = create_app()
    host = API_CONFIG['server_host']
    port = API_CONFIG['server_port']
    app.run(host=host, port=port, debug=DEBUG)

if __name__ == '__main__':
    run_app() 