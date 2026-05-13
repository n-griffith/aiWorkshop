# Vulnerability Report - Plaintext Password Storage

## Description

I identified a security vulnerability in `main.py`.

I am committed to working with you to help resolve this issue. In this report you will find everything needed to understand and reproduce the vulnerability.

If at any point you have concerns or questions about this process, please do not hesitate to reach out.

If you are NOT the correct point of contact for this report, please let me know.

## Summary

Passwords are stored in plaintext in the SQLite database without hashing or encryption. Any user with access to the database file can read credentials directly.

## Product

aiWorkshop > task2-faultystudentrecord > main.py

## Tested Version

Version on main branch

## Details

```python
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')
