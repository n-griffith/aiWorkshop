# Vulnerability Report - No Input Validation for Student Data

## Description

The application accepts student information directly from user input without validating the values. Invalid or unsafe data can be stored in the system.

---

## Summary

Several fields such as student number, name, contact information, SSN, course, and grade are accepted without validation checks.

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

## Proof of Concept (PoC)

Example invalid inputs accepted by the application:
- Empty student name
- Invalid SSN: `abc123`
- Invalid grade: `999`
- Extremely long text values
- Invalid contact information format

---

## Impact

Attackers or users may store incorrect or invalid data in the system.

This can make student records unreliable and may cause problems later in the application.

---

## Remediation

Add validation checks before saving data, for example:
- check that required fields are not empty
- validate SSN format
- limit input length
- check valid grade ranges
- validate contact information format

---

## Credit

Reported by: Farah Ahmed Hasan

---

## Contact



---

## Disclosure Policy

The Group #5 research team is dedicated to working closely with the
open source community and with projects that are affected by vulnerabilities in order to protect users
and ensure coordinated disclosure.
Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.

