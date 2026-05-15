import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

st.title("📄 Student PDF Report Generator")

st.write("Enter student details below to generate a PDF report.")

# Input form
name = st.text_input("Student Name")
math = st.number_input("Math Marks", min_value=0, max_value=100)
cs = st.number_input("Computer Science Marks", min_value=0, max_value=100)

students = []

if st.button("Add Student"):
    if name:
        students.append({"name": name, "math": math, "cs": cs})
        st.success(f"{name} added!")
    else:
        st.warning("Please enter a name")

# Store session data (important for Streamlit)
if "data" not in st.session_state:
    st.session_state.data = []

if st.button("Save Student"):
    if name:
        st.session_state.data.append({
            "name": name,
            "math": math,
            "cs": cs
        })
        st.success("Student saved!")

# Show table
if st.session_state.data:
    st.subheader("📊 Student Data")
    st.table(st.session_state.data)

# PDF Generator function
def generate_pdf(data, filename="report.pdf"):
    pdf = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Student Report Card")

    pdf.setFont("Helvetica", 12)
    y = 750

    for student in data:
        total = student["math"] + student["cs"]

        pdf.drawString(100, y, f"Name: {student['name']}")
        pdf.drawString(250, y, f"Math: {student['math']}")
        pdf.drawString(350, y, f"CS: {student['cs']}")
        pdf.drawString(450, y, f"Total: {total}")

        y -= 30

    pdf.save()
    return filename

# Generate PDF button
if st.button("Generate PDF Report"):
    if st.session_state.data:
        file = generate_pdf(st.session_state.data)

        with open(file, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name="student_report.pdf",
                mime="application/pdf"
            )
        st.success("PDF generated successfully!")
    else:
        st.warning("No data to generate PDF")
