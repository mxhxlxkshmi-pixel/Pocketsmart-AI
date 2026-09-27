import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "pocketsmart_secret_key"

# Initialize official Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Temporary user storage
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

# Helper function to clean Markdown formatting from JSON
def clean_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text

# 1. HOME INTERIOR PLANNER ROUTE
@app.route("/generate_home", methods=["POST"])
def generate_home():
    try:
        data = request.get_json() or {}
        rooms = data.get("rooms", "")
        budget = data.get("budget", "")
        
        prompt = f"""
        Act as a home interior budget planner. Plan interior for: {rooms} with budget: {budget}.
        Return ONLY valid JSON in this exact structure without markdown or backticks:
        {{
            "total_budget": "{budget}",
            "remaining_budget": "500",
            "categories": [
                {{
                    "name": "Lighting",
                    "allocation": "1500",
                    "items": [
                        {{"item": "LED Bulb", "description": "Energy-efficient LED bulbs for general lighting", "price": "100", "quantity": 5}}
                    ]
                }},
                {{
                    "name": "Furniture",
                    "allocation": "2000",
                    "items": [
                        {{"item": "Wooden Table", "description": "Simple wooden dining table", "price": "500", "quantity": 1}}
                    ]
                }}
            ]
        }}
        """
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        cleaned_result = clean_json_response(response.text)
        return jsonify({"result": cleaned_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. JEWELRY PLANNER ROUTE
@app.route("/generate_jewelry", methods=["POST"])
def generate_jewelry():
    try:
        data = request.get_json() or {}
        items = data.get("items", "")
        budget = data.get("budget", "")
        
        prompt = f"""
        Act as a jewelry budget planner. Plan jewelry for: {items} with total budget: {budget}.
        Return ONLY valid JSON in this exact structure without markdown or backticks:
        {{
            "total_budget": "{budget}",
            "outfit_analysis": {{
                "colors": "Gold / Diamond",
                "style": "Partywear / Casual",
                "formality": "High"
            }},
            "recommendations": [
                {{
                    "name": "Gold Ring",
                    "description": "Minimalist ring suitable for formal and party wear",
                    "price": "3000",
                    "style": "Modern"
                }},
                {{
                    "name": "Silver Watch",
                    "description": "Classic silver watch to match party wear",
                    "price": "5000",
                    "style": "Classic"
                }}
            ],
            "tips": [
                "Keep metal tones uniform across all accessories.",
                "Balance statement pieces with subtle accents."
            ]
        }}
        """
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        cleaned_result = clean_json_response(response.text)
        return jsonify({"result": cleaned_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. PARTY PLANNER ROUTE
@app.route("/generate_party", methods=["POST"])
def generate_party():
    try:
        data = request.get_json() or {}
        event_type = data.get("event_type", "")
        guests = data.get("guests", "")
        budget = data.get("budget", "")
        
        prompt = f"""
        Act as a party event planner. Plan a {event_type} party for {guests} guests with a budget of {budget}.
        Return ONLY valid JSON in this exact structure without markdown or backticks:
        {{
            "total_budget": "{budget}",
            "categories": [
                {{
                    "name": "Venue",
                    "items": [
                        {{"name": "Hall Rental", "description": "Spacious party hall including seats", "price": "2000"}}
                    ]
                }},
                {{
                    "name": "Catering",
                    "items": [
                        {{"name": "Buffet Dinner", "description": "Full course dinner for guests", "price": "1500"}}
                    ]
                }},
                {{
                    "name": "Entertainment",
                    "items": [
                        {{"name": "DJ & Sound System", "description": "Audio system with music setup", "price": "1000"}}
                    ]
                }}
            ]
        }}
        """
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        cleaned_result = clean_json_response(response.text)
        return jsonify({"result": cleaned_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
