"""
受理单相关路由
"""
from flask import request, jsonify
from app.routes import appeals_blueprint
from app.services import appeal_record_service
from app.utils.auth import require_token

@appeals_blueprint.route('/summary', methods=['GET'])
@require_token
def get_appeal_summary():
    """
    获取受理单摘要API端点
    
    查询参数:
    - id_card_number: 身份证号
    
    响应示例(成功):
    {
        "success": 1,
        "message": "查询成功",
        "data": {
            "person_name": "张三",
            "appeal_count": 2,
            "latest_appeal": "2025-05-17 10:20:52",
            "handling_status_stats": {
                "办理中": 1,
                "已结案": 1
            },
            "departments": ["矛盾调解中心"]
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "未找到身份证号为 xxxxxxx 的受理单记录",
        "data": {}
    }
    """
    id_card_number = request.args.get('id_card_number')
    if not id_card_number:
        return jsonify({
            "success": 0,
            "message": "缺少必要参数: id_card_number",
            "data": {}
        }), 400
    
    result = appeal_record_service.get_appeal_summary(id_card_number)
    return jsonify(result)

@appeals_blueprint.route('', methods=['POST'])
@require_token
def add_appeal_record():
    """
    添加受理单记录API端点
    
    请求体示例:
    {
        "case_number": "MTDJ-20250517-112318-123456",
        "person_name": "张三",
        "contact_info": "13800138000",
        "gender": "男性",
        "id_card_number": "330102199001011234",
        "address": "浙江省杭州市西湖区文三路123号",
        "incident_time": "2025年5月15日",
        "incident_location": "文三路小区门口",
        "incident_description": "邻居家装修噪音问题，影响休息",
        "people_involved": "3",
        "submitted_materials": "无",
        "handling_department": "矛盾调解中心",
        "handling_status": "办理中",
        "expected_completion": "3个工作日内",
        "qr_code": "https://example.com/qr/MTDJ-20250517-112318-123456.png",
        "markdown_doc": "# 受理单详情\n\n- **案件编号**: MTDJ-20250517-112318-123456\n- **申请人**: 张三\n- **事件**: 邻居家装修噪音问题"
    }
    
    响应示例(成功):
    {
        "success": 1,
        "message": "受理单记录添加成功",
        "case_number": "MTDJ-20250517-112318-123456"
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "缺少必要字段: xxx",
        "data": {}
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": 0,
            "message": "请求体为空或格式错误",
            "data": {}
        }), 400
    
    result = appeal_record_service.add_appeal_record(data)
    return jsonify(result)

@appeals_blueprint.route('/search', methods=['GET'])
@require_token
def search_appeals():
    """
    通用查询受理单API端点
    
    查询参数:
    - value: 查询值（必填）
    - type: 查询类型(id_card_number/case_number/contact_info)，可选
    - limit: 返回记录数量限制，默认20条（可选）
    - offset: 起始偏移量，默认0（可选）
    
    响应示例(成功):
    {
        "success": 1,
        "message": "查询成功，共找到 5 条记录，返回 5 条",
        "data": {
            "total": 5,
            "records": [
                {
                    "id": 1,
                    "case_number": "MTDJ-20250516-112318-288808",
                    "person_name": "陈忠",
                    ...
                },
                // 更多记录...
            ]
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "未找到匹配 xxx 的受理单记录",
        "data": {
            "total": 0,
            "records": []
        }
    }
    """
    # 获取查询参数
    search_value = request.args.get('value')
    search_type = request.args.get('type')
    
    if not search_value:
        return jsonify({
            "success": 0,
            "message": "缺少必要参数: value",
            "data": {
                "total": 0,
                "records": []
            }
        }), 400
    
    try:
        limit = int(request.args.get('limit', 20))
    except:
        limit = 20
        
    try:
        offset = int(request.args.get('offset', 0))
    except:
        offset = 0
    
    # 调用服务
    result = appeal_record_service.search_appeal_records(
        search_value, 
        search_type, 
        limit, 
        offset
    )
    
    return jsonify(result)

@appeals_blueprint.route('/all', methods=['GET'])
@require_token
def get_all_appeals():
    """
    获取所有受理单记录API端点
    
    查询参数:
    - limit: 返回记录数量限制，默认100条（可选）
    - offset: 起始偏移量，默认0（可选）
    
    响应示例(成功):
    {
        "success": 1,
        "message": "查询成功，共找到 150 条记录，返回 100 条",
        "data": {
            "total": 150,
            "records": [
                {
                    "id": 1,
                    "case_number": "MTDJ-20250516-112318-288808",
                    "person_name": "陈忠",
                    ...
                },
                // 更多记录...
            ]
        }
    }
    
    响应示例(失败):
    {
        "success": 0,
        "message": "未找到受理单记录",
        "data": {
            "total": 0,
            "records": []
        }
    }
    """
    # 获取查询参数
    try:
        limit = int(request.args.get('limit', 100))
    except:
        limit = 100
        
    try:
        offset = int(request.args.get('offset', 0))
    except:
        offset = 0
    
    # 调用服务
    result = appeal_record_service.get_all_appeals(limit, offset)
    
    return jsonify(result)

# 支持OPTIONS请求的路由
@appeals_blueprint.route('/summary', methods=['OPTIONS'])
def options_appeal_summary():
    """处理受理单摘要API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
    return response

@appeals_blueprint.route('', methods=['OPTIONS'])
def options_appeals():
    """处理受理单API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
    return response

@appeals_blueprint.route('/all', methods=['OPTIONS'])
def options_appeals_all():
    """处理获取所有受理单API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
    return response

@appeals_blueprint.route('/search', methods=['OPTIONS'])
def options_appeals_search():
    """处理搜索受理单API的OPTIONS请求"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
    return response 