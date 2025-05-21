"""
数据库连接和操作模块
"""
import mysql.connector
import json
import logging
from app.config import DB_CONFIG

# 配置日志记录
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_connection():
    """
    创建数据库连接
    
    Returns:
        connection: MySQL数据库连接对象
    """
    try:
        logger.info(f"尝试连接数据库: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port'],
        )
        logger.info("数据库连接成功")
        return connection
    except Exception as e:
        error_msg = f"数据库连接错误: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        raise

def get_dict_cursor(connection):
    """
    获取返回字典结果的游标
    
    Args:
        connection: 数据库连接
        
    Returns:
        cursor: 返回字典结果的游标
    """
    return connection.cursor(dictionary=True)

def create_tables_if_not_exist():
    """
    如果数据表不存在，则创建必要的表结构
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 创建用户表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL COMMENT '姓名',
                contact_info VARCHAR(20) NOT NULL COMMENT '联系方式',
                id_card_number VARCHAR(18) NOT NULL COMMENT '身份证号',
                address VARCHAR(255) DEFAULT '' COMMENT '联系地址',
                verified BOOLEAN DEFAULT FALSE COMMENT '是否已验证',
                verification_result TEXT COMMENT '验证结果',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) COMMENT='用户身份信息表';
            """)
            
            # 创建验证记录表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL COMMENT '用户ID',
                request_data TEXT COMMENT '请求数据',
                response_data TEXT COMMENT '响应数据',
                status VARCHAR(20) COMMENT '验证状态',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) COMMENT='身份验证日志表';
            """)
            
            # 创建历史受理单记录表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS appeal_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_number VARCHAR(50) NOT NULL COMMENT '受理编号',
                person_name VARCHAR(50) NOT NULL COMMENT '姓名',
                contact_info VARCHAR(20) DEFAULT NULL COMMENT '联系方式',
                gender VARCHAR(10) DEFAULT NULL COMMENT '性别',
                id_card_number VARCHAR(20) DEFAULT NULL COMMENT '身份证号',
                address VARCHAR(255) DEFAULT NULL COMMENT '地址',
                incident_time VARCHAR(50) DEFAULT NULL COMMENT '事件时间',
                incident_location VARCHAR(255) DEFAULT NULL COMMENT '事件地点',
                incident_description TEXT COMMENT '事件描述',
                people_involved VARCHAR(10) DEFAULT NULL COMMENT '涉及人数',
                submitted_materials TEXT COMMENT '提交材料',
                handling_department VARCHAR(50) DEFAULT NULL COMMENT '处理部门',
                handling_status VARCHAR(20) DEFAULT NULL COMMENT '处理状态',
                expected_completion VARCHAR(50) DEFAULT NULL COMMENT '预计完成时间',
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                qr_code VARCHAR(255) DEFAULT NULL COMMENT '二维码URL或数据',
                markdown_doc TEXT COMMENT 'Markdown格式文档'
            ) COMMENT='历史受理单记录表';
            """)
            
        connection.commit()
        print("数据表创建成功")
    except Exception as e:
        print(f"创建数据表失败: {e}")
        raise
    finally:
        connection.close()

def insert_test_data():
    """
    插入测试数据
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 检查是否已存在测试数据
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            if result['count'] > 0:
                print("数据库已有数据，跳过测试数据插入")
                return
            
            # 插入测试数据
            test_data = [
                ('张三', '13800138001', '330102199001011234', '浙江省杭州市西湖区文三路123号'),
                ('李四', '13800138002', '330102199002022345', '浙江省杭州市余杭区文一西路456号'),
                ('王五', '13800138003', '330102199003033456', '浙江省杭州市滨江区网商路789号'),
                ('赵六', '13800138004', '330102199004044567', '浙江省杭州市上城区延安路101号'),
                ('钱七', '13800138005', '330102199005055678', '浙江省杭州市下城区体育场路202号')
            ]
            
            insert_query = """
            INSERT INTO users (name, contact_info, id_card_number, address) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.executemany(insert_query, test_data)
            
            # 插入测试受理单记录
            appeal_test_data = [
                ('MTDJ-20250516-112318-288808', '陈忠', '13787674567', '男性', '330102199912212341', 
                 '浙江省杭州市萧山区金色家园', '2025年12月2日', '金色小区家园小区楼下', 
                 '林先生家的宠物狗在小区内随地大小便，陈女士多次提醒无果，影响小区环境卫生。', 
                 '2', '无', '矛盾调解中心', '办理中', '3个工作日内', '2024-02-12 12:32:23',
                 'https://example.com/qr/MTDJ-20250516-112318-288808.png',
                 '# 受理单详情\n\n- **案件编号**: MTDJ-20250516-112318-288808\n- **申请人**: 陈忠\n- **事件**: 宠物狗扰民')
            ]
            
            appeal_query = """
            INSERT INTO appeal_records
            (case_number, person_name, contact_info, gender, id_card_number, 
             address, incident_time, incident_location, incident_description, 
             people_involved, submitted_materials, handling_department, 
             handling_status, expected_completion, create_time, qr_code, markdown_doc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(appeal_query, appeal_test_data)
            
        connection.commit()
        print(f"已插入{len(test_data)}条测试用户数据和测试受理单记录")
    except Exception as e:
        print(f"插入测试数据失败: {e}")
        raise
    finally:
        connection.close()

def get_user_by_id_card(id_card_number):
    """
    根据身份证号查询用户信息
    
    Args:
        id_card_number: 身份证号
        
    Returns:
        dict: 用户信息字典
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            query = "SELECT * FROM users WHERE id_card_number = %s LIMIT 1"
            cursor.execute(query, (id_card_number,))
            return cursor.fetchone()
    except Exception as e:
        print(f"查询用户失败: {e}")
        return None
    finally:
        connection.close()

