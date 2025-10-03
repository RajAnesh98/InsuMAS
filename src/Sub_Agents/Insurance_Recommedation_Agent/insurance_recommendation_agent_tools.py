from src.Core.utils import (
    tool, chromadb
)


# Use the EXACT SAME path as the first file
DB_PATH = "src/RAG/Database/chroma_db"

# Initialize the persistent client, pointing to the existing database
client = chromadb.PersistentClient(path=DB_PATH)
# Get the existing collection by its name
collection = client.get_collection(name="Database")


# Define insurance recommendation tool
@tool
def query_insurance_recommendation_tool(query: str) -> str:
    """
    (MOCK) Searches an insurance knowledge base using a simulated RAG retrieval process.

    This function simulates a real RAG system's 'retrieval' step. It scores documents
    in a knowledge base based on keyword overlap with the user's query and returns the
    most relevant ones. A real implementation would use vector embeddings and a vector
    database for more accurate semantic search.

    Args:
        query: A detailed query string, ideally containing the user's question,
               age, state, and county.

    Returns:
        A single string containing the content of the top-k most relevant documents,
        or an empty string if no relevant documents are found.
    """
    print(f"--- Running Tool: query_insurance_recommendation_tool ---")

    # Query the collection to prove the data is there
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results['metadatas']
