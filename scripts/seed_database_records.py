import random
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import get_db, init_db, detect_engine

random.seed(42)

FIRST_NAMES = [
    "Aadhya", "Aarav", "Abhinav", "Aditi", "Aishwarya", "Ajay", "Akash", "Akhil", "Amal", "Ananya",
    "Anjali", "Anu", "Arjun", "Ashwin", "Athira", "Deepak", "Devika", "Divya", "Fahad", "Farhan",
    "Gautam", "Gopika", "Harikrishnan", "Haritha", "Jithin", "Kavya", "Keerthi", "Kiran", "Madhav", "Meera",
    "Midhun", "Nandana", "Navaneeth", "Neeraj", "Nikhil", "Parvathy", "Pooja", "Pranav", "Rahul", "Reshma",
    "Rithika", "Rohit", "Roshan", "Sanjay", "Sarath", "Shabnam", "Sneha", "Sreehari", "Varun", "Vishnu"
]

LAST_NAMES = [
    "Nair", "Menon", "Pillai", "Kurup", "Kumar", "Prasad", "Varma", "Das", "Raj", "Mohan",
    "Nambiar", "Sharma", "K.", "M.", "V.", "S.", "R.", "Babu", "Joseph", "Mathew"
]

DEPARTMENTS = [
    "Computer Science & Engineering",
    "Artificial Intelligence & Data Science",
    "Electronics & Communication Engineering",
    "Information Technology"
]

def seed_database():
    engine = detect_engine()
    print(f"Active database engine detected: {engine}")
    init_db()

    conn = get_db()
    c = conn.cursor()

    # Check existing subjects
    c.execute("SELECT subject_id, subject_name FROM subjects")
    subjects = c.fetchall()
    if not subjects:
        core_subjects = [
            ("Data Structures & Algorithms", 4),
            ("Engineering Mathematics", 4),
            ("Database Management Systems", 3),
            ("Operating Systems", 3),
            ("Machine Learning & AI", 4)
        ]
        for s_name, creds in core_subjects:
            c.execute("INSERT INTO subjects(subject_name, credits) VALUES (%s, %s)", (s_name, creds))
        conn.commit()
        c.execute("SELECT subject_id, subject_name FROM subjects")
        subjects = c.fetchall()

    sub_ids = [s[0] for s in subjects]

    # Clear previous student cohort records
    c.execute("DELETE FROM predictions")
    c.execute("DELETE FROM marks")
    c.execute("DELETE FROM attendance")
    c.execute("DELETE FROM performance")
    c.execute("DELETE FROM students")
    conn.commit()

    print("Populating 50 diverse student records into database...")

    students_data = []
    for i in range(50):
        first = FIRST_NAMES[i % len(FIRST_NAMES)]
        last = LAST_NAMES[(i * 3 + 7) % len(LAST_NAMES)]
        full_name = f"{first} {last}"
        
        dept = DEPARTMENTS[i % len(DEPARTMENTS)]
        semester = (i % 6) + 1  # S1 to S6
        students_data.append((full_name, dept, semester))

    c.executemany("INSERT INTO students(name, department, semester) VALUES (%s, %s, %s)", students_data)
    conn.commit()

    # Retrieve all student IDs
    c.execute("SELECT student_id, name FROM students ORDER BY student_id ASC")
    all_students = c.fetchall()

    for idx, (stu_id, name) in enumerate(all_students):
        # Academic cohort distribution:
        # High performers (30%), Average performers (45%), At-Risk performers (25%)
        mod = idx % 10
        if mod in [0, 3, 6]: # High
            tier = "High"
            base_att = random.uniform(86.0, 97.0)
            base_int = random.uniform(80.0, 96.0)
            base_assign = random.uniform(82.0, 96.0)
            base_exam = random.uniform(82.0, 98.0)
            gpa = round(random.uniform(8.3, 9.8), 2)
            grade = "A+" if gpa >= 9.0 else "A"
            pred_class = "High"
            prob = round(random.uniform(0.92, 0.99), 4)
        elif mod in [1, 4, 7, 8]: # Average
            tier = "Average"
            base_att = random.uniform(72.0, 84.0)
            base_int = random.uniform(62.0, 78.0)
            base_assign = random.uniform(65.0, 80.0)
            base_exam = random.uniform(60.0, 76.0)
            gpa = round(random.uniform(6.2, 7.8), 2)
            grade = "B+" if gpa >= 7.0 else "B"
            pred_class = "Average"
            prob = round(random.uniform(0.85, 0.95), 4)
        else: # At Risk / Low
            tier = "Low"
            base_att = random.uniform(42.0, 68.0)
            base_int = random.uniform(34.0, 52.0)
            base_assign = random.uniform(40.0, 58.0)
            base_exam = random.uniform(32.0, 50.0)
            gpa = round(random.uniform(3.8, 5.4), 2)
            grade = "C" if gpa >= 5.0 else "D"
            pred_class = "Low"
            prob = round(random.uniform(0.88, 0.98), 4)

        # Subject-wise marks and attendance
        for s_idx, sub_id in enumerate(sub_ids):
            variation = random.uniform(-4.0, 4.0)
            s_att = round(max(30.0, min(100.0, base_att + variation)), 1)
            s_int = round(max(20.0, min(100.0, base_int + variation)), 1)
            s_assign = round(max(25.0, min(100.0, base_assign + variation)), 1)
            s_exam = round(max(20.0, min(100.0, base_exam + variation)), 1)

            c.execute(
                "INSERT INTO attendance(student_id, subject_id, percentage) VALUES (%s, %s, %s)",
                (stu_id, sub_id, s_att)
            )
            c.execute(
                "INSERT INTO marks(student_id, subject_id, internal, assignment, exam) VALUES (%s, %s, %s, %s, %s)",
                (stu_id, sub_id, s_int, s_assign, s_exam)
            )

        # Performance table entry
        c.execute(
            "INSERT INTO performance(student_id, gpa, grade) VALUES (%s, %s, %s)",
            (stu_id, gpa, grade)
        )

        # Prediction table entry
        c.execute(
            "INSERT INTO predictions(student_id, predicted_class, probability) VALUES (%s, %s, %s)",
            (stu_id, pred_class, prob)
        )

    conn.commit()

    c.execute("SELECT COUNT(*) FROM students")
    print(f"Total students now in database: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM marks")
    print(f"Total marks records: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM attendance")
    print(f"Total attendance records: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM performance")
    print(f"Total performance records: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM predictions")
    print(f"Total predictions logged: {c.fetchone()[0]}")

    c.close()
    conn.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
