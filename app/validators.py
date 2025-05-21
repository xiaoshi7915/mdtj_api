"""
输入参数验证模块 - 提供各种输入参数的验证功能
"""
import re
import datetime
from functools import wraps
from flask import request, jsonify

# 身份证号验证正则表达式（支持15位和18位）
ID_CARD_PATTERN = r'^\d{15}$|^\d{17}[\dXx]$'

# 手机号验证正则表达式（中国大陆手机号）
PHONE_PATTERN = r'^1[3-9]\d{9}$'

# 邮箱验证正则表达式
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_id_card(id_card):
    """
    验证身份证号格式
    
    Args:
        id_card: 身份证号
        
    Returns:
        bool: 是否通过验证
    """
    if not id_card:
        return False
        
    if not re.match(ID_CARD_PATTERN, id_card):
        return False
        
    # 对18位身份证的最后一位校验码进行验证
    if len(id_card) == 18:
        try:
            # 加权因子
            factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            # 校验码对应值
            parity = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            
            # 根据前17位计算校验码
            sum_val = sum(int(id_card[i]) * factors[i] for i in range(17))
            index = sum_val % 11
            
            # 校验第18位
            if id_card[17].upper() != parity[index]:
                return False
        except Exception:
            return False
    
    # 基本格式验证通过
    return True

def validate_phone(phone):
    """
    验证手机号格式
    
    Args:
        phone: 手机号
        
    Returns:
        bool: 是否通过验证
    """
    if not phone:
        return False
    
    return bool(re.match(PHONE_PATTERN, phone))

def validate_email(email):
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否通过验证
    """
    if not email:
        return False
    
    return bool(re.match(EMAIL_PATTERN, email))

def validate_date(date_str, formats=None):
    """
    验证日期格式
    
    Args:
        date_str: 日期字符串
        formats: 日期格式列表，默认为['%Y-%m-%d', '%Y/%m/%d']
        
    Returns:
        bool: 是否通过验证
    """
    if not date_str:
        return False
    
    if formats is None:
        formats = ['%Y-%m-%d', '%Y/%m/%d']
    
    for date_format in formats:
        try:
            datetime.datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            continue
    
    return False

def validate_json_request(required_fields=None, field_validators=None):
    """
    验证JSON请求装饰器
    
    Args:
        required_fields: 必需字段列表
        field_validators: 字段验证器字典，格式为{字段名: 验证函数}
        
    Returns:
        decorator: 验证JSON请求的装饰器
    """
    if required_fields is None:
        required_fields = []
    
    if field_validators is None:
        field_validators = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 验证Content-Type
            if request.content_type != 'application/json':
                return jsonify({
                    "success": 0,
                    "message": "请求头Content-Type必须为application/json",
                    "data": {}
                }), 400
            
            # 获取JSON数据
            data = request.get_json()
            if data is None:
                return jsonify({
                    "success": 0,
                    "message": "无效的JSON数据",
                    "data": {}
                }), 400
            
            # 验证必需字段
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        "success": 0,
                        "message": f"缺少必要字段: {field}",
                        "data": {}
                    }), 400
            
            # 验证字段格式
            for field, validator in field_validators.items():
                if field in data and data[field] and not validator(data[field]):
                    return jsonify({
                        "success": 0,
                        "message": f"字段格式错误: {field}",
                        "data": {}
                    }), 400
            
            # 验证通过，调用原函数
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def validate_query_params(required_params=None, param_validators=None):
    """
    验证查询参数装饰器
    
    Args:
        required_params: 必需参数列表
        param_validators: 参数验证器字典，格式为{参数名: 验证函数}
        
    Returns:
        decorator: 验证查询参数的装饰器
    """
    if required_params is None:
        required_params = []
    
    if param_validators is None:
        param_validators = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 验证必需参数
            for param in required_params:
                if param not in request.args or not request.args.get(param):
                    return jsonify({
                        "success": 0,
                        "message": f"缺少必要参数: {param}",
                        "data": {}
                    }), 400
            
            # 验证参数格式
            for param, validator in param_validators.items():
                if param in request.args and request.args.get(param) and not validator(request.args.get(param)):
                    return jsonify({
                        "success": 0,
                        "message": f"参数格式错误: {param}",
                        "data": {}
                    }), 400
            
            # 验证通过，调用原函数
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator 