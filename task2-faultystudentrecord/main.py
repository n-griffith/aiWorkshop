import sqlite3
import os
import hashlib
import secrets
from getpass import getpass

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create students table
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_number TEXT PRIMARY KEY,
                    name TEXT,
                    contact TEXT,
                    ssn TEXT,
                    image_path TEXT
                )''')

# Create grades table
cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY,
                    student_id TEXT,
                    course TEXT,
                    grade TEXT,
                    FOREIGN KEY (student_id) REFERENCES students (student_number)
                )''')

# Create users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

conn.commit()

# Create image directory
if not os.path.exists("images"):
    os.mkdir("images")


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    try:
        salt, stored_hash = stored_password.split("$")
        return hash_password(password, salt) == stored_password
    except ValueError:
        return False


def create_admin_if_needed():
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        print("No users found. Create an admin account.")

        username = input("Create admin username: ").strip()

        while not username:
            print("Username cannot be empty.")
            username = input("Create admin username: ").strip()

        password = getpass("Create admin password: ")

        while len(password) < 8:
            print("Password must be at least 8 characters long.")
            password = getpass("Create admin password: ")

        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        print("Admin account created successfully.")


def login():
    while True:
        username = input("Enter username: ").strip()
        password = getpass("Enter password: ")

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and verify_password(password, user[0]):
            print("Login successful.")
            break
        else:
            print("Incorrect username or password. Please try again.")


def add_student():
    student_number = input("Enter student number: ")
    name = input("Enter student name: ")
    contact = input("Enter student contact information: ")
    ssn = input("Enter student SSN: ")

    image_path = input("Enter the image file name (e.g., student_card.png, press Enter to skip): ")

    if image_path:
        image_path = os.path.join("images", image_path)

        if not os.path.exists(image_path):
            print("Image file not found. Student added without an image.")
            image_path = None

    cursor.execute(
        "INSERT INTO students (student_number, name, contact, ssn, image_path) VALUES (?, ?, ?, ?, ?)",
        (student_number, name, contact, ssn, image_path)
    )

    conn.commit()
    print("Student added to the database.")


def add_grades():
    student_number = input("Enter the student number of the student to add grades for: ")
    course = input("Enter course name: ")
    grade = input("Enter the grade: ")

    cursor.execute("SELECT student_number FROM students WHERE student_number = ?", (student_number,))
    student_id = cursor.fetchone()

    if student_id:
        cursor.execute(
            "INSERT INTO grades (student_id, course, grade) VALUES (?, ?, ?)",
            (student_number, course, grade)
        )
        conn.commit()
        print("Grade added successfully.")
    else:
        print("Student not found.")


def search_student():
    student_number = input("Enter the student number of the student to search for: ")

    cursor.execute("SELECT * FROM students WHERE student_number = ?", (student_number,))
    student = cursor.fetchone()

    if student:
        print("Student found:")
        print(f"Student Number: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Contact: {student[2]}")
        print(f"SSN: {student[3]}")
        print(f"Image Path: {student[4]}")
    else:
        print("Student not found.")


def display_all_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if students:
        print("All students:")

        for student in students:
            print(f"Student Number: {student[0]}")
            print(f"Name: {student[1]}")
            print(f"Contact: {student[2]}")
            print(f"SSN: {student[3]}")
            print(f"Image Path: {student[4]}")
            print()
    else:
        print("No students in the database.")


def upload_image():
    student_number = input("Enter the student number (image will be associated with this student): ")
    image_file = input("Enter the image file name (e.g., student_card.png): ")

    image_path = os.path.join("images", image_file)

    if os.path.exists(image_path):
        cursor.execute(
            "UPDATE students SET image_path = ? WHERE student_number = ?",
            (image_path, student_number)
        )
        conn.commit()
        print("Image uploaded and associated with the student.")
    else:
        print("Image file not found.")


def download_student_image():
    student_number = input("Enter the student number of the student whose image you want to download: ")

    cursor.execute("SELECT image_path FROM students WHERE student_number = ?", (student_number,))
    image_path = cursor.fetchone()

    if image_path:
        image_path = image_path[0]

        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                image_data = f.read()

            new_image_name = input("Enter a new file name for the image (e.g., downloaded_image.png): ")

            with open(new_image_name, "wb") as f:
                f.write(image_data)

            print(f"Image downloaded as '{new_image_name}'.")
        else:
            print("Image not found on the server.")
    else:
        print("Student not found.")


def main():
    create_admin_if_needed()
    login()

    while True:
        print("\nSelect an action:")
        print("1. Add a student")
        print("2. Add grades for a student")
        print("3. Search for a student by student number")
        print("4. Display all students")
        print("5. Upload an image for a student")
        print("6. Download a student's image")
        print("7. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grades()
        elif choice == "3":
            search_student()
        elif choice == "4":
            display_all_students()
        elif choice == "5":
            upload_image()
        elif choice == "6":
            download_student_image()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
