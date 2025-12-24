# 任务完成后的建议检查

## 后端
- 若修改了后端 API/服务逻辑：
  - 启动验证：`.\venv\Scripts\python -m api.server`
  - 可选风格检查（如已安装）：`.\venv\Scripts\python -m flake8`

## 前端/桌面
- 若修改了 UI 或 Electron 相关代码：
  - 开发运行验证：`pnpm dev`
  - 构建验证：`pnpm build`（包含 `tsc -b`）

## 说明
- 仓库内未发现明确的测试命令/CI 约定（仅看到 `.pytest_cache` 忽略项），如后续补充测试框架可更新此文件。