# Vulnerability Report - Unlimited Login Attemps / Brute Force Risk

## Summary 
The login sysytem allows users to try password unlimited times without any limit.

## Affected Code 
- `login()`

## The problem 
The program uses a `while True` loop for login attempts and does not stop users after many failed tries. 

## Example Attacks 
An attacker can keep trying password such as:
- `123456`
- `password`
- ` admin`

Until the correct password is guessed.

## Risk
Attackers may gain unauthorized access by repeatedly guessing passwords.

## Suggested Fix 
Add a limit for a failed login attemps or add a waiting time after serveral failed tries. 
