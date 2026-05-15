import unittest
import sqlite3
import your_code  # Korvaa 'your_code' koodisi tiedoston nimellä
import os
import time

class TestStudentDatabase(unittest.TestCase):

    def setUp(self):
        # Initialize the database and test data
        self.conn = sqlite3.connect("test_students.db")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            -- Create a test database and tables
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                contact TEXT,
                ssn TEXT,
                student_number TEXT,
                image_path TEXT
            );
            -- Add a test user
            INSERT INTO students (name, contact, ssn, student_number, image_path)
            VALUES ('Test Student', 'test@example.com', '123-45-6789', 'S12345', 'test_image.png');
        """)

    def tearDown(self):
        # Close the database and remove the test database file
        self.conn.close()
        # Remove the test database
        os.remove("test_students.db")

    def test_login_successful(self):
        # Test successful login with correct username and password
        username = "admin"
        password = "password"
        result = your_code.login(username, password)
        self.assertEqual(result, "Login successful.")

    def test_login_incorrect_credentials(self):
        # Test login with incorrect username and password
        username = "wrong_user"
        password = "wrong_password"
        result = your_code.login(username, password)
        self.assertEqual(result, "Incorrect username or password. Please try again.")

    def test_add_student_success(self):
        # Test adding a student to the database successfully
        name = "Test Student 2"
        contact = "test2@example.com"
        ssn = "987-65-4321"
        student_number = "S54321"
        image_path = "test_image2.png"
        result = your_code.add_student(name, contact, ssn, student_number, image_path)
        self.assertEqual(result, "Student added to the database.")

    def test_search_student_found(self):
        # Test searching for a student when the student is found
        name = "Test Student"
        result = your_code.search_student(name)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Test Student")
        
def test_login_brute_force_lockout(self):
    # Test that login locks out after 5 failed attempts
    import time
    username = "admin"
    wrong_password = "wrongpassword"

    start_time = time.time()

    for i in range(5):
        result = your_code.login(username, wrong_password)
        self.assertEqual(result, f"Incorrect username or password. Attempt {i+1}/5.")

    elapsed_time = time.time() - start_time

    # After 5 attempts there should be a delay of at least 30 seconds
    self.assertGreaterEqual(elapsed_time, 30)


if __name__ == '__main__':
    unittest.main()







