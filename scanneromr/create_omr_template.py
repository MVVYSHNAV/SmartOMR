import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def create_omr_template(num_questions, num_choices, college_name, exam_name, filename="omr_template.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = 0.5 * inch
    bubble_diameter = 0.25 * inch
    spacing = 0.35 * inch
    question_number_width = 1.0 * inch
    bubble_width = (num_choices * spacing) + (0.5 * inch)
    questions_per_column = 10
    num_columns = (num_questions - 1) // questions_per_column + 1

    # Draw the outer border
    border_margin = 0.3 * inch
    c.setLineWidth(2)
    c.rect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin)

    # Draw the college and exam name fields
    c.setLineWidth(1)
    c.drawString(margin, height - margin, "College:")
    c.rect(margin + 1.2 * inch, height - margin - 0.2 * inch, 3 * inch, 0.3 * inch)
    c.drawString(margin + 1.25 * inch, height - margin - 0.15 * inch, college_name)

    c.drawString(margin + 4.5 * inch, height - margin, "Exam:")
    c.rect(margin + 5.5 * inch, height - margin - 0.2 * inch, 2 * inch, 0.3 * inch)
    c.drawString(margin + 5.55 * inch, height - margin - 0.15 * inch, exam_name)

    # Draw the name and date fields
    c.drawString(margin, height - margin - 0.5 * inch, "Name :")
    c.rect(margin + 1.5 * inch, height - margin - 0.7 * inch, 2 * inch, 0.3 * inch)
    c.drawString(width - margin - 2.5 * inch, height - margin - 0.5 * inch, "Date :")
    c.rect(width - margin - 1.5 * inch, height - margin - 0.7 * inch, 1.5 * inch, 0.3 * inch)

    # Draw the question number and bubble containers
    for col in range(num_columns):
        question_number_x = margin + (question_number_width + bubble_width + 0.2 * inch) * col
        question_number_y_start = height - margin - 1.5 * inch
        container_height = min(questions_per_column, num_questions - col * questions_per_column) * 0.5 * inch
        c.rect(question_number_x, question_number_y_start - container_height, question_number_width, container_height)
        bubbles_x = question_number_x + question_number_width + 0.1 * inch
        c.rect(bubbles_x, question_number_y_start - container_height, bubble_width, container_height)

        # Draw the question numbers and bubbles
        for i in range(min(questions_per_column, num_questions - col * questions_per_column)):
            y_pos = question_number_y_start - (i + 1) * 0.5 * inch + 0.2 * inch
            question_index = col * questions_per_column + i + 1
            c.drawString(question_number_x + 0.2 * inch, y_pos, str(question_index))
            for j in range(num_choices):
                x_pos = bubbles_x + j * spacing + 0.2 * inch
                c.circle(x_pos, y_pos, bubble_diameter / 2)
                c.drawString(x_pos - bubble_diameter / 4, y_pos - bubble_diameter / 4, chr(65 + j))

    # Draw the mark field near the bubbles
    mark_field_y = question_number_y_start - container_height - 2.5 * inch
    c.drawString(margin, mark_field_y, "Mark:")
    c.rect(margin + 0.5 * inch, mark_field_y - 0.2 * inch, 2 * inch, 0.3 * inch)

    c.save()

def save_template():
    try:
        num_questions = int(num_questions_entry.get())
        if num_questions > 20:
            raise ValueError("Maximum number of questions allowed is 20.")
        
        num_choices = int(num_choices_entry.get())
        college_name = college_name_entry.get()
        exam_name = exam_name_entry.get()
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            create_omr_template(num_questions, num_choices, college_name, exam_name, filename)
            status_label.config(text="OMR template created successfully!", foreground="green")
            root.after(2000, root.destroy)  # Close the application after 2 seconds
    except ValueError as ve:
        status_label.config(text=str(ve), foreground="red")
    except Exception as e:
        status_label.config(text="An error occurred: " + str(e), foreground="red")

# Create the main application window
root = tk.Tk()
root.title("OMR Template Generator")
root.configure(bg="black")

# Set window size
root.geometry("500x500")

# Create a style for the labels and entries
style = ttk.Style()
style.configure("TLabel", background="black", foreground="white")
style.configure("TEntry", fieldbackground="black", foreground="black", selectbackground="blue", selectforeground="white")
style.configure("TButton", background="blue", foreground="blue", padding=6)

# Create and place the widgets
college_name_label = ttk.Label(root, text="College Name:")
college_name_label.pack(pady=10)
college_name_entry = ttk.Entry(root, width=40)
college_name_entry.pack(pady=5)

exam_name_label = ttk.Label(root, text="Exam Name:")
exam_name_label.pack(pady=10)
exam_name_entry = ttk.Entry(root, width=40)
exam_name_entry.pack(pady=5)

num_questions_label = ttk.Label(root, text="Number of Questions (Max 20):")
num_questions_label.pack(pady=10)
num_questions_entry = ttk.Entry(root)
num_questions_entry.pack(pady=5)

num_choices_label = ttk.Label(root, text="Number of Choices per Question:")
num_choices_label.pack(pady=10)
num_choices_entry = ttk.Entry(root)
num_choices_entry.pack(pady=5)

save_button = ttk.Button(root, text="Save OMR Template", command=save_template)
save_button.pack(pady=20)

status_label = ttk.Label(root, text="", background="black", foreground="white")
status_label.pack(pady=10)

# Start the application
root.mainloop()
