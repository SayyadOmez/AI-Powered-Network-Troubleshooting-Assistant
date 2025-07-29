from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import SystemMessage, HumanMessage

# ─── Load and Embed Documentation ─── #
loader = TextLoader("sample_docs/network_docs.txt")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever()

# ─── Configure LLM ─── #
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# ─── RAG-based Initial Log Analysis ─── #
def analyze_with_rag(log_data):
    context = (
        "You are a network troubleshooting assistant. "
        "A network engineer is pasting logs, and you must diagnose the issue based on them. "
        "Return problem summary, likely cause, and suggested fix."
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    query = f"{context}\nLogs:\n{log_data}"
    output = chain.invoke({"query": query})  # ✅ FIXED: use invoke

    response = output["result"]
    docs_used = "\n\n".join([doc.page_content[:500] for doc in output["source_documents"][:2]])
    category = detect_error_category(log_data)
    return response, docs_used, category

# ─── Handle Follow-up Q&A ─── #
def handle_follow_up(log_data, initial_response, follow_up_question):
    messages = [
        SystemMessage(content="You're a helpful assistant aiding in network log analysis."),
        HumanMessage(content=f"Initial diagnosis:\n{initial_response}"),
        HumanMessage(content=f"Logs:\n{log_data}"),
        HumanMessage(content=f"Follow-up question: {follow_up_question}")
    ]
    reply = llm(messages)
    return reply.content

# ─── Simple Heuristic Categorization ─── #
def detect_error_category(log_data):
    log_data = log_data.lower()
    if "timeout" in log_data or "dropped" in log_data:
        return "Packet Loss"
    elif "cannot resolve" in log_data or "dns" in log_data:
        return "DNS Resolution Issue"
    elif "latency" in log_data or "time=" in log_data:
        return "High Latency"
    elif "connection refused" in log_data or "filtered" in log_data:
        return "Firewall Block"
    else:
        return "General Network Error"
