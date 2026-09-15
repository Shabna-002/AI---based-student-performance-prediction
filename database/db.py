import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "database", "student_performance.db")

# Load local .env if present
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))

class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        if params is not None:
            # Replace MySQL '%s' parameter placeholder with SQLite '?'
            query = query.replace("%s", "?")
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)

    def executemany(self, query, seq_of_params):
        query = query.replace("%s", "?")
        return self.cursor.executemany(query, seq_of_params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchmany(self, size=None):
        return self.cursor.fetchmany(size) if size else self.cursor.fetchmany()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def close(self):
        try:
            return self.cursor.close()
        except Exception:
            pass

class SQLiteConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return SQLiteCursorWrapper(self.conn.cursor())

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def close(self):
        try:
            return self.conn.close()
        except Exception:
            pass

_DB_ENGINE = None

def detect_engine():
    global _DB_ENGINE
    if _DB_ENGINE is not None:
        return _DB_ENGINE

    preferred = os.getenv("DB_ENGINE", "").lower()
    if preferred == "sqlite":
        _DB_ENGINE = "sqlite"
        return _DB_ENGINE

    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "root")
    database = os.getenv("DB_NAME", "student_performance")
    port = int(os.getenv("DB_PORT", 3306))

    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=3
        )
        conn.close()
        _DB_ENGINE = "mysql"
        logger.info("Successfully connected to MySQL database: %s@%s/%s", user, host, database)
        return _DB_ENGINE
    except Exception as e:
        logger.warning(
            "MySQL connection failed (%s). Falling back to SQLite database at: %s",
            e, SQLITE_DB_PATH
        )
        _DB_ENGINE = "sqlite"
        return _DB_ENGINE

def get_db():
    engine = detect_engine()
    if engine == "mysql":
        import mysql.connector
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "student_performance"),
            port=int(os.getenv("DB_PORT", 3306))
        )
    else:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        return SQLiteConnectionWrapper(conn)

