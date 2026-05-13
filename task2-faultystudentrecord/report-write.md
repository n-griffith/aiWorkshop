# Directory Traversal Vulnerability - Arbitrary File Write

## Summary

The program lets the user choose any filename when downloading a student's image. Because the filename is not checked, it is possible to use paths like ../../hacked.txt to save the file outside the project folder.

## Severity

High

## Where the problem is

In main.py, inside the download_student_image() function, the program asks the user for a new filename and then writes to that filename directly:

new_image_name = input("Enter a new file name for the image (e.g., downloaded_image.png): ")
with open(new_image_name, "wb") as f:
f.write(image_data)

The value entered by the user is passed directly to open() without any validation.

## How to reproduce
Run the program with:

python main.py

Log in using:

Username: admin
Password: password

Add a student and use an existing file (demo.txt) as the image.
Choose option 6, which is "Download a student's image".
Enter the student's number.
When asked for a new filename, enter:

../../hacked.txt

The program saves the file outside the current folder.

## What happens

The file is written to a location chosen by the user instead of being restricted to a safe directory.

## Why this is a problem

A malicious user could overwrite files that the program has permission to access. This could include source code, configuration files, or other important files.

## Suggested fix

Only allow normal filenames without ../ and save all downloaded files to a specific folder.