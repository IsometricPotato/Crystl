import json
from .user_storage import load_user_data
from .user_storage import save_user_data
import pandas as pd
import argparse

# This function would contain your API calls for external data.
# For now, it just returns placeholder data.
def get_api_estimates(zipcode):
    """Placeholder for external API calls to get estimates."""
    return {
        "rent": "$1500",
        "taxes": "$3000",
        "utilities": "$200"
    }

def prepare_prompt_data():
    """
    Cleans, validates, and fills in missing user data.
    """
    # Define a default structure for the data
    processed_data = {
        "salary": "0",
        "zip_code": "15213", # Default for Pittsburgh
        "rent": "Not provided",
        "disability": "None",
        "food": "Not provided",
        "transportation": "Not provided",
        "medical": "Not provided",
        "utilities": "Not provided",
        "savings": "Not provided",
        "student_loans": "0",
        "debt": "Not provided",
        "taxes": "Not provided",
        "fun_money": "0"
    }

    user_data = load_user_data()
    # Overwrite defaults with user-provided data
    for key, value in user_data.items():
        if key in processed_data and value:
            processed_data[key] = value

    # Fill in missing data with API estimates
    # (or a default guess)
    api_estimates = get_api_estimates(processed_data["zip_code"])
    if processed_data["rent"] == "Not provided":
        processed_data["rent"] = api_estimates["rent"]
    if processed_data["taxes"] == "Not provided":
        processed_data["taxes"] = api_estimates["taxes"]
    if processed_data["utilities"] == "Not provided":
        processed_data["utilities"] = api_estimates["utilities"]

    save_user_data(user_data)

    return processed_data

def lookup_expense(csv_file: str, zip_code_name: str, zip_code: int, value: str):
    """
    Looks up a specific column value for a given ZIP code in a CSV file.

    Args:
        csv_file (str): Path to the CSV file
        zip_code (int or str): ZIP code to search
        column (str): Column name to retrieve

    Returns:
        str: The value if found, or a message if not
    """
    # Load CSV
    df = pd.read_csv(csv_file)

    # Check if ZIP column exists
    if zip_code_name not in df.columns:
        return "Error: Invalid zipcode name."

    # Check if target column exists
    if value not in df.columns:
        return f"Error: No '{value}' column in the file."

    # Check if ZIP is present
    matches = df.loc[df[zip_code_name] == int(zip_code), value]
    if matches.empty:
        return f"ZIP {zip_code} not found in the file."

    # Return the first match (in case multiple rows exist)
    return round(matches.iloc[0], 2)

def calculateIncomeTax(csv_file: str, zip_code: int, income: int):
    state_tax_rates = {
        "AL": 0.05,
        "AK": 0.00,
        "AZ": 0.025,
        "AR": 0.039,
        "CA": 0.133,
        "CO": 0.044,
        "CT": 0.0699,
        "DE": 0.066,
        "FL": 0.00,
        "GA": 0.0539,
        "HI": 0.11,
        "ID": 0.057,
        "IL": 0.0495,
        "IN": 0.03,
        "IA": 0.05,
        "KS": 0.0558,
        "KY": 0.04,
        "LA": 0.045,
        "ME": 0.0715,
        "MD": 0.0575,
        "MA": 0.05,
        "MI": 0.0425,
        "MN": 0.0985,
        "MS": 0.044,
        "MO": 0.047,
        "MT": 0.059,
        "NE": 0.052,
        "NV": 0.00,
        "NH": 0.00,   # no tax on earned income
        "NJ": 0.1075,
        "NM": 0.059,
        "NY": 0.109,
        "NC": 0.0425,
        "ND": 0.025,
        "OH": 0.035,
        "OK": 0.0475,
        "OR": 0.099,
        "PA": 0.0307,
        "RI": 0.0599,
        "SC": 0.062,
        "SD": 0.00,
        "TN": 0.00,   # no tax on earned income
        "TX": 0.00,
        "UT": 0.0455,
        "VT": 0.0875,
        "VA": 0.0575,
        "WA": 0.00,   # no income tax on wages
        "WV": 0.0482,
        "WI": 0.0765,
        "WY": 0.00,
    }

    fedTax = 0
    if income < 40000:
        fedTax = 0.10
    elif income < 100000:
        fedTax = 0.18
    elif income < 200000:
        fedTax - 0.22
    else:
        fedTax = 0.28


    df = pd.read_csv(csv_file)
    row = df.loc[df["ZIPCODE"] == int(zip_code), "STATE"]

    if row.empty:
        return {"error": f"ZIP code {zip_code} not found in CSV."}

    state = row.values[0]

    # Get state tax rate (default 0 if missing)
    state_rate = state_tax_rates.get(state, 0.0)

    # Tax calculations
    fed_tax = income * fedTax
    state_tax = income * state_rate
    total_tax = fed_tax + state_tax

    return(total_tax)





# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input type of expense and zip code")
    parser.add_argument("expense", help="Expense:") #rent, income, etc
    parser.add_argument("zip_code", type=int, help="Zip code:") #mandatory
    parser.add_argument("income", type=int, help="Income:") #0 if not applicable

    args = parser.parse_args()

    if(args.expense == "rent"):
        result = lookup_expense("rent.csv", "RegionName", args.zip_code, "2025-08-31")
    if(args.expense == "income"):
        result = calculateIncomeTax("incomeTax.csv", args.zip_code, args.income)
    print(result)