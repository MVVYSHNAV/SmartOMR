import cv2
import numpy as np
import utile

#image selection and  setups
path = "1.png"
widthImg = 700
heightImg = 700
questions = 10
choice = 4
ans = [0, 0, 1, 3, 3, 0, 0, 0, 0, 0]

img = cv2.imread(path)

#preprocessing the img
img = cv2.resize(img,(widthImg,heightImg))
imgContours = img.copy()
imgFinal = img.copy()
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny = cv2.Canny(imgBlur,10,50)


#all countours find()
contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, contours, -1,(0,255,0),10)
#rectcountour find()
rectCon= utile.rectCountour(contours)
biggestContour = utile.getCornerPoints(rectCon[0])
# print(biggestContour.shape)
gradePoints = utile.getCornerPoints(rectCon[2]) #change here to match the box


if biggestContour.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
    cv2.drawContours(imgBiggestContours,gradePoints,-1,(255,0,0),20)

    biggestContour =  utile.reorder(biggestContour)
    gradePoints       =  utile.reorder(gradePoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0], [widthImg,0], [0,heightImg],[widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored = cv2.warpPerspective(img,matrix,(widthImg,heightImg))
    
    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32([[0,0], [325,0], [0,150],[325,150]])
    matrixg = cv2.getPerspectiveTransform(ptG1,ptG2)
    imgGradeDisplay = cv2.warpPerspective(img,matrixg,(325,150))
    # cv2.imshow("GRADE", imgGradeDisplay)

    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray,170,255,cv2.THRESH_BINARY_INV)[1]
    

    boxes = utile.splitBoxes(imgThresh)
    # cv2.imshow("test",boxes[2])
    # print(cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]))

    # pixelvalues of each  dark points
    yPixelVal = np.zeros((questions,choice))
    countC = 0
    countR = 0

    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        yPixelVal[countR][countC] = totalPixels
        countC +=1
        if(countC == choice):countR +=1; countC = 0
    print(yPixelVal)
#finding index value of the marking
    yIndex = []
    for x in range (0,questions):
        arr = yPixelVal[x]
        # print("arr",arr)
        yIndexVal = np.where(arr==np.amax(arr))
        # print(yIndexVal[0]) 
        yIndex.append(yIndexVal[0][0])
    # print(yIndex)


    #grading 

    grading = []
    for x in range (0, questions):
        if ans[x] == yIndex[x]:
            grading.append(1)
        else: grading.append(0)
    # print(grading)

    score = (sum(grading)/questions) * 100 
    print(score)

    #display answers
    imgResult = imgWarpColored.copy()
    imgResult = utile.showAnswers(imgResult,yIndex,grading,ans,questions,choice)

    imgRawDrawing = np.zeros_like(imgWarpColored)
    imgRawDrawing = utile.showAnswers(imgRawDrawing,yIndex,grading,ans,questions,choice)
    
    inMatrix = cv2.getPerspectiveTransform(pt2,pt1)
    imgInvWarp = cv2.warpPerspective(imgRawDrawing,inMatrix,(widthImg,heightImg))
    
    imgRawGrade = np.zeros_like(imgGradeDisplay)
    cv2.putText(imgRawGrade, str(int(score))+"%",(60,80),cv2.FONT_HERSHEY_COMPLEX,1,(215,255,0),1)
    cv2.imshow("Grade",imgRawGrade)
    invMatrixg = cv2.getPerspectiveTransform(ptG2,ptG1)
    imgInvGradeDis = cv2.warpPerspective(img,invMatrixg,(widthImg,heightImg))

    imgFinal = cv2.addWeighted(imgFinal,1,imgInvWarp,1,0)
    imgFinal = cv2.addWeighted(imgFinal,1,imgInvGradeDis,1,0)



imgBlank = np.zeros_like(img)
imageArray = ([img, imgGray,imgBlur,imgCanny],
              [imgContours, imgBiggestContours, imgWarpColored, imgThresh],
              [imgResult, imgRawDrawing, imgInvWarp, imgFinal])
imgstacked = utile.stackImages(imageArray, 0.3)
 

cv2.imshow("final Result",imgFinal)
cv2.imshow("stacked images", imgstacked)
cv2.waitKey(0)