def update_verification_result(user_id, verified, result):
    """
    更新用户验证结果
    
    Args:
        user_id: 用户ID
        verified: 是否验证通过
        result: 验证结果内容
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            query = """
            UPDATE users SET verified = %s, verification_result = %s 
            WHERE id = %s
            """
            cursor.execute(query, (verified, result, user_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"更新验证结果失败: {e}")
        return False
    finally:
        connection.close()

def log_verification(user_id, request_data, response_data, status):
    """
    记录验证日志
    
    Args:
        user_id: 用户ID
        request_data: 请求数据
        response_data: 响应数据
        status: 验证状态
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            query = """
            INSERT INTO verification_logs (user_id, request_data, response_data, status)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                user_id,
                json.dumps(request_data, ensure_ascii=False),
                json.dumps(response_data, ensure_ascii=False),
                status
            ))
        connection.commit()
        return True
    except Exception as e:
        print(f"记录验证日志失败: {e}")
        return False
    finally:
        connection.close()

def get_all_users(limit=100):
    """
    获取所有用户信息
    
    Args:
        limit: 最大返回数量
    
    Returns:
        list: 用户信息列表
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            query = f"SELECT * FROM users LIMIT {limit}"
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"获取所有用户失败: {e}")
        return []
    finally:
        connection.close()

def get_appeal_records_by_id_card(id_card_number, limit=20, offset=0):
    """
    根据身份证号查询受理单记录
    
    Args:
        id_card_number: 身份证号
        limit: 最大返回数量
        offset: 跳过记录数
    
    Returns:
        tuple: (总记录数, 记录列表)
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 查询总记录数
            count_query = "SELECT COUNT(*) as total FROM appeal_records WHERE id_card_number = %s"
            cursor.execute(count_query, (id_card_number,))
            total = cursor.fetchone()['total']
            
            # 如果没有记录，直接返回
            if total == 0:
                return 0, []
            
            # 查询数据
            query = """
            SELECT * FROM appeal_records 
            WHERE id_card_number = %s
            ORDER BY create_time DESC
            LIMIT %s OFFSET %s
            """
            cursor.execute(query, (id_card_number, limit, offset))
            records = cursor.fetchall()
            
            return total, records
    except Exception as e:
        print(f"查询受理单记录失败: {e}")
        return 0, []
    finally:
        connection.close()

def get_appeal_record_by_case_number(case_number):
    """
    根据案件编号查询受理单记录
    
    Args:
        case_number: 案件编号
    
    Returns:
        dict: 受理单记录
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            query = "SELECT * FROM appeal_records WHERE case_number = %s LIMIT 1"
            cursor.execute(query, (case_number,))
            return cursor.fetchone()
    except Exception as e:
        print(f"查询受理单记录失败: {e}")
        return None
    finally:
        connection.close()

