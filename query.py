import os
import sys
import warnings
warnings.filterwarnings("ignore")

from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def query_rag(question: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set. Run: export GROQ_API_KEY='your-key'")
        return

    # 1. Connect to Chroma vector store
    embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_func)

    # 2. Retrieve top-2 relevant document chunks
    results = db.similarity_search(question, k=2)
    context_text = "\n---\n".join([doc.page_content for doc in results])

    # 3. Formulate prompt
    prompt_template = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:

{context}

Question: {question}

Provide a direct answer and reference the document source details.
""")
    prompt = prompt_template.format(context=context_text, question=question)

    # 4. Generate answer using an active model on your account
    llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0)
    response = llm.invoke(prompt)

    print("\n=== AI ANSWER ===")
    print(response.content)
    print("\n=== RETRIEVED CONTEXT USED ===")
    print(context_text)

if __name__ == "__main__":
    query_text = sys.argv[1] if len(sys.argv) > 1 else "What do I do if error rates spike above 2%?"
    query_rag(query_text)
