# Vulnerability Report - Directory traversal arbitrary file write

## Description

I identified a potential security vulnerability in main.py.

I am committed to working with you to help resolve this issue. In this report you will find everything you need to effectively coordinate a resolution of the issue.

If at any point you have concerns or questions about this process, please do not hesitate to reach out to me.

If you are NOT the correct point of contact for this report, please let me know!

## Summary

The program allows the user to choose any filename when downloading a student's image. The filename is not checked before being used, so a user can enter a path such as "../../hacked.txt" and make the program write a file outside the intended folder.

## Product

aiWorkshop > task2-faultystudentrecord > main.py

## Tested Version

Version on main branch

## Details

The vulnerability is in the download_student_image() function.

The vulnerable code is:

new_image_name = input("Enter a new file name for the image (e.g., downloaded_image.png): ")
with open(new_image_name, "wb") as f:
    f.write(image_data)

The value of new_image_name comes directly from user input. The program does not check whether the filename contains path traversal patterns like "../". Because of this, the user can choose a path outside the current folder.

For example, entering "../../hacked.txt" causes the file to be written outside the task2-faultystudentrecord folder.

## PoC

Open the task2-faultystudentrecord folder.

Create a demo file inside the images folder:

mkdir -p images
echo "test file" > images/demo.txt

Run the program:

python main.py

Log in with the default credentials:

Username: admin
Password: password

Choose option 1 to add a student.

Enter example student information:

Student number: 456
Student name: Test Student
Contact: test@example.com
SSN: 111-22-3333
Image file name: demo.txt

Choose option 6 to download a student's image.

Enter the student number:

456

When asked for a new filename, enter:

../../hacked.txt

The program says the image was downloaded as "../../hacked.txt". This shows that the program wrote a file outside the intended folder.

## Impact

A user can write files outside the expected directory. Depending on file permissions, this could allow a user to overwrite source code, configuration files, or other files that the program has access to.

## Remediation

Only allow safe filenames when downloading images.

The program should reject filenames that contain "../" or absolute paths. It should also force downloaded files to be saved inside a specific safe folder.

A safer approach would be to use os.path.basename() to remove directory paths from the filename, or check the resolved absolute path before writing the file.

## Credit

Malak El Qochairi

## Contact

https://github.com/MalQoch

## Disclosure Policy

The Group #5 research team is dedicated to working closely with the open source community and with projects that are affected by a vulnerability, in order to protect users and ensure a coordinated disclosure.

Our disclosure deadline for publicly disclosing a vulnerability is: 90 days after the first report to the project team.