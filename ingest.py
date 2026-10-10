import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def run_ingestion():
    print("1. Loading document...")
    loader = TextLoader("sample_docs.txt")
    docs = loader.load()

    print("2. Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")

    print("3. Embedding text and storing in ChromaDB...")
    embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = Chroma.from_documents(
        documents=splits,
        embedding=embedding_func,
        persist_directory="./chroma_db"
    )
    print("Ingestion complete. Database saved to ./chroma_db")

if __name__ == "__main__":
    run_ingestion()