def init_db():
    engine = detect_engine()
    conn = get_db()
    c = conn.cursor()

    # Core table creations (MySQL compatible syntax)
    if engine == "sqlite":
        c.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(100),
            semester INT
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name VARCHAR(100) NOT NULL,
            credits INT DEFAULT 3
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            subject_id INT,
            percentage DECIMAL(5,2)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS marks(
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            subject_id INT,
            internal DECIMAL(5,2),
            assignment DECIMAL(5,2),
            exam DECIMAL(5,2)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS performance(
            performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            gpa DECIMAL(4,2),
            grade VARCHAR(10)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            predicted_class VARCHAR(20),
            probability DECIMAL(6,4),
            predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    else:
        # MySQL tables
        c.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(100),
            semester INT
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            subject_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(100) NOT NULL,
            credits INT DEFAULT 3
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            attendance_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            percentage DECIMAL(5,2)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS marks(
            mark_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            internal DECIMAL(5,2),
            assignment DECIMAL(5,2),
            exam DECIMAL(5,2)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS performance(
            performance_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            gpa DECIMAL(4,2),
            grade VARCHAR(10)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            prediction_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            predicted_class VARCHAR(20),
            probability DECIMAL(6,4),
            predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    # Default admin user seed
    c.execute("SELECT user_id FROM users WHERE username = %s", ("admin",))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "admin123"))

    # Seed Core Academic Subjects
    c.execute("SELECT COUNT(*) FROM subjects")
    if c.fetchone()[0] == 0:
        core_subjects = [
            ("Data Structures & Algorithms", 4),
            ("Engineering Mathematics", 4),
            ("Database Management Systems", 3),
            ("Operating Systems", 3),
            ("Machine Learning & AI", 4)
        ]
        for s_name, creds in core_subjects:
            c.execute("INSERT INTO subjects(subject_name, credits) VALUES (%s, %s)", (s_name, creds))

    # Seed Diverse Academic Student Cohort
    c.execute("SELECT COUNT(*) FROM students")
    current_student_count = c.fetchone()[0]
    if current_student_count < 10:
        cohort = [
            ("Anu V.", "CSE", 3),
            ("Rahul M.", "CSE", 3),
            ("Shabnam K.", "CSE", 3),
            ("Hari Prasad", "CSE", 2),
            ("Akhila S.", "CSE", 2),
            ("Amina N.", "CSE", 2),
            ("Kiran Raj", "ECE", 4),
            ("Sneha Nair", "IT", 3),
            ("Fahad Fazil", "CSE", 4),
            ("Devika Menon", "IT", 2),
            ("Arjun Das", "ECE", 3),
            ("Meera Krishna", "CSE", 3),
            ("Vivek G.", "IT", 4),
            ("Rithika Pillai", "CSE", 2),
            ("Sanjay Kumar", "ECE", 3)
        ]
        for name, dept, sem in cohort:
            c.execute("SELECT student_id FROM students WHERE name = %s", (name,))
            if not c.fetchone():
                c.execute("INSERT INTO students(name, department, semester) VALUES (%s, %s, %s)", (name, dept, sem))

    conn.commit()

    # Seed Marks, Attendance & Performance for all students
    seed_cohort_performance_data(conn)

    conn.commit()
    c.close()
    conn.close()
    logger.info("Initialized database schema and seed records successfully.")

def seed_cohort_performance_data(conn):
    """
    Ensures every student has realistic subject-wise marks,
    attendance records, and GPA records across the 3 academic tiers.
    """
    c = conn.cursor()
    c.execute("SELECT student_id, name FROM students")
    students = c.fetchall()

    c.execute("SELECT subject_id FROM subjects")
    subject_ids = [row[0] for row in c.fetchall()]
    if not subject_ids:
        return

    for idx, (stu_id, name) in enumerate(students):
        # Check if already has marks
        c.execute("SELECT COUNT(*) FROM marks WHERE student_id = %s", (stu_id,))
        if c.fetchone()[0] > 0:
            continue

        # Deterministic tier assignment based on index to create realistic early warning distribution:
        # At Risk (30%), Monitoring (40%), Performing Well (30%)
        tier = idx % 3
        if tier == 0:
            # 🟢 Performing Well (High consistency)
            base_att = 88.0 + (idx % 8)
            base_int = 82.0 + (idx % 12)
            base_assign = 85.0 + (idx % 10)
            base_exam = 86.0 + (idx % 10)
            gpa = min(9.6, 8.2 + (idx % 15) * 0.1)
            grade = "A+" if gpa >= 9.0 else "A"
            failures = 0
        elif tier == 1:
            # 🟠 Needs Monitoring (Average stability)
            base_att = 72.0 + (idx % 6)
            base_int = 64.0 + (idx % 8)
            base_assign = 66.0 + (idx % 8)
            base_exam = 65.0 + (idx % 8)
            gpa = 6.2 + (idx % 10) * 0.1
            grade = "B"
            failures = 0 if idx % 2 == 0 else 1
        else:
            # 🔴 Needs Immediate Attention (At Risk)
            base_att = 54.0 + (idx % 14)
            base_int = 44.0 + (idx % 12)
            base_assign = 48.0 + (idx % 12)
            base_exam = 45.0 + (idx % 12)
            gpa = 4.6 + (idx % 8) * 0.12
            grade = "C" if gpa >= 5.0 else "D"
            failures = 1 + (idx % 3)

        # Insert subject-wise attendance & marks
        for s_idx, sub_id in enumerate(subject_ids):
            subj_att = max(40.0, min(100.0, base_att + ((s_idx * 3) % 7) - 3))
            subj_int = max(35.0, min(100.0, base_int + ((s_idx * 4) % 9) - 4))
            subj_assign = max(40.0, min(100.0, base_assign + ((s_idx * 2) % 6) - 3))
            subj_exam = max(35.0, min(100.0, base_exam + ((s_idx * 5) % 11) - 5))

            c.execute(
                "INSERT INTO attendance(student_id, subject_id, percentage) VALUES (%s, %s, %s)",
                (stu_id, sub_id, round(subj_att, 1))
            )
            c.execute(
                "INSERT INTO marks(student_id, subject_id, internal, assignment, exam) VALUES (%s, %s, %s, %s, %s)",
                (stu_id, sub_id, round(subj_int, 1), round(subj_assign, 1), round(subj_exam, 1))
            )

        # Insert performance GPA
        c.execute(
            "INSERT INTO performance(student_id, gpa, grade) VALUES (%s, %s, %s)",
            (stu_id, round(gpa, 2), grade)
        )

def get_student_profile_data(student_id):
    """
    Fetches full academic profile including subject-wise marks,
    overall attendance %, previous GPA, and total failures.
    """
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT student_id, name, department, semester FROM students WHERE student_id = %s", (student_id,))
    student = c.fetchone()
    if not student:
        c.close()
        conn.close()
        return None

    # Fetch performance GPA
    c.execute("SELECT gpa, grade FROM performance WHERE student_id = %s ORDER BY performance_id DESC LIMIT 1", (student_id,))
    perf = c.fetchone()
    gpa = float(perf[0]) if perf and perf[0] is not None else 6.5
    grade = perf[1] if perf else "B"

    # Fetch subject-wise marks & attendance
    query = """
    SELECT sub.subject_name, sub.credits, m.internal, m.assignment, m.exam, a.percentage
    FROM subjects sub
    LEFT JOIN marks m ON sub.subject_id = m.subject_id AND m.student_id = %s
    LEFT JOIN attendance a ON sub.subject_id = a.subject_id AND a.student_id = %s
    ORDER BY sub.subject_id ASC
    """
    c.execute(query, (student_id, student_id))
    rows = c.fetchall()

    subject_records = []
    total_att = 0.0
    total_internal = 0.0
    total_assign = 0.0
    valid_subs = 0
    calculated_failures = 0

    for r in rows:
        sub_name = r[0]
        credits = r[1] or 3
        internal = float(r[2]) if r[2] is not None else 65.0
        assignment = float(r[3]) if r[3] is not None else 70.0
        exam = float(r[4]) if r[4] is not None else 68.0
        att = float(r[5]) if r[5] is not None else 75.0

        if exam < 45.0 or internal < 45.0:
            calculated_failures += 1

        total_att += att
        total_internal += internal
        total_assign += assignment
        valid_subs += 1

        subject_records.append({
            "subject_name": sub_name,
            "credits": credits,
            "internal": internal,
            "assignment": assignment,
            "exam": exam,
            "attendance": att,
            "total_score": round((internal * 0.4) + (exam * 0.6), 1)
        })

    avg_att = round(total_att / valid_subs, 1) if valid_subs > 0 else 75.0
    avg_int = round(total_internal / valid_subs, 1) if valid_subs > 0 else 65.0
    avg_assign = round(total_assign / valid_subs, 1) if valid_subs > 0 else 70.0

    # Retrieve latest prediction if available
    c.execute("SELECT predicted_class, probability FROM predictions WHERE student_id = %s ORDER BY prediction_id DESC LIMIT 1", (student_id,))
    latest_pred = c.fetchone()

    c.close()
    conn.close()

    return {
        "student_id": student[0],
        "name": student[1],
        "department": student[2],
        "semester": student[3],
        "gpa": gpa,
        "grade": grade,
        "attendance": avg_att,
        "internal": avg_int,
        "assignment": avg_assign,
        "failures": calculated_failures,
        "subjects": subject_records,
        "latest_pred": latest_pred
    }

def get_early_warning_triage():
    """
    Classifies all enrolled students into Early Warning tiers:
    - 🔴 At Risk: Immediate attention needed
    - 🟠 Monitoring: Needs monitoring
    - 🟢 Performing Well: Good consistency
    """
    from ml.predictor import predict_student_performance

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT student_id, name, department, semester FROM students ORDER BY student_id ASC")
    students = c.fetchall()
    c.close()
    conn.close()

    at_risk = []
    monitoring = []
    performing_well = []

    for s in students:
        p_data = get_student_profile_data(s[0])
        if not p_data:
            continue

        pred = predict_student_performance(
            attendance=p_data["attendance"],
            internal=p_data["internal"],
            assignment=p_data["assignment"],
            gpa=p_data["gpa"],
            failures=p_data["failures"]
        )

        item = {
            "student_id": s[0],
            "name": s[1],
            "department": s[2],
            "semester": s[3],
            "gpa": p_data["gpa"],
            "attendance": p_data["attendance"],
            "failures": p_data["failures"],
            "predicted_gpa": pred["predicted_gpa"],
            "category": pred["category"],
            "badge_class": pred["badge_class"],
            "confidence": pred["confidence"],
            "risks_count": len(pred["risks"])
        }

        if pred["category"] == "At Risk":
            at_risk.append(item)
        elif pred["category"] == "Average":
            monitoring.append(item)
        else:
            performing_well.append(item)

    return {
        "counts": {
            "at_risk": len(at_risk),
            "monitoring": len(monitoring),
            "performing_well": len(performing_well),
            "total": len(students)
        },
        "at_risk_list": at_risk,
        "monitoring_list": monitoring,
        "performing_well_list": performing_well
    }

