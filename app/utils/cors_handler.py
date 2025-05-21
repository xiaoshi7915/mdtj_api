"""
通用跨域处理工具
"""
from flask import jsonify, make_response, request, current_app
from functools import wraps

def add_cors_headers(response):
    """
    添加跨域相关的响应头
    
    Args:
        response: Flask响应对象
        
    Returns:
        response: 添加了跨域头的响应对象
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 
                         'Content-Type,Authorization,token,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 
                         'GET,POST,PUT,DELETE,OPTIONS,PATCH')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def cors_preflight(methods=None):
    """
    处理OPTIONS预检请求的装饰器
    
    Args:
        methods: 允许的HTTP方法列表
        
    Returns:
        装饰器函数
    """
    if methods is None:
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
        
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if request.method == 'OPTIONS':
                response = make_response()
                response = add_cors_headers(response)
                response.headers.add('Access-Control-Allow-Methods', 
                                     ','.join(methods))
                return response
            else:
                return f(*args, **kwargs)
        return wrapped_function
    return decorator

def register_cors_handler(app):
    """
    为Flask应用注册通用的跨域处理机制
    
    Args:
        app: Flask应用实例
    """
    # 注册after_request处理器，为所有响应添加CORS头
    @app.after_request
    def after_request(response):
        return add_cors_headers(response)
    
    # 处理全局OPTIONS请求
    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_handler(path):
        """处理所有路径的OPTIONS请求"""
        response = jsonify({})
        response = add_cors_headers(response)
        return response
    
    # 处理根路径的OPTIONS请求
    @app.route('/', methods=['OPTIONS'])
    def root_options_handler():
        """处理根路径的OPTIONS请求"""
        response = jsonify({})
        response = add_cors_headers(response)
        return response 