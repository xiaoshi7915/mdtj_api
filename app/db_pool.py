"""
数据库连接池管理模块 - 提供数据库连接池功能
"""
import mysql.connector
from mysql.connector import pooling
import threading
import logging
import time
from contextlib import contextmanager
from app.config import DB_CONFIG

# 配置日志
logger = logging.getLogger("db_pool")

# 全局连接池对象
_pool = None
_pool_lock = threading.Lock()
_initialized = False

# 连接池配置
POOL_NAME = "mdtj_mysql_pool"
POOL_SIZE = 10
POOL_RESET_SESSION = True
MAX_RETRIES = 3
RETRY_DELAY = 1  # 秒

def init_pool():
    """
    初始化数据库连接池
    
    Returns:
        bool: 初始化是否成功
    """
    global _pool, _initialized
    
    if _initialized:
        return True
    
    with _pool_lock:
        if _initialized:
            return True
        
        try:
            logger.info(f"正在初始化数据库连接池，连接到 {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
            # 创建连接池
            _pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=POOL_NAME,
                pool_size=POOL_SIZE,
                pool_reset_session=POOL_RESET_SESSION,
                **DB_CONFIG
            )
            _initialized = True
            logger.info(f"数据库连接池初始化成功，连接池大小：{POOL_SIZE}")
            return True
        except Exception as e:
            logger.error(f"数据库连接池初始化失败: {e}")
            return False

def get_pool():
    """
    获取数据库连接池
    
    Returns:
        MySQLConnectionPool: MySQL连接池对象
    """
    global _pool
    
    if not _initialized:
        init_pool()
    
    return _pool

@contextmanager
def get_connection(auto_commit=False):
    """
    从连接池获取数据库连接的上下文管理器
    
    Args:
        auto_commit: 是否自动提交事务
        
    Yields:
        connection: 数据库连接对象
        
    Raises:
        Exception: 无法获取数据库连接时抛出异常
    """
    if not _initialized:
        init_pool()
    
    conn = None
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            conn = _pool.get_connection()
            break
        except Exception as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"无法获取数据库连接，已重试 {retries} 次: {e}")
                raise Exception(f"无法获取数据库连接: {e}")
            
            logger.warning(f"获取数据库连接失败，准备重试（{retries}/{MAX_RETRIES}）: {e}")
            time.sleep(RETRY_DELAY)
    
    try:
        conn.autocommit = auto_commit
        yield conn
    except Exception as e:
        if not auto_commit and conn:
            try:
                conn.rollback()
                logger.info("数据库事务已回滚")
            except Exception as rollback_error:
                logger.error(f"数据库事务回滚失败: {rollback_error}")
        raise
    finally:
        if conn:
            try:
                conn.close()
            except Exception as close_error:
                logger.warning(f"关闭数据库连接失败: {close_error}")

@contextmanager
def get_cursor(cursor_type=None, auto_commit=False, named_tuple=False, dictionary=True, buffered=True):
    """
    从连接池获取数据库游标的上下文管理器
    
    Args:
        cursor_type: 游标类型
        auto_commit: 是否自动提交事务
        named_tuple: 是否返回命名元组结果
        dictionary: 是否返回字典结果
        buffered: 是否使用缓冲游标
        
    Yields:
        cursor: 数据库游标对象
    """
    with get_connection(auto_commit) as conn:
        cursor = None
        try:
            cursor_params = {
                "named_tuple": named_tuple,
                "dictionary": dictionary,
                "buffered": buffered
            }
            
            if cursor_type:
                cursor_params["cursor_class"] = cursor_type
            
            cursor = conn.cursor(**cursor_params)
            yield cursor
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    logger.warning(f"关闭数据库游标失败: {e}")

def close_pool():
    """
    关闭数据库连接池
    """
    global _pool, _initialized
    
    with _pool_lock:
        if _initialized and _pool:
            _pool = None
            _initialized = False
            logger.info("数据库连接池已关闭")

def execute_query(query, params=None, dictionary=True, fetch_one=False):
    """
    执行查询SQL并返回结果
    
    Args:
        query: SQL查询语句
        params: 查询参数
        dictionary: 是否返回字典结果
        fetch_one: 是否只返回第一条结果
        
    Returns:
        list/dict: 查询结果
    """
    with get_cursor(dictionary=dictionary) as cursor:
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        else:
            return cursor.fetchall()

def execute_update(query, params=None):
    """
    执行更新SQL并返回影响行数
    
    Args:
        query: SQL更新语句
        params: 更新参数
        
    Returns:
        int: 影响行数
        
    Raises:
        Exception: 执行失败时抛出异常
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows

def execute_transaction(queries):
    """
    执行事务，包含多个SQL操作
    
    Args:
        queries: 包含(query, params)元组的列表
        
    Returns:
        bool: 事务是否成功
        
    Raises:
        Exception: 执行失败时抛出异常
    """
    with get_connection() as conn:
        try:
            with conn.cursor() as cursor:
                for query, params in queries:
                    cursor.execute(query, params or ())
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"事务执行失败: {e}")
            raise

def ping_db():
    """
    测试数据库连接是否正常
    
    Returns:
        bool: 连接是否正常
    """
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False 