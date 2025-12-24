# 建议命令（Windows / PowerShell）

## 后端（Python）
- 安装依赖（可选创建虚拟环境）：
  - `cd backend`
  - `python -m venv venv`
  - `.\venv\Scripts\python -m pip install -U pip`
  - `.\venv\Scripts\pip install -e .`
- 启动服务：
  - `cd backend`
  - `.\venv\Scripts\python -m api.server`
- 访问：
  - API 文档：`http://localhost:9001/docs`

## 桌面端（Electron + React）
- 安装依赖：
  - `cd desktop`
  - `pnpm install`
- 启动开发模式：
  - `cd desktop`
  - `pnpm dev`
- 访问：
  - Vite：`http://localhost:5173/`

## 可选校验
- 后端静态检查（如已安装 flake8）：`cd backend; .\venv\Scripts\python -m flake8`
- 前端构建校验：`cd desktop; pnpm build`
