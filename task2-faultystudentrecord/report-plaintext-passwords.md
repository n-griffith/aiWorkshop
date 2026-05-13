# Vulnerability Report: Plaintext Password Storage

## Vulnerability
Passwords are stored in plaintext in the database.

## Location
File: `main.py`

The vulnerable code is:

```python
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')
