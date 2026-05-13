# Vulnerability Report - Hardcoded default credentials

## Description
I identified potential security vulnerabilities in main.py.

I am committed to working with you to help resolve these issues. In this report you will find everything you need to effectively coordinate a resolution of these issues.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

## Summary
The file contains hardcoded default credentials stored in plain text. The credentials are stored in the database each time the program is run, so anyone can access to the source code to log in.

## Product
aiWorkshop > main.py

## Tested Version
Version on main branch

## Details
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))

The line runs every time, each attempt is stored in the database in the user's table. If the username and password are changed as an example to "newadmin" and "newpassword", those new credentials will also be stored in the database table. Log in then will work with old and new credentials.

## PoC
Open main.py file
Run the program
To log in enter username as "admin" and password as "password"
Credentials are accepted and you are logged in.
If you exit and run the program again, credentials will continue to work and are added as a new row. If changing the username and password in the code, it will accept new and old credentials. Database will reflect both as many times as they are input.

## Impact
Anyone who can access to the source code can log into the application.

## Remediation
1. Remove hardcoded credentials.
2. Prompt the user to set up an admin account on first run.
3. Passwords should be hashed before storing.

## Credit
Nicolle Griffith Gonzalez

## Contact
https://github.com/n-griffith

## Disclosure Policy
The Group #5 research team is dedicated to working closely with the open source community and with projects that are affected by a vulnerability, in order to protect users and ensure a coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.

** Note for assignment purposes:
I am the owner of the repository. So I do not have the option of "Report a vulnerability" in Security and quality > Advisories. Only option was "New draft security advisory". I created this report under that option, it shows as a draft.