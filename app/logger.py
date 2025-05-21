"""
日志系统模块 - 提供统一的日志配置和管理
"""
import os
import logging
import logging.handlers
import json
import datetime
import traceback
from logging.config import dictConfig
from flask import request, g, has_request_context
import time

# 默认日志配置
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] [%(request_id)s] - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_DIR = "logs"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 10  # 保留10个备份文件

class RequestIDFilter(logging.Filter):
    """
    在日志记录中添加请求ID的过滤器
    """
    def filter(self, record):
        # 添加请求ID字段
        if has_request_context() and hasattr(request, 'request_id'):
            record.request_id = request.request_id
        elif hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'no-request-id'
            
        return True

class JSONFormatter(logging.Formatter):
    """
    JSON格式的日志格式化器
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).strftime(DEFAULT_DATE_FORMAT),
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, 'request_id', 'no-request-id'),
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加异常信息（如果有）
        if record.exc_info:
            log_record["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stacktrace": traceback.format_exception(*record.exc_info)
            }
        
        # 添加额外字段
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", 
                          "filename", "funcName", "id", "levelname", "levelno", 
                          "lineno", "module", "msecs", "message", "msg", "name", 
                          "pathname", "process", "processName", "relativeCreated", 
                          "request_id", "stack_info", "thread", "threadName"]:
                log_record[key] = value
                
        return json.dumps(log_record, ensure_ascii=False)

def get_log_file_handlers(app_name):
    """
    获取文件日志处理器
    
    Args:
        app_name: 应用名称，用于日志文件命名
        
    Returns:
        dict: 文件日志处理器字典
    """
    # 确保日志目录存在
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    handlers = {
        # 普通日志文件处理器
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": os.path.join(LOG_DIR, f"{app_name}.log"),
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": BACKUP_COUNT,
            "encoding": "utf8",
            "filters": ["request_id"]
        },
        # 错误日志文件处理器
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": os.path.join(LOG_DIR, f"{app_name}_error.log"),
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": BACKUP_COUNT,
            "encoding": "utf8",
            "level": "ERROR",
            "filters": ["request_id"]
        },
        # JSON格式日志文件处理器
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": os.path.join(LOG_DIR, f"{app_name}_json.log"),
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": BACKUP_COUNT,
            "encoding": "utf8",
            "filters": ["request_id"]
        }
    }
    
    return handlers

def configure_logging(app_name, log_level=None, enable_console=True, enable_json=True):
    """
    配置日志系统
    
    Args:
        app_name: 应用名称
        log_level: 日志级别，默认为INFO
        enable_console: 是否启用控制台日志
        enable_json: 是否启用JSON格式日志
    """
    if log_level is None:
        log_level = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    
    # 基本配置
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": DEFAULT_LOG_FORMAT,
                "datefmt": DEFAULT_DATE_FORMAT
            },
            "json": {
                "()": JSONFormatter
            }
        },
        "filters": {
            "request_id": {
                "()": RequestIDFilter
            }
        },
        "handlers": {},
        "loggers": {
            "": {  # 根日志器
                "handlers": [],
                "level": log_level,
                "propagate": True
            }
        }
    }
    
    # 添加文件处理器
    file_handlers = get_log_file_handlers(app_name)
    config["handlers"].update(file_handlers)
    config["loggers"][""]["handlers"].extend(file_handlers.keys())
    
    # 添加控制台处理器（如果启用）
    if enable_console:
        config["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": log_level,
            "stream": "ext://sys.stdout",
            "filters": ["request_id"]
        }
        config["loggers"][""]["handlers"].append("console")
    
    # 如果不启用JSON日志，移除相关处理器
    if not enable_json and "json_file" in config["handlers"]:
        config["handlers"].pop("json_file")
        if "json_file" in config["loggers"][""]["handlers"]:
            config["loggers"][""]["handlers"].remove("json_file")
    
    # 应用配置
    dictConfig(config)
    
    # 获取根日志器
    logger = logging.getLogger()
    
    # 输出配置信息
    logger.info(f"日志系统已配置，应用：{app_name}，日志级别：{log_level}")
    logger.info(f"日志保存在：{os.path.abspath(LOG_DIR)}")

def get_logger(name):
    """
    获取指定名称的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        Logger: 日志器对象
    """
    return logging.getLogger(name)

def log_request(response=None):
    """
    记录请求日志
    
    Args:
        response: Flask响应对象（可选）
        
    Returns:
        Response: 原始响应对象
    """
    logger = logging.getLogger("request")
    
    if has_request_context():
        # 请求处理时间
        request_time = getattr(request, 'request_time', None)
        process_time = None
        
        if request_time:
            process_time = time.time() - request_time
            process_time = round(process_time * 1000, 2)  # 毫秒
        
        # 状态码
        status_code = response.status_code if response else "-"
        
        # 记录请求日志
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": status_code,
            "ip": request.remote_addr,
            "user_agent": request.user_agent.string,
            "process_time_ms": process_time
        }
        
        # 添加查询参数（如果有）
        if request.args:
            log_data["query_params"] = dict(request.args)
        
        # 对于非GET请求，记录请求体（排除敏感信息）
        if request.method != "GET" and request.is_json:
            request_body = request.get_json(silent=True)
            if request_body:
                # 过滤敏感字段
                filtered_body = filter_sensitive_data(request_body)
                log_data["request_body"] = filtered_body
        
        logger.info(f"HTTP请求: {json.dumps(log_data, ensure_ascii=False)}")
    
    return response

def filter_sensitive_data(data, sensitive_fields=None):
    """
    过滤敏感数据，用于日志记录
    
    Args:
        data: 原始数据
        sensitive_fields: 敏感字段列表
        
    Returns:
        dict: 过滤后的数据
    """
    if sensitive_fields is None:
        sensitive_fields = ["password", "token", "secret", "api_key", "id_card", 
                           "id_card_number", "phone", "credit_card", "address"]
    
    if isinstance(data, dict):
        filtered_data = {}
        for key, value in data.items():
            if any(field.lower() in key.lower() for field in sensitive_fields):
                # 对敏感信息进行脱敏
                if isinstance(value, str):
                    filtered_data[key] = mask_sensitive_string(value)
                else:
                    filtered_data[key] = "***MASKED***"
            elif isinstance(value, (dict, list)):
                filtered_data[key] = filter_sensitive_data(value, sensitive_fields)
            else:
                filtered_data[key] = value
        return filtered_data
    elif isinstance(data, list):
        return [filter_sensitive_data(item, sensitive_fields) for item in data]
    else:
        return data

def mask_sensitive_string(value):
    """
    对敏感字符串进行脱敏处理
    
    Args:
        value: 原始字符串
        
    Returns:
        str: 脱敏后的字符串
    """
    if not value:
        return value
    
    # 根据字符串长度决定保留的字符数
    length = len(value)
    
    if length <= 3:
        return "***"
    elif length <= 6:
        return value[0] + "***"
    elif length <= 9:
        return value[:2] + "***" + value[-2:]
    else:
        return value[:3] + "***" + value[-3:] 