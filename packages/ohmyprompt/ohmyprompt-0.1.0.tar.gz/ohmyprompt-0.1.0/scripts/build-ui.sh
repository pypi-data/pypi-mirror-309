#!/bin/bash

# 确保脚本在任何错误时退出
set -e

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# UI 源码目录
UI_DIR="$PROJECT_ROOT/ui"

# FastAPI 静态文件目录
STATIC_DIR="$PROJECT_ROOT/src/ohmyprompt/web/static"
DIST_DIR="$STATIC_DIR/dist"

echo "=== 开始构建前端 ==="

# 进入 UI 目录
cd "$UI_DIR"

# 安装依赖
echo "正在安装依赖..."
npm install

# 构建项目
echo "正在构建项目..."
npm run build

echo "=== 前端构建完成 ==="
echo "静态文件已生成到: $DIST_DIR" 