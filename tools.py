# from langchain_core.tools import tool
# from typing import List, Dict, Optional
# import pandas as pd 
# # Try to extract JSON from response
# import json
# import re
# from difflib import get_close_matches
# import chromadb
# import google.generativeai as genai
# import os
# from typing import Optional, List, Dict
# from langchain_core.tools import tool
# import chromadb
from PIL import Image
# import base64
# import io

from Agents.utils import (
    tool, List, Dict, Optional, pd, chromadb, Image, base64, 
    io, re, json, get_close_matches, genai, 
)


# Configure the library with your API key
genai.configure(api_key="AIzaSyB3JsYuzVmJee4rmktxiGmYmv-AMvnguTI")


# Use the EXACT SAME path as the first file
DB_PATH = "C:/Users/Raja/Desktop/hackathon-demo/chroma_db"

DB_PATH_DOCTORS = "C:/Users/Raja/Desktop/hackathon-demo/chroma_db_doctors"

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
# --- 2. Tool Definition ---
def get_insurance_plan_details(
    county: str,
    zip_code: str,
    plan_name: Optional[str] = None,
    metal_level: Optional[str] = None
) -> List[Dict]:
    """
    Retrieves detailed financial information about insurance plans from the database
    based on the user's location and other optional filters.

    Args:
        county: The user's county of residence.
        zip_code: The user's 5-digit zip code.
        plan_name: An optional keyword from the plan's marketing name.
        metal_level: The plan's metal tier (e.g., "Bronze", "Silver").

    Returns:
        A list of dictionaries, where each dictionary represents a matching insurance plan.
    """

    data = {
    'County': ['Miami-Dade', 'Miami-Dade', 'Broward', 'Palm Beach'],
    'Zip': ['33178', '33178', '33301', '33411'],
    'Plan ID': ['78606FL0420010', '78606FL0420012', '12345FL0123456', '54321FL6543210'],
    'Issuer Name': ['Blue Cross', 'Aetna', 'Sunshine Health', 'Blue Cross'],
    'Plan Marketing Name': ['BlueCare Silver PPO 2500', 'Aetna Silver HMO', 'Sunshine Gold HMO', 'BlueCare Gold PPO 1000'],
    'Metal Level': ['Silver', 'Silver', 'Gold', 'Gold'],
    'Plan Type': ['PPO', 'HMO', 'HMO', 'PPO'],
    'Medical Deductible Individual': [5000.00, 5500.00, 2000.00, 1000.00],
    'Medical Deductible Family': [10000.00, 11000.00, 4000.00, 2000.00],
    'Coinsurance Rate': [0.20, 0.30, 0.15, 0.10],
    'Medical OOP Max Individual': [8000.00, 8500.00, 4500.00, 3000.00],
    'Medical OOP Max Family': [16000.00, 17000.00, 9000.00, 6000.00],
    'Summary of Benefits URL': ['http://bc.com/sbc1.pdf', 'http://aetna.com/sbc2.pdf', 'http://sun.com/sbc3.pdf', 'http://bc.com/sbc4.pdf'],
    'Network URL': ['http://bc.com/net1', 'http://aetna.com/net2', 'http://sun.com/net3', 'http://bc.com/net4']
    }
    insurance_df = pd.DataFrame(data)
    # Start with a copy of the full dataframe
    results_df = insurance_df.copy()

    # Apply required filters (case-insensitive for county)
    results_df = results_df[
        (results_df['County'].str.lower() == county.lower()) &
        (results_df['Zip'] == zip_code)
    ]

    # Apply optional filters if they are provided
    if plan_name:
        results_df = results_df[results_df['Plan Marketing Name'].str.contains(plan_name, case=False)]

    if metal_level:
        results_df = results_df[results_df['Metal Level'].str.lower() == metal_level.lower()]

    # Format the filtered results into the specified JSON structure
    output_plans = []
    for _, row in results_df.iterrows():
        plan_details = {
            "plan_id": row['Plan ID'],
            "issuer_name": row['Issuer Name'],
            "plan_marketing_name": row['Plan Marketing Name'],
            "metal_level": row['Metal Level'],
            "plan_type": row['Plan Type'],
            "financials": {
                "medical_deductible_individual": row['Medical Deductible Individual'],
                "medical_deductible_family": row['Medical Deductible Family'],
                "coinsurance_rate": row['Coinsurance Rate'],
                "medical_oop_max_individual": row['Medical OOP Max Individual'],
                "medical_oop_max_family": row['Medical OOP Max Family']
            },
            "urls": {
                "summary_of_benefits": row['Summary of Benefits URL'],
                "network_url": row['Network URL']
            }
        }
        output_plans.append(plan_details)

    return output_plans



    # Initialize Gemini model (using Flash for faster, cheaper responses)
    #gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')  # or 'gemini-1.5-pro' for better accuracy



