# Vulnerability Report - No Input Validation for Student Data

## Description

l identified a potential security vulnerability in main.py.

I am committed to working with you to help resolve this issue. In this report you will find everything you need to effectively coordinate a resolution of the issue.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.
If you are NOT the correct point of contact for this report, please let me know!

---

## Summary

Several fields in the application, including student number, name, contact information, SSN, course, and grade, are accepted directly from user input without proper validation checks. The application does not check whether the entered values are empty, written in the wrong format, too long, or outside the expected range before saving them to the database.
The functions used to add student information and grades allow invalid or unexpected data to be stored in the system. Because of this, student records may become unreliable and could cause errors or unexpected problems in other parts of the application.

---

## Product
aiWorkshop > task2-faultystudentrecord › main.py

---

## Tested Version
Version on main branch

---

## Details

The functions `add_student()` and `add_grades()` accept user input without properly validating the information before saving it to the database.

The application does not check:
- empty values
- invalid formats
- very long inputs
- invalid grade ranges

This allows incorrect or unexpected data to be saved in the database.

---

## PoC

Example invalid inputs accepted by the application:
- Empty student name
- Invalid SSN: `abc123`
- Invalid grade: `999`
- Extremely long text values
- Invalid contact information format

---

## Impact

Attackers or users may store invalid or unexpected data in the system because the application does not properly validate user input.

This can make student records unreliable and may lead to errors, inconsistent records, or unexpected behavior in other parts of the application and the system over time.

---

## Remediation

Add validation checks before saving data, for example:
- check that required fields are not empty
- validate SSN format
- limit input length
- check that grade values are within a valid range
- validate contact information format

---

## Credit

Farah Ahmed Hasan

---

## Contact

https://github.com/Faa208

---

## Disclosure Policy

The Group #5 research team is dedicated to working closely with the
open source community and with projects that are affected by vulnerabilities in order to protect users
and ensure coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.

