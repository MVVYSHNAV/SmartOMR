import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import csv
import time
from omr_processing import process_omr

class OMRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartOMR")
        self.num_questions = 0
        self.num_choices = 0
        self.answers = []
        self.marks = []
        self.imgFinal = None
        self.myIndex = []

        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("500x700")
        self.root.configure(bg='#381466')  # Background color based on the provided reference image

        self.create_widgets()
        self.arrange_widgets()

    def create_widgets(self):
        # Colors and styles based on the provided reference image
        label_bg = "#381466"
        label_fg = "white"
        button_bg = "#b932c5"
        button_fg = "#FFFFFF"
        entry_bg = "white"
        entry_fg = "black"

        self.label1 = tk.Label(self.root, text="SmartOMR", font=("Helvetica", 24, "bold"), bg=label_bg, fg=label_fg)
        self.question_label = tk.Label(self.root, text="Number of Questions:", bg=label_bg, fg=label_fg)
        self.question_entry = tk.Entry(self.root, bg=entry_bg, fg=entry_fg)

        self.choice_label = tk.Label(self.root, text="Number of Choices per Question:", bg=label_bg, fg=label_fg)
        self.choice_entry = tk.Entry(self.root, bg=entry_bg, fg=entry_fg)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_details, bg=button_bg, fg=button_fg)

        self.upload_button = tk.Button(self.root, text="Upload Answer Sheet", command=self.choose_image, bg=button_bg, fg=button_fg)
        self.upload_answers_button = tk.Button(self.root, text="Upload Answers", command=self.upload_answers, bg=button_bg, fg=button_fg)
        self.save_button = tk.Button(self.root, text="Save Result", command=self.save_result, bg=button_bg, fg=button_fg)
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv, bg=button_bg, fg=button_fg)

        self.grade_label = tk.Label(self.root, text="", font=("Helvetica", 18), bg=label_bg, fg=label_fg)

        self.answer_entries = []
        self.mark_entries = []

    def arrange_widgets(self):
        # Positioning the widgets based on the provided reference image
        self.label1.place(x=190, y=50)  # Title

        self.question_label.place(x=50, y=150)
        self.question_entry.place(x=250, y=150, width=200, height=30)

        self.choice_label.place(x=50, y=200)
        self.choice_entry.place(x=250, y=200, width=200, height=30)

        self.submit_button.place(x=200, y=250, width=100, height=40)

        self.upload_answers_button.place(x=100, y=320, width=300, height=40)
        self.upload_button.place(x=100, y=370, width=300, height=40)
        self.save_button.place(x=100, y=420, width=300, height=40)
        self.export_button.place(x=100, y=470, width=300, height=40)

        self.grade_label.place(x=200, y=540)  # Grade label

        self.root.bind_all('<KeyPress-s>', self.save_result_keypress)

    def submit_details(self):
        try:
            self.num_questions = int(self.question_entry.get())
            self.num_choices = int(self.choice_entry.get())
            self.display_answer_mark_entries()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for questions and choices.")

    def display_answer_mark_entries(self):
        # Clear previous entries
        for entry in self.answer_entries + self.mark_entries:
            entry.destroy()
        self.answer_entries.clear()
        self.mark_entries.clear()

        for i in range(self.num_questions):
            answer_label = tk.Label(self.root, text=f"Answer for Q{i+1}:", bg="#381466", fg="white")
            answer_label.place(x=50, y=280 + i*50)
            answer_entry = tk.Entry(self.root, bg="white", fg="black")
            answer_entry.place(x=200, y=280 + i*50, width=50, height=30)
            self.answer_entries.append(answer_entry)

            mark_label = tk.Label(self.root, text=f"Marks for Q{i+1}:", bg="#381466", fg="white")
            mark_label.place(x=270, y=280 + i*50)
            mark_entry = tk.Entry(self.root, bg="white", fg="black")
            mark_entry.place(x=400, y=280 + i*50, width=50, height=30)
            self.mark_entries.append(mark_entry)

        submit_answers_button = tk.Button(self.root, text="Submit Answers", command=self.save_answers_and_marks, bg="#b932c5", fg="white")
        submit_answers_button.place(x=200, y=280 + self.num_questions*50, width=100, height=30)

    def save_answers_and_marks(self):
        try:
            self.answers = [int(entry.get()) for entry in self.answer_entries]
            self.marks = [int(entry.get()) for entry in self.mark_entries]
            messagebox.showinfo("Success", "Answers and marks have been saved.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for answers and marks.")

    def choose_image(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                img = cv2.imread(file_path)
                if img is not None:
                    self.process_image(img)
                else:
                    messagebox.showerror("File Error", "Could not read the image file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def upload_answers(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                with open(file_path, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    self.answers = []
                    self.marks = []
                    for row in reader:
                        self.answers.append(int(row[1]))
                        self.marks.append(int(row[2]))
                messagebox.showinfo("Upload Success", "Answers and marks uploaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_image(self, img):
        try:
            widthImg = 700
            heightImg = 700
            self.imgFinal, score = process_omr(img, self.answers, self.num_questions, self.num_choices, widthImg, heightImg)
            
            if self.imgFinal is not None:
                cv2.imshow("Final Result", self.imgFinal)
                
                if score is not None:
                    self.grade_label.config(text=f"Grade: {score:.2f}%", bg="#381466", fg="white")
                else:
                    self.grade_label.config(text="Grade: Not available", bg="#381466", fg="white")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def export_to_csv(self):
        if self.imgFinal is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if save_path:
                try:
                    with open(save_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Question", "Correct Answer", "User Answer", "Marks"])
                        for i in range(self.num_questions):
                            writer.writerow([i+1, self.answers[i], self.myIndex[i], self.marks[i]])
                    messagebox.showinfo("Export Success", f"Results exported to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while exporting: {e}")
            else:
                messagebox.showwarning("Export Canceled", "Export operation canceled.")
        else:
            messagebox.showerror("Export Error", "No result image to export.")

    def save_result(self, event=None):
        try:
            if self.imgFinal is not None:
                folder_path = "results"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                timestamp = int(time.time())
                save_path = os.path.join(folder_path, f"finalResult_{timestamp}.jpg")
                
                cv2.imwrite(save_path, self.imgFinal)
                messagebox.showinfo("Save Success", f"Result saved as {save_path}")
            else:
                messagebox.showerror("Save Error", "No result image to save.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_result_keypress(self, event):
        if event.char == 's':
            self.save_result()

if __name__ == "__main__":
    root = tk.Tk()
    app = OMRApp(root)
    root.mainloop()
