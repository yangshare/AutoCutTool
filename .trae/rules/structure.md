---
alwaysApply: false
description: 项目结构与技术栈（按需参考）
---
### 目录结构
*   `backend/`：Python 后端与核心剪辑逻辑（FastAPI + Uvicorn）
*   `desktop/`：Electron + React + TypeScript 桌面端（Vite/rolldown-vite + Tailwind）
*   `logs/`：运行日志

### 关键入口
*   后端入口模块：`python -m api.server`
*   桌面端入口脚本：`desktop/package.json` 的 `pnpm dev`

