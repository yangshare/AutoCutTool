# 项目概览（AutoCutTool / capcut-api）

## 目的
- 视频自动剪辑工具，提供 Python 后端 API 与 Electron+React 桌面端

## 技术栈
- 后端：Python 3.10+，FastAPI + Uvicorn
- 前端/桌面：Electron + React + TypeScript + Vite（rolldown-vite）+ Tailwind

## 目录结构（粗略）
- `backend/`：后端与核心业务
  - 入口：`python -m api.server`（默认 9001）
  - Python 包：`api/`、`config/`、`domain/`、`infra/`、`services/`
- `desktop/`：桌面端
  - 入口：`pnpm dev`（Vite 本地 5173，Electron 由插件驱动）
- `logs/`：日志输出
