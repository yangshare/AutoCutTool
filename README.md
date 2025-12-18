# AutoCutTool

视频自动剪辑工具，支持 API 调用和本地桌面应用。

## 📁 目录结构

*   **backend/**: Python 后端服务
    *   核心剪辑逻辑 (Draft, FFmpeg)
    *   FastAPI 接口服务
*   **desktop/**: Electron + React 桌面客户端
    *   用户交互界面
    *   本地文件管理

## 🚀 快速开始

### 1. 启动后端 (Python)

确保已安装 Python 3.10+。

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境 (可选)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖（基于 pyproject.toml）
pip install -e .

# 启动服务 (默认端口 9001)
python -m api.server
```

### 2. 启动前端 (Desktop)

确保已安装 Node.js 18+ 和 pnpm。

```bash
# 进入桌面端目录
cd desktop

# 安装依赖（仅使用 pnpm）
pnpm install

# 启动开发模式
pnpm dev
```

启动后，桌面应用将自动打开，前端预览地址为 `http://localhost:5173/`。

> 注意：前端 `desktop/` 目录只使用 pnpm 管理依赖。
> 请不要在该目录执行 `npm install` 或 `yarn install`，避免锁文件和依赖树冲突。

## 🛠️ 开发指南

*   **后端开发**: 修改 `backend/` 下的代码。API 文档位于 `http://localhost:9001/docs`。
*   **前端开发**: 修改 `desktop/` 下的代码。支持热重载。

## 📦 构建发布

```bash
cd desktop
pnpm build
```
构建产物将位于 `desktop/dist` 和 `desktop/release` 目录。
