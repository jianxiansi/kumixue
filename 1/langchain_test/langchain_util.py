from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_community. llms import Tongyi

# 记忆对象
memory=ConversationBufferMemory(return_message=True)

#usage
def get_response(prompt,api_key):
    model=Tongyi(model="qwen-max",api_key=api_key)
    chain=ConversationChain(llm=model,memory=memory)

    #发送请求
    response=chain.invoke({"input":prompt})
    return response["response"]

if __name__ =="__main__":
    print(get_response("请用python输出1-10",))
