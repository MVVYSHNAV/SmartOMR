import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import csv
import time
from omr_processing import process_omr  # Ensure this is properly implemented

class OMRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartOMR")
        self.num_questions = 0
        self.num_choices = 0
        self.answers = []
        self.mark = 1  # Default mark for each question
        self.imgFinal = None
        self.myIndex = []
        self.score = None
        self.correct_answers_count = 0

        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("500x700")
        self.root.configure(bg='#381466')

        self.create_widgets()
        self.arrange_widgets()

    def create_widgets(self):
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

        self.mark_label = tk.Label(self.root, text="Mark per Question:", bg=label_bg, fg=label_fg)
        self.mark_entry = tk.Entry(self.root, bg=entry_bg, fg=entry_fg)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_details, bg=button_bg, fg=button_fg)

        self.upload_button = tk.Button(self.root, text="Upload Answer Sheet", command=self.choose_image, bg=button_bg, fg=button_fg)
        self.use_webcam_button = tk.Button(self.root, text="Use Webcam", command=self.use_webcam, bg=button_bg, fg=button_fg)
        self.save_button = tk.Button(self.root, text="Save Result", command=self.save_result, bg=button_bg, fg=button_fg)
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv, bg=button_bg, fg=button_fg)

        self.grade_label = tk.Label(self.root, text="", font=("Helvetica", 18), bg=label_bg, fg=label_fg)

    def arrange_widgets(self):
        self.label1.place(x=190, y=50)

        self.question_label.place(x=50, y=150)
        self.question_entry.place(x=250, y=150, width=200, height=30)

        self.choice_label.place(x=50, y=200)
        self.choice_entry.place(x=250, y=200, width=200, height=30)

        self.mark_label.place(x=50, y=250)
        self.mark_entry.place(x=250, y=250, width=200, height=30)

        self.submit_button.place(x=200, y=300, width=100, height=40)

        self.use_webcam_button.place(x=100, y=370, width=300, height=40)
        self.upload_button.place(x=100, y=420, width=300, height=40)
        self.save_button.place(x=100, y=470, width=300, height=40)
        self.export_button.place(x=100, y=520, width=300, height=40)

        self.grade_label.place(x=200, y=590)

        self.root.bind_all('<KeyPress-s>', self.save_result_keypress)

    def submit_details(self):
        try:
            self.num_questions = int(self.question_entry.get())
            self.num_choices = int(self.choice_entry.get())
            self.mark = int(self.mark_entry.get())
            self.enter_answers()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for questions, choices, and mark.")

    def enter_answers(self):
        self.answers = []
        for i in range(self.num_questions):
            answer = self.custom_input_dialog(f"Answer for question {i+1}: (1-{self.num_choices})", 1, self.num_choices)
            if answer is not None:
                self.answers.append(answer)
            else:
                return

    def custom_input_dialog(self, prompt, min_val, max_val):
        dialog = tk.Toplevel(self.root)
        dialog.title("Input")

        label_bg = "#381466"
        label_fg = "white"
        button_bg = "#b932c5"
        button_fg = "#FFFFFF"
        entry_bg = "white"
        entry_fg = "black"

        dialog.configure(bg=label_bg)

        tk.Label(dialog, text=prompt, bg=label_bg, fg=label_fg).pack(pady=20)
        entry = tk.Entry(dialog, bg=entry_bg, fg=entry_fg)
        entry.pack(pady=5)

        result = [None]

        def on_submit():
            try:
                value = int(entry.get())
                if min_val <= value <= max_val:
                    result[0] = value
                    dialog.destroy()
                else:
                    messagebox.showerror("Input Error", f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                messagebox.showerror("Input Error", f"Please enter a valid number between {min_val} and {max_val}.")

        submit_button = tk.Button(dialog, text="Submit", command=on_submit, bg=button_bg, fg=button_fg)
        submit_button.pack(pady=10)

        self.root.wait_window(dialog)
        return result[0]

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

    def use_webcam(self):
        try:
            cap = cv2.VideoCapture(0)
            cap.set(10, 150) 

            while True:
                success, img = cap.read()
                if success:
                    # cv2.imshow("Webcam", img)
                    self.process_image(img) 

                    key = cv2.waitKey(1)
                    key = cv2.waitKey(1)
                    if key == ord('q') or key == 27:
                        break
                    elif key == ord('s'):
                        self.save_result_from_webcam()
                else:
                    messagebox.showerror("Camera Error", "Failed to capture image from webcam.")

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def process_image(self, img):
        try:
            widthImg = 700
            heightImg = 700
            marks = [self.mark] * self.num_questions
            self.imgFinal, self.score, self.myIndex, self.correct_answers_count = process_omr(img, self.answers, self.num_questions, self.num_choices, marks, widthImg, heightImg)
            
            if self.imgFinal is not None:
                cv2.imshow("Final Result", self.imgFinal)
                
                if self.score is not None:
                    grade_text = f"Grade: {self.score:.2f}%\nCorrect Answers: {self.correct_answers_count}/{self.num_questions}\nTotal Score: {self.correct_answers_count * self.mark}"
                    self.grade_label.config(text=grade_text, bg="#381466", fg="white")
                else:
                    self.grade_label.config(text="Grade: Not available", bg="#381466", fg="white")
                    
                self.root.update_idletasks()  # Ensure the label is updated immediately
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def export_to_csv(self):
        if self.imgFinal is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if save_path:
                try:
                    with open(save_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Question", "Correct Answer", "User Answer", "Marks"])
                        for i in range(self.num_questions):
                            writer.writerow([i + 1, self.answers[i], self.myIndex[i], self.mark])

                        # Write total score information
                        writer.writerow([])  # Blank row for separation
                        writer.writerow(["Total Score", "", "", self.correct_answers_count * self.mark])

                    messagebox.showinfo("Export Success", f"Results exported to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while exporting: {e}")
            else:
                messagebox.showwarning("Export Canceled", "Export operation canceled.")
        else:
            messagebox.showerror("Export Error", "No result image to export.")

    def save_result_from_webcam(self):
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
