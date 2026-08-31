import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
# Secret key required for Flask session management
app.secret_key = "super_secret_key"


# --- SQLite Database Helper ---
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Access columns by name: row['name']
    return conn


# --- Create Database Table ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            dob TEXT,
            gender TEXT,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Create table automatically on app startup
init_db()


# --- Main Navigation Routes ---
@app.route("/")
def home():  
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/trainers")
def trainers():
    return render_template("trainers.html")


# --- Register Route ---
@app.route("/register", methods=["GET", "POST"])
@app.route("/api/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        dob = data.get("dob")
        gender = data.get("gender")
        course = data.get("course")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        existing_user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if existing_user:
            conn.close()
            return jsonify({"status": "error", "message": "Email already registered! Please login."})

        # Insert new user with all fields into SQLite database
        cursor.execute(
            "INSERT INTO users (name, email, password, dob, gender, course) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, password, dob, gender, course)
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Registration successful! Please login."})

    return render_template("register.html")


# --- Login Route ---
@app.route("/login", methods=["GET", "POST"])
@app.route("/api/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Search for user matching email and password
        user = cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            # Store logged-in user in session
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            return jsonify({"status": "success", "message": "Login successful!"})
        else:
            return jsonify({"status": "error", "message": "Invalid email or password!"})

    return render_template("login.html")


# --- Logout Route ---
@app.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

