import streamlit as st
import ollama

# 导入ollama客户端
client=ollama.Client(host="http://localhost:11434")

if "message" not in st.session_state:
    st.session_state["message"]=[]
st.title("剑仙")
st.write("交谈")
st.divider()

# 输出历史对话
for message in st.session_state["message"]:
     st.chat_message(message["role"]).markdown(message["content"])

# 用户输入记录后并马上输出对话
prompt=st.chat_input("请输入......")
if prompt:
    st.session_state["message"].append({"role":"user","content":prompt})
    st.chat_message("user").markdown(prompt)

    #导入参数等待模型思考
    with st.spinner("剑仙凝神思索..."):
        response=client.chat(
            model="deepseek-r1:7b",
            messages=[{"role":"user","content":prompt}]
        )

        # 模型思考后记录并输出对话
        st.session_state["message"].append({"role": "assistant", "content": response["message"]["content"]})
        st.chat_message(response["message"]["role"]).markdown(response["message"]["content"])













