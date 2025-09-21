import google.generativeai as genai
import os
from dotenv import load_dotenv
from data_processor import prepare_prompt_data, lookup_expense, calculateIncomeTax
from user_storage import update_user_data, return_user_data

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Your core prompt structure, with placeholders
PROMPT_TEMPLATE = """
Role and Persona: You are a helpful and empathetic financial assistant specializing in reviewing personalized budgets and providing financial advice. You are working with a user who has the following disabilities, if any: [{disability}]. You should heavily consider this in your response.

Your role is to review the data given and fill in only data that is missing a data point (0 for example)

You will provide tips for lowering expenses or getting more income, tailored to their situation considering disabilities if applicable.

You will be given some information from the individual and the information they do not give will be filled by you to make an educated guess. Here is all the additional information given to you by the user/API:

Zip code: [{zip_code}]
Salary: [{income_amount}] (
Rent: [{rent}]
Food: [{food}]
Transportation: [{transportation}]
Medical: [{medical}]
Utilities [{utilities}]
Savings [{savings}]
Student Loans [{student_loans}] (assume 0 if no value is given)

Debt Payments [{debt}]
Yearly Taxes [{taxes}]
Fun money [{fun_money}]

Fill in any parameters that are not provided, and don't change the ones that are.

If the expenses input are too high for the income, you must adjust "savings" categories accordingly even if negative or potentially allocating a value of $0.

Your output should look EXACTLY like this. It needs to be in this format to work correctly, and there should be no extra text before or after. Your tips should be separated by “TIP #” with the numbers filled in with 5 tips. One of the tips can be how to claim disability for assistance with income/taxes.  

You should also add a score 1-10 of how good their financial situation is along with a short explanation of their situation. For the monthly income through fun money parameters, write a dollar sign then the number, and no other text on the line:

<div class="budget">
    <p>Monthly Income: ${income_amount}</p>
    <p>Rent: ${rent}</p>
    <p>Food: ${food}</p>
    <p>Transportation: ${transportation}</p>
    <p>Medical: ${medical}</p>
    <p>Utilities: ${utilities}</p>
    <p>Student Loan Payments: ${student_loans}</p>
    <p>Debt Payments: ${debt}</p>
    <p>Money set aside for taxes: ${taxes}</p>
    <p>Fun money: ${fun_money}</p>
    <p>Savings: ${savings}</p>

    <ul>
        <li>TIP 1: [TIP 1]</li>
        <li>TIP 2: [TIP 2]</li>
        <li>TIP 3: [TIP 3]</li>
        <li>TIP 4: [TIP 4]</li>
        <li>TIP 5: [TIP 5]</li>
    </ul>

    <p><strong>Financial Score:</strong> [SCORE]</p>
    <p><strong>Score Explanation:</strong> [EXPLANATION]</p>
</div>
"""

def call_gemini_api():
    """
    Sends the user data to the Gemini API with the specified prompt.
    """
    try:

        user_data = prepare_prompt_data()

        model = genai.GenerativeModel('gemini-1.5-pro')

        estimated_rent = lookup_expense(
            csv_file="src/rent.csv",
            zip_code_name="RegionName",
            zip_code=15213,
            value="2025-08-31")
        print(f"Estimated Rent: {estimated_rent}")

        estimated_tax = calculateIncomeTax(
            csv_file="src/incomeTax.csv",
            zip_code=15213,
            income=return_user_data("income_amount")
        )
        print(f"Estimated Tax: {estimated_tax}")

        if user_data.get("tax") is None:
            update_user_data("tax", estimated_tax)
        if user_data.get("rent") is None:
            update_user_data("rent", estimated_rent)

        prompt = PROMPT_TEMPLATE.format(
            disability=user_data.get("disability", "None"),
            income_amount=user_data.get("income_amount", "None"),
            zip_code=user_data.get("zip_code", "15213"),
            rent=user_data.get("rent", "Not provided"),
            food=user_data.get("food", "Not provided"),
            transportation=user_data.get("transportation", "Not provided"),
            medical=user_data.get("medical", "Not provided"),
            utilities=user_data.get("utilities", "Not provided"),
            savings=user_data.get("savings", "0"),
            student_loans=user_data.get("student_loans", "0"), # Default to 0 as per prompt
            debt=user_data.get("debt", "Not provided"),
            taxes=user_data.get("taxes", "Not provided"),
            fun_money=user_data.get("fun_money", "Not provided")

        )

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text
        else:
            return "Error: Could not get a valid response from the API."

    except Exception as e:
        return f"An error occurred: {e}"

def getAI(ai_response, data):
    lines = ai_response.splitlines()
    aiOutput = ""

    for line in lines:
        if line.startswith(data + ":"):
            aiOutput = line.split(":", 1)[1].strip()
            break

    return aiOutput