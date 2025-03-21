import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, tool

# Load environment variables
load_dotenv()

# Get model IDs from environment variables
reasoning_model_id = os.getenv("REASONING_MODEL_ID")
tool_model_id = os.getenv("TOOL_MODEL_ID")

# Validate environment variables
if not reasoning_model_id or not tool_model_id:
    raise ValueError("Environment variables REASONING_MODEL_ID and TOOL_MODEL_ID must be set.")


# Function to get the model
def get_model(model_id):
    if not model_id:
        raise ValueError("model_id cannot be None or empty.")
    return OpenAIServerModel(
        model_id=model_id,
        api_base="http://localhost:11434/v1",
        api_key="ollama"
    )


# Initialize models
reasoning_model = get_model(reasoning_model_id)
tool_model = get_model(tool_model_id)

# Create the reasoner for better RAG
reasoner = CodeAgent(tools=[], model=reasoning_model, add_base_tools=False, max_steps=2)

# Initialize vector store and embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'}
)
db_dir = os.path.join(os.path.dirname(__file__), "faiss_db")
vectordb = FAISS.load_local(db_dir, embeddings, allow_dangerous_deserialization=True)


@tool
def rag_with_reasoner(user_query: str) -> str:
    """
    This is a RAG tool that takes in a user query and searches for relevant content from the vector database.
    The result of the search is given to a reasoning LLM to generate a response, so what you'll get back
    from this tool is a short answer to the user's question based on RAG context.

    Args:
        user_query: The user's question to query the vector database with.
    """
    # Validate the query
    if not user_query or not isinstance(user_query, str):
        return "Invalid query. Please provide a valid question."

    try:
        # Search for relevant documents
        docs = vectordb.similarity_search(user_query, k=3)

        # Combine document contents
        context = "\n\n".join(doc.page_content for doc in docs)

        # Create prompt with context
        prompt = f"""Based on the following context, answer the user's question. Be concise and specific.
        If there isn't sufficient information, give as your answer a better query to perform RAG with.

Context:
{context}

Question: {user_query}

Answer:"""

        # Get response from reasoning model
        response = reasoner.run(prompt, reset=False)
        return response
    except Exception as e:
        return f"An error occurred while processing the query: {str(e)}"


# Create the primary agent to direct the conversation
primary_agent = ToolCallingAgent(tools=[rag_with_reasoner], model=tool_model, add_base_tools=False, max_steps=3)

if __name__ == "__main__":
    primary_agent.run("What is the capital of France?")
