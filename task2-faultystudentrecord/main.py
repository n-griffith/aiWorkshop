import sqlite3
import os
import hashlib
import secrets
import re
import shutil
from getpass import getpass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
DB_PATH = os.path.join(BASE_DIR, "students.db")

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    ssn TEXT NOT NULL,
                    image_path TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    course TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (student_number)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


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


def is_safe_filename(filename):
    filename = filename.strip()
    basename = os.path.basename(filename)

    if filename != basename:
        return False

    if ".." in filename or "/" in filename or "\\" in filename:
        return False

    extension = os.path.splitext(filename)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


def get_safe_image_path(filename):
    if not is_safe_filename(filename):
        return None

    image_path = os.path.abspath(os.path.join(IMAGES_DIR, filename))

    if not image_path.startswith(IMAGES_DIR + os.sep):
        return None

    return image_path


def validate_student_number(student_number):
    return bool(re.fullmatch(r"[A-Za-z0-9-]{1,20}", student_number))


def validate_name(name):
    return bool(name.strip()) and len(name.strip()) <= 100


def validate_contact(contact):
    return bool(contact.strip()) and len(contact.strip()) <= 100


def validate_ssn(ssn):
    return bool(re.fullmatch(r"[A-Za-z0-9-]{4,20}", ssn))


def validate_grade(grade):
    valid_grades = {"0", "1", "2", "3", "4", "5", "pass", "fail"}
    return grade.strip().lower() in valid_grades


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
    student_number = input("Enter student number: ").strip()
    name = input("Enter student name: ").strip()
    contact = input("Enter student contact information: ").strip()
    ssn = input("Enter student SSN: ").strip()

    if not validate_student_number(student_number):
        print("Invalid student number.")
        return

    if not validate_name(name):
        print("Invalid student name.")
        return

    if not validate_contact(contact):
        print("Invalid contact information.")
        return

    if not validate_ssn(ssn):
        print("Invalid SSN.")
        return

    image_path = None
    image_file = input("Enter the image file name (e.g., student_card.png, press Enter to skip): ").strip()

    if image_file:
        safe_path = get_safe_image_path(image_file)

        if safe_path and os.path.exists(safe_path):
            image_path = safe_path
        else:
            print("Invalid or missing image file. Student added without an image.")

    try:
        cursor.execute(
            "INSERT INTO students (student_number, name, contact, ssn, image_path) VALUES (?, ?, ?, ?, ?)",
            (student_number, name, contact, ssn, image_path)
        )
        conn.commit()
        print("Student added to the database.")
    except sqlite3.IntegrityError:
        print("Student number already exists.")


def add_grades():
    student_number = input("Enter the student number of the student to add grades for: ").strip()
    course = input("Enter course name: ").strip()
    grade = input("Enter the grade: ").strip()

    if not validate_student_number(student_number):
        print("Invalid student number.")
        return

    if not course or len(course) > 100:
        print("Invalid course name.")
        return

    if not validate_grade(grade):
        print("Invalid grade.")
        return

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
    student_number = input("Enter the student number of the student to search for: ").strip()

    cursor.execute("SELECT * FROM students WHERE student_number = ?", (student_number,))
    student = cursor.fetchone()

    if student:
        print("Student found:")
        print(f"Student Number: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Contact: {student[2]}")
        print("SSN: [hidden]")
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
            print("SSN: [hidden]")
            print(f"Image Path: {student[4]}")
            print()
    else:
        print("No students in the database.")


def upload_image():
    student_number = input("Enter the student number (image will be associated with this student): ").strip()
    image_file = input("Enter the image file name (e.g., student_card.png): ").strip()

    safe_path = get_safe_image_path(image_file)

    if not safe_path:
        print("Invalid image filename.")
        return

    if not os.path.exists(safe_path):
        print("Image file not found.")
        return

    cursor.execute("SELECT student_number FROM students WHERE student_number = ?", (student_number,))
    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        return

    cursor.execute("UPDATE students SET image_path = ? WHERE student_number = ?", (safe_path, student_number))
    conn.commit()
    print("Image uploaded and associated with the student.")


def download_student_image():
    student_number = input("Enter the student number of the student whose image you want to download: ").strip()

    cursor.execute("SELECT image_path FROM students WHERE student_number = ?", (student_number,))
    image_path = cursor.fetchone()

    if not image_path:
        print("Student not found.")
        return

    image_path = image_path[0]

    if not image_path or not os.path.exists(image_path):
        print("Image not found on the server.")
        return

    real_image_path = os.path.abspath(image_path)

    if not real_image_path.startswith(IMAGES_DIR + os.sep):
        print("Invalid image path.")
        return

    new_image_name = input("Enter a new file name for the image (e.g., downloaded_image.png): ").strip()

    if not is_safe_filename(new_image_name):
        print("Invalid download filename.")
        return

    destination_path = os.path.abspath(os.path.join(DOWNLOADS_DIR, new_image_name))

    if not destination_path.startswith(DOWNLOADS_DIR + os.sep):
        print("Invalid download path.")
        return

    shutil.copyfile(real_image_path, destination_path)
    print(f"Image downloaded safely to '{destination_path}'.")


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

        choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()

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
