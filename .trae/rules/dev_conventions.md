---
alwaysApply: false
description: 开发约定与协作规范（按需参考）
---
### 协作约定
*   **前后端分离**：UI 放 `desktop/`，复杂处理走 `backend/` API
*   **依赖管理**：后端用 `pip`（基于 `backend/pyproject.toml`），前端只用 `pnpm`
*   **锁文件**：只保留 `desktop/pnpm-lock.yaml`；发现 `package-lock.json`/`yarn.lock` 删除

### 端口与地址
*   后端：`http://localhost:9001/`（Docs：`/docs`）
*   前端：`http://localhost:5173/`

