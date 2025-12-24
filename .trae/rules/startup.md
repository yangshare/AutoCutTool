---
alwaysApply: false
description: 启动项目（强约束：环境与命令）
---
### 启动与依赖（必须遵守）
*   **后端**：仅用 `backend/.venv/`（禁 `backend/venv/`）；安装 `cd backend` → `python -m venv .venv` → `.\.venv\Scripts\python -m pip install -U pip` → `.\.venv\Scripts\pip install -e .`；启动 `.\.venv\Scripts\python -m api.server`（9001）；`http://localhost:9001/docs`。
*   **前端**：仅用 `pnpm`（禁 `desktop/` 下 `npm/yarn`，仅保留 `pnpm-lock.yaml`）；启动 `cd desktop` → `pnpm install` → `pnpm dev`；`http://localhost:5173/`。

