Vulnerability Report - Plaintext Password Storage
Description
I identified a potential security vulnerability in main.py.

I am committed to working with you to help resolve this issue. In this report you will find everything needed to effectively coordinate a resolution of the issue.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

Summary
Passwords are stored in plaintext in the SQLite database without hashing or encryption. Any user with access to the database file can read credentials directly.

Product
aiWorkshop > task2-faultystudentrecord > main.py

Tested Version
Version on main branch

Details
The vulnerability is located in the database table creation for user credentials.

The vulnerable code stores passwords directly in the database without hashing or encryption.

The password field stores passwords directly without hashing or encryption. This means sensitive credentials are exposed if the SQLite database file is accessed.

PoC
Open the task2-faultystudentrecord folder.

Run the program.

Create a new user account or log in with existing credentials.

Open the generated SQLite database file using any SQLite viewer or command-line tool.

Inspect the users table.

The password values are visible in plaintext.

Impact
Anyone with access to the SQLite database file can obtain user credentials directly. Depending on password reuse, this could lead to unauthorized access, credential theft, or compromise of additional systems.

Remediation
Passwords should never be stored in plaintext.

Use secure password hashing algorithms such as bcrypt, Argon2, or PBKDF2 before storing credentials in the database.

Access to the SQLite database file should also be restricted to authorized users only.

Credit
Pedro Douetts Pedrosa

Contact
https://github.com/pedrodouettts-byte

Disclosure Policy
The Group #5 research team is dedicated to working closely with the open source community and with projects that are affected by vulnerabilities in order to protect users and ensure coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.
