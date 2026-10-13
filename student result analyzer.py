
import customtkinter as ctk
import csv
import os
import qrcode
import subprocess
import sys

from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# ******************************************
# 1. PROJECT SETTINGS
# ******************************************

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "students.csv")
CERTIFICATE_DIR = os.path.join(BASE_DIR, "certificates")
QR_DIR = os.path.join(BASE_DIR, "qr_codes")

FIELDS = [
    "Name",
    "Roll Number",
    "Python",
    "C",
    "Java",
    "Percentage",
    "Grade"
]

os.makedirs(CERTIFICATE_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)


# ******************************************
# 2. INITIALIZE CSV FILE
# ******************************************

def initialize_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


initialize_file()


# ******************************************
# 3. GET AND VALIDATE STUDENT DATA
# ******************************************

def get_student_data():
    name = name_entry.get().strip()
    roll_number = roll_entry.get().strip()
    python_marks = python_entry.get().strip()
    c_marks = c_entry.get().strip()
    java_marks = java_entry.get().strip()

    if not name or not roll_number:
        messagebox.showerror(
            "Input Error",
            "Please enter the student's name and roll number."
        )
        return None

    if not all([python_marks, c_marks, java_marks]):
        messagebox.showerror(
            "Input Error",
            "Please enter marks for all three subjects."
        )
        return None

    try:
        python_marks = float(python_marks)
        c_marks = float(c_marks)
        java_marks = float(java_marks)

    except ValueError:
        messagebox.showerror(
            "Invalid Marks",
            "Please enter valid numeric marks."
        )
        return None

    marks = [python_marks, c_marks, java_marks]

    if any(mark < 0 or mark > 100 for mark in marks):
        messagebox.showerror(
            "Invalid Marks",
            "Marks must be between 0 and 100."
        )
        return None

    total = sum(marks)
    percentage = total / 3

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    status = "Pass" if all(mark >= 40 for mark in marks) else "Fail"

    return {
        "Name": name,
        "Roll Number": roll_number,
        "Python": python_marks,
        "C": c_marks,
        "Java": java_marks,
        "Total": total,
        "Percentage": percentage,
        "Grade": grade,
        "Status": status
    }


# ******************************************
# 4. FORMAT RESULT FOR DISPLAY
# ******************************************

def format_result(student):
    return (
        f"Name: {student['Name']}\n"
        f"Roll Number: {student['Roll Number']}\n"
        f"Python Marks: {student['Python']}\n"
        f"C Marks: {student['C']}\n"
        f"Java Marks: {student['Java']}\n"
        f"Total Marks: {student['Total']}/300\n"
        f"Percentage: {student['Percentage']:.2f}%\n"
        f"Grade: {student['Grade']}\n"
        f"Status: {student['Status']}"
    )


# ******************************************
# 5. CALCULATE RESULT
# ******************************************

def calculate_result():
    student = get_student_data()

    if student is None:
        return

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.insert("end", format_result(student))
    result_box.configure(state="disabled")


# ******************************************
# 6. SAVE STUDENT RECORD
# ******************************************

def save_student():
    student = get_student_data()

    if student is None:
        return

    # Check whether the roll number already exists.
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Roll Number"].strip().lower() == (
                student["Roll Number"].strip().lower()
            ):
                messagebox.showerror(
                    "Duplicate Roll Number",
                    "This roll number already exists.\n"
                    "Please use a different roll number."
                )
                return

    # Save only the required fields.
    saved_student = {
        "Name": student["Name"],
        "Roll Number": student["Roll Number"],
        "Python": student["Python"],
        "C": student["C"],
        "Java": student["Java"],
        "Percentage": f"{student['Percentage']:.2f}",
        "Grade": student["Grade"]
    }

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow(saved_student)

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.insert(
        "end",
        format_result(student) + "\n\nRecord saved successfully!"
    )
    result_box.configure(state="disabled")

    messagebox.showinfo(
        "Success",
        "Student record saved successfully!"
    )


# ******************************************
# 7. VIEW ALL SAVED STUDENTS
# ******************************************

def view_all_students():
    if not os.path.exists(CSV_FILE):
        messagebox.showinfo("No Records", "No student records found.")
        return

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        students = list(reader)

    if not students:
        messagebox.showinfo(
            "No Records",
            "There are no saved student records."
        )
        return

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")

    for student in students:
        result_box.insert(
            "end",
            f"Name: {student['Name']}\n"
            f"Roll Number: {student['Roll Number']}\n"
            f"Python: {student['Python']}\n"
            f"C: {student['C']}\n"
            f"Java: {student['Java']}\n"
            f"Percentage: {student['Percentage']}%\n"
            f"Grade: {student['Grade']}\n"
            f"{'*' * 35}\n"
        )

    result_box.configure(state="disabled")


# ******************************************
# 8. SEARCH STUDENT BY ROLL NUMBER
# ******************************************

