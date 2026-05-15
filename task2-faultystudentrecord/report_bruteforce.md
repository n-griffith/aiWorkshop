# Vulnerability Report - Unlimited Login Attempts (Brute Force Vulnerability)

## Description

I identified a potential security vulnerability in main.py.

I am committed to working with you to help resolve this issue. In this report you will find everything needed to effectively coordinate a resolution of the issue.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

## Summary

The login function allows unlimited password attempts with no delay, lockout, or rate limiting. An attacker can automate credential guessing at full hardware speed until a valid password is found.

## Product

aiWorkshop > task2-faultystudentrecord > main.py

## Tested Version

Version on main branch

## Details

The vulnerability is located in the `login()` function in main.py.

```python
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
```

On a failed login, the function immediately loops back and prompts again with no delay and no limit on the number of attempts. There is no account lockout, no exponential backoff, and no logging of failed attempts. This means an attacker can attempt as many passwords as they like, as fast as the system allows.

## PoC

1. Run the program.
2. At the login prompt, enter a valid username (e.g. the admin account created on first run).
3. Enter an incorrect password. Observe that the program immediately prompts again with no delay.
4. Repeat steps 2–3 continuously — there is no lockout, no cooldown, and no error threshold.
5. An attacker can script this loop to try thousands of passwords per second until the correct one is found.

## Impact

An attacker with access to the program can perform an unlimited brute force or dictionary attack against any account. The minimum password length of 8 characters provides limited protection on its own without rate limiting. Given enough time, any password can be recovered. A successful attack gives full access to all student records, including sensitive personal data such as SSNs.

## Remediation

- Add a delay between failed login attempts (e.g. 2–5 seconds), increasing with each consecutive failure (exponential backoff).
- Lock an account temporarily after a set number of consecutive failures (e.g. 5 attempts), requiring a wait period or admin reset before retrying.
- Log all failed login attempts, including the timestamp and username, to allow detection of ongoing attacks.
- Consider a maximum attempts counter per session that exits the program after repeated failures.

## Credit

Victor andres cardenas

## Contact

https://github.com/Victor-tietoturva

## Disclosure Policy

The Group #5 research team is dedicated to working closely with the open source community and with projects that are affected by vulnerabilities in order to protect users and ensure coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.