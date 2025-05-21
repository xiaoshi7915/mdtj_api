FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY run.py .
COPY app/ ./app/
COPY sql/ ./sql/

# 确保日志目录存在
RUN mkdir -p logs

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露API端口
EXPOSE 8701

# 设置环境变量
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# 启动应用
CMD ["gunicorn", "--bind", "0.0.0.0:8701", "--workers", "4", "--timeout", "120", "run:app"] 