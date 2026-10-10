from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore
from langchain_ollama.embeddings import OllamaEmbeddings
from qdrant_client import QdrantClient, models
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 全局
embedding = OllamaEmbeddings(model="qwen3-embedding:8b")
client = QdrantClient(path="./qdrant_data")
COLLECTION_NAME = "demo"

# 载入数据
loader = TextLoader(r"D:\Downloads\Q&A.md", encoding="utf-8")
docs = loader.load()
if not docs:
    print("未检测到文件，请检查文件路径是否正确")
    exit()
# 分割数据
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 修正：collection_exists 判断集合是否存在
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=4096, distance=models.Distance.COSINE)
    )
vectorstore = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embedding
)
vectorstore.add_documents(chunks)
"""for doc, score in vectorstore.similarity_search_with_relevance_scores("介绍rag", k=2):
    print(score, doc.page_content)"""
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

load_dotenv()
model = init_chat_model(
    model="qwen3.7-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

prompt = ChatPromptTemplate.from_template(
    """你是知识库助手。只依据资料回答，资料没有的就说'资料中未找到'，不要编造资料
    问题：{question}
    资料：{context}"""
)

question = "RAG 的全称是什么，主要解决大模型哪些问题？"
hits = retriever.invoke(question)
context = "\n\n".join(d.page_content for d in hits)
res = model.invoke(prompt.format_messages(context=context, question=question)).content
print(res)




