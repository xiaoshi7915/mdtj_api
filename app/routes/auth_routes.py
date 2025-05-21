"""
认证相关路由
"""
from flask import request, jsonify
from app.routes import auth_blueprint
from app.utils.auth import require_token, validate_token, generate_token

@auth_blueprint.route('/token', methods=['POST'])
@require_token
def generate_api_token():
    """
    生成API令牌
    
    请求体示例:
    {
        "admin_token": "admin_secret_token"
    }
    
    响应示例(成功):
    {
        "success": 1,
        "message": "令牌生成成功",
        "data": {
            "token": "your_api_token_here",
            "expires_at": 1747541814.899
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "管理员令牌无效",
        "data": {}
    }
    """
    # 这里应该有更复杂的逻辑，例如验证管理员权限
    # 简化起见，直接返回默认令牌
    
    token, expires_at = generate_token()
    
    return jsonify({
        "success": 1,
        "message": "令牌生成成功",
        "data": {
            "token": token,
            "expires_at": expires_at
        }
    })

@auth_blueprint.route('/validate', methods=['GET'])
def validate_api_token():
    """
    验证API令牌
    
    查询参数:
    - token: 需要验证的API令牌
    
    响应示例(成功):
    {
        "success": 1,
        "message": "令牌有效",
        "data": {
            "valid": true,
            "expires_at": 1747541814.899
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "无效的令牌或令牌已过期",
        "data": {
            "valid": false
        }
    }
    """
    token = request.args.get('token')
    
    if not token:
        return jsonify({
            "success": 0,
            "message": "缺少必要参数: token",
            "data": {
                "valid": False
            }
        }), 400
    
    valid, message, expires_at = validate_token(token)
    
    if valid:
        return jsonify({
            "success": 1,
            "message": message,
            "data": {
                "valid": True,
                "expires_at": expires_at
            }
        })
    else:
        return jsonify({
            "success": 0,
            "message": message,
            "data": {
                "valid": False
            }
        }) 