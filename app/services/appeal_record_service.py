"""
受理单记录服务 - 处理历史受理单记录的相关功能
"""
import time
import datetime
from app.models import database

def get_appeal_records_by_id_card(id_card_number, limit=20, offset=0):
    """
    根据身份证号获取受理单记录
    
    Args:
        id_card_number: 身份证号
        limit: 最大返回数量
        offset: 跳过记录数
        
    Returns:
        dict: 查询结果
    """
    # 验证参数
    if not id_card_number:
        return {
            "success": 0,
            "message": "缺少必要参数: id_card_number",
            "data": {
                "total": 0,
                "records": []
            }
        }
    
    # 查询记录
    total, records = database.get_appeal_records_by_id_card(
        id_card_number, 
        limit=limit, 
        offset=offset
    )
    
    # 构建响应
    if total > 0:
        return {
            "success": 1,
            "message": f"查询成功，共找到 {total} 条记录，返回 {len(records)} 条",
            "data": {
                "total": total,
                "records": records
            }
        }
    else:
        return {
            "success": 0,
            "message": f"未找到身份证号为 {id_card_number} 的受理单记录",
            "data": {
                "total": 0,
                "records": []
            }
        }

def get_appeal_record_by_case_number(case_number):
    """
    根据案件编号获取受理单记录
    
    Args:
        case_number: 案件编号
        
    Returns:
        dict: 查询结果
    """
    # 验证参数
    if not case_number:
        return {
            "success": 0,
            "message": "缺少必要参数: case_number",
            "data": {}
        }
    
    # 查询记录
    record = database.get_appeal_record_by_case_number(case_number)
    
    # 构建响应
    if record:
        return {
            "success": 1,
            "message": "查询成功",
            "data": record
        }
    else:
        return {
            "success": 0,
            "message": f"未找到案件编号为 {case_number} 的受理单记录",
            "data": {}
        }

def search_appeal_records(search_value, search_type=None, limit=20, offset=0):
    """
    通用查询受理单记录
    
    Args:
        search_value: 查询值
        search_type: 查询类型(id_card_number/case_number/contact_info)
        limit: 最大返回数量
        offset: 跳过记录数
        
    Returns:
        dict: 查询结果
    """
    # 验证参数
    if not search_value:
        return {
            "success": 0,
            "message": "缺少必要参数: value",
            "data": {
                "total": 0,
                "records": []
            }
        }
    
    # 根据搜索类型选择查询方法
    if search_type == "case_number" or (not search_type and len(search_value) > 15 and search_value.startswith("MTDJ-")):
        # 按案件编号查询
        record = database.get_appeal_record_by_case_number(search_value)
        
        if record:
            return {
                "success": 1,
                "message": "查询成功，共找到 1 条记录",
                "data": {
                    "total": 1,
                    "records": [record]
                }
            }
        else:
            return {
                "success": 0,
                "message": f"未找到匹配 {search_value} 的受理单记录",
                "data": {
                    "total": 0,
                    "records": []
                }
            }
            
    elif search_type == "id_card_number" or (not search_type and len(search_value) >= 15 and search_value.isdigit()):
        # 按身份证号查询
        total, records = database.get_appeal_records_by_id_card(
            search_value, 
            limit=limit, 
            offset=offset
        )
        
    elif search_type == "contact_info" or (not search_type and len(search_value) == 11 and search_value.isdigit()):
        # 按联系方式查询
        total, records = database.get_appeal_records_by_contact_info(
            search_value, 
            limit=limit, 
            offset=offset
        )
        
    else:
        # 尝试按多个字段查询（这里可以实现更复杂的逻辑）
        # 这里简单示例，先按身份证号查
        total_id, records_id = database.get_appeal_records_by_id_card(
            search_value, 
            limit=limit, 
            offset=offset
        )
        
        if total_id > 0:
            return {
                "success": 1,
                "message": f"查询成功，共找到 {total_id} 条记录，返回 {len(records_id)} 条",
                "data": {
                    "total": total_id,
                    "records": records_id
                }
            }
            
        # 再尝试按联系方式查
        total, records = database.get_appeal_records_by_contact_info(
            search_value, 
            limit=limit, 
            offset=offset
        )
    
    # 构建响应
    if total > 0:
        return {
            "success": 1,
            "message": f"查询成功，共找到 {total} 条记录，返回 {len(records)} 条",
            "data": {
                "total": total,
                "records": records
            }
        }
    else:
        return {
            "success": 0,
            "message": f"未找到匹配 {search_value} 的受理单记录",
            "data": {
                "total": 0,
                "records": []
            }
        }

def get_all_appeals(limit=100, offset=0):
    """
    获取所有受理单记录
    
    Args:
        limit: 最大返回数量
        offset: 跳过记录数
        
    Returns:
        dict: 查询结果
    """
    # 查询记录
    total, records = database.get_all_appeal_records(
        limit=limit, 
        offset=offset
    )
    
    # 构建响应
    if total > 0:
        return {
            "success": 1,
            "message": f"查询成功，共找到 {total} 条记录，返回 {len(records)} 条",
            "data": {
                "total": total,
                "records": records
            }
        }
    else:
        return {
            "success": 0,
            "message": "未找到受理单记录",
            "data": {
                "total": 0,
                "records": []
            }
        }

def add_appeal_record(data):
    """
    添加受理单记录
    
    Args:
        data: 受理单数据
        
    Returns:
        dict: 添加结果
    """
    # 验证必要字段
    required_fields = ['case_number', 'person_name', 'id_card_number']
    for field in required_fields:
        if field not in data:
            return {
                "success": 0,
                "message": f"缺少必要字段: {field}",
                "data": {}
            }
    
    # 检查是否已存在相同案件编号
    existing = database.get_appeal_record_by_case_number(data['case_number'])
    if existing:
        return {
            "success": 0,
            "message": f"案件编号 {data['case_number']} 已存在",
            "data": {}
        }
    
    # 添加记录
    success, message = database.add_appeal_record(data)
    
    if success:
        return {
            "success": 1,
            "message": "受理单记录添加成功",
            "case_number": data['case_number']
        }
    else:
        return {
            "success": 0,
            "message": f"受理单记录添加失败: {message}",
            "data": {}
        }

def get_appeal_summary(id_card_number):
    """
    获取受理单摘要信息
    
    Args:
        id_card_number: 身份证号
        
    Returns:
        dict: 摘要信息
    """
    # 查询该身份证号的所有受理单记录
    total, records = database.get_appeal_records_by_id_card(
        id_card_number, 
        limit=100  # 获取足够多的记录以生成摘要
    )
    
    if total == 0:
        return {
            "success": 0,
            "message": f"未找到身份证号为 {id_card_number} 的受理单记录",
            "data": {}
        }
    
    # 提取摘要数据
    # 1. 用户姓名（取第一条记录的值）
    person_name = records[0]['person_name']
    
    # 2. 总记录数
    appeal_count = total
    
    # 3. 最新的受理单时间（时间最大的一条）
    latest_appeal = max([record.get('created_at', '1970-01-01 00:00:00') for record in records])
    
    # 4. 办理状态统计
    status_stats = {}
    for record in records:
        status = record.get('handling_status', '未知')
        status_stats[status] = status_stats.get(status, 0) + 1
    
    # 5. 涉及的部门列表（去重）
    departments = list(set([record.get('handling_department', '未知') for record in records]))
    
    return {
        "success": 1,
        "message": "查询成功",
        "data": {
            "person_name": person_name,
            "appeal_count": appeal_count,
            "latest_appeal": latest_appeal,
            "handling_status_stats": status_stats,
            "departments": departments
        }
    } 