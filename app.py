from flask import Flask, render_template, request, session, redirect, url_for
import json

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
        income = request.form.get("income")

        budget_data = read_budget()
        budget_data["0"] = {} # id: 0
        budget_data["0"]["zip_code"] = zip_code
        budget_data["0"]["income"] = income
        write_budget(budget_data)

        return redirect(url_for("expenses_page"))
    return render_template("form.html")


@app.route("/budget")
def expenses_page():
    return render_template("expenses_page.html", user_data=session.get("user_data", {}))


@app.route("/update_income", methods=["POST"])
def update_income():
    income_type = request.form.get("income_type")
    income_amount = request.form.get("income_amount")

    budget_data = read_budget()
    budget_data["0"]["income_type"] = income_type
    budget_data["0"]["income_amount"] = income_amount
    write_budget(budget_data)

    print(session)

    # Redirect back to /budget, which reloads the page
    return redirect(url_for("expenses_page"))

@app.route("/update_housing", methods=["POST"])
def update_housing():
    rent_cost = request.form.get("rent_cost")

    budget_data = read_budget()
    budget_data["0"]["rent_cost"] = rent_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_utilities", methods=["POST"])
def update_utilities():
    utilities_cost = request.form.get("utilities_cost")

    budget_data = read_budget()
    budget_data["0"]["utilities_cost"] = utilities_cost
    write_budget(budget_data)

    # Redirect back to /budget to reload page
    return redirect(url_for("expenses_page"))

@app.route("/update_food", methods=["POST"])
def update_food():
    food_cost = request.form.get("food_cost")

    budget_data = read_budget()
    budget_data["0"]["food_cost"] = food_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))


@app.route("/update_transportation", methods=["POST"])
def update_transportation():
    transportation_cost = request.form.get("transportation_cost")

    budget_data = read_budget()
    budget_data["0"]["transportation_cost"] = transportation_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))


@app.route("/update_entertainment", methods=["POST"])
def update_entertainment():
    entertainment_cost = request.form.get("entertainment_cost")

    budget_data = read_budget()
    budget_data["0"]["entertainment_cost"] = entertainment_cost
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/update_debt", methods=["POST"])
def update_debt():
    student_loans = request.form.get("student_loans")
    other_debt = request.form.get("other_debt")

    budget_data = read_budget()
    budget_data["0"]["student_loans"] = student_loans
    budget_data["0"]["other_debt"] = other_debt
    write_budget(budget_data)

    return redirect(url_for("expenses_page"))

@app.route("/reset_data", methods=["POST"])
def reset_data():

    session["user_data"] = {}

    return redirect(url_for("expenses_page"))

if __name__ == "__main__":
    app.run(debug=True)
