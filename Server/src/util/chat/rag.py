import torch
from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, tool
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

load_dotenv()

reasoning_model_id = os.getenv("REASONING_MODEL_ID")
tool_model_id = os.getenv("TOOL_MODEL_ID")


def get_model(model_id):
    return OpenAIServerModel(
            model_id=model_id,
            api_base="http://localhost:11434/v1",
            api_key="ollama"
        )


# Create the reasoner for better RAG
reasoning_model = get_model(reasoning_model_id)
reasoner = CodeAgent(tools=[], model=reasoning_model, add_base_tools=False, max_steps=2)

# Initialize vector store and embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
)
# Replace Chroma with FAISS
db_dir = os.path.join(os.path.dirname(__file__), "faiss_db")
if os.path.exists(db_dir):
    # Load existing FAISS index if it exists
    vectordb = FAISS.load_local(db_dir, embeddings, allow_dangerous_deserialization=True)
else:
    # Create a new FAISS index
    vectordb = FAISS.from_texts(["Initialize with some text"], embeddings)
    vectordb.save_local(db_dir)  # Save the index to disk


@tool
def rag_with_reasoner(user_query: str) -> str:
    """
    This is a RAG tool that takes in a user query and searches for relevant content from the vector database.
    The result of the search is given to a reasoning LLM to generate a response, so what you'll get back
    from this tool is a short answer to the user's question based on RAG context.

    Args:
        user_query: The user's question to query the vector database with.
    """
    # Search for relevant documents
    docs = vectordb.similarity_search(user_query, k=3)

    # Combine document contents
    context = "\n\n".join(doc.page_content for doc in docs)

    # Create prompt with context
    prompt = f"""Based on the following context, answer the user's question concisely and specifically.
    If there isn't sufficient information, suggest a better query for RAG.
    Context:
    {context}

    Metadata:
    Retrieved from {len(docs)} documents.

    Question: {user_query}

    Answer:"""

    # Get response from reasoning model
    response = reasoner.run(prompt, reset=False)
    return response


# Create the primary agent to direct the conversation
tool_model = get_model(tool_model_id)
primary_agent = ToolCallingAgent(tools=[rag_with_reasoner], model=tool_model, add_base_tools=False, max_steps=3)


# Example prompt: Compare and contrast the services offered by RankBoost and Omni Marketing
def main():
    # Start the conversation
    response = primary_agent.run("what is liberalism?")
    print(response)


if __name__ == "__main__":
    main()