def search_student():
    roll_number = roll_entry.get().strip()

    if not roll_number:
        messagebox.showerror(
            "Input Error",
            "Please enter a roll number in the Roll Number field."
        )
        return

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Roll Number"].strip().lower() == roll_number.lower():
                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "end",
                    f"Name: {row['Name']}\n"
                    f"Roll Number: {row['Roll Number']}\n"
                    f"Python Marks: {row['Python']}\n"
                    f"C Marks: {row['C']}\n"
                    f"Java Marks: {row['Java']}\n"
                    f"Percentage: {row['Percentage']}%\n"
                    f"Grade: {row['Grade']}"
                )

                result_box.configure(state="disabled")
                return

    messagebox.showinfo(
        "Not Found",
        "No student found with this roll number."
    )


# ******************************************
# 9. CLEAR INPUT FIELDS
# ******************************************

def clear_fields():
    name_entry.delete(0, "end")
    roll_entry.delete(0, "end")
    python_entry.delete(0, "end")
    c_entry.delete(0, "end")
    java_entry.delete(0, "end")

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.configure(state="disabled")

    name_entry.focus()


# ******************************************
# 10. CLEAR SAVED STUDENT RECORDS
# ******************************************

def clear_saved_results():
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        "Are you sure you want to delete all saved student records?\n\n"
        "Certificates and QR code images will not be deleted."
    )

    if not confirm:
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.configure(state="disabled")

    messagebox.showinfo(
        "Success",
        "All saved student records have been cleared.\n"
        "Certificates and QR codes are safe."
    )


# ******************************************
# 11. GENERATE QR CODE
# ******************************************

def generate_qr_code(student):
    roll_number = student["Roll Number"]

    qr_text = (
        f"Student Name: {student['Name']}\n"
        f"Roll Number: {roll_number}\n"
        f"Percentage: {student['Percentage']:.2f}%"
    )

    qr_image = qrcode.make(qr_text)

    safe_roll = "".join(
        character for character in roll_number
        if character.isalnum() or character in ("-", "_")
    )

    qr_path = os.path.join(
        QR_DIR,
        f"QR_{safe_roll}.png"
    )

    qr_image.save(qr_path)

    return qr_path


# ******************************************
# 12. GENERATE CERTIFICATE PDF
# ******************************************

def generate_certificate():
    student = get_student_data()

    if student is None:
        return

    safe_roll = "".join(
        character for character in student["Roll Number"]
        if character.isalnum() or character in ("-", "_")
    )

    certificate_path = os.path.join(
        CERTIFICATE_DIR,
        f"Certificate_{safe_roll}.pdf"
    )

    # Generate the QR code.
    qr_path = generate_qr_code(student)

    # Create the certificate PDF.
    pdf = canvas.Canvas(
        certificate_path,
        pagesize=A4
    )

    page_width, page_height = A4

    # Certificate border.
    pdf.setLineWidth(3)
    pdf.rect(
        35,
        35,
        page_width - 70,
        page_height - 70
    )

    pdf.setLineWidth(1)
    pdf.rect(
        45,
        45,
        page_width - 90,
        page_height - 90
    )

    # Certificate heading.
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 120,
        "STUDENT RESULT CERTIFICATE"
    )

    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 155,
        "Academic Performance Record"
    )

    pdf.line(
        100,
        page_height - 175,
        page_width - 100,
        page_height - 175
    )

    # Only the requested student details are displayed.
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 235,
        f"Student Name: {student['Name']}"
    )

    pdf.drawCentredString(
        page_width / 2,
        page_height - 280,
        f"Roll Number: {student['Roll Number']}"
    )

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 335,
        f"Percentage: {student['Percentage']:.2f}%"
    )

    # Add QR code to the certificate.
    qr_image = ImageReader(qr_path)

    qr_size = 120

    pdf.drawImage(
        qr_image,
        (page_width - qr_size) / 2,
        page_height - 510,
        width=qr_size,
        height=qr_size
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 535,
        "Scan the QR code to view student details."
    )

    pdf.save()

    messagebox.showinfo(
        "Certificate Generated",
        f"Certificate saved successfully!\n\n{certificate_path}"
    )


# ******************************************
# 13. VIEW SAVED CERTIFICATES
# ******************************************

def view_saved_certificates():
    if not os.path.exists(CERTIFICATE_DIR):
        messagebox.showinfo(
            "No Certificates",
            "The certificates folder does not exist."
        )
        return

    certificates = sorted(
        filename
        for filename in os.listdir(CERTIFICATE_DIR)
        if filename.lower().endswith(".pdf")
    )

    if not certificates:
        messagebox.showinfo(
            "No Certificates",
            "No saved certificates were found."
        )
        return

    # Create a window listing all saved certificates.
    certificate_window = ctk.CTkToplevel(app)
    certificate_window.title("Saved Certificates")
    certificate_window.geometry("550x450")

    heading = ctk.CTkLabel(
        certificate_window,
        text="Saved Certificates",
        font=("Arial", 22, "bold")
    )
    heading.pack(pady=15)

    certificate_list = ctk.CTkScrollableFrame(
        certificate_window,
        width=480,
        height=320
    )
    certificate_list.pack(padx=15, pady=10, fill="both", expand=True)

    def open_certificate(filename):
        path = os.path.join(CERTIFICATE_DIR, filename)

        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])

        except Exception as error:
            messagebox.showerror(
                "Open Error",
                f"Could not open the certificate.\n{error}"
            )

    for filename in certificates:
        row = ctk.CTkFrame(certificate_list)
        row.pack(fill="x", padx=5, pady=5)

        label = ctk.CTkLabel(
            row,
            text=filename,
            anchor="w"
        )
        label.pack(
            side="left",
            padx=8,
            pady=8,
            fill="x",
            expand=True
        )

        button = ctk.CTkButton(
            row,
            text="Open",
            width=80,
            command=lambda name=filename: open_certificate(name)
        )
        button.pack(side="right", padx=8, pady=5)


