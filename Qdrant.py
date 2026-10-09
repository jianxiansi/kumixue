from uuid import uuid4
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient,models
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="qwen3-embedding:8b ",)

try:
    client = QdrantClient(path="./qdrant_data")
    client.create_collection(
        collection_name="demo",
        vectors_config={"size": 4096, "distance": "Cosine"},
    )
except:
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="demo",
        embedding=embeddings,
    )
    docs = [
        Document(page_content="LangGraph 是构建有状态 Agent 的最佳框架", metadata={"source": "note"}),
        Document(page_content="退换货政策第3条：7天内可无理由退货", metadata={"source": "faq"}),
    ]

    vector_store.add_documents(documents=docs, ids=[str(uuid4()), str(uuid4())])
    found = vector_store.similarity_search("agent", k=2)
    print(found)
    all = client.scroll(collection_name="demo")
    print(all)

finally:
    client.close()
print(len(embeddings.embed_query("测试")))

