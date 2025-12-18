---
alwaysApply: false
description: 新增修改模块代码或者启动项目
---
### 1. 目录结构
*   **`backend/` (Python)**：
    *   存放所有核心业务逻辑与 API 代码。
    *   启动入口：`backend/api/server.py`。
    *   依赖管理：`pyproject.toml` 。
*   **`desktop/` (Electron + React)**：
    *   存放前端与桌面端代码。
    *   技术栈：React, TypeScript, Vite, Electron。
    *   包管理：统一使用 **Yarn**。

### 2. 启动命令
*   **后端**：进入 `backend/` 目录执行 `python -m api.server` (默认运行在 9001 端口)。
*   **前端**：进入 `desktop/` 目录执行 `yarn dev` (同时启动 Vite 和 Electron 窗口)。

### 3. 开发规范
*   **前后端分离**：前端负责 UI 交互，复杂逻辑（如视频处理）必须请求后端 API。
*   **依赖安装**：后端使用 `pip`，前端使用 `yarn`。