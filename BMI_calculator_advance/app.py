from flask import Flask, render_template, request, redirect, url_for
from storage import save_bmi, load_user_data
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bmi_result = None
    category = None
    username = None

    if request.method == "POST":
        # Get form data
        username = request.form["username"].strip()
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        # BMI calculation
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        # Categorization
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        # Save record
        save_bmi(username, weight, height, bmi, category)

        # Redirect to GET request (avoids form re-submission issues)
        return redirect(url_for("index", username=username, bmi=bmi, category=category))

    # GET request – fetch data from query params
    username = request.args.get("username")
    bmi_result = request.args.get("bmi")
    category = request.args.get("category")

    return render_template("index.html", bmi_result=bmi_result, category=category, username=username)

@app.route("/history/<username>", methods=["GET"])
def history(username):
    data = load_user_data(username)
    chart_data = {
        "dates": data["date"].tolist(),
        "bmi_values": data["bmi"].tolist()
    }
    return render_template("history.html", username=username, chart_data=json.dumps(chart_data))

if __name__ == "__main__":
    app.run(debug=True)
