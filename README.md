# 矛盾调解受理服务 API

本项目是一个基于Flask开发的矛盾调解身份验证和受理单管理服务，提供RESTful API接口。系统支持身份验证、历史受理单查询和管理等功能。

## 项目特点

- 基于 Flask 的现代化 RESTful API 设计
- 模块化的代码结构，便于维护和扩展
- 完善的跨域请求(CORS)支持
- Swagger API 文档自动生成
- 多环境配置支持 (开发/生产)
- 令牌认证机制
- 数据库连接池和异常处理
- 可通过Docker容器化部署

## 目录结构

```
mdtj_api/
├── app/                    # 应用程序代码
│   ├── __init__.py         # 包初始化
│   ├── main.py             # 主应用程序入口
│   ├── config.py           # 配置文件
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py         # 用户模型
│   │   ├── appeal_record.py # 受理单模型
│   │   └── database.py     # 数据库操作封装
│   ├── routes/             # 路由定义
│   │   ├── __init__.py
│   │   ├── appeals_routes.py    # 受理单相关路由
│   │   ├── auth_routes.py       # 认证相关路由
│   │   ├── health_routes.py     # 健康检查路由
│   │   ├── identity_routes.py   # 身份验证路由
│   │   └── user_routes.py       # 用户管理路由 
│   ├── services/           # 业务服务层
│   │   ├── __init__.py
│   │   ├── appeal_record_service.py # 受理单服务
│   │   └── verification_service.py # 验证服务
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── auth.py         # 认证工具
│   │   └── cors_handler.py # 跨域处理
│   ├── swagger.json        # Swagger API文档
│   ├── error_handlers.py   # 错误处理
│   ├── validators.py       # 数据验证
│   ├── logger.py           # 日志管理
│   └── db_pool.py          # 数据库连接池
├── logs/                   # 日志文件目录
├── sql/                    # SQL脚本文件
│   ├── init.sql            # 初始化数据库脚本
│   └── sample_data.sql     # 示例数据
├── scripts/                # 脚本文件
│   ├── start.sh            # 启动脚本
│   └── restart.sh          # 重启脚本
├── docker/                 # Docker相关文件
│   ├── Dockerfile          # Docker构建文件
│   └── docker-compose.yml  # Docker Compose配置
├── mdtj_env/               # Python虚拟环境
├── test_api.py             # API测试脚本
├── run.py                  # 应用统一入口（直接运行和WSGI服务器）
├── requirements.txt        # 项目依赖
├── .env.example            # 环境变量配置示例
└── README.md               # 说明文档
```

## 环境要求

- Python 3.8+
- MySQL 8.0+
- Docker (可选，如果使用Docker部署)

## 部署方式

### 方式一：源码部署（一键部署）

1. **准备环境**

   确保已安装Python 3.8+和MySQL 8.0+

   ```bash
   # CentOS/RHEL
   yum install -y python38 python38-devel mysql-devel gcc

   # Ubuntu/Debian
   apt-get update && apt-get install -y python3.8 python3.8-dev default-libmysqlclient-dev build-essential
   ```

2. **克隆代码**

   ```bash
   git clone https://github.com/xiaoshi7915/mdtj_api.git
   cd /opt/mdtj_api
   ```

3. **一键部署**

   ```bash
   # 复制环境变量示例文件并修改为你的配置
   cp .env.example .env
   
   # 编辑.env文件，修改数据库连接信息
   # DB_HOST=你的数据库主机地址
   # DB_PASSWORD=你的数据库密码
   vi .env
   
   # 执行部署脚本（自动创建虚拟环境、安装依赖并启动服务）
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

4. **验证服务运行**

   访问 http://服务器IP:8701/api/docs/ 查看API文档

### 方式二：Docker部署（一键部署）

1. **安装Docker和Docker Compose**

   ```bash
   # 安装Docker
   curl -fsSL https://get.docker.com | sh
   
   # 安装Docker Compose
   curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   ```

2. **克隆代码**

   ```bash
   git clone https://github.com/xiaoshi7915/mdtj_api.git
   cd /opt/mdtj_api
   ```

3. **一键部署**

   ```bash
   # 修改docker-compose.yml中的数据库配置（如需要）
   vi docker/docker-compose.yml
   
   # 构建并启动容器
   cd docker
   docker-compose up -d
   ```

4. **验证服务运行**

   访问 http://服务器IP:8701/api/docs/ 查看API文档

## 环境变量配置

系统使用`.env`文件加载环境变量。主要配置项包括：

```
# 环境设置 (development/production)
FLASK_ENV=development

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mt_zt
DB_USER=mt_zt 
DB_PASSWORD=your_password_here

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8701
DEBUG=True  # 仅在开发环境生效

# API令牌配置
TOKEN_ENABLED=True
API_TOKEN=api_token_2025
TOKEN_HEADER=token
TOKEN_QUERY_PARAM=token
TOKEN_LIFETIME=7776000  # 令牌有效期(秒)，默认3个月
TOKEN_EXCLUDE_PATHS=/api/health,/api/docs,/api/swagger.json,/api/auth/validate

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```


## 服务管理

```bash
# 启动服务
./scripts/start.sh

# 重启服务
./scripts/restart.sh

# 停止服务
pkill -f "gunicorn.*run:app"
```

## 数据库初始化

系统启动时会自动检查并创建必要的数据库表。如果需要手动初始化数据库：

```bash
# 进入项目目录
cd /opt/mdtj_api

# 激活虚拟环境
source mdtj_env/bin/activate

# 运行数据库初始化命令
python -c "from app.models import database; database.create_tables_if_not_exist(); database.insert_test_data()"
```

## API测试

系统提供了改进的测试脚本用于验证API接口功能：

```bash
# 激活虚拟环境
source mdtj_env/bin/activate

# 运行全部测试
python test_api.py

# 运行特定测试
python test_api.py --test=health,identity

```

测试脚本会检查所有主要接口，并提供详细的测试结果和错误信息。

## 跨域支持

系统内置了跨域支持，开箱即用，无需额外配置。API支持以下跨域功能：

- 允许所有源访问
- 支持凭证请求
- 支持多种HTTP方法
- 自动处理OPTIONS预检请求

## 故障排除

如遇到问题，请检查：

1. 数据库连接是否正常
2. 端口是否被占用
3. 日志文件中的错误信息（`logs/app.log`）
4. 环境变量配置是否正确

如需重启服务，可使用：

```bash
# 源码部署
./scripts/restart.sh

# Docker部署
cd docker
docker-compose restart api
```