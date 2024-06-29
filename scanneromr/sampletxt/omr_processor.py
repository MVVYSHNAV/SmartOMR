import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import os
import csv
from utils import stackImages, rectCountour, getCornerPoints, reorder, splitBoxes, showAnswers

def process_omr(img, ans, num_questions, num_choices, widthImg, heightImg):
    if img is None:
        print("Image not loaded properly.")
        return None, None

    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    try:
        contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        rectCon = rectCountour(contours)
        if len(rectCon) < 2:
            print("Not enough rectangular contours found.")
            return imgFinal, None
        biggestContour = getCornerPoints(rectCon[0])
        gradePoints = getCornerPoints(rectCon[2])

        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours, [biggestContour], -1, (0, 255, 0), 20)
            cv2.drawContours(imgBiggestContours, [gradePoints], -1, (255, 0, 0), 20)

            biggestContour = reorder(biggestContour)
            gradePoints = reorder(gradePoints)

            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixg = cv2.getPerspectiveTransform(ptG1, ptG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixg, (325, 150))

            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

            boxes = splitBoxes(imgThresh, num_questions, num_choices)

            yPixelVal = np.zeros((num_questions, num_choices), dtype=int)
            for countR in range(num_questions):
                for countC in range(num_choices):
                    yPixelVal[countR, countC] = cv2.countNonZero(boxes[countR * num_choices + countC])

            yIndex = [np.argmax(yPixelVal[x]) for x in range(num_questions)]
            grading = [1 if ans[x] == yIndex[x] + 1 else 0 for x in range(num_questions)]
            score = (sum(grading) / num_questions) * 100
            print("Score:", score)

            imgResult = showAnswers(imgWarpColored.copy(), yIndex, grading, ans, num_questions, num_choices)
            imgRawDrawing = showAnswers(np.zeros_like(imgWarpColored), yIndex, grading, ans, num_questions, num_choices)

            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            imgRawGrade = np.zeros_like(imgGradeDisplay)
            for _ in range(5):
                cv2.putText(imgRawGrade, f"{int(score)}%", (60, 80), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 7)
            invMatrixg = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDis = cv2.warpPerspective(imgRawGrade, invMatrixg, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDis, 1, 0)

        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGray, imgBlur, imgCanny],
                      [imgContours, imgBiggestContours, imgWarpColored, imgThresh],
                      [imgResult, imgRawDrawing, imgInvWarp, imgFinal])

    except Exception as e:
        print(f"Error: {e}")
        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGray, imgBlur, imgCanny],
                      [imgBlank, imgBlank, imgBlank, imgBlank],
                      [imgBlank, imgBlank, imgBlank, imgBlank])

    labels = [["Original", "Gray", "Blur", "Canny"],
              ["Contours", "Biggest Con", "Warp", "Threshold"],
              ["Result", "Raw Drawing", "Inv Warp", "Final"]]
    imgstacked = stackImages(imageArray, 0.3, labels)

    cv2.imshow("Final Result", imgFinal)
    cv2.imshow("Stacked Images", imgstacked)
    return imgFinal, score


class OMRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OMR Scanner")
        self.num_questions = 0
        self.num_choices = 0
        self.answers = []
        self.marks = []
        self.imgFinal = None
        self.myIndex = []

        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("500x700")
        self.root.configure(bg='black')

        self.create_widgets()
        self.arrange_widgets()

    def create_widgets(self):
        label_bg = "black"
        label_fg = "white"
        button_bg = "#007BFF"
        button_fg = "#FFFFFF"
        entry_bg = "white"
        entry_fg = "black"

        self.label1 = tk.Label(self.root, text="OMRScan", font=("Helvetica", 24, "bold"), bg=label_bg, fg=label_fg)
        self.question_label = tk.Label(self.root, text="Number of Questions:", bg=label_bg, fg=label_fg)
        self.question_entry = tk.Entry(self.root, bg=entry_bg, fg=entry_fg)

        self.choice_label = tk.Label(self.root, text="Number of Choices per Question:", bg=label_bg, fg=label_fg)
        self.choice_entry = tk.Entry(self.root, bg=entry_bg, fg=entry_fg)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_details, bg=button_bg, fg=button_fg)

        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.choose_image, bg=button_bg, fg=button_fg)
        self.webcam_button = tk.Button(self.root, text="Use Webcam", command=self.use_webcam, bg=button_bg, fg=button_fg)
        self.save_button = tk.Button(self.root, text="Save Result", command=self.save_result, bg=button_bg, fg=button_fg)
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv, bg=button_bg, fg=button_fg)

        self.grade_label = tk.Label(self.root, text="", font=("Helvetica", 18), bg=label_bg, fg=label_fg)

        self.label2 = tk.Label(self.root, text="Developed @Profzer", font=("Helvetica", 10, "bold"), bg=label_bg, fg=label_fg)

    def arrange_widgets(self):
        self.label1.pack(pady=20)
        
        self.question_label.pack(pady=5)
        self.question_entry.pack(pady=5)
        
        self.choice_label.pack(pady=5)
        self.choice_entry.pack(pady=10)
        
        self.submit_button.pack(pady=20)
        
        self.upload_button.pack(pady=10)
        self.webcam_button.pack(pady=10)
        self.save_button.pack(pady=10)
        self.export_button.pack(pady=10)
        
        self.grade_label.pack(pady=20)

        self.label2.pack(pady=5)

        self.root.bind_all('<KeyPress-s>', self.save_result_keypress)

    def submit_details(self):
        try:
            self.num_questions = int(self.question_entry.get())
            self.num_choices = int(self.choice_entry.get())
            self.enter_answers_and_marks()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for questions and choices.")


    def enter_answers_and_marks(self):
        self.answers = []
        self.marks = []
        for i in range(self.num_questions):
            while True:
                try:
                    answer = simpledialog.askinteger("Input", f"Answer for question {i+1}: (1-{self.num_choices})")
                    if answer is not None and 1 <= answer <= self.num_choices:
                        self.answers.append(answer)
                        break
                    else:
                        messagebox.showerror("Input Error", f"Please enter a number between 1 and {self.num_choices}.")
                except ValueError:
                    messagebox.showerror("Input Error", f"Please enter a valid number between 1 and {self.num_choices}.")
            while True:
                try:
                    mark = simpledialog.askinteger("Input", f"Marks for question {i+1}:")
                    if mark is not None and mark > 0:
                        self.marks.append(mark)
                        break
                    else:
                        messagebox.showerror("Input Error", f"Please enter a positive number for marks.")
                except ValueError:
                    messagebox.showerror("Input Error", f"Please enter a valid positive number for marks.")

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
                    cv2.imshow("Webcam", img)
                    self.process_image(img) 

                    key = cv2.waitKey(1)
                    if key == ord('q') or key == 27:
                        break
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
            self.imgFinal, score = process_omr(img, self.answers, self.num_questions, self.num_choices, widthImg, heightImg)
            
            if self.imgFinal is not None:
                cv2.imshow("Final Result", self.imgFinal)  
                
                if score is not None:
                    self.grade_label.config(text=f"Grade: {score:.2f}%", bg="black", fg="white")
                else:
                    self.grade_label.config(text="Grade: Not available", bg="black", fg="white")
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
