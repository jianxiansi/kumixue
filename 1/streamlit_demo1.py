import streamlit as st
from langchain_test.langchain_util import get_response as res
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv("DASHSCOPE_API_KEY")

st.title("剑仙")
st.write("开始对话吧！")
st.divider()
if "message" not in st.session_state:
    st.session_state["message"]=[]
for message in st.session_state["message"]:
    st.chat_message(message["role"]).markdown(message["content"])
# 用户输入记录后并马上输出对话
prompt=st.chat_input("请输入......")
if prompt:
    with st.spinner("思考中..."):
        st.chat_message("user").markdown(prompt)
        st.session_state["message"].append({"role":"user","content":prompt})
        st.chat_message("assistant").markdown(res(prompt,api_key))
        st.session_state["message"].append({"role": "assistant", "content":res})












