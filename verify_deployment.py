import os
import sys
import unittest

class TestDeploymentReadiness(unittest.TestCase):
    def setUp(self):
        from app import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_01_app_import_and_wsgi(self):
        from app import app
        self.assertIsNotNone(app)
        self.assertEqual(app.name, "app")

    def test_02_model_exists_and_loads(self):
        import joblib
        from app import MODEL_PATH
        self.assertTrue(os.path.exists(MODEL_PATH), f"Model file not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        self.assertIsNotNone(model)

    def test_03_login_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign In", response.data)
        self.assertIn(b"/signup", response.data)

    def test_03b_signup_page_renders(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create Account", response.data)
        self.assertIn(b"Sign Up", response.data)

    def test_03c_signup_flow_and_validation(self):
        import database.db as db_mod
        test_user = "testuser_reg"

        # Clean up any leftover test user
        conn = db_mod.get_db()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = %s", (test_user,))
        conn.commit()
        c.close()
        conn.close()

        # Test password mismatch
        mismatch_res = self.client.post("/signup", data={
            "username": test_user,
            "password": "password123",
            "confirm_password": "password456"
        })
        self.assertEqual(mismatch_res.status_code, 200)
        self.assertIn(b"Passwords do not match", mismatch_res.data)

        # Test successful signup
        success_res = self.client.post("/signup", data={
            "username": test_user,
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=False)
        self.assertEqual(success_res.status_code, 302)
        self.assertTrue(success_res.headers["Location"].startswith("/") and "success=" in success_res.headers["Location"])

        # Test duplicate username rejection
        duplicate_res = self.client.post("/signup", data={
            "username": test_user,
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(duplicate_res.status_code, 200)
        self.assertIn(b"Username already exists", duplicate_res.data)

        # Test login with newly created user
        login_res = self.client.post("/", data={
            "username": test_user,
            "password": "password123"
        }, follow_redirects=False)
        self.assertEqual(login_res.status_code, 302)
        self.assertIn("/dashboard", login_res.headers["Location"])

        # Clean up test user
        conn = db_mod.get_db()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = %s", (test_user,))
        conn.commit()
        c.close()
        conn.close()

    def test_04_admin_login(self):
        response = self.client.post("/", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
        # Should redirect to /dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

    def test_05_dashboard_access_with_session(self):
        with self.client.session_transaction() as sess:
            sess["user"] = "admin"
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Performance Analytics", response.data)

    def test_06_students_page_access(self):
        with self.client.session_transaction() as sess:
            sess["user"] = "admin"
        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)

    def test_07_prediction_model_inference(self):
        with self.client.session_transaction() as sess:
            sess["user"] = "admin"
        # Test predict endpoint with sample features
        payload = {
            "student_id": "1",
            "attendance": "85.0",
            "internal": "42.0",
            "assignment": "18.0",
            "gpa": "8.5",
            "failures": "0"
        }
        response = self.client.post("/predict", data=payload)
        self.assertEqual(response.status_code, 200)
        # Check prediction result returned in template
        self.assertTrue(b"Prediction Result" in response.data or b"Pass" in response.data or b"predicted_class" in response.data or b"%" in response.data)

    def test_08_sqlite_mode_operations(self):
        import database.db as db_mod
        original_engine = db_mod._DB_ENGINE
        try:
            db_mod._DB_ENGINE = "sqlite"
            db_mod.init_db()
            conn = db_mod.get_db()
            c = conn.cursor()
            c.execute("INSERT INTO students(name, department, semester) VALUES (%s, %s, %s)", ("Test Student", "CSE", 4))
            conn.commit()
            c.execute("SELECT student_id, name FROM students WHERE name = %s", ("Test Student",))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[1], "Test Student")
            c.execute("DELETE FROM students WHERE name = %s", ("Test Student",))
            conn.commit()
            conn.close()
        finally:
            db_mod._DB_ENGINE = original_engine

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDeploymentReadiness)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