@tool
def find_medical_specialty(
    condition_description: Optional[str] = None,
    image_path: Optional[str] = None
) -> Dict[str, str]:
    """
    Uses Gemini AI to analyze a medical condition (from text and/or image) and suggest 
    the most appropriate medical specialty from the available list.
    
    Args:
        condition_description: Text description of the medical condition (optional)
        image_path: Path to an image of the condition (optional)
        
    Returns:
        Dictionary with:
        - specialty: The recommended medical specialty
    """
    # List of available medical specialties in your database
    AVAILABLE_SPECIALTIES = [
        "Cardiology",
        "Dermatology", 
        "Endocrinology",
        "Gastroenterology",
        "General Practice",
        "Gynecology",
        "Hematology",
        "Infectious Disease",
        "Internal Medicine",
        "Nephrology",
        "Neurology",
        "Obstetrics",
        "Oncology",
        "Ophthalmology",
        "Orthopedics",
        "Otolaryngology (ENT)",
        "Pediatrics",
        "Psychiatry",
        "Pulmonology",
        "Radiology",
        "Rheumatology",
        "Surgery",
        "Urology",
        "Emergency Medicine",
        "Family Medicine",
        "Sports Medicine",
        "Pain Management",
        "Allergy & Immunology",
        "Plastic Surgery",
        "Podiatry"
    ]

    gemini_model = genai.GenerativeModel('gemini-2.5-pro')

    if not condition_description and not image_path:
        return {
            "specialty": "",
            "confidence": "none",
            "reasoning": "No condition description or image provided",
            "disclaimer": "Please provide either a description of your condition or an image."
        }
    
    try:
        # Construct the prompt for Gemini
        prompt_parts = []
        
        # System prompt with available specialties
        system_prompt = f"""You are a medical specialty classifier. Your task is to analyze the provided medical condition 
        and suggest the MOST appropriate medical specialty from this exact list:
        
        {', '.join(AVAILABLE_SPECIALTIES)}
        
        Instructions:
        1. Analyze the condition description and/or image carefully
        2. Select ONLY ONE specialty from the list above that best matches
        
        Output format (JSON):
        {{
            "specialty": "<exact specialty name from list>"
        }}
        """
        
        prompt_parts.append(system_prompt)
        
        # Add condition description if provided
        if condition_description:
            prompt_parts.append(f"\nCondition Description: {condition_description}")
        
        # Process image if provided
        if image_path:
            try:
                # Open and prepare the image
                img = Image.open(image_path)
                
                # Convert to RGB if necessary (handles RGBA, etc.)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if image is too large (Gemini has limits)
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert to base64 for Gemini
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Add image context to prompt
                prompt_parts.append("\nAn image of the condition has been provided for analysis.")
                
                # Create the message with both text and image
                response = gemini_model.generate_content([
                    ' '.join(prompt_parts),
                    Image.open(image_path)  # Gemini SDK handles the image directly
                ])
            except Exception as e:
                print(f"Error processing image: {e}")
                # Fall back to text-only analysis
                response = gemini_model.generate_content(' '.join(prompt_parts))
        else:
            # Text-only analysis
            response = gemini_model.generate_content(' '.join(prompt_parts))
        
        # Parse the response
        response_text = response.text.strip()
        
        # Find JSON in response (in case there's extra text)
        json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                
                # Validate that the specialty is in our list
                if result.get('specialty') not in AVAILABLE_SPECIALTIES:
                    # Find closest match
                    close_matches = get_close_matches(
                        result.get('specialty', ''), 
                        AVAILABLE_SPECIALTIES, 
                        n=1, 
                        cutoff=0.6
                    )
                    if close_matches:
                        result['specialty'] = close_matches[0]
                    else:
                        result['specialty'] = "General Practice"
                
                return {
                    "specialty": result.get('specialty', 'General Practice')
                }
            except json.JSONDecodeError:
                pass
        
        # Fallback if JSON parsing fails - use simple keyword matching with Gemini's response
        response_lower = response_text.lower()
        for specialty in AVAILABLE_SPECIALTIES:
            if specialty.lower() in response_lower:
                return {
                    "specialty": specialty
                }
        
        # Default fallback
        return {
            "specialty": "General Practice"
        }
        
    except Exception as e:
        print(f"Error in specialty finder: {e}")
        return {
            "specialty": "General Practice"
        }


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
    client_doctor = chromadb.PersistentClient(path=DB_PATH_DOCTORS)
    
    # Get the existing collection
    collection_doctors = client_doctor.get_collection(name="Doctors_Database")
    
    # Create search query
    query = f"{specialty} {county_name} {state}"
    
    # Query the collection
    results = collection_doctors.query(
        query_texts=[query],
        n_results=5  # Get top 5 matches
    )
    
    # Format the results
    doctors = results['metadatas']
    return doctors