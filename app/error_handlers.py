"""
全局异常处理模块 - 提供统一的异常捕获和处理
"""
import traceback
import logging
import time
import uuid
from flask import request, jsonify

# 配置日志
logger = logging.getLogger("error_handlers")

def init_error_handlers(app):
    """
    初始化应用的错误处理器
    
    Args:
        app: Flask应用实例
    """
    # 处理400错误 - 错误请求
    @app.errorhandler(400)
    def handle_bad_request(e):
        return _generate_error_response(
            status_code=400,
            error_type="Bad Request",
            message=str(e),
            error_code="BAD_REQUEST"
        )
    
    # 处理401错误 - 未授权
    @app.errorhandler(401)
    def handle_unauthorized(e):
        return _generate_error_response(
            status_code=401,
            error_type="Unauthorized",
            message="未提供有效的认证凭据",
            error_code="UNAUTHORIZED"
        )
    
    # 处理403错误 - 禁止访问
    @app.errorhandler(403)
    def handle_forbidden(e):
        return _generate_error_response(
            status_code=403,
            error_type="Forbidden",
            message="没有权限访问此资源",
            error_code="FORBIDDEN"
        )
    
    # 处理404错误 - 资源不存在
    @app.errorhandler(404)
    def handle_not_found(e):
        return _generate_error_response(
            status_code=404,
            error_type="Not Found",
            message="请求的资源不存在",
            error_code="NOT_FOUND"
        )
    
    # 处理405错误 - 方法不允许
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return _generate_error_response(
            status_code=405,
            error_type="Method Not Allowed",
            message="请求方法不允许",
            error_code="METHOD_NOT_ALLOWED"
        )
    
    # 处理500错误 - 服务器内部错误
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return _handle_generic_exception(e, is_internal=True)
    
    # 处理未捕获的异常
    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        return _handle_generic_exception(e, is_internal=True)

    # 请求前处理 - 添加请求ID
    @app.before_request
    def before_request():
        request.request_id = str(uuid.uuid4())
        request.start_time = time.time()

    # 请求后处理 - 记录请求日志
    @app.after_request
    def after_request(response):
        # 计算请求处理时间
        process_time = round((time.time() - getattr(request, 'start_time', time.time())) * 1000, 2)
        
        # 获取请求ID
        request_id = getattr(request, 'request_id', 'unknown')
        
        # 记录请求日志
        logger.info(
            f"RequestID: {request_id} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time}ms | "
            f"IP: {request.remote_addr}"
        )
        
        # 在响应头中添加请求ID和处理时间
        response.headers['X-Request-ID'] = request_id
        response.headers['X-Process-Time'] = f"{process_time}ms"
        
        return response

def _generate_error_response(status_code, error_type, message, error_code=None, details=None):
    """
    生成标准错误响应
    
    Args:
        status_code: HTTP状态码
        error_type: 错误类型
        message: 错误消息
        error_code: 错误代码（可选）
        details: 错误详情（可选）
        
    Returns:
        Response: Flask响应对象
    """
    response = {
        "success": 0,
        "error": {
            "type": error_type,
            "message": message
        }
    }
    
    # 添加错误代码（如果有）
    if error_code:
        response["error"]["code"] = error_code
    
    # 添加错误详情（如果有）
    if details:
        response["error"]["details"] = details
    
    # 添加请求ID（如果有）
    if hasattr(request, 'request_id'):
        response["request_id"] = request.request_id
    
    return jsonify(response), status_code

def _handle_generic_exception(e, is_internal=False):
    """
    处理通用异常
    
    Args:
        e: 异常对象
        is_internal: 是否为内部服务器错误
        
    Returns:
        Response: Flask响应对象
    """
    # 获取异常堆栈信息
    stack_trace = traceback.format_exc()
    
    # 获取请求ID
    request_id = getattr(request, 'request_id', str(uuid.uuid4()))
    
    # 记录错误日志
    logger.error(
        f"RequestID: {request_id} | "
        f"Exception: {type(e).__name__} | "
        f"Message: {str(e)} | "
        f"Path: {request.path} | "
        f"Method: {request.method}"
    )
    logger.debug(f"Stack Trace:\n{stack_trace}")
    
    # 错误消息（生产环境中不暴露详细错误信息）
    if is_internal:
        message = "服务器内部错误，请稍后再试"
        details = {"error_reference": request_id}
    else:
        message = str(e)
        details = None
    
    return _generate_error_response(
        status_code=500,
        error_type="Internal Server Error",
        message=message,
        error_code="INTERNAL_ERROR",
        details=details
    ) 