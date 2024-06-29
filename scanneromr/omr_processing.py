
import cv2
import numpy as np
from utils import stackImages, rectCountour, getCornerPoints, reorder, splitBoxes, showAnswers


def process_omr(img, ans, num_questions, num_choices, marks, widthImg, heightImg):
    try:
        if img is None:
            print("Image not loaded properly.")
            return None, None, None, None

        img = cv2.resize(img, (widthImg, heightImg))
        imgContours = img.copy()
        imgFinal = img.copy()
        imgBiggestContours = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 50)

        contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        rectCon = rectCountour(contours)
        if len(rectCon) < 2:
            print("Not enough rectangular contours found.")
            return imgFinal, None, None, None

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

            # Calculate correct answers count
            correct_answers_count = sum(1 for i in range(num_questions) if ans[i] == yIndex[i] + 1)

            # Calculate the total marks
            total_marks = sum(marks)

            # Calculate the score based on answers and total marks
            total_score = sum(marks[i] for i in range(num_questions) if ans[i] == yIndex[i] + 1)

            score_percentage = (total_score / total_marks) * 100
            print("Total Score:", total_score)
            print("Score Percentage:", score_percentage)

            imgResult = showAnswers(imgWarpColored.copy(), yIndex, ans, num_questions, num_choices, marks)
            imgRawDrawing = showAnswers(np.zeros_like(imgWarpColored), yIndex, ans, num_questions, num_choices, marks)

            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade, f"{int(score_percentage)}%", (60, 80), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 7)
            invMatrixg = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDis = cv2.warpPerspective(imgRawGrade, invMatrixg, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDis, 1, 0)

        else:
            print("Failed to detect required contours.")
            return imgFinal, None, None, None

        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGray, imgBlur, imgCanny],
                      [imgContours, imgBiggestContours, imgWarpColored, imgThresh],
                      [imgResult, imgRawDrawing, imgInvWarp, imgFinal])

        labels = [["Original", "Gray", "Blur", "Canny"],
                  ["Contours", "Biggest Contour", "Warp", "Threshold"],
                  ["Result", "Raw Drawing", "Inv Warp", "Final"]]
        imgstacked = stackImages(imageArray, 0.3, labels)

        cv2.imshow("Final Result", imgFinal)
        cv2.imshow("Stacked Images", imgstacked)

        return imgFinal, score_percentage, yIndex, correct_answers_count

    except Exception as e:
        print(f"Error in processing: {e}")
        return None, None, None, None
