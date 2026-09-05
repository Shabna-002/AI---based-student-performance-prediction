import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector, joblib

# Load local .env if present
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret")
DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
    database=os.getenv("DB_NAME", "student_performance")
)

def db():
    return mysql.connector.connect(**DB)

@app.route("/", methods=["GET", "POST"])
def login():
    success = request.args.get("success")
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if username == "admin" and password == "admin123":
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        conn = db()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = %s", (username,))
        row = c.fetchone()
        c.close()
        conn.close()
        if row and row[0] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials", success=success)
    return render_template("login.html", success=success)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")
        if not username or not password:
            return render_template("signup.html", error="Username and password are required")
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")
        conn = db()
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if c.fetchone():
            c.close()
            conn.close()
            return render_template("signup.html", error="Username already exists. Please choose another.")
        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        c.close()
        conn.close()
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM students")
    n = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM predictions")
    p = c.fetchone()[0]
    c.execute("SELECT AVG(gpa) FROM performance")
    g = c.fetchone()[0] or 0
    c.close()
    conn.close()
    return render_template("dashboard.html", students=n, predictions=p, gpa=round(float(g), 2))

@app.route("/students", methods=["GET", "POST"])
def students():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    if request.method == "POST":
        student_name = request.form["name"].strip().title()
        c.execute(
            "INSERT INTO students(name,department,semester) VALUES(%s,%s,%s)",
            (student_name, request.form["department"].strip(), request.form["semester"]),
        )
        conn.commit()
    sort_by = request.args.get("sort", "name")
    if sort_by == "id":
        c.execute("SELECT * FROM students ORDER BY student_id ASC")
    else:
        c.execute("SELECT * FROM students ORDER BY LOWER(name) ASC, student_id ASC")
    rows = c.fetchall()
    c.close()
    conn.close()
    return render_template("students.html", rows=rows, sort_by=sort_by)

@app.route("/students/delete/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    c.execute("DELETE FROM predictions WHERE student_id = %s", (student_id,))
    c.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()
    c.close()
    conn.close()
    return redirect(url_for("students"))

@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    if request.method == "POST":
        name = request.form["name"].strip().title()
        department = request.form["department"].strip()
        semester = request.form["semester"]
        c.execute(
            "UPDATE students SET name = %s, department = %s, semester = %s WHERE student_id = %s",
            (name, department, semester, student_id),
        )
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for("students"))
    c.execute("SELECT student_id, name, department, semester FROM students WHERE student_id = %s", (student_id,))
    student = c.fetchone()
    c.close()
    conn.close()
    if not student:
        return redirect(url_for("students"))
    return render_template("edit_student.html", student=student)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))
    result = None
    if request.method == "POST":
        features = [float(request.form[k]) for k in ["attendance", "internal", "assignment", "gpa", "failures"]]
        v = pd.DataFrame([features], columns=["attendance", "internal", "assignment", "gpa", "failures"])
        m = joblib.load("ml/student_performance_model.pkl")
        pred = m.predict(v)[0]
        prob = max(m.predict_proba(v)[0])
        conn = db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions(student_id,predicted_class,probability) VALUES(%s,%s,%s)",
            (request.form["student_id"], pred, float(prob)),
        )
        conn.commit()
        c.close()
        conn.close()
        result = (pred, round(prob * 100, 2))
    return render_template("predict.html", result=result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
