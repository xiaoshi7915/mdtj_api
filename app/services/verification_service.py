"""
身份验证服务 - 提供身份证号验证功能
"""
import json
from app.models import database

def verify_identity(id_card_number):
    """
    验证身份证号是否存在于系统中
    
    Args:
        id_card_number: 身份证号
        
    Returns:
        dict: 验证结果
    """
    # 查询用户信息
    user = database.get_user_by_id_card(id_card_number)
    
    # 构造响应结果
    if user:
        result = {
            "success": 1,
            "message": "身份证号验证通过",
            "data": {
                "id_card_number": user['id_card_number'],
                "name": user['name'],
                "contact_info": user['contact_info'],
                "address": user['address']
            }
        }
        
        # 记录验证日志
        database.update_verification_result(
            user['id'], 
            True, 
            json.dumps(result, ensure_ascii=False)
        )
        database.log_verification(
            user['id'],
            {"id_card_number": id_card_number},
            result,
            "success"
        )
    else:
        result = {
            "success": 0,
            "message": f"身份证号 {id_card_number} 在系统中不存在",
            "data": {}
        }
        
        # 无法记录到用户日志，因为用户不存在
    
    return result

def get_verification_status(id_card_number):
    """
    获取身份证号验证状态
    
    Args:
        id_card_number: 身份证号
        
    Returns:
        dict: 验证状态信息
    """
    # 查询用户信息
    user = database.get_user_by_id_card(id_card_number)
    
    # 构造响应结果
    if user:
        result = {
            "success": 1,
            "message": "获取用户信息成功",
            "data": {
                "id_card_number": user['id_card_number'],
                "name": user['name'],
                "contact_info": user['contact_info'],
                "address": user['address'],
                "verified": bool(user['verified'])
            }
        }
    else:
        result = {
            "success": 0,
            "message": f"身份证号 {id_card_number} 在系统中不存在",
            "data": {}
        }
    
    return result 