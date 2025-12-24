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

### 代码规范 (Code Style)
*   **Python**:
    *   遵循 **PEP 8** 规范。
    *   推荐使用 `ruff` 进行 Lint 和格式化。
    *   类型注解：所有公共函数和类方法必须包含 Type Hints。
*   **TypeScript/Frontend**:
    *   遵循 `ESLint` + `Prettier` 规则。
    *   组件命名：PascalCase (e.g., `MyComponent.tsx`)。
    *   函数/变量命名：camelCase。

### 测试策略 (Testing)
*   **后端**:
    *   `domain/` 层必须包含单元测试。
    *   使用 `pytest` 作为测试框架。
*   **前端**:
    *   工具函数 (`lib/utils.ts`) 需包含单元测试。

### Git 提交规范
*   遵循 **Conventional Commits**：
    *   `feat`: 新功能
    *   `fix`: 修复 Bug
    *   `docs`: 文档变更
    *   `style`: 代码格式调整（不影响逻辑）
    *   `refactor`: 代码重构
    *   `chore`: 构建/工具链变动
