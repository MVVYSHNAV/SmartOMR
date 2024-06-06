import cv2
import numpy as np
import utile

# Image selection and setups
path = "1.jpg"
widthImg = 700
heightImg = 700
questions = 10
choices = 4

# Get answers from user input
ans = []
print(f"Please enter the correct answers for {questions} questions (choices range from 1 to {choices}):")
for i in range(questions):
    while True:
        try:
            answer = int(input(f"Answer for question {i+1}: "))
            if 1 <= answer <= choices:
                ans.append(answer)
                break
            else:
                print(f"Invalid input. Please enter a number between 1 and {choices}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

webcamFeed = True
cameraNo = 0

cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)

while True:
    if webcamFeed:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from webcam.")
            continue
    else:
        img = cv2.imread(path)

    # Preprocessing the image
    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    try:
        # Find all contours
        contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        # Find rectangular contours
        rectCon = utile.rectCountour(contours)
        if len(rectCon) < 2:
            print("Not enough rectangular contours found.")
            continue
        biggestContour = utile.getCornerPoints(rectCon[0])
        gradePoints = utile.getCornerPoints(rectCon[1])

        if biggestContour.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imgBiggestContours, [biggestContour], -1, (0, 255, 0), 20)
            cv2.drawContours(imgBiggestContours, [gradePoints], -1, (255, 0, 0), 20)

            biggestContour = utile.reorder(biggestContour)
            gradePoints = utile.reorder(gradePoints)

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

            boxes = utile.splitBoxes(imgThresh)

            # Pixel values of each dark point
            yPixelVal = np.zeros((questions, choices), dtype=int)

            for countR in range(questions):
                for countC in range(choices):
                    yPixelVal[countR, countC] = cv2.countNonZero(boxes[countR * choices + countC])

            # Finding index value of the marking
            yIndex = [np.argmax(yPixelVal[x]) for x in range(questions)]

            # Grading
            grading = [1 if ans[x] == yIndex[x] else 0 for x in range(questions)]
            score = (sum(grading) / questions) * 100
            print("Score:", score)

            # Display answers
            imgResult = utile.showAnswers(imgWarpColored.copy(), yIndex, grading, ans, questions, choices)
            imgRawDrawing = utile.showAnswers(np.zeros_like(imgWarpColored), yIndex, grading, ans, questions, choices)

            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            imgRawGrade = np.zeros_like(imgGradeDisplay)
            cv2.putText(imgRawGrade, f"{int(score)}%", (60, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (215, 255, 0), 1)
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
    imgstacked = utile.stackImages(imageArray, 0.3, labels)

    cv2.imshow("Final Result", imgFinal)
    cv2.imshow("Stacked Images", imgstacked)
    if cv2.waitKey(1) & 0xff == ord('s'):
        cv2.imwrite("finalResult.jpg", imgFinal)
        cv2.waitKey(300)
