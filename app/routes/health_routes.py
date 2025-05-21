"""
健康检查路由
"""
from flask import jsonify
from app.routes import health_blueprint
from app.utils.cors_handler import cors_preflight

@health_blueprint.route('/health', methods=['GET'])
@cors_preflight(['GET', 'OPTIONS'])
def health_check():
    """健康检查API端点"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    }) 