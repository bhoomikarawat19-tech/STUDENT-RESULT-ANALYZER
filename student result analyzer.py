# Student Result Analyzer 

students = []


# Function to calculate grade
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# Number of students
n = int(input("Enter number of students: "))


# Taking student details
for i in range(n):
    print("\nStudent", i + 1)

    name = input("Enter name: ")

    python = float(input("Enter Python marks: "))
    c = float(input("Enter C marks: "))
    java = float(input("Enter Java marks: "))

    total = python + c + java
    percentage = (total / 300) * 100

    # Pass if marks in every subject are >= 40
    if python >= 40 and c >= 40 and java >= 40:
        status = "PASS"
    else:
        status = "FAIL"

    grade = calculate_grade(percentage)

    student = {
        "name": name,
        "python": python,
        "c": c,
        "java": java,
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "status": status
    }

    students.append(student)


# Display results
print("\n*********** STUDENT RESULT ***********")

for student in students:
    print("\nName:", student["name"])
    print("Python:", student["python"])
    print("C:", student["c"])
    print("Java:", student["java"])
    print("Total:", student["total"], "/ 300")
    print("Percentage:", round(student["percentage"], 2), "%")
    print("Grade:", student["grade"])
    print("Status:", student["status"])


# Class average
total_percentage = 0

for student in students:
    total_percentage += student["percentage"]

average = total_percentage / n

print("\n*********** CLASS AVERAGE ***********")
print("Class Average:", round(average, 2), "%")


# Highest scorer
highest = students[0]

for student in students:
    if student["percentage"] > highest["percentage"]:
        highest = student

print("\nHighest Scorer:", highest["name"])
print("Highest Percentage:", round(highest["percentage"], 2), "%")


# ------------------------------------------------
# FILE HANDLING
# ------------------------------------------------

with open("student_results.txt", "w") as file:

    file.write("*********** STUDENT RESULT ***********\n")

    for student in students:
        file.write("\nName: " + student["name"] + "\n")
        file.write("Python: " + str(student["python"]) + "\n")
        file.write("C: " + str(student["c"]) + "\n")
        file.write("Java: " + str(student["java"]) + "\n")
        file.write("Total: " + str(student["total"]) + " / 300\n")
        file.write("Percentage: " +
                   str(round(student["percentage"], 2)) + "%\n")
        file.write("Grade: " + student["grade"] + "\n")
        file.write("Status: " + student["status"] + "\n")

    file.write("\n*********** CLASS AVERAGE ***********\n")
    file.write("Class Average: " + str(round(average, 2)) + "%\n")

    file.write("\nHighest Scorer: " + highest["name"] + "\n")
    file.write("Highest Percentage: " +
               str(round(highest["percentage"], 2)) + "%\n")


print("\nResults have been saved to student_results.txt")
import os
print("File saved at:", os.path.abspath("student_results.txt"))