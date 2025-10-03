from src.Core.utils import (
    tool, chromadb 
)


# Use the EXACT SAME path as the first file
DB_PATH = "src/RAG/Database/chroma_db"


# Initialize the persistent client, pointing to the existing database
client = chromadb.PersistentClient(path=DB_PATH)
# Get the existing collection by its name
collection = client.get_collection(name="Database")



# Define insurance info tool
@tool
def get_insurance_info_tool(query: str) -> str:
    """
    (MOCK) Searches an insurance knowledge base using a simulated RAG retrieval process.

    This function simulates a RAG system's 'retrieval' step. It scores documents
    based on keyword overlap with the user's query and returns the most relevant ones.

    Args:
        query: A query string, typically the user's direct question.

    Returns:
        A single string containing the content of the top-k most relevant documents,
        or an empty string if no relevant documents are found.
    """
    print(f"--- Running Tool: get_insurance_info_tool ---")

    # Query the collection to prove the data is there
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results['metadatas']