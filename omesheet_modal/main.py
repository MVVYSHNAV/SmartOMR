import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import messagebox
from utils import stackImages, rectCountour, getCornerPoints, reorder, splitBoxes, showAnswers

class OMRScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("OMR Scanner")
        self.root.geometry("800x600")

        self.num_questions = 0
        self.num_choices = 0
        self.ans = []

        self.create_widgets()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="Enter number of questions:")
        self.question_label.pack()

        self.question_entry = tk.Entry(self.root)
        self.question_entry.pack()

        self.choice_label = tk.Label(self.root, text="Enter number of choices per question:")
        self.choice_label.pack()

        self.choice_entry = tk.Entry(self.root)
        self.choice_entry.pack()

        self.answer_label = tk.Label(self.root, text="Enter correct answers (separated by commas):")
        self.answer_label.pack()

        self.answer_entry = tk.Entry(self.root)
        self.answer_entry.pack()

        self.scan_button = tk.Button(self.root, text="Scan OMR Sheet", command=self.scan_omr)
        self.scan_button.pack()

        self.score_label = tk.Label(self.root, text="Score: ")
        self.score_label.pack()

    def scan_omr(self):
        self.num_questions = int(self.question_entry.get())
        self.num_choices = int(self.choice_entry.get())
        self.ans = list(map(int, self.answer_entry.get().split(',')))

        widthImg = 700
        heightImg = 700

        cap = cv2.VideoCapture(0)  # Use laptop camera
        ret, img = cap.read()
        if not ret:
            messagebox.showerror("Error", "Unable to capture image from camera.")
            return

        imgFinal = self.process_omr(img, self.ans, self.num_questions, self.num_choices, widthImg, heightImg)

        score = self.calculate_score(imgFinal)
        self.score_label.config(text=f"Score: {score}%")

    def process_omr(self, img, ans, num_questions, num_choices, widthImg, heightImg):
        # Your OMR processing code here
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
                return imgFinal
            biggestContour = getCornerPoints(rectCon)
            gradePoints = getCornerPoints(rectCon)

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
                imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)

                boxes = splitBoxes(imgThresh, num_questions, num_choices)

                yPixelVal = np.zeros((num_questions, num_choices), dtype=int)

                for countR in range(num_questions):
                    for countC in range(num_choices):
                        yPixelVal[countR, countC] = cv2.countNonZero(boxes[countR * num_choices + countC])

                yIndex = [np.argmax(yPixelVal[x]) for x in range(num_questions)]

                grading = [1 if ans[x] == yIndex[x] + 1 else 0 for x in range(num_questions)]  # Correcting index offset
                score = (sum(grading) / num_questions) * 100
                print("Score:", score)

                imgResult = showAnswers(imgWarpColored.copy(), yIndex, grading, ans, num_questions, num_choices)
                imgRawDrawing = showAnswers(np.zeros_like(imgWarpColored), yIndex, grading, ans, num_questions, num_choices)

                invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
                imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

                imgRawGrade = np.zeros_like(imgGradeDisplay)
                cv2.putText(imgRawGrade, f"{int(score)}%", (60, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (215, 255, 0), 1)
                invMatrixg = cv2.getPerspectiveTransform(ptG2, ptG1)
                imgInvGradeDis = cv2.warpPerspective(imgRawGrade, invMatrixg, (widthImg, heightImg))

                imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
                imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDis, 1, 0)

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
        return imgFinal

    def calculate_score(self, imgFinal):
        # Your score calculation code here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = OMRScanner(root)
    root.mainloop()