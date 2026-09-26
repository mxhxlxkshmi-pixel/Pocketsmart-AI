from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------------------------------------
# PAGE ROUTES (Renders HTML templates)
# ---------------------------------------------------------

@app.route("/")
def home():
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


# ---------------------------------------------------------
# API ENDPOINTS (Handles Gemini AI generation requests)
# ---------------------------------------------------------

# Generate Home Interior Plan
@app.route("/generate_home", methods=["POST"])
def generate_home():
    data = request.json
    
    # Logic for home interior planning using Gemini API
    prompt = f"""
    Create a home interior plan for the following rooms:
    {data.get('rooms')}

    Budget: {data.get('budget')}

    Provide practical, attractive and budget-friendly interior design suggestions.
    """
    
    response = model.generate_content(prompt)
    return jsonify({"result": response.text})


# Generate Party Plan
@app.route("/generate_party", methods=["POST"])
def generate_party():
    data = request.json

    # Logic for party planning using Gemini API
    prompt = f"""
    Plan a party for {data.get('guests')} guests
    with event type {data.get('event_type')}
    and budget {data.get('budget')}.

    Suggest decorations, food, activities and a suitable schedule.
    """

    response = model.generate_content(prompt)
    return jsonify({"result": response.text})


# Generate Jewelry Suggestions
@app.route("/generate_jewelry", methods=["POST"])
def generate_jewelry():
    data = request.json

    # Logic for jewelry selection using Gemini API
    prompt = f"""
    Suggest jewelry for the occasion:
    {data.get('occasion')}

    Budget: {data.get('budget')}

    Recommend suitable jewelry styles and explain why they would be appropriate.
    """

    response = model.generate_content(prompt)
    return jsonify({"result": response.text})


# ---------------------------------------------------------
# SERVER LAUNCHER
# ---------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
