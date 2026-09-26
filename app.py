import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Use stable gemini-1.5-flash model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

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
        response = model.generate_content(prompt)
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
        response = model.generate_content(prompt)
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
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
