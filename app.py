import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import joblib
from database.db import get_db, init_db, detect_engine, get_student_profile_data, get_early_warning_triage
from ml.predictor import predict_student_performance, simulate_what_if

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

    # Early Warning System Triage (🔴 At Risk, 🟠 Monitoring, 🟢 Performing Well)
    early_warning = get_early_warning_triage()

    return render_template(
        "dashboard.html",
        students=n,
        predictions=p,
        gpa=round(float(g), 2),
        early_warning=early_warning
    )

@app.route("/students", methods=["GET", "POST"])
def students():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    if request.method == "POST":
        student_name = request.form["name"].strip().title()
        dept = request.form["department"].strip()
        sem = request.form["semester"]
        c.execute(
            "INSERT INTO students(name,department,semester) VALUES(%s,%s,%s)",
            (student_name, dept, sem),
        )
        conn.commit()
        new_id = c.lastrowid
        # Seed default marks & performance for new student
        c.execute("SELECT subject_id FROM subjects")
        sub_ids = [row[0] for row in c.fetchall()]
        for sub_id in sub_ids:
            c.execute("INSERT INTO attendance(student_id, subject_id, percentage) VALUES (%s, %s, 75.0)", (new_id, sub_id))
            c.execute("INSERT INTO marks(student_id, subject_id, internal, assignment, exam) VALUES (%s, %s, 65.0, 70.0, 68.0)", (new_id, sub_id))
        c.execute("INSERT INTO performance(student_id, gpa, grade) VALUES (%s, 6.8, 'B')", (new_id,))
        conn.commit()

    # Retrieve students enriched with latest performance & attendance
    c.execute("SELECT student_id, name, department, semester FROM students ORDER BY student_id ASC")
    rows = c.fetchall()

    enriched_students = []
    for r in rows:
        p_data = get_student_profile_data(r[0])
        enriched_students.append({
            "student_id": r[0],
            "name": r[1],
            "department": r[2],
            "semester": r[3],
            "attendance": p_data["attendance"] if p_data else 75.0,
            "gpa": p_data["gpa"] if p_data else 6.5
        })

    c.close()
    conn.close()
    return render_template("students.html", rows=rows, enriched_students=enriched_students)

@app.route("/student/<int:student_id>")
def student_profile(student_id):
    if "user" not in session:
        return redirect(url_for("login"))
    profile = get_student_profile_data(student_id)
    if not profile:
        return redirect(url_for("students"))

    # Compute AI Performance Prediction & Risk Diagnostics
    ai_res = predict_student_performance(
        attendance=profile["attendance"],
        internal=profile["internal"],
        assignment=profile["assignment"],
        gpa=profile["gpa"],
        failures=profile["failures"]
    )

    # Class / Cohort Benchmarks
    conn = db()
    c = conn.cursor()
    c.execute("SELECT AVG(gpa) FROM performance")
    avg_gpa = round(float(c.fetchone()[0] or 6.8), 2)
    c.execute("SELECT AVG(percentage) FROM attendance")
    avg_att = round(float(c.fetchone()[0] or 76.5), 1)
    c.close()
    conn.close()

    benchmarks = {
        "class_avg_gpa": avg_gpa,
        "class_avg_attendance": avg_att
    }

    return render_template(
        "student_profile.html",
        student=profile,
        ai=ai_res,
        benchmarks=benchmarks
    )

@app.route("/what-if")
def what_if():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    c.execute("SELECT student_id, name, department, semester FROM students ORDER BY student_id ASC")
    all_students = c.fetchall()
    c.close()
    conn.close()

    target_id = request.args.get("student_id", type=int)
    selected_student = None
    if target_id:
        selected_student = get_student_profile_data(target_id)
    elif all_students:
        selected_student = get_student_profile_data(all_students[0][0])

    return render_template(
        "what_if.html",
        all_students=all_students,
        selected_student=selected_student
    )

@app.route("/api/what-if-simulate", methods=["POST"])
def api_what_if_simulate():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(silent=True) or request.form

    try:
        current_metrics = {
            "attendance": float(data.get("current_attendance", 70)),
            "internal": float(data.get("current_internal", 65)),
            "assignment": float(data.get("current_assignment", 60)),
            "gpa": float(data.get("gpa", 6.5)),
            "failures": float(data.get("failures", 0)),
            "lab_marks": float(data.get("lab_marks", 0)),
            "project_marks": float(data.get("project_marks", 0))
        }
        improved_metrics = {
            "attendance": float(data.get("target_attendance", 90)),
            "internal": float(data.get("target_internal", 80)),
            "assignment": float(data.get("target_assignment", 85)),
            "gpa": float(data.get("gpa", 6.5)),
            "failures": float(data.get("target_failures", 0)),
            "lab_marks": float(data.get("target_lab_marks", 0)),
            "project_marks": float(data.get("target_project_marks", 0))
        }
        simulation = simulate_what_if(current_metrics, improved_metrics)
        return jsonify({"success": True, "simulation": simulation})
    except Exception as e:
        app.logger.error("What-If simulation error: %s", e)
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/students/delete/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = db()
    c = conn.cursor()
    c.execute("DELETE FROM predictions WHERE student_id = %s", (student_id,))
    c.execute("DELETE FROM marks WHERE student_id = %s", (student_id,))
    c.execute("DELETE FROM attendance WHERE student_id = %s", (student_id,))
    c.execute("DELETE FROM performance WHERE student_id = %s", (student_id,))
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
    ai_res = None
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
        internal_raw = request.form.get("internal")
        prev_exam_raw = request.form.get("previous_exam")
        if internal_raw is not None and str(internal_raw).strip() != "":
            exam_marks = float(internal_raw)
        elif prev_exam_raw is not None and str(prev_exam_raw).strip() != "":
            exam_marks = float(prev_exam_raw)
        else:
            exam_marks = 0.0

        lab_marks = float(request.form.get("lab_marks", 0) or 0)
        project_marks = float(request.form.get("project_marks", 0) or 0)
        assignment = float(request.form.get("assignment", 0))
        gpa = float(request.form.get("gpa", 0))
        failures = float(request.form.get("failures", 0))

        # Advanced AI inference
        ai_res = predict_student_performance(
            attendance=attendance,
            internal=exam_marks,
            assignment=assignment,
            gpa=gpa,
            failures=failures,
            lab_marks=lab_marks,
            project_marks=project_marks
        )

        conn = db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO predictions(student_id, predicted_class, probability) VALUES(%s, %s, %s)",
            (student_id, ai_res["category"], float(ai_res["confidence"] / 100.0)),
        )
        conn.commit()
        c.close()
        conn.close()

        # result tuple for backwards compatibility: (category, confidence, predicted_gpa)
        result = (ai_res["category"], ai_res["confidence"], ai_res["predicted_gpa"])

    return render_template("predict.html", result=result, ai=ai_res)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

