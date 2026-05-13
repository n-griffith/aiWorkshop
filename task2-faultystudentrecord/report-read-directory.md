# Vulnerability Report - Directory traversal arbitrary file read

## Description

I identified a potential security vulnerability in main.py.

I am committed to working with you to help resolve this issue. In this report you will find everything you need to effectively coordinate a resolution of the issue.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

## Summary

The program is supposed to use image files from the images folder, but the image filename is not properly checked. Because of this, a user can enter a path such as "../secret.txt" and make the program read a file outside the intended images folder.

## Product

aiWorkshop > task2-faultystudentrecord > main.py

## Tested Version

Version on main branch

## Details

The vulnerability starts in the add_student() function.

The vulnerable code is:

image_path = os.path.join("images", image_path)

The program joins the user-provided image filename with the images folder, but it does not check whether the final path actually stays inside that folder.

Later, in download_student_image(), the program reads the saved image path directly:

with open(image_path, "rb") as f:
    image_data = f.read()

Because of this, a path like "../secret.txt" becomes "images/../secret.txt", which points outside the images folder.

## PoC

Open the task2-faultystudentrecord folder.

Create a test file outside the images folder:

echo "this file is outside the images folder" > secret.txt

Run the program:

python main.py

Log in with the default credentials:

Username: admin

Password: password

Choose option 1 to add a student.

Enter example student information:

Student number: 789

Student name: Read Test

Contact: read@test.com

SSN: 111-22-3333

Image file name: ../secret.txt

The program stores the path as images/../secret.txt, which points outside the images folder.

Choose option 6 to download a student's image.

Enter the student number: 789

When asked for a new filename, enter:

stolen-secret.txt

Exit the program.

Check the downloaded file:

cat stolen-secret.txt

The file contains:

this file is outside the images folder

This shows that the program read a file outside the intended images directory.

## Impact

A user can read files outside the expected images folder. Depending on file permissions, this could expose source code, configuration files, database files, or other sensitive information that the program can access.

## Remediation

The program should validate the final resolved path before reading the file.

It should reject filenames that contain "../" or absolute paths. It should also check that the absolute path stays inside the intended images folder before opening the file.

## Credit

Malak El Qochairi

## Contact

https://github.com/MalQoch

## Disclosure Policy

The Group #5 research team is dedicated to working closely with the open source community and with projects that are affected by a vulnerability, in order to protect users and ensure a coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.