def get_appeal_records_by_contact_info(contact_info, limit=20, offset=0):
    """
    根据联系方式查询受理单记录
    
    Args:
        contact_info: 联系方式
        limit: 最大返回数量
        offset: 跳过记录数
    
    Returns:
        tuple: (总记录数, 记录列表)
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 查询总记录数
            count_query = "SELECT COUNT(*) as total FROM appeal_records WHERE contact_info = %s"
            cursor.execute(count_query, (contact_info,))
            total = cursor.fetchone()['total']
            
            # 如果没有记录，直接返回
            if total == 0:
                return 0, []
            
            # 查询数据
            query = """
            SELECT * FROM appeal_records 
            WHERE contact_info = %s
            ORDER BY create_time DESC
            LIMIT %s OFFSET %s
            """
            cursor.execute(query, (contact_info, limit, offset))
            records = cursor.fetchall()
            
            return total, records
    except Exception as e:
        print(f"查询受理单记录失败: {e}")
        return 0, []
    finally:
        connection.close()

def get_all_appeal_records(limit=100, offset=0):
    """
    获取所有受理单记录
    
    Args:
        limit: 最大返回数量
        offset: 跳过记录数
    
    Returns:
        tuple: (总记录数, 记录列表)
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 查询总记录数
            count_query = "SELECT COUNT(*) as total FROM appeal_records"
            cursor.execute(count_query)
            total = cursor.fetchone()['total']
            
            # 如果没有记录，直接返回
            if total == 0:
                return 0, []
            
            # 查询数据
            query = """
            SELECT * FROM appeal_records 
            ORDER BY create_time DESC
            LIMIT %s OFFSET %s
            """
            cursor.execute(query, (limit, offset))
            records = cursor.fetchall()
            
            return total, records
    except Exception as e:
        print(f"查询所有受理单记录失败: {e}")
        return 0, []
    finally:
        connection.close()

def add_appeal_record(data):
    """
    添加受理单记录
    
    Args:
        data: 受理单数据
    
    Returns:
        tuple: (成功标志, 消息)
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 检查案件编号是否已存在
            check_query = "SELECT COUNT(*) as count FROM appeal_records WHERE case_number = %s"
            cursor.execute(check_query, (data.get('case_number'),))
            if cursor.fetchone()['count'] > 0:
                return False, f"案件编号 {data.get('case_number')} 已存在"
            
            # 准备字段和值
            fields = []
            values = []
            placeholders = []
            
            for key, value in data.items():
                fields.append(key)
                values.append(value)
                placeholders.append('%s')
            
            # 构建SQL
            query = f"""
            INSERT INTO appeal_records ({', '.join(fields)})
            VALUES ({', '.join(placeholders)})
            """
            
            # 执行插入
            cursor.execute(query, values)
            
        connection.commit()
        return True, "受理单记录添加成功"
    except Exception as e:
        print(f"添加受理单记录失败: {e}")
        return False, f"添加受理单记录失败: {e}"
    finally:
        connection.close()

def get_appeal_summary_by_id_card(id_card_number):
    """
    获取用户的受理单摘要信息
    
    Args:
        id_card_number: 身份证号
    
    Returns:
        dict: 摘要信息
    """
    connection = get_connection()
    try:
        with get_dict_cursor(connection) as cursor:
            # 查询用户名
            query = "SELECT person_name FROM appeal_records WHERE id_card_number = %s LIMIT 1"
            cursor.execute(query, (id_card_number,))
            person_record = cursor.fetchone()
            
            if not person_record:
                return None
            
            person_name = person_record['person_name']
            
            # 查询受理单数量
            count_query = "SELECT COUNT(*) as total FROM appeal_records WHERE id_card_number = %s"
            cursor.execute(count_query, (id_card_number,))
            appeal_count = cursor.fetchone()['total']
            
            # 查询最新受理单时间
            latest_query = "SELECT create_time FROM appeal_records WHERE id_card_number = %s ORDER BY create_time DESC LIMIT 1"
            cursor.execute(latest_query, (id_card_number,))
            latest_appeal = cursor.fetchone()['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            
            # 查询处理状态统计
            status_query = """
            SELECT handling_status, COUNT(*) as count 
            FROM appeal_records 
            WHERE id_card_number = %s 
            GROUP BY handling_status
            """
            cursor.execute(status_query, (id_card_number,))
            status_stats = {row['handling_status']: row['count'] for row in cursor.fetchall()}
            
            # 查询部门列表
            dept_query = """
            SELECT DISTINCT handling_department 
            FROM appeal_records 
            WHERE id_card_number = %s
            """
            cursor.execute(dept_query, (id_card_number,))
            departments = [row['handling_department'] for row in cursor.fetchall()]
            
            return {
                'person_name': person_name,
                'appeal_count': appeal_count,
                'latest_appeal': latest_appeal,
                'handling_status_stats': status_stats,
                'departments': departments
            }
    except Exception as e:
        print(f"获取受理单摘要失败: {e}")
        return None
    finally:
        connection.close() 