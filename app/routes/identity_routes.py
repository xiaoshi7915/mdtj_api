"""
身份验证相关路由
"""
from flask import request, jsonify
from app.routes import identity_blueprint
from app.services import verification_service
from app.utils.auth import require_token


@identity_blueprint.route('/verify', methods=['POST'])
@require_token
def verify_identity():
    """
    身份验证API端点 - 通过身份证号验证用户是否存在
    
    请求体示例:
    {
        "id_card_number": "330102199001011234"
    }
    
    响应示例(成功):
    {
        "success": 1,
        "message": "身份证号验证通过",
        "data": {
            "id_card_number": "330102199001011234",
            "name": "张三",
            "contact_info": "13800138001",
            "address": "浙江省杭州市西湖区文三路123号"
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "身份证号 330102199009099999 在系统中不存在",
        "data": {}
    }
    """
    data = request.get_json()
    
    # 检查必要字段
    if 'id_card_number' not in data:
        return jsonify({
            "success": 0,
            "message": "缺少必要字段: id_card_number",
            "data": {}
        }), 400
    
    # 调用验证服务
    result = verification_service.verify_identity(data.get('id_card_number'))
    
    # 根据验证结果确定HTTP状态码
    status_code = 200
    
    return jsonify(result), status_code


@identity_blueprint.route('/status', methods=['GET'])
@require_token
def verification_status():
    """
    查询验证状态API端点
    
    查询参数:
    - id_card_number: 身份证号
    
    响应示例(成功):
    {
        "success": 1,
        "message": "获取用户信息成功",
        "data": {
            "id_card_number": "330102199001011234",
            "name": "张三",
            "contact_info": "13800138001",
            "address": "浙江省杭州市西湖区文三路123号",
            "verified": true
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "身份证号 330102199009099999 在系统中不存在",
        "data": {}
    }
    """
    id_card_number = request.args.get('id_card_number')
    if not id_card_number:
        return jsonify({
            "success": 0,
            "message": "缺少必要参数: id_card_number"
        }), 400
    
    result = verification_service.get_verification_status(id_card_number)
    return jsonify(result)


# 支持OPTIONS请求的路由
@identity_blueprint.route('/verify', methods=['OPTIONS'])
def options_identity_verify():
    """处理身份验证API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    return response


@identity_blueprint.route('/status', methods=['OPTIONS'])
def options_identity_status():
    """处理身份验证状态API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
    return response