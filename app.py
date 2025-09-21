from flask import Flask, render_template, request, session, redirect, url_for
import json
from api_service import call_gemini_api

app = Flask(__name__)
app.secret_key = "hackathon"

DATA_FILE = "budget_data.json"

def read_budget():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_budget(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        zip_code = request.form.get("zip_code")
        income = request.form.get("income_amount")

        budget_data = read_budget()
        budget_data["zip_code"] = zip_code
        budget_data["income_amount"] = income
        write_budget(budget_data)

        call_gemini_api()

        return redirect(url_for("expenses_page"))
    return render_template("form.html")


@app.route("/budget")
def expenses_page():
    budget_data = read_budget()
    financial_info = call_gemini_api()  # get API output
    return render_template(
        "expenses_page.html",
        user_data=budget_data.get("0", {}),
        financial_info=financial_info
    )


@app.route("/update_income", methods=["POST"])
def update_income():
    income_type = request.form.get("income_type")
    income_amount = request.form.get("income_amount")

    budget_data = read_budget()
    budget_data["income_type"] = income_type
    budget_data["income_amount"] = income_amount
    write_budget(budget_data)

    call_gemini_api()
    # Redirect back to /budget, which reloads the page
    return redirect(url_for("expenses_page"))

@app.route("/update_housing", methods=["POST"])
def update_housing():
    rent_cost = request.form.get("rent_cost")

    budget_data = read_budget()
    budget_data["rent_cost"] = rent_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_utilities", methods=["POST"])
def update_utilities():
    utilities_cost = request.form.get("utilities_cost")

    budget_data = read_budget()
    budget_data["utilities_cost"] = utilities_cost
    write_budget(budget_data)

    # Redirect back to /budget to reload page
    return redirect(url_for("expenses_page"))

@app.route("/update_food", methods=["POST"])
def update_food():
    food_cost = request.form.get("food_cost")

    budget_data = read_budget()
    budget_data["food_cost"] = food_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_medical", methods=["POST"])
def update_medical():
    medical_bills = request.form.get("medical_bills")

    budget_data = read_budget()
    budget_data["medical_bills"] = medical_bills
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))


@app.route("/update_transportation", methods=["POST"])
def update_transportation():
    transportation_cost = request.form.get("transportation_cost")

    budget_data = read_budget()
    budget_data["transportation_cost"] = transportation_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))


@app.route("/update_entertainment", methods=["POST"])
def update_entertainment():
    entertainment_cost = request.form.get("entertainment_cost")

    budget_data = read_budget()
    budget_data["entertainment_cost"] = entertainment_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_debt", methods=["POST"])
def update_debt():
    student_loans = request.form.get("student_loans")
    other_debt = request.form.get("other_debt")

    budget_data = read_budget()
    budget_data["student_loans"] = student_loans
    budget_data["other_debt"] = other_debt
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_disabilities", methods=["POST"])
def update_disabilities():
    disability = request.form.get("disabilities")

    budget_data = read_budget()
    if "disabilities" not in budget_data:
        budget_data["disabilities"] = []
    budget_data["disabilities"].append(disability)
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/reset_data", methods=["POST"])
def reset_data():

    budget_data = read_budget()
    budget_data = {
    "utilities_cost": "0",
    "income_type": "hourly",
    "income_amount": "0",
    "rent_cost": "0",
    "food_cost": "0",
    "transportation_cost": "0",
    "entertainment_cost": "0",
    "student_loans": "0",
    "other_debt": "0",
    "disabilities": [],
    "tax": 0,
    "rent": 0
    }
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

if __name__ == "__main__":
    app.run(debug=True)
