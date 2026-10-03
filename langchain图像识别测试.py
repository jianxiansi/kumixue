import os,base64
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import tkinter as tk
from tkinter import filedialog

def image_b64():
    # 隐藏tk主窗口
    root = tk.Tk()
    root.withdraw()
    # 弹出文件选择框，只允许图片
    file_path = filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if not file_path:
        return None
    # 读取图片二进制
    with open(file_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_b64

base64_image = image_b64()

load_dotenv()
model = init_chat_model(
    model="qwen3.5-omni-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
agent = create_agent(model=model)
messages = HumanMessage(
    [
        {"type":"image","base64": base64_image, "mime_type": "image/png"},
        {"type":"text","text":"描述图片"}
    ]
)
try:
    for chunk, metadata in agent.stream({"messages": [messages]}, stream_mode="messages"):
        print(chunk.content,end="",flush=True)
except:
    print(model.invoke("你是"))