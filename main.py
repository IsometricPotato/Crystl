from src.api_service import call_gemini_api
from src.user_storage import update_user_data, save_user_data, load_user_data
from src.data_processor import lookup_expense, calculateIncomeTax, prepare_prompt_data

#temp variables
test_user_id = "test_user_123"
test_zip_code = 15213
test_income = 60000

#call prepare_prompt_data() to create a user with parameters
prepare_prompt_data()

#update user data
update_user_data("disability", "autism, and I'm wheelchair bound")
update_user_data("medical", "300")
update_user_data("debt", 50000)
update_user_data("salary", 60000)

#call gemini api with variables and print result
print(call_gemini_api())