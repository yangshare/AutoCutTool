# 通过CapCutApi连接AI生成的一切

## 项目概览

**CapCutApi** 是一款强大的云端 剪辑 API，它赋予您对 AI 生成素材（包括图片、音频、视频和文字）的精确控制权。
它提供了精确的编辑能力来拼接原始的 AI 输出，例如给视频变速或将图片镜像反转。这种能力有效地解决了 AI 生成的结果缺乏精确控制，难以复制的问题，让您能够轻松地将创意想法转化为精致的视频。

### 核心优势

1. 通过API的方式，提供强大的剪辑能力

2. 可以在网页实时预览剪辑结果，无需下载，极大方便工作流开发。

3. 可以下载剪辑结果，并导入到剪映/CapCut中二次编辑。

4. 可以利用API将剪辑结果生成视频，实现全云端操作。


## 核心功能


| 功能模块 | API | MCP 协议 | 描述 |
|---------|----------|----------|------|
| **草稿管理** | ✅ | ✅ | 创建、保存剪映/CapCut草稿文件 |
| **视频处理** | ✅ | ✅ | 多格式视频导入、剪辑、转场、特效 |
| **音频编辑** | ✅ | ✅ | 音频轨道、音量控制、音效处理 |
| **图像处理** | ✅ | ✅ | 图片导入、动画、蒙版、滤镜 |
| **文本编辑** | ✅ | ✅ | 多样式文本、阴影、背景、动画 |
| **字幕系统** | ✅ | ✅ | SRT 字幕导入、样式设置、时间同步 |
| **特效引擎** | ✅ | ✅ | 视觉特效、滤镜、转场动画 |
| **贴纸系统** | ✅ | ✅ | 贴纸素材、位置控制、动画效果 |
| **关键帧** | ✅ | ✅ | 属性动画、时间轴控制、缓动函数 |
| **媒体分析** | ✅ | ✅ | 视频时长获取、格式检测 |

## 快速开始

### 1. 系统要求

- Python 3.10+
- 剪映
- FFmpeg

### 2. 安装部署

```bash
# 1. 克隆项目
git clone https://github.com/sun-guannan/CapCutApi.git
cd CapCutApi

# 2. 创建虚拟环境 (推荐)
python -m venv venv-capcut
source venv-capcut/bin/activate  # Linux/macOS
# 或 venv-capcut\Scripts\activate  # Windows

# 3. 安装依赖
pip install .           # 安装项目及基础依赖
# 或者安装开发模式
pip install -e .
# 如果需要 MCP 协议支持
pip install .[mcp]

# 4. 配置文件
# 系统支持 .env 文件(推荐)或环境变量配置
cp .env.example .env
# 根据需要编辑 .env 文件
```

### 3. 启动服务

```bash
python capcut_server.py # 启动HTTP API服务器, 默认端口: 9001
```


## 工作流说明
**“排版” -> “打印”**

CapCutApi 的核心设计理念是：先在服务器内存中完成所有剪辑操作的“排版”，最后一次性“打印”出草稿文件。

1.  **排版阶段（积累操作）**
    *   调用 `/add_video`、`/add_text`、`/add_audio` 等接口。
    *   每次调用都会返回一个 `draft_id`（如果是第一次调用，会新建一个；后续调用需带上这个 ID）。
    *   **注意**：此时所有的修改都只存在于服务器内存中，不会立即生成草稿文件。

2.  **打印阶段（生成交付）**
    *   调用 `/save_draft` 接口（传入之前的 `draft_id`）。
    *   这一步才会触发：
        *   下载所有素材。
        *   生成剪映专用的配置文件。
        *   在磁盘上创建最终的草稿文件夹（`dfd_` 开头）。

### 推荐调用顺序

1.  **创建草稿并添加第一个视频**：
    ```http
    POST /add_video
    { "video_url": "..." }
    -> 返回 "draft_id": "xxxxx"
    ```

2.  **继续添加素材**（务必带上 `draft_id`）：
    ```http
    POST /add_text
    { "draft_id": "xxxxx", "text": "字幕内容" }
    
    POST /add_audio
    { "draft_id": "xxxxx", "audio_url": "..." }
    ```

3.  **保存草稿**（生成最终文件）：
    ```http
    POST /save_draft
    { "draft_id": "xxxxx", "draft_folder": "..." }
    ```

## 使用示例

### 1. API 示例
添加视频素材

```python
import requests

# 添加背景视频
response = requests.post("http://localhost:9001/add_video", json={
    "video_url": "https://example.com/background.mp4",
    "start": 0,
    "end": 10
    "volume": 0.8,
    "transition": "fade_in"
})

print(f"视频添加结果: {response.json()}")
```

创建样式文本

```python
import requests

# 添加标题文字
response = requests.post("http://localhost:9001/add_text", json={
    "text": "欢迎使用 CapCutAPI",
    "start": 0,
    "end": 5,
    "font": "思源黑体",
    "font_color": "#FFD700",
    "font_size": 48,
    "shadow_enabled": True,
    "background_color": "#000000"
})

print(f"文本添加结果: {response.json()}")
```

可以在`example.py`文件中获取更多示例。


### 2. 下载草稿

调用 `save_draft` 会在`capcut_server.py`当前目录下生成一个 `dfd_` 开头的文件夹，将其复制到剪映/CapCut 草稿目录，即可在应用中看到生成的草稿。

## 模版
我们汇总了一些模版，放在`pattern`文件夹下。


