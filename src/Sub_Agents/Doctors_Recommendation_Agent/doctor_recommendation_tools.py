from src.Core.utils import (
    tool, Dict, chromadb 
)

DB_PATH_DOCTORS = "src/RAG/Database/chroma_db_doctors"



@tool
def search_doctor_database(
    specialty: str, 
    county_name: str, 
    state: str
) -> Dict:
    """
    Searches the local doctor database for matching doctors.
    
    Args:
        specialty: The medical specialty to search for
        county_name: The county to filter by
        state: The state to filter by
        
    Returns:
        Dictionary containing:
        - doctors: List of matching doctor records
    """
    # Initialize the persistent client

    print('--- Running Tool: search_doctor_database ---')
    client_doctor = chromadb.PersistentClient(path=DB_PATH_DOCTORS)
    
    # Get the existing collection
    collection_doctors = client_doctor.get_collection(name="Doctors_Database")
    
    # Create search query
    query = f"{specialty} {county_name} {state}"
    
    # Query the collection
    results = collection_doctors.query(
        query_texts=[query],
        n_results=3  # Get top 5 matches
    )

    return results['metadatas']