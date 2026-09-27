import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "pocketsmart_secret_key"

# Initialize official Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Mock user database (for testing)
users = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users[username] = password
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/home_planner")
def home_planner():
    return render_template("home_planner.html")

@app.route("/jewelry_planner")
def jewelry_planner():
    return render_template("jewelry_planner.html")

@app.route("/party_planner")
def party_planner():
    return render_template("party_planner.html")

@app.route("/generate_home", methods=["POST"])
def generate_home():
    try:
        data = request.get_json() or {}
        rooms = data.get("rooms", "")
        budget = data.get("budget", "")
        
        prompt = f"Plan home interior for {rooms} with total budget {budget}. Give itemized breakdown and recommendations."
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_jewelry", methods=["POST"])
def generate_jewelry():
    try:
        data = request.get_json() or {}
        items = data.get("items", "")
        budget = data.get("budget", "")
        
        prompt = f"Plan jewelry purchase for {items} within budget {budget}. Suggest breakdown and options."
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_party", methods=["POST"])
def generate_party():
    try:
        data = request.get_json() or {}
        event_type = data.get("event_type", "")
        guests = data.get("guests", "")
        budget = data.get("budget", "")
        
        prompt = f"Plan a {event_type} party for {guests} guests with a budget of {budget}. Provide a breakdown for catering, decoration, and venue."
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
