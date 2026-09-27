import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from google import genai

app = Flask(__name__)

# Security: Load secret key from environment or fallback to a secure random default
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Initialize Gemini Client (uses GEMINI_API_KEY from environment variables)
client = genai.Client()

# Model Selection: gemini-3.8-flash (or switch to "gemini-2.5-flash")
MODEL_NAME = "gemini-3.8-flash"

# In-memory user store (For production, substitute with a real database like PostgreSQL/SQLite)
users = {}

# Helper function to enforce authentication on protected routes
def is_authenticated():
    return "user" in session


@app.route("/")
def home():
    return render_template("index.html", user=session.get("user"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for("register"))

        if username in users:
            flash("Username already exists. Please choose another.", "warning")
            return redirect(url_for("register"))

        # Security: Hash password before saving
        users[username] = generate_password_hash(password)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        
        flash("Invalid username or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/generate_home", methods=["POST"])
def generate_home():
    if not is_authenticated():
        return redirect(url_for("login"))

    prompt = request.form.get("prompt", "")
    if not prompt:
        flash("Please provide a prompt.", "warning")
        return redirect(url_for("home"))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        output = response.text
    except Exception as e:
        output = f"Error generating content: {str(e)}"

    return render_template("home.html", result=output)


@app.route("/generate_jewelry", methods=["POST"])
def generate_jewelry():
    if not is_authenticated():
        return redirect(url_for("login"))

    prompt = request.form.get("prompt", "")
    if not prompt:
        flash("Please provide a prompt.", "warning")
        return redirect(url_for("home"))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"Generate jewelry recommendation/ideas for: {prompt}",
        )
        output = response.text
    except Exception as e:
        output = f"Error generating content: {str(e)}"

    return render_template("jewelry.html", result=output)


@app.route("/generate_party", methods=["POST"])
def generate_party():
    if not is_authenticated():
        return redirect(url_for("login"))

    prompt = request.form.get("prompt", "")
    if not prompt:
        flash("Please provide a prompt.", "warning")
        return redirect(url_for("home"))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"Generate party planning ideas for: {prompt}",
        )
        output = response.text
    except Exception as e:
        output = f"Error generating content: {str(e)}"

    return render_template("party.html", result=output)


if __name__ == "__main__":
    app.run(debug=True)
