"""
用户相关路由
"""
from flask import jsonify
from app.routes import user_blueprint
from app.models import database
from app.utils.auth import require_token

@user_blueprint.route('', methods=['GET'])
@require_token
def list_users():
    """获取所有用户列表"""
    try:
        users = database.get_all_users()
        return jsonify({
            "success": 1,
            "message": "查询成功",
            "data": users
        })
    except Exception as e:
        return jsonify({
            "success": 0,
            "message": "获取用户列表失败",
            "error": str(e)
        }), 500

@user_blueprint.route('/<int:user_id>', methods=['GET'])
@require_token
def get_user(user_id):
    """获取单个用户信息"""
    try:
        # 此处需要实现获取单个用户的函数
        # user = database.get_user_by_id(user_id)
        # 暂时返回模拟数据
        return jsonify({
            "success": 1,
            "message": "查询成功",
            "data": {
                "id": user_id,
                "name": "测试用户",
                "contact_info": "13800138000",
                "id_card_number": "330102199001010000",
                "address": "浙江省杭州市"
            }
        })
    except Exception as e:
        return jsonify({
            "success": 0,
            "message": "获取用户信息失败",
            "error": str(e)
        }), 500 