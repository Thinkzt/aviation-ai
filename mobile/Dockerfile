FROM python:3.11-slim

WORKDIR /app

# 安装Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装前端依赖并构建
RUN npm install && npm run build

# 暴露端口
EXPOSE 5174

# 启动命令
CMD ["python", "server.py"]