# ******************************************
# 14. GUI SETUP
# ******************************************

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Student Result Analyzer")
app.geometry("850x800")
app.minsize(750, 700)

heading = ctk.CTkLabel(
    app,
    text="STUDENT RESULT ANALYZER",
    font=("Arial", 27, "bold")
)
heading.pack(pady=15)


# ******************************************
# 15. INPUT FORM
# ******************************************

input_frame = ctk.CTkFrame(app)
input_frame.pack(padx=20, pady=10, fill="x")

name_label = ctk.CTkLabel(
    input_frame,
    text="Student Name"
)
name_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter student name",
    width=250
)
name_entry.grid(row=0, column=1, padx=10, pady=8)

roll_label = ctk.CTkLabel(
    input_frame,
    text="Roll Number"
)
roll_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

roll_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter roll number",
    width=250
)
roll_entry.grid(row=1, column=1, padx=10, pady=8)

python_label = ctk.CTkLabel(
    input_frame,
    text="Python Marks"
)
python_label.grid(row=2, column=0, padx=10, pady=8, sticky="w")

python_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Marks out of 100",
    width=250
)
python_entry.grid(row=2, column=1, padx=10, pady=8)

c_label = ctk.CTkLabel(
    input_frame,
    text="C Marks"
)
c_label.grid(row=3, column=0, padx=10, pady=8, sticky="w")

c_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Marks out of 100",
    width=250
)
c_entry.grid(row=3, column=1, padx=10, pady=8)

java_label = ctk.CTkLabel(
    input_frame,
    text="Java Marks"
)
java_label.grid(row=4, column=0, padx=10, pady=8, sticky="w")

java_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Marks out of 100",
    width=250
)
java_entry.grid(row=4, column=1, padx=10, pady=8)


# ******************************************
# 16. BUTTONS
# ******************************************

button_frame = ctk.CTkFrame(app)
button_frame.pack(padx=20, pady=10, fill="x")

calculate_button = ctk.CTkButton(
    button_frame,
    text="Calculate Result",
    command=calculate_result
)
calculate_button.grid(row=0, column=0, padx=8, pady=8)

save_button = ctk.CTkButton(
    button_frame,
    text="Save Student",
    command=save_student
)
save_button.grid(row=0, column=1, padx=8, pady=8)

view_button = ctk.CTkButton(
    button_frame,
    text="View All Students",
    command=view_all_students
)
view_button.grid(row=0, column=2, padx=8, pady=8)

search_button = ctk.CTkButton(
    button_frame,
    text="Search Student",
    command=search_student
)
search_button.grid(row=1, column=0, padx=8, pady=8)

clear_fields_button = ctk.CTkButton(
    button_frame,
    text="Clear Fields",
    command=clear_fields
)
clear_fields_button.grid(row=1, column=1, padx=8, pady=8)

clear_records_button = ctk.CTkButton(
    button_frame,
    text="Clear Saved Results",
    command=clear_saved_results
)
clear_records_button.grid(row=1, column=2, padx=8, pady=8)

certificate_button = ctk.CTkButton(
    button_frame,
    text="Generate Certificate",
    command=generate_certificate
)
certificate_button.grid(row=2, column=0, padx=8, pady=8)

view_certificates_button = ctk.CTkButton(
    button_frame,
    text="View Saved Certificates",
    command=view_saved_certificates
)
view_certificates_button.grid(row=2, column=1, padx=8, pady=8)


# ******************************************
# 17. RESULT DISPLAY
# ******************************************

result_label = ctk.CTkLabel(
    app,
    text="Student Result",
    font=("Arial", 18, "bold")
)
result_label.pack(pady=(10, 5))

result_box = ctk.CTkTextbox(
    app,
    width=650,
    height=200,
    font=("Consolas", 14)
)
result_box.pack(padx=20, pady=10, fill="both", expand=True)

result_box.configure(state="disabled")


# ******************************************
# 18. KEYBOARD SHORTCUTS
# ******************************************

# Press Enter to save the student record.
app.bind("<Return>", lambda event: save_student())

# Keep the cursor in the first input field when the app starts.
name_entry.focus()


# ******************************************
# 19. RUN APPLICATION
# ******************************************

app.mainloop()

