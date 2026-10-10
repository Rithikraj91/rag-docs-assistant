import os
import warnings
warnings.filterwarnings("ignore")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(
    title="RAG DevOps Documentation Assistant",
    version="1.0.0"
)

# Request schema
class QueryRequest(BaseModel):
    question: str

# Response schema
class QueryResponse(BaseModel):
    question: str
    answer: str
    context: str

# Global embedding function and Chroma connection
embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_func)

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

Question: {question}

Provide a direct answer and reference the document source details.
"""

@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "rag-docs-assistant"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured on the server.")

    # 1. Similarity Search
    results = db.similarity_search(payload.question, k=2)
    context_text = "\n---\n".join([doc.page_content for doc in results])

    # 2. Format Prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=payload.question)

    # 3. Invoke LLM
    try:
        llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0)
        response = llm.invoke(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM Error: {str(e)}")

    return QueryResponse(
        question=payload.question,
        answer=response.content,
        context=context_text
    )
