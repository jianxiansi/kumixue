from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage, ToolMessage, SystemMessage, HumanMessage
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
import os

load_dotenv()

# 导入模型
model = init_chat_model(
    model="qwen3.7-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add]

# 定义工具
@tool
def add(a: float, b: float) -> float:
    """两数相加
    Args:
        a: 数字1
        b: 数字2
    """
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """两数相乘
    Args:
        a: 数字1
        b: 数字2
    """
    return a * b

@tool
def subtract(a: float, b: float) -> float:
    """两数相减
    Args:
        a: 被减数
        b: 减数
    """
    return a - b

@tool
def divide(a: float, b: float) -> float:
    """两数相除
    Args:
        a: 被除数
        b: 除数，不能为0
    """
    return a / b

tools = [add, multiply, subtract, divide]
tool_name = {tool.name:tool for tool in tools}
model_with_tools = model.bind_tools(tools)

# ====================定义节点与条件边====================
# 调用模型
def llm_call(state: State) -> State:
    print("=====LLM Call=====`")
    ai_mes=model_with_tools.invoke(state["messages"])
    return {"messages": [ai_mes]}

# 调用工具
def tool_node(state: State) -> State:
    print("=====Tool Node=====")
    result=[]
    last_msg = state["messages"][-1]
    for tool_call in last_msg.tool_calls:
        print(f"Tool call: {tool_call}")
        func = tool_name[tool_call["name"]]
        output = func.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(output), tool_call_id=tool_call["id"]))
    return {"messages": result}

# 条件边判定
def should_continue(state: State):
    print("=====Should Continue=====")
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tool_node"
    return END

# 连线建图
builder = StateGraph(State)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")
graph = builder.compile()

# 运行测试
if __name__ == "__main__":
    user_query = "计算 35148161684+441688-555614869*686168/51581657"
    res = graph.invoke({
        "messages": [
            SystemMessage(content="你是计算器助手。"),
            HumanMessage(content=user_query)
        ]
    })
    # 打印完整消息链
    print("=====完整消息历史=====")
    for msg in res["messages"]:
        print(f"\n【{type(msg).__name__}】: {msg.content}")
        # 额外打印工具调用信息，方便调试
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"====> tool_calls: {msg.tool_calls}")