from src.Core.utils import (
    tool, chromadb
)




# Define tools for FAQ agent

# Use the EXACT SAME path as the first file
DB_PATH = "src/RAG/Database/chroma_db"

# Initialize the persistent client, pointing to the existing database
client = chromadb.PersistentClient(path=DB_PATH)
# Get the existing collection by its name
collection = client.get_collection(name="Database")

@tool
def FAQ_insurance_tool(query: str) -> str:
    """
    (MOCK) Searches an FAQ and glossary knowledge base using a simulated RAG process.

    This function simulates retrieving a definition from a curated database. It scores
    documents based on keyword overlap with the user's query.

    Args:
        query: A query string, typically asking for a definition.

    Returns:
        A single string containing the content of the most relevant document,
        or an empty string if no relevant definition is found.
    """
    print(f"--- Running Tool: FAQ_insurance_tool ---")

    # Query the collection to prove the data is there
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results['metadatas']