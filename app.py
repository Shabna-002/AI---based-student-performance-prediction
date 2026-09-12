import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
import joblib
from database.db import get_db, init_db, detect_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "student_performance_model.pkl")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret")

# Auto-initialize database tables and seed records if needed
try:
    init_db()
except Exception as err:
    app.logger.warning("Database init warning: %s", err)

def db():
    return get_db()

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
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not password or not confirm_password:
            return render_template("signup.html", error="Please fill in all fields.", username=username)

        if len(username) < 3:
            return render_template("signup.html", error="Username must be at least 3 characters long.", username=username)

        if len(password) < 4:
            return render_template("signup.html", error="Password must be at least 4 characters long.", username=username)

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match. Please re-enter.", username=username)

        conn = db()
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
        existing_user = c.fetchone()
        if existing_user:
            c.close()
            conn.close()
            return render_template("signup.html", error="Username already exists. Please choose another.", username=username)

        try:
            c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
        except Exception as e:
            conn.rollback()
            c.close()
            conn.close()
            app.logger.error("Signup error: %s", e)
            return render_template("signup.html", error="An error occurred during registration. Please try again.", username=username)

        c.close()
        conn.close()
        return redirect(url_for("login", success="Account created successfully! Please sign in."))

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
    # Order strictly by student_id in ascending order only
    c.execute("SELECT * FROM students ORDER BY student_id ASC")
    rows = c.fetchall()
    c.close()
    conn.close()
    return render_template("students.html", rows=rows)

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
        raw_sid = str(request.form.get("student_id", "1")).strip().upper()
        if raw_sid.startswith("STU-"):
            sid = raw_sid.replace("STU-", "")
        elif raw_sid.startswith("#"):
            sid = raw_sid.replace("#", "")
        else:
            sid = raw_sid
        try:
            student_id = int(sid)
        except ValueError:
            student_id = 1

        # Retrieve academic parameters
        attendance = float(request.form.get("attendance", 85.0))
        exam_marks = float(request.form.get("internal", request.form.get("previous_exam", 0)))
        lab_marks = float(request.form.get("lab_marks", 0) or 0)
        project_marks = float(request.form.get("project_marks", 0) or 0)

        # If lab & project marks are provided, factor them into internal evaluation
        if lab_marks > 0 or project_marks > 0:
            internal_val = round((exam_marks * 0.6) + (lab_marks * 0.2) + (project_marks * 0.2), 2)
        else:
            internal_val = exam_marks

        assignment = float(request.form.get("assignment", 0))
        gpa = float(request.form.get("gpa", 0))
        failures = float(request.form.get("failures", 0))

        features = [attendance, internal_val, assignment, gpa, failures]
        v = pd.DataFrame([features], columns=["attendance", "internal", "assignment", "gpa", "failures"])
        m = joblib.load(MODEL_PATH)
        pred = m.predict(v)[0]
        prob = max(m.predict_proba(v)[0])
        conn = db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions(student_id,predicted_class,probability) VALUES(%s,%s,%s)",
            (student_id, pred, float(prob)),
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
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
