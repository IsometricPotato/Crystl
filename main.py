from src.api_service import call_gemini_api
from src.user_storage import update_user_data, save_user_data, load_user_data
from src.data_processor import lookup_expense, calculateIncomeTax, prepare_prompt_data

# --- Test Data ---
# This is where you define the data you'd get from the user
test_user_id = "test_user_123"
test_zip_code = 15213
test_income = 60000

# --- Function Calls and Data Processing ---
# 1. Create a new user data dictionary with initial values
prepare_prompt_data()
user_data = load_user_data()


# 2. Call the functions and update the dictionary
estimated_rent = lookup_expense(
    csv_file="src/rent.csv",
    zip_code_name="RegionName",
    zip_code=test_zip_code,
    value="2025-08-31"
)
update_user_data("rent", estimated_rent)
print(f"Estimated Rent: {estimated_rent}")

estimated_tax = calculateIncomeTax(
    csv_file="src/incomeTax.csv",
    zip_code=test_zip_code,
    income=test_income
)
update_user_data("tax", estimated_tax)
print(f"Estimated Yearly Tax: {estimated_tax}")

# 3. Add other specific user data
update_user_data("disability", "autism, and I'm wheelchair bound")
update_user_data("medical", "300")
update_user_data("debt", 50000)
update_user_data("salary", 60000)
print(call_gemini_api())