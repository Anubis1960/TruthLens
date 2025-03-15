from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
import shutil

load_dotenv()


def load_and_process_pdfs(data_dir: str):
    """Load PDFs from directory and split into chunks."""
    docs = []
    for doc_file in os.listdir(data_dir):
        file_path = Path(data_dir) / doc_file

        print(file_path)

        try:
            if doc_file.endswith(".pdf"):
                loader = PyPDFLoader(str(file_path))  # Ensure file_path is a string
            elif doc_file.endswith(".docx"):
                loader = Docx2txtLoader(str(file_path))
            elif doc_file.endswith(".txt") or doc_file.endswith(".md"):
                loader = TextLoader(str(file_path))
            else:
                print(f"Document type {doc_file} not supported.")
                continue

            docs.extend(loader.load())

        except Exception as e:
            print(f"Error loading document {doc_file}: {e}")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(docs)

    # Log the number of chunks created
    print(f"Created {len(chunks)} chunks from {len(docs)} documents.")
    return chunks


def create_vector_store(chunks, persist_directory: str):
    """Create and persist FAISS vector store."""
    # Clear existing vector store if it exists
    if os.path.exists(persist_directory):
        print(f"Clearing existing vector store at {persist_directory}")
        shutil.rmtree(persist_directory)

    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Generate embeddings for the first chunk to test
    if not chunks:
        raise ValueError("No chunks available to create embeddings.")

    try:
        sample_embedding = embeddings.embed_query(chunks[0].page_content)
        print(f"Sample embedding size: {len(sample_embedding)}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings: {e}")

    # Create and persist FAISS vector store
    print("Creating new vector store...")
    vectordb = FAISS.from_documents(chunks, embeddings)
    vectordb.save_local(persist_directory)
    return vectordb


def add_pdf_to_faiss(data_dir, persist_directory):
    # Step 1: Load and process PDFs
    print("Loading and processing PDFs...")
    chunks = load_and_process_pdfs(data_dir)

    # Step 3: Create and persist the FAISS vector store
    print("Adding chunks to FAISS vector store...")
    vectordb = create_vector_store(chunks, persist_directory)

    print(f"FAISS vector store created and saved at {persist_directory}")
    return vectordb


def main():
    pdf_dir = "./docs"
    persist_directory = "faiss_db"
    vectordb = add_pdf_to_faiss(pdf_dir, persist_directory)


if __name__ == "__main__":
    main()