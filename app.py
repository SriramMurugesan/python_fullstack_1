import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key"


# --- Database Connection Helper ---
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Access columns by name: row['name']
    return conn


# --- Create Tables on Startup ---
def init_db():
    conn = get_db()
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# --- Navigation Page Routes ---
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

@app.route("/todos")
def todos_page():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("todo.html")


# --- User Registration ---
@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/api/register", methods=["POST"])
def register_api():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    dob = data.get("dob")
    gender = data.get("gender")
    course = data.get("course")

    conn = get_db()
    cursor = conn.cursor()

    # Check duplicate email
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user:
        conn.close()
        return jsonify({"status": "error", "message": "Email already registered!"})

    # Save user into SQLite
    cursor.execute(
        "INSERT INTO users (name, email, password, dob, gender, course) VALUES (?, ?, ?, ?, ?, ?)",
        (name, email, password, dob, gender, course)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Registration successful!"})


# --- User Login ---
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def login_api():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    conn.close()

    if user:
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        return jsonify({"status": "success", "message": "Login successful!"})

    return jsonify({"status": "error", "message": "Invalid email or password!"})


# --- User Logout ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# --- To-Do List CRUD APIs ---

# 1. READ: Fetch all tasks for logged-in user
@app.route("/api/todos", methods=["GET"])
def get_todos():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM todos WHERE user_id = ?", (session["user_id"],)).fetchall()
    conn.close()

    todos_list = []
    for row in rows:
        todos_list.append({
            "id": row["id"],
            "task": row["task"],
            "status": row["status"]
        })

    return jsonify({"status": "success", "todos": todos_list})


# 2. CREATE: Add new task
@app.route("/api/todos", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    data = request.get_json()
    task = data.get("task")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (user_id, task, status) VALUES (?, ?, ?)", (session["user_id"], task, "Pending"))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Task added!"})


# 3. UPDATE: Change task status
@app.route("/api/todos/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    data = request.get_json()
    status = data.get("status")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET status = ? WHERE id = ? AND user_id = ?", (status, todo_id, session["user_id"]))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Task updated!"})


# 4. DELETE: Remove task
@app.route("/api/todos/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, session["user_id"]))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Task deleted!"})


if __name__ == "__main__":
    app.run(debug=True)
