import cv2
import numpy as np

# Utility functions
def stackImages(imgArray, scale, labels=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        ver = np.hstack(imgArray)

    if len(labels) != 0:
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(rows):
            for c in range(cols):
                cv2.rectangle(ver, (c * eachImgWidth, eachImgHeight * d), (c * eachImgWidth + len(labels[d][c]) * 13 + 27, 30 + eachImgHeight * d), (255, 255, 255), cv2.FILLED)
                cv2.putText(ver, labels[d][c], (eachImgWidth * c + 10, eachImgHeight * d + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver

def rectCountour(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx

def reorder(points):
    points = points.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)
    pointsNew[0] = points[np.argmin(add)]
    pointsNew[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    pointsNew[1] = points[np.argmin(diff)]
    pointsNew[2] = points[np.argmax(diff)]
    return pointsNew

def splitBoxes(img):
    rows = np.vsplit(img, 10)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 4)
        for box in cols:
            boxes.append(box)
    return boxes

def showAnswers(img, yIndex, grading, ans, questions, choice):
    secW = int(img.shape[1] / choice)
    secH = int(img.shape[0] / questions)
    for x in range(questions):
        yAns = yIndex[x]
        cX = (yAns * secW) + secW // 2
        cY = (x * secH) + secH // 2
        if grading[x] == 1:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
            correctAns = ans[x]
            cv2.circle(img, ((correctAns * secW) + secW // 2, (x * secH) + secH // 2), 50, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (cX, cY), 30, color, cv2.FILLED)
    return img