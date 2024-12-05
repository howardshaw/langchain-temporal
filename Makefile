.PHONY: help install run-local run-docker clean stop logs test

# 默认显示帮助信息
help:
	@echo "可用的命令："
	@echo "make install        - 安装项目依赖"
	@echo "make build          - 编译docker镜像"
	@echo "make run-server     - 本地运行服务"
	@echo "make run-worker     - 本地运行worker"
	@echo "make run-base       - 本地运行环境"
	@echo "make run-docker    - 使用 Docker 运行服务"
	@echo "make stop          - 停止 Docker 服务"
	@echo "make clean         - 清理临时文件和 Docker 资源"
	@echo "make logs          - 查看 Docker 容器日志"
	@echo "make test          - 运行测试"

# 安装依赖
install:
	pip install -r requirements.txt

# 编译docker镜像
build:
	docker build -t langchain-temporal .

# 本地运行
run-server:
	@echo "启动本地服务..."
	python server.py

run-worker:
	@echo "启动本地worker..."
	python worker.py 

run-base:
	@echo "启动本地环境..."
	docker compose -f docker-compose-base.yml up -d

# Docker 相关命令
run-docker:
	@echo "构建并启动 Docker 服务..."
	docker compose up --build -d
	@echo "Docker 服务已启动"

stop:
	@echo "停止 Docker 服务..."
	docker compose down
	@echo "Docker 服务已停止"

clean:
	@echo "清理资源..."
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	@echo "清理完成"

logs:
	docker compose logs -f

# 测试命令
test:
	pytest tests/

# 开发环境设置
dev-setup: install
	pre-commit install

# 检查代码风格
lint:
	flake8 .
	black --check .
	isort --check-only .

# 格式化代码
format:
	black .
	isort .

# 构建 Docker 镜像
build:
	docker compose build

# 重启服务
restart: stop run-docker

# 查看服务状态
status:
	docker compose ps

# 进入容器shell
shell-server:
	docker compose exec server /bin/bash

shell-worker:
	docker compose exec worker /bin/bash

# 显示容器日志
logs-server:
	docker compose logs -f server

logs-worker:
	docker compose logs -f worker

logs-temporal:
	docker compose logs -f temporal

logs-redis:
	docker compose logs -f redis 
