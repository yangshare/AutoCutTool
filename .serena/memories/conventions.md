# 代码风格与约定（当前仓库观察）

## 后端（Python）
- 包结构按领域/分层组织：`api/`、`services/`、`domain/`、`infra/`
- `backend/.flake8` 存在，推断项目倾向使用 flake8 进行基础风格检查（max-line-length=140，忽略若干规则）
- 依赖通过 `backend/pyproject.toml` 的 `[project].dependencies` 管理，安装方式为 `pip install -e .`

## 前端（desktop）
- 使用 TypeScript + React
- 依赖管理强制 `pnpm`（`desktop/package.json` 的 `packageManager` 指定）
- 构建脚本 `pnpm build` 会运行 `tsc -b` 再 `vite build` 并 `electron-builder`
