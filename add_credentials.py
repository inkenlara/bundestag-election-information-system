import os

# Prompt the user for input
host = input("Enter the database host: ")
port = input("Enter the database port: ")
name = input("Enter the database name: ")
user = input("Enter the database user: ")
password = input("Enter the database password: ")

# Create the file and write the inputs to it
with open("db_credentials.txt", "w") as f:
    f.write(host + "\n")
    f.write(port + "\n")
    f.write(name + "\n")
    f.write(user + "\n")
    f.write(password + "\n")
print("Credentials saved successfully in db_credentials.txt")
