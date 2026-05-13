# Vulnerability Report - Plaintext Password Storage

## Description
I identified potential security vulnerabilities in main.py.

I am committed to working with you to help resolve these issues. In this report you will find everything you need to effectively coordinate a resolution of these issues.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

## Summary
The application stores user passwords in plaintext inside the SQLite database. Any user with access to the database file can directly read all stored passwords.

## Product
aiWorkshop > main.py

## Tested Version
Version on main branch

## Details
```python
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')
The password field stores passwords directly without hashing or encryption. This means sensitive credentials are exposed if the SQLite database file is accessed.

PoC

Open main.py file.

Run the program.

Create a user account.

Open the generated SQLite database file using any SQLite viewer or command-line tool.

Execute:

SELECT username, password FROM users;

All stored passwords will be visible in plaintext.

Impact

Anyone with access to the database file can read all user passwords. This may lead to unauthorized access, credential theft, account compromise, and password reuse attacks on other services.

Remediation

Passwords should never be stored in plaintext.

Use secure password hashing algorithms such as:

bcrypt
Argon2
PBKDF2

Implement salted password hashing before storing credentials in the database.

Restrict database file access permissions.

Credit

Pedro Douetts Pedrosa

Contact

https://github.com/pedrodouettts-byte
