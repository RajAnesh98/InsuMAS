from src.Core.utils import (
    tool, pd
)


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
        df = pd.read_csv(r'src\RAG\Data\SHOP_Market_Medical.xlsx')

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