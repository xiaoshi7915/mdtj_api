"""
API测试脚本 - 测试矛盾调解受理服务的API接口
"""
import requests
import json
import sys
import time
import socket
import traceback
import argparse
from requests.exceptions import RequestException, Timeout

# 设置调试模式
DEBUG = True
TIMEOUT = 5  # 连接超时时间（秒）

# 解析命令行参数
parser = argparse.ArgumentParser(description='测试矛盾调解受理服务API')
parser.add_argument('--host', default='127.0.0.1', help='API服务器主机名或IP')
parser.add_argument('--port', type=int, default=8701, help='API服务器端口')
parser.add_argument('--token', default='api_token_2025', help='API令牌')
parser.add_argument('--timeout', type=int, default=5, help='请求超时时间(秒)')
parser.add_argument('--debug', action='store_true', help='启用调试模式')
parser.add_argument('--test', default='all', help='运行指定测试(health, identity, appeals, auth, users, all)')

# 尝试获取当前主机IP
try:
    hostname = socket.gethostname()
    SERVER_IP = socket.gethostbyname(hostname)
except:
    SERVER_IP = "127.0.0.1"

# 全局变量
args = None
BASE_URL = None
TOKEN = None
HEADERS = None

# 统计信息
STATS = {
    'passed': 0,
    'failed': 0,
    'total': 0
}

def setup_test_environment():
    """设置测试环境变量"""
    global args, BASE_URL, TOKEN, HEADERS, DEBUG, TIMEOUT
    
    args = parser.parse_args()
    DEBUG = args.debug
    TIMEOUT = args.timeout
    
    # 构建基础URL
    BASE_URL = f"http://{args.host}:{args.port}/api"
    TOKEN = args.token
    HEADERS = {"token": TOKEN}
    
    print(f"测试环境: 服务器={args.host}:{args.port}, 令牌={TOKEN}, 超时={TIMEOUT}秒")

def debug_print(message):
    """调试信息打印"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def make_request(method, url, params=None, data=None, headers=None, timeout=None):
    """发送HTTP请求并处理异常"""
    timeout = timeout or TIMEOUT
    headers = headers or HEADERS
    request_method = getattr(requests, method.lower())
    
    debug_print(f"请求URL: {url}")
    debug_print(f"请求方法: {method.upper()}")
    debug_print(f"请求头: {headers}")
    
    if params:
        debug_print(f"请求参数: {params}")
    if data:
        debug_print(f"请求体: {data}")
    
    try:
        if method.lower() == 'get':
            resp = request_method(url, params=params, headers=headers, timeout=timeout)
        else:
            resp = request_method(url, json=data, headers=headers, timeout=timeout)
        
        print(f"状态码: {resp.status_code}")
        debug_print(f"响应头: {resp.headers}")
        debug_print(f"响应体: {resp.text}")
        
        return resp, True
    except Timeout:
        print(f"请求超时，超过 {timeout} 秒未响应")
        return None, False
    except RequestException as e:
        print(f"请求异常: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return None, False
    except Exception as e:
        print(f"未知异常: {str(e)}")
        if DEBUG:
            traceback.print_exc()
        return None, False

def check_response(resp):
    """检查响应是否成功并处理响应内容"""
    if not resp:
        return False
    
    if resp.status_code < 200 or resp.status_code >= 300:
        print(f"失败: 状态码 {resp.status_code}")
        try:
            print(f"响应内容: {resp.json()}")
        except:
            print(f"响应内容: {resp.text}")
        return False
    
    try:
        response_json = resp.json()
        print(f"响应内容: {response_json}")
        # 检查成功标志（如果存在）
        if 'success' in response_json and response_json['success'] == 0:
            print(f"API返回错误: {response_json.get('message', '未知错误')}")
            return False
        return True
    except Exception as e:
        print(f"解析响应内容失败: {str(e)}")
        return False

def test_health():
    """测试健康检查接口"""
    print("\n测试健康检查接口...")
    url = f"{BASE_URL}/health"
    
    resp, success = make_request('get', url)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_identity_verify():
    """测试身份验证接口"""
    print("\n测试身份验证接口...")
    url = f"{BASE_URL}/identity/verify"
    data = {"id_card_number": "330102199001011234"}
    
    resp, success = make_request('post', url, data=data)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_identity_status():
    """测试身份验证状态接口"""
    print("\n测试身份验证状态接口...")
    url = f"{BASE_URL}/identity/status"
    params = {"id_card_number": "330102199001011234"}
    
    resp, success = make_request('get', url, params=params)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_appeals_summary():
    """测试受理单摘要接口"""
    print("\n测试受理单摘要接口...")
    url = f"{BASE_URL}/appeals/summary"
    params = {"id_card_number": "330102199912212341"}
    
    resp, success = make_request('get', url, params=params)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_appeals_search():
    """测试受理单搜索接口"""
    print("\n测试受理单搜索接口...")
    url = f"{BASE_URL}/appeals/search"
    params = {"value": "330102199912212341", "type": "id_card_number"}
    
    resp, success = make_request('get', url, params=params)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_appeals_all():
    """测试查询所有受理单接口"""
    print("\n测试查询所有受理单接口...")
    url = f"{BASE_URL}/appeals/all"
    
    resp, success = make_request('get', url)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_auth_validate():
    """测试令牌验证接口"""
    print("\n测试令牌验证接口...")
    url = f"{BASE_URL}/auth/validate"
    params = {"token": TOKEN}
    
    resp, success = make_request('get', url, params=params, headers={})
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def test_users():
    """测试用户列表接口"""
    print("\n测试用户列表接口...")
    url = f"{BASE_URL}/users"
    
    resp, success = make_request('get', url)
    if not success:
        STATS['failed'] += 1
        return False
    
    result = check_response(resp)
    if result:
        STATS['passed'] += 1
    else:
        STATS['failed'] += 1
    
    return result

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print(f"矛盾调解受理服务 API 测试开始")
    print("=" * 50)
    
    test_functions = {
        'health': test_health,
        'identity': [test_identity_verify, test_identity_status],
        'appeals': [test_appeals_summary, test_appeals_search, test_appeals_all],
        'auth': test_auth_validate,
        'users': test_users,
    }
    
    # 确定要运行的测试
    tests_to_run = []
    if args.test == 'all':
        # 添加所有测试
        for category, funcs in test_functions.items():
            if isinstance(funcs, list):
                tests_to_run.extend(funcs)
            else:
                tests_to_run.append(funcs)
    else:
        # 添加指定类别的测试
        categories = args.test.split(',')
        for category in categories:
            category = category.strip()
            if category in test_functions:
                funcs = test_functions[category]
                if isinstance(funcs, list):
                    tests_to_run.extend(funcs)
                else:
                    tests_to_run.append(funcs)
    
    # 运行测试
    STATS['total'] = len(tests_to_run)
    for test_func in tests_to_run:
        test_func()
    
    # 打印测试结果
    print("\n" + "=" * 50)
    print(f"测试结果: 总共 {STATS['total']}，通过 {STATS['passed']}，失败 {STATS['failed']}")
    print("=" * 50)
    
    # 检查是否所有测试都通过
    return STATS['failed'] == 0

if __name__ == "__main__":
    setup_test_environment()
    success = run_all_tests()
    sys.exit(0 if success else 1) 