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
    if engine == "sqlite":
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        raw_conn = sqlite3.connect(SQLITE_DB_PATH)
        c = raw_conn.cursor()

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
            percentage DECIMAL(5,2),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS marks(
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            subject_id INT,
            internal DECIMAL(5,2),
            assignment DECIMAL(5,2),
            exam DECIMAL(5,2),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS performance(
            performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            gpa DECIMAL(4,2),
            grade VARCHAR(10),
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INT,
            predicted_class VARCHAR(20),
            probability DECIMAL(6,4),
            predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
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

        # Default admin user seed
        c.execute("SELECT user_id FROM users WHERE username = ?", ("admin",))
        if not c.fetchone():
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))

        # Seed sample students if empty
        c.execute("SELECT COUNT(*) FROM students")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO students(name, department, semester) VALUES (?, ?, ?)", ("Anu", "CSE", 2))
            c.execute("INSERT INTO students(name, department, semester) VALUES (?, ?, ?)", ("Rahul", "CSE", 3))

        raw_conn.commit()
        raw_conn.close()
        logger.info("Initialized SQLite database schema and seed records successfully.")
    else:
        # MySQL initialization if needed
        conn = get_db()
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        c.execute("SELECT user_id FROM users WHERE username = %s", ("admin",))
        if not c.fetchone():
            c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("admin", "admin123"))
        conn.commit()
        c.close()
        conn.close()
