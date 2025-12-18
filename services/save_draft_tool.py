import requests
import json
import os
import shutil
import sys

# 添加当前目录到 sys.path 以便导入项目模块
sys.path.append(os.getcwd())

# 尝试导入项目中的模块
try:
    from save_draft_impl import download_script
    from settings.local import IS_CAPCUT_ENV
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保在项目根目录下运行此脚本。")
    sys.exit(1)

def save_draft_locally(draft_id, output_dir="output_drafts"):
    # 1. 获取草稿数据
    print(f"正在从服务获取草稿 {draft_id} 的数据...")
    try:
        response = requests.post("http://localhost:9001/query_script", json={
            "draft_id": draft_id
        })
        
        if response.status_code != 200:
            print(f"获取草稿失败: HTTP {response.status_code}")
            print(response.text)
            return

        result = response.json()
        if not result.get("success"):
            print(f"获取草稿失败: {result.get('error')}")
            return
            
        # output 是 JSON 字符串，需要再次解析
        script_json_str = result.get("output")
        script_data = json.loads(script_json_str)
        print("成功获取草稿数据。")

    except Exception as e:
        print(f"请求服务出错: {e}")
        return

    # 2. 准备输出目录
    abs_output_dir = os.path.abspath(output_dir)
    if not os.path.exists(abs_output_dir):
        os.makedirs(abs_output_dir)
    
    print(f"准备保存到: {abs_output_dir}")

    # 3. 调用项目内部的 download_script 函数
    # 注意：download_script 会自动处理模板复制和素材下载
    try:
        # download_script 的 draft_folder 参数是父目录，它会在里面创建 draft_id 子目录
        ret = download_script(draft_id, abs_output_dir, script_data)
        
        if ret.get("success"):
            draft_path = os.path.join(abs_output_dir, draft_id)
            print(f"\n✅ 草稿已成功保存！")
            print(f"📂 路径: {draft_path}")
            print("您可以使用剪映/CapCut打开此文件夹。")
        else:
            print(f"❌ 保存失败: {ret.get('error')}")

    except Exception as e:
        print(f"保存过程出错: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python save_draft_tool.py <draft_id>")
    else:
        save_draft_locally(sys.argv[1])
