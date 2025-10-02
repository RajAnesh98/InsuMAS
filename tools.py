from PIL import Image
from Agents.utils import (
    tool, List, Dict, Optional, pd, chromadb, Image, base64, 
    io, re, json, get_close_matches, genai, 
)


# Use the EXACT SAME path as the first file
DB_PATH = "RAG/chroma_db"

DB_PATH_DOCTORS = "RAG/chroma_db_doctors"

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



# Define tools for FAQ agent
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



@tool
def get_health_plan_details(state_code: str, county_name: str, plan_type: str, metal_level: str) -> dict:
    """
    Retrieves health plan details from the SHOP_Market_Medical.csv file.

    Args:
        state_code (str): The two-letter code for the state (e.g., 'WY').
        county_name (str): The name of the county (e.g., 'Weston').
        plan_type (str): The type of the plan (e.g., 'PPO').
        metal_level (str): The metal level of the plan (e.g., 'Gold').

    Returns:
        dict: A dictionary containing the financial details of the matching plan,
              or an error message if no plan is found.
    """
    try:
        # Load the dataset from the CSV file
        df = pd.read_csv(r'C:\Users\Raja\Desktop\SHOP_Market_Medical.xlsx')

        # Filter the DataFrame based on the user's input
        # We use .str.contains() with case=False to make the matching case-insensitive
        filtered_plan = df[
            (df['State Code'].str.strip().str.lower() == state_code.strip().lower()) &
            (df['County Name'].str.strip().str.lower() == county_name.strip().lower()) &
            (df['Plan Type'].str.strip().str.lower() == plan_type.strip().lower()) &
            (df['Metal Level'].str.strip().str.lower() == metal_level.strip().lower())
        ]

        if filtered_plan.empty:
            return {"error": "No matching health plan found for the provided details. Please check your input and try again."}

        # Select the first matching plan
        plan_details = filtered_plan.iloc[0]

        # Extract relevant financial information. Add more fields as needed.
        # The column names are taken from a standard health insurance dataset.
        # You may need to adjust these based on the exact columns in your file.
        result = {
            "Plan Marketing Name": plan_details.get("Plan Marketing Name", "N/A"),
            "Issuer Name": plan_details.get("Issuer Name", "N/A"),
            "Medical Deductible - Individual": plan_details.get("Medical Deductible - Individual - Standard", "N/A"),
            "Medical Deductible - Family": plan_details.get("Medical Deductible - Family - Standard", "N/A"),
            "Medical Maximum Out of Pocket - Individual": plan_details.get("Medical Maximum Out of Pocket - Individual - Standard", "N/A"),
            "Medical Maximum Out of Pocket - Family": plan_details.get("Medical Maximum Out of Pocket - Family - Standard", "N/A"),
            "Primary Care Physician - Office Visit": plan_details.get("Primary Care Physician - Office Visit - Standard", "N/A"),
            "Specialist - Office Visit": plan_details.get("Specialist - Office Visit - Standard", "N/A"),
            "Emergency Room Facility Fee": plan_details.get("Emergency Room Facility Fee - Standard", "N/A"),
            "Inpatient Hospital Services": plan_details.get("Inpatient Hospital Services - Standard", "N/A"),
        }

        return result

    except FileNotFoundError:
        return {"error": "The data file 'SHOP_Market_Medical.csv' was not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



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