# Vulnerability Report - No Input Validation for Student Data
## Summary
The program accepts student information directly from user input without cheking wether the values are valid.

## Affected Code 
- `add _Student()`
- `add_grades()`
  
## Problem 
The fields `student_number`, `name`, `contact`, `ssn`, `course`, and `grade` are accepted without validation.

## Example Invalid Inputs
- Empty student name
- Invalid SSN such as `abc123`
- Invalid grade such as `999`
- Very long text values
- Contact information in the wrong format

## Risk 
Invalid or unexpected data can be stored in the database, which can make student records unreliable and may cause erros later 

## Suggested Fix 
Add validation checks before saving data, suchas checking empty fields, SSN format, grade range, and input length. 
